[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)\
trastodon is **no longer maintained**. this former maintainer's recommendation is to use chr's [ananas][], which supports tracery out of the box

[ananas]: https://github.com/Chronister/ananas

original README contents follow

***

this is a tracery bot harness for mastodon

```
pip install -r requirements.txt
python trastodon.py mybot.state auth https://mastodon.instance.example.com
# then, in a crontab
python trastodon.py mybot.state toot mybot.json
python trastodon.py mybot.state reply mybot.json
```
