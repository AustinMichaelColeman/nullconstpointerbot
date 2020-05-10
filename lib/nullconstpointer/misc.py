from . import processor, user


def help(bot, prefix, cmds):
    bot.send_message(
        "Registered commands: "
        + ",".join([f"{prefix}{cmd}" for cmd in sorted(cmds.keys())])
    )


def hello(bot, chatuser, *args):
    bot.send_message(f"Hey {chatuser['name']}!")


def friendcode(bot, chatuser, *args):
    bot.send_message(f"Add me on your switch! My friend code is SW-2444-3895-1309")


def add(bot, chatuser, *args):
    cmdprocessor = processor.Processor()
    theuser = user.User(chatuser["name"], "xxx-xxx-xxx")
    response = cmdprocessor.add_user(theuser)
    bot.send_message(response)
