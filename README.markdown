this is a tracery bot harness for mastodon

```
pip install -r requirements.txt
python trastodon.py mybot.state auth https://mastodon.instance.example.com
# then, in a crontab
python trastodon.py mybot.state toot mybot.json
python trastodon.py mybot.state reply mybot.json
```
