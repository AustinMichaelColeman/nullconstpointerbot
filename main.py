from nullconstpointer.bot.bot import Bot
import keys


if __name__ == "__main__":
    name = "nullconstpointerbot"
    owner = "nullconstpointer"
    client_id = keys.CLIENT_ID
    token = keys.TOKEN
    bot = Bot(name, owner, client_id, token)
    bot.start()
