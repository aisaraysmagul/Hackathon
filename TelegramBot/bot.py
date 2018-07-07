import pyowm as pyowm
import telebot
import constants
import urllib.request, json
import requests, bs4
from telebot import types
bot = telebot.TeleBot(constants.token)

s=""
food=""
curr =""
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("🍽 Где поесть в Алматы ?")
    user_markup.row("🏔 Где отдохнуть в Алматы ?")
    user_markup.row("🛏 Где переночевать в Алматы ?")
    user_markup.row("📝Планнер")
    user_markup.row("⛅ Погода")
    user_markup.row("Конвертер валют")
    bot.send_message(message.chat.id, 'Добро пожаловать!', reply_markup=user_markup)


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, "Помощь")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    global s
    global food
    global curr
    if message.text == "🍽 Где поесть в Алматы ?":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        near = telebot.types.KeyboardButton(text="Ближайшие")
        spisok = telebot.types.KeyboardButton(text="В городе")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(near, spisok, back)
        bot.send_message(message.chat.id, "Выберите местоположение", reply_markup=keyboard)
        s="food"
    elif message.text=="Ближайшие":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        asian = telebot.types.KeyboardButton(text="Азиатская")
        national = telebot.types.KeyboardButton(text="Национальная")
        europian = telebot.types.KeyboardButton(text="Европейская")
        turkish = telebot.types.KeyboardButton(text="Турецкая")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(national, asian, europian, turkish, back)
        bot.send_message(message.chat.id, "Выберите кухню", reply_markup=keyboard)
        s="nearbyfood"
    elif message.text=="Азиатская":
        k = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        mesto = telebot.types.KeyboardButton(text="Отправить свое местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        k.add(mesto, back)
        bot.send_message(message.chat.id, "Отправьте свое местоположение", reply_markup=k)
        food="asian+food"
    elif message.text == "Национальная":
        k = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        mesto = telebot.types.KeyboardButton(text="Отправить свое местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        k.add(mesto, back)
        bot.send_message(message.chat.id, "Отправьте свое местоположение", reply_markup=k)
        food="national+food"
    elif message.text=="Европейская":
        k = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        mesto = telebot.types.KeyboardButton(text="Отправить свое местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        k.add(mesto, back)
        bot.send_message(message.chat.id, "Отправьте свое местоположение", reply_markup=k)
        food="european+food"
    elif message.text=="Турецкая":
        k = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        mesto = telebot.types.KeyboardButton(text="Отправить свое местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        k.add(mesto, back)
        bot.send_message(message.chat.id, "Отправьте свое местоположение", reply_markup=k)
        food="turkish+food"
    elif message.text == "В городе":
        k = telebot.types.InlineKeyboardMarkup()
        asian = telebot.types.InlineKeyboardButton(text="Азиатская", url = "https://www.visitalmaty.kz/ru/cuisines")
        national = telebot.types.InlineKeyboardButton(text="Национальная", url = "https://www.visitalmaty.kz/ru/cuisines")
        europian = telebot.types.InlineKeyboardButton(text="Европейская", url = "https://www.visitalmaty.kz/ru/cuisines")
        turkish = telebot.types.InlineKeyboardButton(text="Турецкая", url = "https://www.visitalmaty.kz/ru/cuisines")
        k.add(asian, national, europian, turkish)
        bot.send_message(message.chat.id, "Выберите кухню", reply_markup=k)
    elif message.text == "⛅ Погода":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(back)
        city = bot.send_message(message.chat.id, "В каком городе Вам показать погодку?", reply_markup=keyboard)
        bot.register_next_step_handler(city, weath)
    elif message.text == "🛏 Где переночевать в Алматы ?":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = telebot.types.KeyboardButton(text="Ближайшее", request_location=True)
        listed = telebot.types.KeyboardButton(text="Все места")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(button, listed, back)
        bot.send_message(message.chat.id, "Выберите ", reply_markup=keyboard)
        s = "hotel"
    elif message.text == "Все места":
        key = telebot.types.InlineKeyboardMarkup()
        mesta = telebot.types.InlineKeyboardButton(text = "Нажмите здесь", url = "https://www.visitalmaty.kz/ru/accomodations")
        key.add(mesta)
        bot.send_message(message.chat.id, "Места для проживания", reply_markup=key)
    elif message.text == "🕺 Где провеcти время в Алматы ?":
        s = requests.get('https://sxodim.com/almaty/events/vystavki/?show=today')
        b = bs4.BeautifulSoup(s.text, "html.parser")
        l = b.select('.news_list .location')
        d = b.select('.news_list .date')
        c = b.select('.news_list .cost')
        for i in range(0, len(l)):
            n1 = l[i].getText()
            n2 = d[i].getText()
            n3 = c[i].getText()
            bot.send_message(message.chat.id, ":pushpin:" + n1 + "\n:calendar: " + n2 + "\n:dollar: " + n3)
    elif message.text == "◀ Назад":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("🍽 Где поесть в Алматы ?")
        user_markup.row("🏔 Где отдохнуть в Алматы ?")
        user_markup.row("🛏 Где переночевать в Алматы ?")
        user_markup.row("📝Планнер")
        user_markup.row("⛅ Погода")
        user_markup.row("Конвертер валют")
        bot.send_message(message.chat.id, 'Меню', reply_markup=user_markup)

    elif message.text =="Конвертер валют":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text="Перевести с KZT в другую валюту")
        button2 = telebot.types.KeyboardButton(text="Перевести с другой валюты в KZT")
        keyboard.add(button1)
        keyboard.add(button2)
        bot.send_message(message.chat.id, "Выберите, пожалуйста: ", reply_markup=keyboard)

    elif message.text == "Перевести с KZT в другую валюту":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        usd = telebot.types.KeyboardButton(text="USD", )
        gbp = telebot.types.KeyboardButton(text="GBP", )
        chi = telebot.types.KeyboardButton(text="CNY", )
        korea = telebot.types.KeyboardButton(text="KRW", )
        rus = telebot.types.KeyboardButton(text="RUR", )
        eur = telebot.types.KeyboardButton(text="EUR", )
        back = telebot.types.KeyboardButton(text="Назад")
        keyboard.add(usd, gbp, chi, rus, eur, korea, back)
        bot.send_message(message.chat.id, text="Выберите", reply_markup=keyboard)

    elif message.text == "USD":
        bot.send_message(message.chat.id, "Введите сумму:")
        curr = "USD"
    elif message.text == "GBP":
        bot.send_message(message.chat.id, "Введите сумму:")
        curr = "GBP"
    elif message.text == "RUR":
        bot.send_message(message.chat.id, "Введите сумму:")
        curr = "RUR"
    elif message.text == "CNY":
        bot.send_message(message.chat.id, "Введите сумму:")
        curr = "CNY"
    elif message.text == "KRW":
        bot.send_message(message.chat.id, "Введите сумму:")
        curr = "KRW"
    elif message.text == "EUR":
        bot.send_message(message.chat.id, "Введите сумму:")
        curr = "EUR"
    elif isinstance(int(message.text), int):
        if curr=="USD":
            res = int(message.text)*330
            bot.send_message(message.chat.id, "Результат: " + str(res))
            curr==""
    elif isinstance(int(message.text), int):
        if curr=="USD":
         res = int(message.text)*330
        bot.send_message(message.chat.id, "Результат: " + str(res))
        curr==""
    elif isinstance(int(message.text), int):
        if curr=="GBP":
         res = int(message.text)*330
        bot.send_message(message.chat.id, "Результат: " + str(res))
        curr==""
    elif isinstance(int(message.text), int):
        if curr=="KRW":
         res = int(message.text)*330
        bot.send_message(message.chat.id, "Результат: " + str(res))
        curr==""
    elif isinstance(int(message.text), int):
        if curr=="CNY":
         res = int(message.text)*330
        bot.send_message(message.chat.id, "Результат: " + str(res))
        curr==""
    elif isinstance(int(message.text), int):
        if curr=="RUR":
         res = int(message.text)*330
        bot.send_message(message.chat.id, "Результат: " + str(res))
        curr==""
    elif isinstance(int(message.text), int):
        if curr=="EUR":
         res = int(message.text)*330
         bot.send_message(message.chat.id, "Результат: " + str(res))
        curr==""


    elif message.text == "Перевести с другой валюты в KZT":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        usd = telebot.types.KeyboardButton(text="USD", )
        gbp = telebot.types.KeyboardButton(text="GBP", )
        chi = telebot.types.KeyboardButton(text="CNY", )
        korea = telebot.types.KeyboardButton(text="KRW", )
        rus = telebot.types.KeyboardButton(text="RUR", )
        eur = telebot.types.KeyboardButton(text="EUR", )
        back = telebot.types.KeyboardButton(text=":Назад")
        keyboard.add(usd, gbp, chi, rus, eur, korea, back)
        bot.send_message(message.chat.id, text="Выберите", reply_markup=keyboard)
    elif message.text == "USD":
        bot.send_message(message.chat.id, "Введите сумму:")
        curr = "USD"
    elif message.text == "GBP":
        bot.send_message(message.chat.id, "Введите сумму:")
        curr = "GBP"
    elif message.text == "RUR":
        bot.send_message(message.chat.id, "Введите сумму:")
        curr = "RUR"
    elif message.text == "CNY":
        bot.send_message(message.chat.id, "Введите сумму:")
        curr = "CNY"
    elif message.text == "KRW":
        bot.send_message(message.chat.id, "Введите сумму:")
        curr = "KRW"
    elif message.text == "EUR":
        bot.send_message(message.chat.id, "Введите сумму:")
        curr = "EUR"
    elif isinstance(int(message.text), int):
        if curr == "USD":
            res = int(message.text) * 330
        bot.send_message(message.chat.id, "Результат: " + str(res))
        curr == ""
    elif isinstance(int(message.text), int):
        if curr == "USD":
            res = int(message.text) * 330
        bot.send_message(message.chat.id, "Результат: " + str(res))
        curr == ""
    elif isinstance(int(message.text), int):
        if curr == "GBP":
            res = int(message.text) * 330
        bot.send_message(message.chat.id, "Результат: " + str(res))
        curr == ""
    elif isinstance(int(message.text), int):
        if curr == "KRW":
            res = int(message.text) * 330
        bot.send_message(message.chat.id, "Результат: " + str(res))
        curr == ""
    elif isinstance(int(message.text), int):
        if curr == "CNY":
            res = int(message.text) * 330
        bot.send_message(message.chat.id, "Результат: " + str(res))
        curr == ""
    elif isinstance(int(message.text), int):
        if curr == "RUR":
            res = int(message.text) * 330
        bot.send_message(message.chat.id, "Результат: " + str(res))
        curr == ""
    elif isinstance(int(message.text), int):
        if curr == "EUR":
            res = int(message.text) * 330
            bot.send_message(message.chat.id, "Результат: " + str(res))
        curr == ""
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
        path = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + ulat + "," + ulng + "&radius=500&type=cafe&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
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
    elif(s=="nearbyfood"):
        global food
        path = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + food + "&location=" + ulat + "," + ulng + "&radius=300&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
        with urllib.request.urlopen(path) as url:
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                lat = data[i]['geometry']['location']['lat']
                lng = data[i]['geometry']['location']['lng']
                name = data[i]['name']
                address = data[i]['formatted_address']
                if ('opening_hours' in data[i] and 'open_now' in data[i]['opening_hours']):
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
    elif(s=='hotel'):
        path = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + ulat + "," + ulng + "&radius=400&type=lodging&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
        ind = 0
        print(path)
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

bot.polling(none_stop=True, interval=5)
