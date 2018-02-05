import telebot
from telebot import types
import config
from geopy.distance import vincenty

bot = telebot.TeleBot(config.API_TOKEN)

# begin button
markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_magazins = types.KeyboardButton("Ближайший к вам магазин", request_location=True)
start_menu = types.KeyboardButton("Старт")
markup_menu.add(start_menu,
                btn_magazins)

# start button
markup_menu_start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
start_menu_catalog = types.KeyboardButton("Каталог")
start_menu_price = types.KeyboardButton("Получить прайс")
start_menu_call = types.KeyboardButton("Заказать звонок")
back_to_start_menu = types.KeyboardButton("Предыдущее меню: Старт")
markup_menu_start.add(start_menu_catalog,
                      start_menu_price,
                      start_menu_call,
                      back_to_start_menu)

# catalog button
markup_menu_catalog = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
catalog_menu_herring = types.KeyboardButton("Сельдь")
catalog_menu_mackerel = types.KeyboardButton("Скумбрия")
catalog_menu_pink_salmon = types.KeyboardButton("Горбуша")
catalog_menu_pollock = types.KeyboardButton("Минтай")
catalog_menu_blue_whiting = types.KeyboardButton("Путассу")
back_to_catalog_menu = types.KeyboardButton("Предыдущее меню: Каталог")
markup_menu_catalog.add(catalog_menu_herring,
                        catalog_menu_mackerel,
                        catalog_menu_pink_salmon,
                        catalog_menu_pollock,
                        catalog_menu_blue_whiting,
                        back_to_catalog_menu)

# price button
markup_menu_price = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
price_menu_all = types.KeyboardButton("Общая сумма")
back_to_price_menu = types.KeyboardButton("Предыдущее меню: Получить прайс")
markup_menu_price.add(price_menu_all,
                      back_to_price_menu)

# call button
markup_menu_call = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
call_menu = types.KeyboardButton("Заказать звонок")
back_to_call_menu = types.KeyboardButton("Предыдущее меню: Заказать звонок")
markup_menu_call.add(call_menu,
                     back_to_call_menu)


@bot.message_handler(commands=['help'])
def second_welcome(message):
    bot.reply_to(message, "help", reply_markup=markup_menu)


@bot.message_handler(commands=['start'])
def second_welcome(message):
    bot.send_message(message.chat.id,
                     'Привет, для корректного определения ближайшего склада, просим вас включить определение местоположения и мы автоматически выберем ближайший склад отгрузки',
                     reply_markup=markup_menu)


@bot.message_handler(func=lambda message: True, content_types=['location'])
def magazin_location(message):
    lat = message.location.latitude
    long = message.location.longitude
    print(message)
    distance = []
    for i in config.MAGAZINS:
        result = vincenty((i['latm'], i['longm']), (lat, long)).kilometers
        distance.append(result)
    print(distance)
    index = distance.index(min(distance))
    print(config.MAGAZINS[index]['latm'], config.MAGAZINS[index]['longm'], config.MAGAZINS[index]['title'],
          config.MAGAZINS[index]['address'])
    bot.send_message(message.chat.id, 'Магазин, ближайший к вам')
    bot.send_venue(message.chat.id,
                   config.MAGAZINS[index]['latm'],
                   config.MAGAZINS[index]['longm'],
                   config.MAGAZINS[index]['title'],
                   config.MAGAZINS[index]['address'])


@bot.message_handler(func=lambda message: True)
def welcome(message):
    if message.text == "Старт":
        bot.send_message(message.chat.id, "Приветствуем, выбирайте что вам нужно",
                         reply_markup=markup_menu_start)
    elif message.text == "Предыдущее меню: Старт":
        bot.send_message(message.chat.id, "Предыдущее меню",
                         reply_markup=markup_menu)
    elif message.text == "Каталог":
        bot.send_message(message.chat.id, "Наш асортимент",
                         reply_markup=markup_menu_catalog)
    elif message.text == "Предыдущее меню: Каталог":
        bot.send_message(message.chat.id, "Предыдущее меню",
                         reply_markup=markup_menu_start)
    elif message.text == "Получить прайс":
        bot.send_message(message.chat.id, "Ваш прайс",
                         reply_markup=markup_menu_price)
    elif message.text == "Предыдущее меню: Получить прайс":
        bot.send_message(message.chat.id, "Предыдущее меню",
                         reply_markup=markup_menu_start)
    elif message.text == "Заказать звонок":
        bot.send_message(message.chat.id, "Заполните заявку",
                         reply_markup=markup_menu_call)
    elif message.text == "Предыдущее меню: Заказать звонок":
        bot.send_message(message.chat.id, "Предыдущее меню",
                         reply_markup=markup_menu_start)


bot.polling()
