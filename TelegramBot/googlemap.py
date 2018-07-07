import urllib.request, json

with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=43.241671,76.953997&radius=200&type=restaurant&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI") as url:
    data = json.loads(url.read().decode())['results']
    for i in range(len(data)):
        lat = data[i]['geometry']['location']['lat']
        lng = data[i]['geometry']['location']['lng']
        name = data[i]['name']
        openow = data[i]['opening_hours']['open_now']
        rating = data[i]['rating']
        address = data[i]['vicinity']
        print(address)

"""

    elif message.text == "Конвертер валют":
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
        back = telebot.types.KeyboardButton(text=":arrow_backward: Назад")
        keyboard.add(usd, gbp, chi, rus, eur, korea, back)
        money1 = bot.send_message(message.chat.id, "Введите сумму:", reply_markup=keyboard)
        if message.text == "USD":
            bot.send_message(message.chat.id, money1 * 1, reply_markup=keyboard)
        elif message.text == "GBP":
            bot.send_message(message.chat.id, money1 * 1, reply_markup=keyboard)
        elif message.text == "CNY":
            bot.send_message(message.chat.id, money1 * 1, reply_markup=keyboard)
        elif message.text == "KRW":
            bot.send_message(message.chat.id, money1 * 1, reply_markup=keyboard)
        elif message.text == "RUR":
            bot.send_message(message.chat.id, money1 * 1, reply_markup=keyboard)
        elif message.text == "EUR":
            bot.send_message(message.chat.id, money1 * 1, reply_markup=keyboard)

    elif message.text == "Перевести с другой валюты в KZT":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        usd = telebot.types.KeyboardButton(text="USD", )
        gbp = telebot.types.KeyboardButton(text="GBP", )
        chi = telebot.types.KeyboardButton(text="CNY", )
        korea = telebot.types.KeyboardButton(text="KRW", )
        rus = telebot.types.KeyboardButton(text="RUR", )
        eur = telebot.types.KeyboardButton(text="EUR", )
        back = telebot.types.KeyboardButton(text=":arrow_backward: Назад")
        keyboard.add(usd, gbp, chi, rus, eur, korea, back)
        money2 = bot.send_message(message.chat.id, "Введите сумму:?", reply_markup=keyboard)
        if message.text == "USD":
            bot.send_message(message.chat.id, money2 / 1, reply_markup=keyboard)
        elif message.text == "GBP":
            bot.send_message(message.chat.id, money2 / 1, reply_markup=keyboard)
        elif message.text == "CNY":
            bot.send_message(message.chat.id, money2 / 1, reply_markup=keyboard)
        elif message.text == "KRW":
            bot.send_message(message.chat.id, money2 / 1, reply_markup=keyboard)
        elif message.text == "RUR":
            bot.send_message(message.chat.id, money2 / 1, reply_markup=keyboard)
        elif message.text == "EUR":
            bot.send_message(message.chat.id, money2 / 1, reply_markup=keyboard)

"""