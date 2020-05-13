"""
Some code in this file is licensed under the Apache License, Version 2.0.
    http://aws.amazon.com/apache2.0/
"""
from irc.bot import SingleServerIRCBot
from requests import get
from . import processor, user


class Bot(SingleServerIRCBot):
    def __init__(self, botname, owner, client_id, token):
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = botname.lower()
        self.CLIENT_ID = str(client_id)
        self.TOKEN = str(token)
        self.CHANNEL = f"#{owner}"
        self.botname = botname
        self.prefix = "!"
        self.bot_owner = user.User(owner, user.MOD_LEVEL_OWNER)

        self.cmds = {
            "hello": self.hello,
            "friendcode": self.friendcode,
            "add": self.add,
            "github": self.github,
            "list": self.list_levels,
            "nextlevel": self.next_level,
            "next": self.next_level,
            "current": self.current_level,
            "currentlevel": self.current_level,
            "mod": self.mod,
            "unmod": self.unmod,
        }

        url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
        headers = {
            "Client-ID": self.CLIENT_ID,
            "Accept": "application/vnd.twitchtv.v5+json",
        }
        resp = get(url, headers=headers).json()
        self.channel_id = resp["users"][0]["_id"]

        self.cmdprocessor = processor.Processor(self.bot_owner)

        super().__init__(
            [(self.HOST, self.PORT, f"oauth:{self.TOKEN}")],
            self.USERNAME,
            self.USERNAME,
        )

    def on_welcome(self, cxn, event):
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", f":twitch.tv/{req}")

        cxn.join(self.CHANNEL)
        self.send_message("Now online.")

    def on_pubmsg(self, cxn, event):
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        user = {"name": tags["display-name"], "id": tags["user-id"]}
        message = event.arguments[0]

        if user["name"] != self.botname:
            self.process(user, message)

        print(f"Message from {user['name']}: {message}")

    def send_message(self, message):
        self.connection.privmsg(self.CHANNEL, message)

    def process(self, user, message):
        if message.startswith(self.prefix):
            cmd = message.split(" ")[0][len(self.prefix) :]
            args = message.split(" ")[1:]
            self.perform(user, cmd, *args)

    def perform(self, user, cmd, *args):
        for name, func in self.cmds.items():
            if cmd.upper() == name.upper():
                func(user, *args)
                return

        if cmd.upper() == "HELP":
            self.help(self.prefix, self.cmds)

        # else:
        #     bot.send_message(f"{user['name']}, \"{cmd}\" isn't a registered command.")

    def help(self, prefix, cmds):
        self.send_message(
            "Registered commands: "
            + ",".join([f"{prefix}{cmd}" for cmd in sorted(cmds.keys())])
        )

    def hello(self, chatuser, *args):
        self.send_message(f"Hey {chatuser['name']}!")

    def friendcode(self, chatuser, *args):
        self.send_message(f"Add me on your switch! My friend code is SW-2444-3895-1309")

    def add(self, chatuser, *args):
        if len(args) != 1:
            response = chatuser["name"] + ", please provide a valid level code."
        else:
            response = self.cmdprocessor.add_user_level(chatuser["name"], args[0])
        self.send_message(response)

    def list_levels(self, chatuser, *args):
        response = self.cmdprocessor.list_levels()
        self.send_message(response)

    def next_level(self, chatuser, *args):
        response = self.cmdprocessor.next_level(chatuser["name"])
        self.send_message(response)

    def current_level(self, chatuser, *args):
        response = self.cmdprocessor.get_current_level()
        self.send_message(response)

    def mod(self, chatuser, *args):
        username = chatuser["name"]
        user_to_mod = args[0]
        if username == self.bot_owner.username:
            if len(args) != 1:
                response = (
                    chatuser["name"] + ", please provide a valid username to mod."
                )
            else:
                response = self.cmdprocessor.mod(username, user_to_mod)
        else:
            response = username + ", you do not have permission to mod."
        self.send_message(response)

    def unmod(self, chatuser, *args):
        username = chatuser["name"]
        user_to_unmod = args[0]
        if username == self.bot_owner.username:
            if len(args) != 1:
                response = (
                    chatuser["name"] + ", please provide a valid username to mod."
                )
            else:
                response = self.cmdprocessor.unmod(username, user_to_unmod)
        else:
            response = username + ", you do not have permission to mod."
        self.send_message(response)

    def github(self, chatuser, *args):
        self.send_message("https://github.com/AustinMichaelColeman/nullconstpointerbot")
