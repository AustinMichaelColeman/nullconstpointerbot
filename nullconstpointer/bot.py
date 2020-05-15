"""
Some code in this file is licensed under the Apache License, Version 2.0.
    http://aws.amazon.com/apache2.0/
"""
from irc.bot import SingleServerIRCBot
from requests import get
from nullconstpointer.processor import Processor
from nullconstpointer.user import User, MOD_LEVEL_OWNER, MOD_LEVEL_MOD, MOD_LEVEL_USER

from nullconstpointer.commands.list import ListCommand
from nullconstpointer.commands.add import AddCommand
from nullconstpointer.commands.current import CurrentCommand
from nullconstpointer.commands.next import NextCommand
from nullconstpointer.commands.mod import ModCommand
from nullconstpointer.commands.unmod import UnmodCommand
from nullconstpointer.commands.remove import RemoveCommand
from nullconstpointer.commands.clear import ClearCommand
from nullconstpointer.commands.leave import LeaveCommand
from nullconstpointer.commands.random import RandomCommand
from nullconstpointer.commands.finish import FinishCommand


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
        self.bot_owner = User(owner, MOD_LEVEL_OWNER)

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
            "remove": self.remove,
            "leave": self.leave,
            "clear": self.clear,
            "random": self.random,
            "finish": self.finish,
            "habits": self.habits,
        }

        url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
        headers = {
            "Client-ID": self.CLIENT_ID,
            "Accept": "application/vnd.twitchtv.v5+json",
        }
        resp = get(url, headers=headers).json()
        self.channel_id = resp["users"][0]["_id"]

        self.cmdprocessor = Processor(self.bot_owner)

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

        else:
            self.send_message(f"{user['name']}, \"{cmd}\" isn't a registered command.")

    def help(self, prefix, cmds):
        self.send_message(
            "Hi. I'm a Mario Maker 2 Twitch chat bot. Registered commands: "
            + ", ".join([f"{prefix}{cmd}" for cmd in sorted(cmds.keys())])
        )

    def hello(self, chatuser, *args):
        self.send_message(f"Hey {chatuser['name']}!")

    def friendcode(self, chatuser, *args):
        self.send_message(f"Add me on your switch! My friend code is SW-2444-3895-1309")

    def add(self, chatuser, *args):
        if len(args) != 1:
            response = chatuser["name"] + ", please provide a valid level code."
        else:
            command = AddCommand(
                self.cmdprocessor, chatuser["name"], chatuser["name"], args[0]
            )
            response = self.cmdprocessor.process_command(command)
        self.send_message(response)

    def list_levels(self, chatuser, *args):
        command = ListCommand(self.cmdprocessor)
        response = self.cmdprocessor.process_command(command)
        self.send_message(response)

    def next_level(self, chatuser, *args):
        command = NextCommand(self.cmdprocessor, chatuser["name"])
        response = self.cmdprocessor.process_command(command)
        self.send_message(response)

    def current_level(self, chatuser, *args):
        command = CurrentCommand(self.cmdprocessor)
        response = self.cmdprocessor.process_command(command)
        self.send_message(response)

    def mod(self, chatuser, *args):
        username = chatuser["name"]
        if len(args) == 1:
            user_to_mod = args[0]
            command = ModCommand(self.cmdprocessor, username, user_to_mod)
            self.send_message(self.cmdprocessor.process_command(command))
        else:
            command = ModCommand(self.cmdprocessor, username, None)
            self.send_message(self.cmdprocessor.process_command(command))

    def unmod(self, chatuser, *args):
        username = chatuser["name"]
        if len(args) == 1:
            user_to_unmod = args[0]
            command = UnmodCommand(self.cmdprocessor, username, user_to_unmod)
            self.send_message(self.cmdprocessor.process_command(command))
        else:
            command = UnmodCommand(self.cmdprocessor, username, None)
            self.send_message(self.cmdprocessor.process_command(command))

    def remove(self, chatuser, *args):
        username = chatuser["name"]

        if len(args) == 1:
            level_to_remove = args[0]
            command = RemoveCommand(self.cmdprocessor, username, level_to_remove)
            self.send_message(self.cmdprocessor.process_command(command))
        else:
            command = RemoveCommand(self.cmdprocessor, username, None)
            self.send_message(self.cmdprocessor.process_command(command))

    def github(self, chatuser, *args):
        self.send_message("https://github.com/AustinMichaelColeman/nullconstpointerbot")

    def leave(self, chatuser, *args):
        username = chatuser["name"]
        command = LeaveCommand(self.cmdprocessor, username)
        self.send_message(self.cmdprocessor.process_command(command))

    def clear(self, chatuser, *args):
        username = chatuser["name"]
        command = ClearCommand(self.cmdprocessor, username)
        self.send_message(self.cmdprocessor.process_command(command))

    def random(self, chatuser, *args):
        username = chatuser["name"]
        command = RandomCommand(self.cmdprocessor, username)
        self.send_message(self.cmdprocessor.process_command(command))

    def finish(self, chatuser, *args):
        username = chatuser["name"]
        command = FinishCommand(self.cmdprocessor, username)
        self.send_message(self.cmdprocessor.process_command(command))

    def habits(self, chatuser, *args):
        self.send_message("https://pastebin.com/WBMgKmDz")


class CommandInvoker:
    def __init__(self):
        self._commands = {}

    def register(self, command_name, command):
        self._commands[command_name] = command

    def execute(self, command_name):
        if command_name in self._commands.keys():
            self._commands[command_name].execute()
        else:
            print(f"Command [{command_name}] not recognised")
