def help(bot, prefix, cmds):
    bot.send_message(
        "Registered commands: "
        + ",".join([f"{prefix}{cmd}" for cmd in sorted(cmds.keys())])
    )


def hello(bot, user, *args):
    bot.send_message(f"Hey {user['name']}!")
