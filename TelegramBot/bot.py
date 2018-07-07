import pyowm as pyowm
import telebot
import constants
import urllib.request, json
from telebot import types
bot = telebot.TeleBot(constants.token)

s=""

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("🍽 Где поесть в Алматы ?")
    user_markup.row("🏔 Где отдохнуть в Алматы ?")
    user_markup.row("🛏 Где переночевать в Алматы ?")
    user_markup.row("📝Планнер")
    user_markup.row("⛅ Погода")
    bot.send_message(message.chat.id, 'Добро пожаловать!', reply_markup=user_markup)


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, "Помощь")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    global s
    if message.text == "🍽 Где поесть в Алматы ?":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        asian = telebot.types.KeyboardButton(text="Азиатская")
        national = telebot.types.KeyboardButton(text="Национальная")
        europian = telebot.types.KeyboardButton(text="Европейская")
        fastfood = telebot.types.KeyboardButton(text="Фаст-Фуд")
        turkish = telebot.types.KeyboardButton(text="Турецкая")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(national, asian, europian, fastfood, turkish, back)
        bot.send_message(message.chat.id, "Выберите кухню", reply_markup=keyboard)
        s="food"
    elif message.text == "Азиатская":
        key = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        nearby = telebot.types.KeyboardButton(text="Ближайщее", request_location=True)
        listed = telebot.types.KeyboardButton(text="Список")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        key.add(nearby, listed, back)
        bot.send_message(message.chat.id, "Вы выбрали Азиатскую кухню", reply_markup=key)
    elif message.text == "Национальная":
        key = telebot.types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        listed = telebot.types.InlineKeyboardButton(text="Все заведения", url="https://www.visitalmaty.kz/ru/cuisines")
        '''nearby = telebot.types.KeyboardButton(text="Ближайщее", request_location=True)
        listed = telebot.types.KeyboardButton(text="Список")
        back = telebot.types.KeyboardButton(text="◀ Назад")'''
        key.add(listed)
        bot.send_message(message.chat.id, "Вы выбрали Национальную кухню", reply_markup=key)
    elif message.text == "Европейская":
        key = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        nearby = telebot.types.KeyboardButton(text="Ближайщее", request_location=True)
        listed = telebot.types.KeyboardButton(text="Список")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        key.add(nearby, listed, back)
        bot.send_message(message.chat.id, "Вы выбрали Европейскую кухню", reply_markup=key)
    elif message.text == "Фаст-Фуд":
        key = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        nearby = telebot.types.KeyboardButton(text="Ближайщее", request_location=True)
        listed = telebot.types.KeyboardButton(text="Список")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        key.add(nearby, listed, back)
        bot.send_message(message.chat.id, "Вы выбрали Фаст-Фуд", reply_markup=key)
    elif message.text == "Турецкая":
        key = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        nearby = telebot.types.KeyboardButton(text="Ближайщее", request_location=True)
        listed = telebot.types.KeyboardButton(text="Список")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        key.add(nearby, listed, back)
        bot.send_message(message.chat.id, "Вы выбрали Турецкую кухню", reply_markup=key)
    elif message.text == "⛅ Погода":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(back)
        city = bot.send_message(message.chat.id, "В каком городе Вам показать погодку?", reply_markup=keyboard)
        bot.register_next_step_handler(city, weath)
    elif message.text == "🛏 Где переночевать в Алматы ?":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = telebot.types.KeyboardButton(text="Ближайщее", request_location=True)
        listed = telebot.types.KeyboardButton(text="Список")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(button, listed, back)
        bot.send_message(message.chat.id, "Выберите ", reply_markup=keyboard)
        s = "hotel"
    elif message.text == "◀ Назад":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("🍽 Где поесть в Алматы ?")
        user_markup.row("🏔 Где отдохнуть в Алматы ?")
        user_markup.row("🛏 Где переночевать в Алматы ?")
        user_markup.row("📝Планнер")
        user_markup.row("⛅ Погода")
        bot.send_message(message.chat.id, 'Меню', reply_markup=user_markup)

def weath(message):
    owm = pyowm.OWM("6e4cdd6906c809a53f60196519cff051")
    city = message.text
    weather = owm.weather_at_place(city)
    w = weather.get_weather()
    temperature = w.get_temperature("celsius")["temp"]
    wind = w.get_wind()["speed"]
    hum = w.get_humidity()
    desc = w.get_detailed_status()
    bot.send_message(message.chat.id, "Сейчас в городе " + str(city) + " " + str(desc) + ", температура - " + str(temperature) + "°C, влажность - " + str(hum) + "%, скорость ветра - " +str(wind) + "м/с.")



@bot.message_handler(content_types=['location'])
def handle_location(message):
    ulat = str(message.location.latitude)
    ulng = str(message.location.longitude)
    if(s=='food'):
        path = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + ulat + "," + ulng + "&radius=300&type=cafe&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
        ind=0
        with urllib.request.urlopen(path) as url:
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                lat = data[i]['geometry']['location']['lat']
                lng = data[i]['geometry']['location']['lng']
                name = data[i]['name']
                rating = data[i]['rating']
                address = data[i]['vicinity']
                if ('opening_hours' in data[i]):
                    openow = data[i]['opening_hours']['open_now']
                    opennow = ""
                    if (openow == True):
                        opennow = "Open"
                    elif (openow == False):
                        opennow = "Close"
                    bot.send_message(message.chat.id, "____________________________________")
                    bot.send_message(message.chat.id,
                                     "📌 name: " + str(name) + "\n" + "📍 address: " + str(address) + "\n" + "⭐ rating: " + str(
                                         rating) + "\n" + "🚪 Open/Close " + str(opennow)+"\n" + "📍 location: ")
                    bot.send_location(message.chat.id, lat, lng)
                else:
                    bot.send_message(message.chat.id, "____________________________________")
                    bot.send_message(message.chat.id,
                                     "📌 name: " + str(name) + "\n" + "📍 address: " + str(
                                         address) + "\n" + "⭐ rating: " + str(
                                         rating) + "\n" + "🚪 Open/Close Unknown" + "\n" + "📍 location: ")
                    bot.send_location(message.chat.id, lat, lng)
    elif(s=='hotel'):
        path = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + ulat + "," + ulng + "&radius=400&type=lodging&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
        ind = 0
        with urllib.request.urlopen(path) as url:
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                lat = data[i]['geometry']['location']['lat']
                lng = data[i]['geometry']['location']['lng']
                name = data[i]['name']
                address = data[i]['vicinity']
                if ('opening_hours' in data[i]):
                    openow = data[i]['opening_hours']['open_now']
                    opennow = ""
                    if (openow == True):
                        opennow = "Open"
                    elif (openow == False):
                        opennow = "Close"
                    bot.send_message(message.chat.id, "____________________________________")
                    bot.send_message(message.chat.id,
                                     "📌 name: " + str(name) + "\n" + "📍 address: " + str(
                                         address) + "\n" + "🚪 Open/Close " + str(opennow) + "\n" + "📍 location: ")
                    bot.send_location(message.chat.id, lat, lng)
                else:
                    bot.send_message(message.chat.id, "____________________________________")
                    bot.send_message(message.chat.id,
                                     "📌 name: " + str(name) + "\n" + "📍 address: " + str(
                                         address) + "\n" + "🚪 Open/Close Unknown" + "\n" + "📍 location: ")
                    bot.send_location(message.chat.id, lat, lng)

bot.polling(none_stop=True, interval=1)
