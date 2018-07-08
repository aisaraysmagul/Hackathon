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
lat = data[i]['geometry']['location']['lat']
            lng = data[i]['geometry']['location']['lng']
            name = data[i]['name']
            openow = data[i]['opening_hours']['open_now']
            rating = data[i]['rating']
            address = data[i]['vicinity']
            if (openow == True):
                bot.send_message(message.chat.id, "name: " + name + "/n" + "address: " + address + "/n" + "rating: " + rating + "/n" + "Open now")
            elif (openow == False):
                bot.send_message(message.chat.id, "name: " + name + "/n" + "address: " + address + "/n" + "rating: " + rating + "/n" + "Close now")
            else:
                bot.send_message(message.chat.id, "name: " + name + "/n" + "address: " + address + "/n" + "rating: " + rating)
            bot.send_location(message.chat.id, lat, lng)
"""