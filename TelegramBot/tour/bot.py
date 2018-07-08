import pyowm as pyowm
import telebot
import constants
import urllib.request, json
import pypyodbc
from telebot import types
import requests, bs4

bot = telebot.TeleBot(constants.token)


#upd = bot.get_updates()
#print(upd)
#last_upd = upd[-1]
#message_from_user = last_upd.message
#print(message_from_user)

#print(bot.get_me())

server = 'DESKTOP-MDK8SUM'
db = 'teleBot'
connection = pypyodbc.connect('Driver={SQL Server};'
                              'Server=' + server + ';'
                              'Database=' + db + ';')

#results = cursor.fetchall()
#print(results)
#connection.close()

s = ""
food = ""
ulat=0
ulng=0
string =""
cry = ""
money=""


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("🍽 Где поесть в Алматы ?")
    user_markup.row("🏔 Где отдохнуть в Алматы ?")
    user_markup.row("🛏 Где переночевать в Алматы ?")
    user_markup.row("🏪 Ближайшие магазины/супермаркеты")
    user_markup.row("🏥 Ближайшие больницы")
    user_markup.row("📝 Планнер")
    user_markup.row("🇰🇿 Конвертер валют")
    user_markup.row("⛅️ Погода")
    bot.send_message(message.chat.id, 'Добро пожаловать!', reply_markup=user_markup)

