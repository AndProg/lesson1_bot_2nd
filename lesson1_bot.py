import logging, ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(
    filename='lesson1_bot.log', 
    level=logging.INFO
)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs':{
        'username': settings.PROXY_USERNAME, 
        'password': settings.PROXY_PASSWORD
    }
}

def greet_user(update, context):
    print('вызван /start')
    update.message.reply_text('Здравствуй, Пользователь!')


def stellar(update, context):
    print('Вызван /planet')
    update.message.reply_text('Введите название интересующей Вас планеты (на английском) после команды /planet')
    chosen_planet = str(update.message.text).lower().split()
    print(chosen_planet)
    
    for planet in planet_list:
      if planet in chosen_planet:

        planet = planet.capitalize()
        planet_coords = getattr(ephem, planet)(ephem.now())
        constel = ephem.constellation(planet_coords)
        
        update.message.reply_text('Планета находится в созвездии {}'.format(constel))
        break
 

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', stellar))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    planet_list = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
    main()

