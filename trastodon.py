from mastodon import Mastodon
from tracery import Grammar
from tracery.modifiers import base_english
from argparse import ArgumentParser
import yaml
from yaml.error import YAMLError
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import json

def read_grammar(filename):
    with open(filename) as f:
        try:
            rules = yaml.load(f, Loader=Loader)
        except YAMLError:
            f.seek(0)
            rules = json.load(f)
    return Grammar(rules)

def save_state(filename, state):
    stateyaml = yaml.dumps(state, default_flow_style=False, default_style='', Dumper=Dumper)
    with open(filename, 'w') as f:
        f.write(stateyaml)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('state_file', help='file in which to store or read state')
    command = parser.add_subparsers(help='action to take', dest='command')
    auth = command.add_parser('auth', help='log into the bot\'s account')
    auth.add_argument('server')
    toot = command.add_parser('toot', help='post a toot')
    toot.add_argument('filename', help='path to a tracery ruleset, as JSON or YAML')
    toot.add_argument('--rule', '-r', default='#origin#')
    reply = command.add_parser('reply', help='reply to mentions')
    reply.add_argument('filename', help='path to a tracery ruleset, as JSON or YAML')
    reply.add_argument('--rule', '-r', default='#reply#')
    command.add_parser('clear_notifications', help='ignore all notifications up to now. useful when first setting up a bot')
    args = parser.parse_args()
    if args.command == 'auth':
        try:
            with open(args.state_file) as f:
                state = yaml.load(f, Loader=Loader)
        except OSError:
            state = {}
        state['server'] = args.server
        try:
            state['client_id'], state['client_secret'] =\
                Mastodon.create_app('trastodon',
                    scopes=('read', 'write'), api_base_url=state['server'])
        except:
            print("couldn't register app. check your server url")
            exit(2)
        print("successfully registered app")
        mas = Mastodon(state['client_id'], state['client_secret'],
                api_base_url=state['server'])
        url = mas.auth_request_url(scopes=['read', 'write'])
        print("please go to %s" % (url,))
        print("then paste the authorization code you will be given back into this terminal")
        auth_code = input()
        state['access_token'] = mas.log_in(code=auth_code, scopes=('read', 'write'))
        try:
            if "error" in mas.account_verify_credentials():
                raise Exception()

        except:
            print("couldn't log in with provided authorization code")
            exit(3)

        print('success!')
        try:
            save_state(args.state_file, state)
        except OSError:
            print("could not write state file")
            exit(1)
    else:
        try:
            with open(args.state_file) as f:
                state = yaml.load(f, Loader=Loader)
        except OSError:
            print("Couldn't read state file!")
            exit(1)
        try:
            mas = Mastodon(state['client_id'], state['client_secret'], state['access_token'],
                    api_base_url=state['server'])
            me = mas.account_verify_credentials()
            if "error" in me:
                raise Exception()
        except:
            print("Couldn't log in. Try auth first")
            exit(4)
        try:
            grammar = read_grammar(args.filename)
        except OSError:
            print("Grammar file could not be read! Check your path and permissions")
            exit(1)

        grammar.add_modifiers(base_english)

        if args.command == 'toot':
            mas.status_post(grammar.flatten(args.rule), visibility="unlisted")

        elif args.command == 'reply':
            if "notif_pointer" not in state:
                state["notif_pointer"] = 0
            mentions = filter(lambda n: n["type"] == "mention",
                    mas.notifications(since_id=state["notif_pointer"]))
            for mention in mentions:

                # temp fuckass fix until mastodon.py gets updated for 2.0
                mention['id'] = int(mention['id'])

                visibility = mention['status']['visibility']
                if visibility == 'public':
                    visibility = 'unlisted'
                mas.status_post(
                        "@%s %s" % (mention['status']['account']['acct'], grammar.flatten(args.rule)),
                        in_reply_to_id=mention['status']['id'], visibility=visibility)

                state["notif_pointer"] = max((state['notif_pointer'], mention['id']))
            try:
                save_state(args.state_file, state)
            except OSError:
                print("could not write state file")
                exit(1)
        elif args.command == 'clear_notifications':
            try:
                notification = mas.notifications(limit=1)[0]
                state['notif_pointer'] = notification['id']
                save_state(args.state_file, state)
            except:
                pass

