# nullconstpointerbot
Twitch Mario Maker 2 level chat bot

# requirements
pip install irc requests

# Twitch authentication

To use this bot, make a keys.py and put your credentials in it:

```python
CLIENT_ID = "insertClientIDHere"
TOKEN = "insertTokenHere"
```

CLIENT_ID comes from your twitch application. Go to https://dev.twitch.tv/console/apps and then manage or create your app. Then copy the Client ID.

TOKEN comes from https://twitchapps.com/tmi/ with "oauth:" removed.

See https://dev.twitch.tv/docs/irc for more information

Then run main.py
