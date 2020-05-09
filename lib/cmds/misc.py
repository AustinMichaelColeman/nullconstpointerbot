def help(bot, prefix, cmds):
    bot.send_message(
        "Registered commands: "
        + ",".join([f"{prefix}{cmd}" for cmd in sorted(cmds.keys())])
    )


def hello(bot, user, *args):
    bot.send_message(f"Hey {user['name']}!")


def friendcode(bot, user, *args):
    bot.send_message(f"Add me on your switch! My friend code is SW-2444-3895-1309")
