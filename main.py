from rivescript import RiveScript
from exporter import export
def run():
    bot = RiveScript()
    bot.load_directory("./brain")
    bot.sort_replies()
    while True:
        msg = input('You> ')
        if msg == 'q':
            break
        reply = bot.reply("localuser", msg)
        print('Bot>', reply)
    bot.deparse()
    name= bot.get_uservars().get('localuser').get('name')
    id = bot.get_uservars().get('localuser').get('id')
    export(name,id)

if __name__ == "__main__":
    run()