@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, "Помощь")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    global s, food, cry, money
    if message.text == "🍽 Где поесть в Алматы ?":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        near = telebot.types.KeyboardButton(text="Ближайшие")
        spisok = telebot.types.KeyboardButton(text="В городе")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(near, spisok, back)
        bot.send_message(message.chat.id, "Выберите местоположение", reply_markup=keyboard)
    elif message.text == "Ближайшие":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        asian = telebot.types.KeyboardButton(text="Азиатская")
        national = telebot.types.KeyboardButton(text="Национальная")
        europian = telebot.types.KeyboardButton(text="Европейская")
        turkish = telebot.types.KeyboardButton(text="Турецкая")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(national, asian, europian, turkish, back)
        bot.send_message(message.chat.id, "Выберите кухню", reply_markup=keyboard)
        s = "nearbyfood"
    elif message.text == "Азиатская":
        k = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        mesto = telebot.types.KeyboardButton(text="Отправить свое местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        k.add(mesto, back)
        bot.send_message(message.chat.id, "Отправьте свое местоположение", reply_markup=k)
        food = "asian+food"
    elif message.text == "Национальная":
        k = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        mesto = telebot.types.KeyboardButton(text="Отправить свое местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        k.add(mesto, back)
        bot.send_message(message.chat.id, "Отправьте свое местоположение", reply_markup=k)
        food = "national+food"
    elif message.text == "Европейская":
        k = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        mesto = telebot.types.KeyboardButton(text="Отправить свое местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        k.add(mesto, back)
        bot.send_message(message.chat.id, "Отправьте свое местоположение", reply_markup=k)
        food = "european+food"
    elif message.text == "Турецкая":
        k = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        mesto = telebot.types.KeyboardButton(text="Отправить свое местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        k.add(mesto, back)
        bot.send_message(message.chat.id, "Отправьте свое местоположение", reply_markup=k)
        food = "turkish+food"
    elif message.text == "В городе":
        k = telebot.types.InlineKeyboardMarkup()
        asian = telebot.types.InlineKeyboardButton(text="Азиатская", url="https://www.visitalmaty.kz/ru/cuisines")
        national = telebot.types.InlineKeyboardButton(text="Национальная", url="https://www.visitalmaty.kz/ru/cuisines")
        europian = telebot.types.InlineKeyboardButton(text="Европейская", url="https://www.visitalmaty.kz/ru/cuisines")
        turkish = telebot.types.InlineKeyboardButton(text="Турецкая", url = "https://www.visitalmaty.kz/ru/cuisines")
        k.add(asian, national, europian, turkish)
        bot.send_message(message.chat.id, "Выберите кухню", reply_markup=k)
    elif message.text == "⛅ Погода":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(back)
        city = bot.send_message(message.chat.id, "В каком городе Вам показать погоду?", reply_markup=keyboard)
        bot.register_next_step_handler(city, weath)
    elif message.text == "◀ Назад":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("🍽 Где поесть в Алматы ?")
        user_markup.row("🏔 Где отдохнуть в Алматы ?")
        user_markup.row("🛏 Где переночевать в Алматы ?")
        user_markup.row("🏪 Ближайшие магазины/супермаркеты")
        user_markup.row("🏥 Ближайшие больницы")
        user_markup.row("📝 Планнер")
        user_markup.row("🇰🇿 Конвертер валют")
        user_markup.row("⛅ Погода")
        bot.send_message(message.chat.id, 'Добро пожаловать!', reply_markup=user_markup)
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
        mesta = telebot.types.InlineKeyboardButton(text="Нажмите здесь",
                                                   url="https://www.visitalmaty.kz/ru/accomodations")
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
            bot.send_message(message.chat.id,"📌" + n1 + "\n📆 " + n2 + "\n💵 " + n3)
            keyboard = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(text="Добавить", callback_data="test2" + str(i))
            keyboard.add(button)
            bot.send_message(message.chat.id, "Добавьте в свой to do list: ", reply_markup=keyboard)
    elif message.text == "🏥 Ближайшие больницы":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = telebot.types.KeyboardButton(text="📍 Отправить местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(button)
        keyboard.add(back)
        bot.send_message(message.chat.id, "Отправьте, пожалуйста, локацию: ", reply_markup=keyboard)
        s = "hospital"

    elif message.text == "🏪 Ближайшие магазины/супермаркеты":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = telebot.types.KeyboardButton(text="📍 Отправить местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(back, button)
        bot.send_message(message.chat.id, "Отправьте, пожалуйста, локацию: ", reply_markup=keyboard)
        s = "store"

    elif message.text == "🚕 Транспорт":
        sqlQuery  = ("""
                    SELECT Name, Number 
                    FROM dbo.Taxi
        """)
        cursor = connection.cursor()
        cursor.execute(sqlQuery)
        results = cursor.fetchall()
        for row in results:
            Name = row[0]
            Number = row[1]
            print(str(Name),str(Number))
            bot.send_message(message.chat.id, "🚕 " + str(Name) + "📞 " + str(Number))
    elif message.text == "📝 Планнер":
        global string
        bot.send_message(message.chat.id, "Планнер на сегодня: ")
        query1 = ("SELECT NAME, ADDRESS FROM dbo.food")
        cursor = connection.cursor()
        cursor.execute(query1)
        results = cursor.fetchall()
        for row in results:
            NAME = row[0]
            ADDRESS = row[1]
            print(str(NAME),str(ADDRESS))
            string += " 🍽 "+str(NAME)+" "+str(ADDRESS)+" "
        query2 = ("SELECT location, cost FROM dbo.event1")
        cursor = connection.cursor()
        cursor.execute(query2)
        results = cursor.fetchall()
        for row in results:
            location = row[0]
            cost = row[1]
            print(str(location), str(cost))
            string += "🕺 " + str(location)+" "+str(cost)+" "
        query3 = ("SELECT name, description FROM dbo.Mountain")
        cursor = connection.cursor()
        cursor.execute(query3)
        results = cursor.fetchall()
        for row in results:
            name = row[0]
            description = row[1]
            print(str(name), str(description))
            string += "🕺 " + str(name)+" "+str(description)+" "
        query4 = ("SELECT name, address FROM dbo.park")
        cursor = connection.cursor()
        cursor.execute(query4)
        results = cursor.fetchall()
        for row in results:
            name = row[0]
            address = row[1]
            print(str(name), str(address))
            string += "🕺 " + str(name) + " " + str(address) + " "
        query5 = ("SELECT name, address FROM dbo.trc")
        cursor = connection.cursor()
        cursor.execute(query5)
        results = cursor.fetchall()
        for row in results:
            name = row[0]
            address = row[1]
            print(str(name), str(address))
            string += "🕺 " + str(name) + " " + str(address) + " "
        bot.send_message(message.chat.id, string)
        string = " "
    elif message.text == "🇰🇿 Конвертер валют":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text="Перевести KZT ➡")
        button2 = telebot.types.KeyboardButton(text="Перевести KZT ⬅")
        keyboard.add(button1, button2)
        bot.send_message(message.chat.id, "Выберите, пожалуйста: ", reply_markup=keyboard)

    elif message.text == "Перевести KZT ➡":
        money = "kzt"
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        usd = telebot.types.KeyboardButton(text="KZT -> USD 🇺🇸")
        gbp = telebot.types.KeyboardButton(text="KZT -> GBP 🇬🇧")
        cny = telebot.types.KeyboardButton(text="KZT -> CNY 🇨🇳")
        krw = telebot.types.KeyboardButton(text="KZT -> KRW 🇰🇷")
        rur = telebot.types.KeyboardButton(text="KZT -> RUR 🇷🇺")
        eur = telebot.types.KeyboardButton(text="KZT -> EUR 🇪🇺")
        jpy = telebot.types.KeyboardButton(text="KZT -> JPY 🇯🇵")
        kgs = telebot.types.KeyboardButton(text="KZT -> KGS 🇰🇬")
        uzs = telebot.types.KeyboardButton(text="KZT -> UZS 🇺🇿")
        chf = telebot.types.KeyboardButton(text="KZT -> CHF 🇨🇭")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(usd, gbp, cny, krw, rur, eur, jpy, kgs, uzs, chf, back)
        bot.send_message(message.chat.id, text="Выберите валюту: ", reply_markup=keyboard)
    elif message.text == "KZT -> USD 🇺🇸":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "USD"
    elif message.text == "KZT -> GBP 🇬🇧":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "GBP"
    elif message.text == "KZT -> CNY 🇨🇳":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "CNY"
    elif message.text == "KZT -> KRW 🇰🇷":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "KRW"
    elif message.text == "KZT -> RUR 🇷🇺":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "RUR"
    elif message.text == "KZT -> EUR 🇪🇺":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "EUR"
    elif message.text == "KZT -> JPY 🇯🇵":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "JPY"
    elif message.text == "KZT -> KGS 🇰🇬":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "KGS"
    elif message.text == "KZT -> UZS 🇺🇿":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "UZS"
    elif message.text == "KZT -> CHF 🇨🇭":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "CHF"

    elif message.text == "Перевести KZT ⬅":
        money = "curr"
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        usd = telebot.types.KeyboardButton(text="🇺🇸 USD -> KZT")
        gbp = telebot.types.KeyboardButton(text="🇬🇧 GBP -> KZT")
        cny = telebot.types.KeyboardButton(text="🇨🇳 CNY -> KZT")
        krw = telebot.types.KeyboardButton(text="🇰🇷 KRW -> KZT")
        rur = telebot.types.KeyboardButton(text="🇷🇺 RUR -> KZT")
        eur = telebot.types.KeyboardButton(text="🇪🇺 EUR -> KZT")
        jpy = telebot.types.KeyboardButton(text="🇯🇵 JPY -> KZT")
        kgs = telebot.types.KeyboardButton(text="🇰🇬 KGS -> KZT")
        uzs = telebot.types.KeyboardButton(text="🇺🇿 UZS -> KZT")
        chf = telebot.types.KeyboardButton(text="🇨🇭 CHF -> KZT")
        back = telebot.types.KeyboardButton(text="◀ Назад")
        keyboard.add(usd, gbp, cny, krw, rur, eur, jpy, kgs, uzs, chf)
        keyboard.add(back)
        bot.send_message(message.chat.id, text="Выберите валюту: ", reply_markup=keyboard)

    elif message.text == "🇺🇸 USD -> KZT":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "USD1"
    elif message.text == "🇬🇧 GBP -> KZT":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "GBP1"
    elif message.text == "🇨🇳 CNY -> KZT":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "CNY1"
    elif message.text == "🇰🇷 KRW -> KZT":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "KRW1"
    elif message.text == "🇷🇺 RUR -> KZT":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "RUR1"
    elif message.text == "🇪🇺 EUR -> KZT":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "EUR1"
    elif message.text == "🇯🇵 JPY -> KZT":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "JPY1"
    elif message.text == "🇰🇬 KGS -> KZT":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "KGS1"
    elif message.text == "🇺🇿 UZS -> KZT":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "UZS1"
    elif message.text == "🇨🇭 CHF -> KZT":
        bot.send_message(message.chat.id, "Введите сумму: ")
        cry = "CHF1"

    elif message.text == "🏔 Где отдохнуть в Алматы ?":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("⚱️ Музеи")
        user_markup.row("🏔 Горы")
        user_markup.row("🎡 Парки развлечений")
        user_markup.row("ТРЦ")
        user_markup.row("Курортные зоны")
        user_markup.row("◀ Назад")
        bot.send_message(message.chat.id, 'Выберите место отдыха', reply_markup=user_markup)

    elif message.text == "⚱️ Музеи":
        with urllib.request.urlopen(
                "https://maps.googleapis.com/maps/api/place/textsearch/json?query=museum+in+Almaty&keyword=food&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI") as url:
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                lat = data[i]['geometry']['location']['lat']
                lng = data[i]['geometry']['location']['lng']
                name = data[i]['name']
                address = data[i]['formatted_address']
                keyboard = telebot.types.InlineKeyboardMarkup()
                button = telebot.types.InlineKeyboardButton(text="Добавить", callback_data="test3" + str(i))
                keyboard.add(button)
                if ('opening_hours' in data[i]):
                    openow = data[i]['opening_hours']['open_now']
                    opennow = ""
                    if (openow == True):
                        opennow = "Open"
                    elif (openow == False):
                        opennow = "Close"
                else:
                    opennow = "unknown"
                if ('rating' in data[i]):
                    rating = data[i]['rating']
                else:
                    rating = "unknown"
                bot.send_message(message.chat.id, "____________________________________")
                bot.send_message(message.chat.id,
                                 "📌 name: " + str(name) + "\n" + "📍 address: " + str(
                                     address) + "\n" + "⭐️ rating: " + str(
                                     rating) + "\n" + "🚪 Open/Close: " + opennow + "\n" + "📍 location: ")
                bot.send_location(message.chat.id, lat, lng)
                bot.send_message(message.chat.id, "Добавьте в свой to do list: ", reply_markup=keyboard)
    elif message.text == "🎡 Парки развлечений":
        with urllib.request.urlopen(
                "https://maps.googleapis.com/maps/api/place/textsearch/json?query=amusement_park+in+Almaty&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI") as url:
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                lat = data[i]['geometry']['location']['lat']
                lng = data[i]['geometry']['location']['lng']
                name = data[i]['name']
                address = data[i]['formatted_address']
                keyboard = telebot.types.InlineKeyboardMarkup()
                button = telebot.types.InlineKeyboardButton(text="Добавить", callback_data="test4" + str(i))
                keyboard.add(button)
                if ('opening_hours' in data[i]):
                    openow = data[i]['opening_hours']['open_now']
                    opennow = ""
                    if (openow == True):
                        opennow = "Open"
                    elif (openow == False):
                        opennow = "Close"
                else:
                    opennow = "unknown"
                if ('rating' in data[i]):
                    rating = data[i]['rating']
                else:
                    rating = "unknown"
                bot.send_message(message.chat.id, "____________________________________")
                bot.send_message(message.chat.id,
                                 "📌 name: " + str(name) + "\n" + "📍 address: " + str(
                                     address) + "\n" + "⭐️ rating: " + str(
                                     rating) + "\n" + "🚪 Open/Close: " + opennow + "\n" + "📍 location: ")
                bot.send_location(message.chat.id, lat, lng)
                bot.send_message(message.chat.id, "Добавьте в свой to do list: ", reply_markup=keyboard)
    elif message.text == "ТРЦ":
        with urllib.request.urlopen(
                "https://maps.googleapis.com/maps/api/place/textsearch/json?query=shopping_mall+in+Almaty&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI") as url:
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                lat = data[i]['geometry']['location']['lat']
                lng = data[i]['geometry']['location']['lng']
                name = data[i]['name']
                address = data[i]['formatted_address']
                keyboard = telebot.types.InlineKeyboardMarkup()
                button = telebot.types.InlineKeyboardButton(text="Добавить", callback_data="test5" + str(i))
                keyboard.add(button)
                if ('opening_hours' in data[i]):
                    openow = data[i]['opening_hours']['open_now']
                    opennow = ""
                    if (openow == True):
                        opennow = "Open"
                    elif (openow == False):
                        opennow = "Close"
                else:
                    opennow = "unknown"
                if ('rating' in data[i]):
                    rating = data[i]['rating']
                else:
                    rating = "unknown"
                bot.send_message(message.chat.id, "____________________________________")
                bot.send_message(message.chat.id,
                                 "📌 name: " + str(name) + "\n" + "📍 address: " + str(
                                     address) + "\n" + "⭐️ rating: " + str(
                                     rating) + "\n" + "🚪 Open/Close: " + opennow + "\n" + "📍 location: ")
                bot.send_location(message.chat.id, lat, lng)
                bot.send_message(message.chat.id, "Добавьте в свой to do list: ", reply_markup=keyboard)
    elif message.text == "Курортные зоны":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("Шымбулак")
        user_markup.row("Высокогорный Спортивный Комплекс МЕДЕУ")
        user_markup.row("Кок-тобе")
        user_markup.row("Ак булак")
        user_markup.row("Home club")
        user_markup.row("◀ Назад")
        bot.send_message(message.chat.id, 'Выберите, чтобы посмотреть маршрут: ', reply_markup=user_markup)
    elif message.text == "Кок-тобе":
        bot.send_message(message.chat.id,"Гора Кок-Тобе, является одним из самых красивых и удивительных мест Казахстана.")
        key = telebot.types.InlineKeyboardMarkup()
        mesta = telebot.types.InlineKeyboardButton(text="Кок-тобе", url="http://www.koktobe.com")
        key.add(mesta)
        keyboard = telebot.types.InlineKeyboardMarkup()
        bot.send_location(message.chat.id, 43.2249503, 76.93780819999999)
        bot.send_message(message.chat.id, "Кок-тобе", reply_markup=key)
    elif message.text == "Высокогорный Спортивный Комплекс МЕДЕУ":
        bot.send_message(message.chat.id,
                         "Достопримечательность южной столицы Алматы - каток Медео имеет мировую славу. Медео - это самый высокогорный в мире спортивный комплекс. Этот сказочный дворец вписался в панораму ущелья на высоте 1961 метр над уровнем моря. давление, безветрие, чистая горная вода, из которой готовят лёд катка.")

        key = telebot.types.InlineKeyboardMarkup()
        mesta = telebot.types.InlineKeyboardButton(text="Медеу", url="http://medey.kz")
        key.add(mesta)
        bot.send_location(message.chat.id, 43.2089289, 76.9122691)
        bot.send_message(message.chat.id, "Высокогорный Спортивный Комплекс МЕДЕУ", reply_markup=key)
    elif message.text == "Шымбулак":
        bot.send_message(message.chat.id,
                         "Чимбулак – это разнообразие маршрутов, среди которых пологие и мягкие склоны для начинающих, длинные трассы для подготовленных лыжников, ФИС-трассы для скоростного спуска, дикие долины.")
        key = telebot.types.InlineKeyboardMarkup()
        mesta = telebot.types.InlineKeyboardButton(text="Шымбулак", url="https://www.shymbulak.com/contacts/")
        key.add(mesta)
        bot.send_location(message.chat.id, 43.119901, 77.097272)
        bot.send_message(message.chat.id, "Шымбулак", reply_markup=key)
    elif message.text == "Ак булак":
        bot.send_message(message.chat.id,
                         "«Ақ Бұлақ» предлагает провести время на фоне очаровательных горных пейзажей.  Географическое расположение высокогорного курорта действительно способствует организации качественного отдыха: умеренные климатические условия – перепад высот от 2600 м до 1400 м над уровнем моря, средняя температура летом от +15 до +2.")
        key = telebot.types.InlineKeyboardMarkup()
        mesta = telebot.types.InlineKeyboardButton(text="Ак булак", url="http://ak-bulak.kz")
        key.add(mesta)
        bot.send_location(message.chat.id, 43.2556675, 76.8049533)
        bot.send_message(message.chat.id, "Ак булак", reply_markup=key)
    elif message.text == "Home club":
        bot.send_message(message.chat.id,
                         "Изюминкой семейно-развлекательный комплекса «Home Club» является гармоничное сочетание современной инфраструктуры и девственной природы.")
        key = telebot.types.InlineKeyboardMarkup()
        mesta = telebot.types.InlineKeyboardButton(text="Home club", url="http://www.home-club.kz")
        key.add(mesta)
        bot.send_location(message.chat.id, 43.1541841, 76.5659784)
        bot.send_message(message.chat.id, "Home club", reply_markup=key)

    elif message.text == "🏔 Горы":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("Кок-Жайляу")
        user_markup.row("Пик Фурманова")
        user_markup.row("Бутаковские водопады")
        user_markup.row("Мынжилки")
        user_markup.row("Лесной перевал")
        user_markup.row("◀ Назад")
        bot.send_message(message.chat.id, 'Выберите, чтобы посмотреть маршрут: ', reply_markup=user_markup)

    elif message.text == "Кок-Жайляу":
        bot.send_message(message.chat.id,
                         "Кок-Жайляу, или Зеленое пастбище — одно из самых красивых мест в горах Алматы. Сохраняет свою привлекательность для любителей прогулок в горной местности на протяжении почти всего года")
        key = telebot.types.InlineKeyboardMarkup()
        mesta = telebot.types.InlineKeyboardButton(text="Маршурт",
                                                   url="https://www.google.com/maps/dir/ул.+Горная+550,+Алматы,+Казахстан/Kok+Zhailau,+Unnamed+Road,,+Алматы,+Казахстан/@43.1508555,77.011721,4395m/data=!3m1!1e3!4m14!4m13!1m5!1m1!1s0x38837b1dc375a513:0x250afa938525781e!2m2!1d77.0400669!2d43.1658753!1m5!1m1!1s0x388364b672b8c015:0x1732d09e1a098c24!2m2!1d77.0039902!2d43.1428419!3e2?hl=ru-RU")
        key.add(mesta)
        bot.send_message(message.chat.id, "Маршрут до Кок-жайляу", reply_markup=key)
    elif message.text == "Пик Фурманова":
        bot.send_message(message.chat.id,
                         "Путь начинается от экологического поста (со шлагбаумом), что находится в полутора километрах от ВСК «Медеу».")
        bot.send_message(message.chat.id,
                         "После того как заканчивается асфальтированная дорога, начинается хорошая грунтовая тропа, которая выводит на гребень, ведущий к пику Фурманова. Идите дальше вверх по гребню, в скором вы увидите знаменитые на качели, это место называется «Флаг».")
        key = telebot.types.InlineKeyboardMarkup()
        mesta = telebot.types.InlineKeyboardButton(text="Маршурт",
                                                   url="https://www.google.com/maps/@43.1542349,77.0836786,3116m/data=!3m2!1e3!4b1!4m2!6m1!1s1KTPoydxKbHNqKhHtNImIQMXroEw?hl=ru-RU")
        key.add(mesta)
        bot.send_message(message.chat.id, "Маршрут до Фурмановки", reply_markup=key)

    elif message.text == "Бутаковские водопады":
        bot.send_message(message.chat.id,
                         "Два водопада — Нижний (Большой) и Верхний находятся в Бутаковском ущелье. Добраться до водопадов вполне легко. Удобно начать путь к ним от второго шлагбаума в Бутаковском ущелье, добравшись до него на машине. Если же вы хотите обойтись без автомобиля, то можно доехать до поворота на Бутаковку на 29-ом автобусе. ")
        bot.send_message(message.chat.id,
                         "Далее дойдя до первого шлагбаума следует оплатить проход на Бутаковку. Пройдя первое ограждение, нужно идти до второго, за которым, через два километра будет база «Экстрим», от нее по тропинке около 800 метров располагается Нижний Бутаковский водопад.")
        key = telebot.types.InlineKeyboardMarkup()
        mesta = telebot.types.InlineKeyboardButton(text="Маршурт",
                                                   url="https://www.google.com/maps/@43.1542793,77.083516,3083m/data=!3m1!1e3!4m2!6m1!1s1T_bb0XdDHVKaZuM2BxhKgU6FBOE?hl=ru-RU")
        key.add(mesta)
        bot.send_message(message.chat.id, "Маршрут Бутаковского водопада", reply_markup=key)

    elif message.text == "Мынжилки":
        bot.send_message(message.chat.id,
                         "Урочище Мынжилки располагается на высоте 3100 метров над уровнем моря. Самый легкий способ добраться до него — это дорога, берущая начало от ВСК «Медеу». Далее следует подняться до ГЛК «Чимбулак», от которого идти вверх по дороге 5.7 километров пешком.")
        key = telebot.types.InlineKeyboardMarkup()
        t = "Мынжылки"
        mesta = telebot.types.InlineKeyboardButton(text="Маршурт",
                                                   url="https://www.google.com/maps/dir/Carlsberg+Kazakhstan,+Unnamed+Road,,+Алматы,+Казахстан/Плотина+Мынжылки,+Алматы,+Казахстан/@43.1115739,77.0427603,15305m/data=!3m1!1e3!4m14!4m13!1m5!1m1!1s0x38836b7f7f05aa09:0xb8068ad520575471!2m2!1d76.915183!2d43.3053436!1m5!1m1!1s0x38837db86b71ad99:0xea7159e2c16db99f!2m2!1d77.0783343!2d43.0845147!3e2?hl=ru-RU")
        key.add(mesta)
        bot.send_message(message.chat.id, "Маршрут Бутаковские водопады", reply_markup=key)
    elif message.text == "Лесной перевал":
        bot.send_message(message.chat.id,
                         "Данный перевал расположен в восточном водоразделе Бутаковского ущелья. Он соединяет Бутаковское ущелье и ущелье Котырбулак в районе туристической базы «Алматау». Доступен для походов круглый год, однако, зимой возможен сход лавин, проявляйте бдительность.")
        key = telebot.types.InlineKeyboardMarkup()
        mesta = telebot.types.InlineKeyboardButton(text="Маршурт",
                                                   url="https://www.google.com/maps/@43.1542793,77.083516,3083m/data=!3m1!1e3!4m2!6m1!1s1UWmveE88VWWw4F747lQmlbHSPI4?hl=ru-RU")
        key.add(mesta)
        bot.send_message(message.chat.id, "Маршрут до Лесного перевала", reply_markup=key)

    elif isinstance(int(message.text), int) and money == "curr":
        money = ""
        if cry == "USD1":
            url = 'https://v3.exchangerate-api.com/bulk/ed1e4a889e77bbc411367004/USD'
            response = requests.get(url)
            data = response.json()['rates']
            res = int(message.text) * data['KZT']
            bot.send_message(message.chat.id, res)
            cry = ""
        elif cry == "GBP1":
            url = 'https://v3.exchangerate-api.com/bulk/ed1e4a889e77bbc411367004/GBP'
            response = requests.get(url)
            data = response.json()['rates']
            res = int(message.text) * data['KZT']
            bot.send_message(message.chat.id, res)
            cry = ""
        elif cry == "RUR1":
            url = 'https://v3.exchangerate-api.com/bulk/ed1e4a889e77bbc411367004/RUR'
            response = requests.get(url)
            data = response.json()['rates']
            res = int(message.text) * data['KZT']
            bot.send_message(message.chat.id, res)
            cry = ""
        elif cry == "CNY1":
            url = 'https://v3.exchangerate-api.com/bulk/ed1e4a889e77bbc411367004/CNY'
            response = requests.get(url)
            data = response.json()['rates']
            res = int(message.text) * data['KZT']
            bot.send_message(message.chat.id, res)
            cry = ""
        elif cry == "EUR1":
            url = 'https://v3.exchangerate-api.com/bulk/ed1e4a889e77bbc411367004/EUR'
            response = requests.get(url)
            data = response.json()['rates']
            res = int(message.text) * data['KZT']
            bot.send_message(message.chat.id, res)
            cry = ""
        elif cry == "UZS1":
            url = 'https://v3.exchangerate-api.com/bulk/ed1e4a889e77bbc411367004/UZS'
            response = requests.get(url)
            data = response.json()['rates']
            res = int(message.text) * data['KZT']
            bot.send_message(message.chat.id, res)
            cry = ""
        elif cry == "JPY1":
            url = 'https://v3.exchangerate-api.com/bulk/ed1e4a889e77bbc411367004/JPY'
            response = requests.get(url)
            data = response.json()['rates']
            res = int(message.text) * data['KZT']
            bot.send_message(message.chat.id, res)
            cry = ""
        elif cry == "KGS1":
            url = 'https://v3.exchangerate-api.com/bulk/ed1e4a889e77bbc411367004/KGS'
            response = requests.get(url)
            data = response.json()['rates']
            res = int(message.text) * data['KZT']
            bot.send_message(message.chat.id, res)
            cry = ""
        elif cry == "KRW1":
            url = 'https://v3.exchangerate-api.com/bulk/ed1e4a889e77bbc411367004/KRW'
            response = requests.get(url)
            data = response.json()['rates']
            res = int(message.text) * data['KZT']
            bot.send_message(message.chat.id, res)
            cry = ""
        elif cry == "CHF1":
            url = 'https://v3.exchangerate-api.com/bulk/ed1e4a889e77bbc411367004/CHF'
            response = requests.get(url)
            data = response.json()['rates']
            res = int(message.text) * data['KZT']
            bot.send_message(message.chat.id, res)
            cry = ""

    elif isinstance(int(message.text), int) and money == "kzt":
        print("dgfd")
        url = 'https://v3.exchangerate-api.com/bulk/ed1e4a889e77bbc411367004/KZT'
        response = requests.get(url)
        data = response.json()['rates']
        money = ""
        if cry == "USD":
                res = int(message.text) * data['USD']
                bot.send_message(message.chat.id, res)
                cry = ""
        elif cry == "GBP":
                res = int(message.text) * data['GBP']
                bot.send_message(message.chat.id, res)
                cry = ""
        elif cry == "RUR":
                res = int(message.text) * data['RUR']
                bot.send_message(message.chat.id, res)
                cry = ""
        elif cry == "CNY":
                res = int(message.text) * data['CNY']
                bot.send_message(message.chat.id, res)
                cry = ""
        elif cry == "EUR":
                res = int(message.text) * data['EUR']
                bot.send_message(message.chat.id, res)
                cry = ""
        elif cry == "UZS":
                res = int(message.text) * data['UZS']
                bot.send_message(message.chat.id, res)
                cry = ""
        elif cry == "JPY":
                res = int(message.text) * data['JPY']
                bot.send_message(message.chat.id, res)
                cry = ""
        elif cry == "KGS":
                res = int(message.text) * data['KGS']
                bot.send_message(message.chat.id, res)
                cry = ""
        elif cry == "KRW":
                res = int(message.text) * data['KRW']
                bot.send_message(message.chat.id, res)
                cry = ""
        elif cry == "CHF":
                res = int(message.text) * data['CHF']
                bot.send_message(message.chat.id, res)
                cry = ""


@bot.message_handler(content_types=['location'])
def handle_location(message):
    global s, ulat, ulng
    ulat = str(message.location.latitude)
    ulng = str(message.location.longitude)
    if(s=="nearbyfood"):
        global food
        path = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + food + "&location=" + ulat + "," + ulng + "&radius=300&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
        with urllib.request.urlopen(path) as url:
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                lat = data[i]['geometry']['location']['lat']
                lng = data[i]['geometry']['location']['lng']
                name = data[i]['name']
                address = data[i]['formatted_address']
                keyboard = telebot.types.InlineKeyboardMarkup()
                button = telebot.types.InlineKeyboardButton(text="Добавить", callback_data="test"+str(i))
                keyboard.add(button)
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
                    bot.send_message(message.chat.id, "Добавьте в свой to do list: ", reply_markup=keyboard)
                else:
                    bot.send_message(message.chat.id, "____________________________________")
                    bot.send_message(message.chat.id,
                                     "📌 name: " + str(name) + "\n" + "📍 address: " + str(
                                         address) + "\n" + "🚪 Open/Close Unknown" + "\n" + "📍 location: ")
                    bot.send_location(message.chat.id, lat, lng)
                    bot.send_message(message.chat.id, "Добавьте в свой to do list: ", reply_markup=keyboard)
    elif(s=='hotel'):
        path = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + ulat + "," + ulng + "&radius=400&type=lodging&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
        with urllib.request.urlopen(path) as url:
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                lat = data[i]['geometry']['location']['lat']
                lng = data[i]['geometry']['location']['lng']
                name = data[i]['name']
                address = data[i]['vicinity']
                keyboard = telebot.types.InlineKeyboardMarkup()
                button = telebot.types.InlineKeyboardButton(text="Добавить", callback_data="test")
                keyboard.add(button)
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
                    bot.send_message(message.chat.id, "Добавьте в свой to do list: ", reply_markup=keyboard)
                else:
                    bot.send_message(message.chat.id, "____________________________________")
                    bot.send_message(message.chat.id,
                                     "📌 name: " + str(name) + "\n" + "📍 address: " + str(
                                         address) + "\n" + "🚪 Open/Close Unknown" + "\n" + "📍 location: ")
                    bot.send_location(message.chat.id, lat, lng)
                    bot.send_message(message.chat.id, "Добавьте в свой to do list: ", reply_markup=keyboard)
    elif s == "hospital":
        path = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + ulat + "," + ulng + "&radius=400&type=" + "hospital" + "&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
        with urllib.request.urlopen(path) as url:
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                lat = data[i]['geometry']['location']['lat']
                lng = data[i]['geometry']['location']['lng']
                name = data[i]['name']
                address = data[i]['vicinity']
                if ('rating' in data[i]):
                    rating = data[i]['rating']
                else:
                    rating = "unknown"
                if ('opening_hours' in data[i]):
                    openow = data[i]['opening_hours']['open_now']
                    opennow = ""
                    if (openow == True):
                        opennow = "Open"
                    elif (openow == False):
                        opennow = "Close"

            bot.send_message(message.chat.id, "____________________________________")
            bot.send_message(message.chat.id, "📌 name: " + str(name) + "\n" + "📍 address: " + str(
                address) + "\n" + "⭐️ rating: " + str(
                rating) + "\n" + "🚪 Open/Close: " + opennow + "\n" + "📍 location: ")
            bot.send_location(message.chat.id, lat, lng)
        s = ""

    elif s == "store":
        path = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + ulat + "," + ulng + "&radius=500&type=" + "supermarket" + "&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
        with urllib.request.urlopen(path) as url:
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                lat = data[i]['geometry']['location']['lat']
                lng = data[i]['geometry']['location']['lng']
                name = data[i]['name']
                address = data[i]['vicinity']
                if ('rating' in data[i]):
                    rating = data[i]['rating']
                else:
                    rating = "unknown"
                if ('opening_hours' in data[i]):
                    openow = data[i]['opening_hours']['open_now']
                    opennow = ""
                    if (openow == True):
                        opennow = "Open"
                    elif (openow == False):
                        opennow = "Close"
                bot.send_message(message.chat.id, "____________________________________")
                bot.send_message(message.chat.id, "📌 name: " + str(name) + "\n" + "📍 address: " + str(
                    address) + "\n" + "⭐️ rating: " + str(
                    rating) + "\n" + "🚪 Open/Close: " + opennow + "\n" + "📍 location: ")
                bot.send_location(message.chat.id, lat, lng)
        s = ""


@bot.message_handler(content_types=['text'])
def weath(message):
    owm = pyowm.OWM("6e4cdd6906c809a53f60196519cff051")
    city = message.text
    weather = owm.weather_at_place(city)
    w = weather.get_weather()
    temperature = w.get_temperature("celsius")["temp"]
    wind = w.get_wind()["speed"]
    hum = w.get_humidity()
    bot.send_message(message.chat.id, "Сейчас в городе " + str(city) + " , температура - " + str(temperature) + "°C, влажность - " + str(hum) + "%, скорость ветра - " +str(wind) + "м/с.")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global ulat, ulng, food
    path = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + food + "&location=" + str(ulat) + "," + str(ulng) + "&radius=300&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
    with urllib.request.urlopen(path) as url:
        data = json.loads(url.read().decode())['results']
        for i in range(len(data)):
            name = data[i]['name']
            address = data[i]['formatted_address']
            if call.data == "test"+str(i):
                cursor = connection.cursor()
                query = ("INSERT into dbo.food"
                         "(NAME,ADDRESS)"
                         "VALUES(?,?)")
                values = (str(name), str(address))
                #print(values)
                cursor.execute(query, values)
                query2 = ("SELECT NAME, ADDRESS FROM dbo.food")
                cursor.execute(query2)
                results = cursor.fetchall()
                for row in results:
                    NAME = row[0]
                    ADDRESS = row[1]
                    print(str(NAME), str(ADDRESS))
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Добавлено!")
        print("qwerty")
        s = requests.get('https://sxodim.com/almaty/events/vystavki/?show=today')
        b = bs4.BeautifulSoup(s.text, "html.parser")
        l = b.select('.news_list .location')
        c = b.select('.news_list .cost')
        for i in range(0, len(l)):
            print("asdfg")
            if call.data == "test2" + str(i):
                loc = l[i].getText()
                cost = c[i].getText()
                print("yuiop")
                cursor = connection.cursor()
                query = ("INSERT into dbo.event1"
                        "(location,cost)"
                        "VALUES(?,?)")
                values = (loc, cost)
                print(values)
                cursor.execute(query, values)
                print("vbnm")
                query2 = ("SELECT location, cost FROM dbo.event1")
                cursor.execute(query2)
                results = cursor.fetchall()
                print("12345678")
                for row in results:
                    print("ghjkl")
                    location = row[0]
                    cost = row[1]
                    print(str(location), str(cost))

        with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/textsearch/json?query=museum+in+Almaty&keyword=food&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI") as url:
            print("123456789")
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                name = data[i]['name']
                address = data[i]['formatted_address']
                if call.data == 'test3' + str(i):
                    cursor = connection.cursor()
                    query = ("INSERT into dbo.Mountain"
                             "(name, description)"
                             "VALUES(?,?)")
                    values = (str(name), str(address))
                    # print(values)
                    cursor.execute(query, values)
                    query2 = ("SELECT name, description FROM dbo.Mountain")
                    cursor.execute(query2)
                    results = cursor.fetchall()
                    for row in results:
                        name = row[0]
                        description = row[1]
                        print(str(name), str(description))

        with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/textsearch/json?query=amusement_park+in+Almaty&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI") as url:
            print("ais")
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                name = data[i]['name']
                address = data[i]['formatted_address']
                if call.data == "test4"+str(i):
                    cursor = connection.cursor()
                    query = ("INSERT into dbo.park"
                             "(name, address)"
                             "VALUES(?,?)")
                    values = (str(name), str(address))
                    print(values)
                    cursor.execute(query, values)
                    query2 = ("SELECT name, address FROM dbo.park")
                    cursor.execute(query2)
                    results = cursor.fetchall()
                    for row in results:
                        name = row[0]
                        address = row[1]
                        print(str(name), str(address))

        with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/textsearch/json?query=shopping_mall+in+Almaty&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI") as url:
            data = json.loads(url.read().decode())['results']
            for i in range(len(data)):
                name = data[i]['name']
                address = data[i]['formatted_address']
                if call.data == "test5"+str(i):
                    cursor = connection.cursor()
                    query = ("INSERT into dbo.trc"
                             "(name, address)"
                             "VALUES(?,?)")
                    values = (str(name), str(address))
                    # print(values)
                    cursor.execute(query, values)
                    query2 = ("SELECT name, address FROM dbo.trc")
                    cursor.execute(query2)
                    results = cursor.fetchall()
                    for row in results:
                        name = row[0]
                        address = row[1]
                        print(str(name), str(address))
bot.polling(none_stop=True, interval=1)


