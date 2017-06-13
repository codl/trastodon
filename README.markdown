this is a tracery bot harness for mastodon

```
pip install -r requirements.txt
python trastodon.py mybot.state auth https://mastodon.instance.example.com
# then, in a crontab
python trastodon.py mybot.state toot mybot.json
python trastodon.py mybot.state reply mybot.json
```

note that as of 2017-06-13, mastodon.py needs to be installed from source for the reply features to work

```
pip install --upgrade git+https://github.com/halcy/Mastodon.py.git@5ed78fbe8372bc9e87968a2f42031859190df8db
```

whenever a version higher than v1.0.7 comes out this probably won't be necessary

note that pyyaml sucks ass so you have to make sure libyaml is installed too if you want emoji to work
