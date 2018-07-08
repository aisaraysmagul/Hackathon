import telebot
import constants
import urllib.request, json
import pyowm

bot = telebot.TeleBot(constants.token)

#upd = bot.get_updates()
#print(upd)
#last_upd = upd[-1]
#message_from_user = last_upd.message
#print(message_from_user)

#print(bot.get_me())

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("🍽 Где поесть в Алматы ?")
    user_markup.row("🏔 Где отдохнуть в Алматы ?")
    user_markup.row("🛏 Где переночевать в Алматы ?")
    user_markup.row("📝 Построить свой план")
    user_markup.row("⛅ Погода")
    bot.send_message(message.chat.id, 'Добро пожаловать!', reply_markup = user_markup)

@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, "Помощь")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "🍽 Где поесть в Алматы ?":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = telebot.types.KeyboardButton(text="📍 Отправить местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="◀ Назад", )
        keyboard.add(button)
        bot.send_message(message.chat.id, "Отправьте пожалуйста локацию: ", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Ошибка")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    ulat = str(message.location.latitude)
    ulng = str(message.location.longitude)
    path = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+ulat+","+ulng+"&radius=300&type=restaurant&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
    with urllib.request.urlopen(path) as url:
        data = json.loads(url.read().decode())['results']
        for i in range(len(data)):
            lat = data[i]['geometry']['location']['lat']
            lng = data[i]['geometry']['location']['lng']
            name = data[i]['name']
            openow = data[i]['opening_hours']['open_now']
            opennow = ""
            if(openow == True):
                opennow = "Open"
            elif(openow == False):
                opennow = "Close"
            rating = data[i]['rating']
            address = data[i]['vicinity']
            bot.send_message(message.chat.id, "____________________________________")
            bot.send_message(message.chat.id, "📌 name: " + str(name) + "\n" + "📍 address: " + str(address) + "\n" + "⭐ rating: " + str(rating) + "\n" + "🚪 Open/Close" + "\n" + "📍 location: ")
            bot.send_location(message.chat.id, lat, lng)


@bot.message_handler(content_types=['text'])
def handle_weather(message):
    if message.text == "⛅ Погода":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        answer = bot.send_message(message.chat.id, "В каком городе Вам показать погоду?")
        bot.register_next_step_handler(answer,weath)
        city = message.text
        weather = owm.weather_at_place(city)
        w = weather.get_weather()
        desc = w.get_detailed_status()
        temp = w.get_temperature("celcius")["temp"]
        hum = w.get_humidity()
        wind = get_wind()["speed"]
        bot.send_message(message.chat.id, "Сейчас в Алматы " + str(desc) + " температура воздуха - " + str(temp) + "℃ ,влажность - " + str(hum) + "% ,скорость ветра - " + str(wind) + "м/c")

def weath(message):
    owm = owm.OWM("6e4cdd6906c809a53f60196519cff051")

bot.polling(none_stop=True, interval=1)
