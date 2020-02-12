# - *- coding: utf- 8 - *-
import telebot
from pyowm.exceptions import api_response_error
from telebot import types
import pyowm
from telebot.types import Message
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta
import pytz

TOKEN = '729553874:AAHxh0x2whEFh69sMw5vqaRbC_hMe3GOlug'
p = 'CAADAgAD-AMAAsflXwntBLTc7kttJhYE'
r = 'CAADAgAD-QMAAsflXwmkhivXpvUn0RYE'
y = 'CAADAgAD8QMAAsflXwnPWLrFG8IkHhYE'
v = 'CAADAgAD6QMAAsflXwn6tqOP1yFc8RYE'
i = 'CAADAgADEAQAAsflXwlh9DQUeITYHRYE'
t = 'CAADAgAD-wMAAsflXwnKZScVasGY6BYE'
owm = pyowm.OWM('24518df4b64477c590040eb626472721')
img_cloud = 'http://i.vikka.ua/1/80436/151238505520597800x500.jpg'
img_mist = 'https://ukranews.com/upload/news/2019/10/26/5a6d7dd6abf2a-screenshot-1_410x272.png?v=1'
img_clear = 'https://fabriory.com.ua/sites/default/files/styles/large/public/1-246.jpg?itok=SFcwHWN8'
img_snow = 'https://media.dyvys.info/2017/11/1450381224_1-696x392.jpg'
img_rain = 'http://www.poetryclub.com.ua/upload/poem_all/00805608.jpeg'
img_haze = 'https://static.espreso.tv/uploads/article/816944/images/im610x343-02.jpg'
img_drizzle = 'http://topnews.pl.ua/img/20191212/a9beb0c68ca2a2e48d4ba6963b6ac9db.jpg'

bot = telebot.TeleBot(TOKEN)

global dict1, dict2
dict1, dict2 = {}, {}

global users
users = 0


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Дізнатися погоду та прогноз на наступні 4 дні в будь-якій точці планети? '
                                      'Просто!\n '
                                      'Просто потрібно ввести назву міста або населеного пункту та обрати з меню '
                                      'подальшу дію і вуаля, дані про '
                                      'погоду в тому місці у вас на екрані.\n '
                                      'Якщо місто не українське, то назву потрібно вводити або англіською, '
                                      'або російською.')


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_sticker(message.chat.id, p)
    bot.send_sticker(message.chat.id, r)
    bot.send_sticker(message.chat.id, y)
    bot.send_sticker(message.chat.id, v)
    bot.send_sticker(message.chat.id, i)
    bot.send_sticker(message.chat.id, t)
    bot.send_message(message.chat.id, 'Як користуватися? /help')



@bot.message_handler(content_types=['text'])
def buttons(message: Message, users = users):
    try:
        city = message.text
        global observation, w, l, forecaster, forecast, weather_list
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        l = observation.get_location()
        forecaster = owm.three_hours_forecast(city)
        forecast = forecaster.get_forecast()
        weather_list = forecast.get_weathers()
        tz = TimezoneFinder().timezone_at(lng=l.get_lon(), lat=l.get_lat())
        local = pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone(tz))
        loc = local.isoformat()
        global diff
        diff = int(loc[26] + loc[27] + loc[28])
        global dd2
        dd2 = (datetime.now() + timedelta(days=2, hours=diff)).day
        if dd2 < 10:
            dd2 = '0' + str(dd2)
        global dm2
        dm2 = (datetime.now() + timedelta(days=2, hours=diff)).month
        if dm2 < 10:
            dm2 = '0' + str(dm2)
        global dd3
        dd3 = (datetime.now() + timedelta(days=3, hours=diff)).day
        if dd3 < 10:
            dd3 = '0' + str(dd3)
        global dm3
        dm3 = (datetime.now() + timedelta(days=3, hours=diff)).month
        if dm3 < 10:
            dm3 = '0' + str(dm3)
        global dd4
        dd4 = (datetime.now() + timedelta(days=4, hours=diff)).day
        if dd4 < 10:
            dd4 = '0' + str(dd4)
        global dm4
        dm4 = (datetime.now() + timedelta(days=4, hours=diff)).month
        if dm4 < 10:
            dm4 = '0' + str(dm4)
        dict1.update({message.from_user.username: city})
        dict2.update({message.chat.id: city})
        f = open('users.txt', 'w')
        str = ''
        for key in dict1:
            users += 1
            str += f'{users}) {key} - {dict1.get(key)}\n'
        f.write(str)
        global keyboard
        keyboard = types.InlineKeyboardMarkup()
        kb1 = types.InlineKeyboardButton(text=f"❌Прогноз до кінця дня у м. {dict1.get(message.from_user.username)}❌", callback_data="today")
        kb2 = types.InlineKeyboardButton(text=f"❌Прогноз на завтра у м. {dict1.get(message.from_user.username)}❌", callback_data="tomorrow")
        kb3 = types.InlineKeyboardButton(text=f"❌Прогноз на {dd2}.{dm2}"+f" у м. {dict1.get(message.from_user.username)}❌", callback_data="2days")
        kb4 = types.InlineKeyboardButton(text=f"❌Прогноз на {dd3}.{dm3}"+f" у м. {dict1.get(message.from_user.username)}❌", callback_data="3days")
        kb5 = types.InlineKeyboardButton(text=f"❌Прогноз на {dd4}.{dm4}"+f" у м. {dict1.get(message.from_user.username)}❌", callback_data="4days")
        kb6 = types.InlineKeyboardButton(text=f"💰Підтримати розробника💰", callback_data="donate")
        keyboard.add(kb1)
        keyboard.add(kb2)
        keyboard.add(kb3)
        keyboard.add(kb4)
        keyboard.add(kb5)
        keyboard.add(kb6)
        temp = round(w.get_temperature('celsius')['temp'], 1)
        wind = w.get_wind()['speed']
        humidity = w.get_humidity()
        hours = local.hour
        if hours < 10:
            hours = f'0{hours}'
        mins = local.minute
        if mins < 10:
            mins = f'0{mins}'
        secs = local.second
        if secs < 10:
            secs = f'0{secs}'
        local_time = f'{hours}:{mins}:{secs}'
        sunrise = w.get_sunrise_time('date') + timedelta(hours=diff)
        sr_hours = sunrise.hour
        if sr_hours < 10:
            sr_hours = f'0{sr_hours}'
        sr_mins = sunrise.minute
        if sr_mins < 10:
            sr_mins = f'0{sr_mins}'
        sr_secs = sunrise.second
        if sr_secs < 10:
            sr_secs = f'0{sr_secs}'
        sunrise = f'{sr_hours}:{sr_mins}:{sr_secs}'
        sunset = w.get_sunset_time('date') + timedelta(hours=diff)
        ss_hours = sunset.hour
        if ss_hours < 10:
            ss_hours = '0' + f'0{ss_hours}'
        ss_mins = sunset.minute
        if ss_mins < 10:
            ss_mins = f'0{ss_mins}'
        ss_secs = sunset.second
        if ss_secs < 10:
            ss_secs = f'0{ss_secs}'
        sunset = f'{ss_hours}:{ss_mins}:{ss_secs}'
        status = w.get_status()
        if status[0] is "M" or status[0] is "F":
            st = "туман"
            img = img_mist
        elif status[0] is "C" and status[1] is "l" and status[2] is "e":
            st = "чисте небо"
            img = img_clear
        elif status[0] is "C" and status[1] is "l" and status[2] is "o":
            st = "хмарно"
            img = img_cloud
        elif status[0] is "S":
            st = "сніг"
            img = img_snow
        elif status[0] is "R":
            st = "дощ"
            img = img_rain
        elif status[0] is "H":
            st = "імла"
            img = img_haze
        elif status[0] is "D":
            st = "мряка"
            img = img_drizzle
        answer = f'У м. {dict1.get(message.from_user.username)} {st}\n🌡️ Температура повітря: {temp}°C\n💨 Швидкість вітру: {wind}м/с\n💧 Вологість повітря: {humidity}' \
                 f'%\n🌞 Схід сонця: {sunrise}\n🌚 Захід сонця: {sunset}\n⌚ Місцевий час: {local_time}'
        bot.send_photo(message.chat.id, img, caption=answer, reply_markup=keyboard)
    except pyowm.exceptions.api_response_error.NotFoundError:
        bot.reply_to(message, "Генерація болота та пошук Петра І для створення міста")
    except pyowm.exceptions.api_call_error.APICallError:
        bot.reply_to(message, "Генерація болота та пошук Петра І для створення міста")
    except pyowm.exceptions.api_call_error.APIInvalidSSLCertificateError:
        bot.reply_to(message, "Генерація болота та пошук Петра І для створення міста")


@bot.callback_query_handler(func=lambda c: True)
def weather(c):
    cid = c.message.chat.id
    if c.data == 'today':
        hours_arr = []
        f = 'Прогноз погоди до кінця дня у м. '+str(dict2.get(cid))+'\n'
        sticker = ''
        for weather in weather_list:
            temp = round(weather.get_temperature('celsius')['temp'], 1)
            status = weather.get_status()
            if status[0] is "M" or status[0] is "F":
                st = "туман"
            elif status[0] is "C" and status[1] is "l" and status[2] is "e":
                st = "чисте небо"
            elif status[0] is "C" and status[1] is "l" and status[2] is "o":
                st = "хмарно"
            elif status[0] is "S":
                st = "сніг"
            elif status[0] is "R":
                st = "дощ"
            elif status[0] is "H":
                st = "імла"
            elif status[0] is "D":
                st = "мряка"
            hours = (weather.get_reference_time('date') + timedelta(hours=diff)).hour
            if hours is 0 or hours is 12:
                sticker = '🕛'
            elif hours is 3 or hours is 15:
                sticker = '🕒'
            elif hours is 6 or hours is 18:
                sticker = '🕕'
            elif hours is 9 or hours is 21:
                sticker = '🕘'
            if hours < 10:
                hours = '0' + str(hours)
            if (weather.get_reference_time('date') + timedelta(hours=diff)).day is (datetime.now() + timedelta(hours=diff)).day or \
                    (weather.get_reference_time('date') + timedelta(hours=diff)).day is (datetime.now() + timedelta(days=1, hours=diff)).day and \
                    (weather.get_reference_time('date') + timedelta(hours=diff)).hour is 0:
                hours_arr.append((weather.get_reference_time('date') + timedelta(hours=diff)).hour)
                f += sticker+" "+str(hours)+":00 - "+str(temp)+"°C, "+st+"\n"
            elif len(hours_arr) is 0:
                f = 'На жаль, поки що неможливо отримати погоду на сьогодні :(\nСпробуйте пізніше...'
        bot.send_message(cid, f)
    elif c.data == 'tomorrow':
        f = 'Прогноз погоди на завтра у м. '+str(dict2.get(cid))+':\n'
        sticker = ''
        for weather in weather_list:
            temp = round(weather.get_temperature('celsius')['temp'], 1)
            status = weather.get_status()
            if status[0] is "M" or status[0] is "F":
                st = "туман"
            elif status[0] is "C" and status[1] is "l" and status[2] is "e":
                st = "чисте небо"
            elif status[0] is "C" and status[1] is "l" and status[2] is "o":
                st = "хмарно"
            elif status[0] is "S":
                st = "сніг"
            elif status[0] is "R":
                st = "дощ"
            elif status[0] is "H":
                st = "імла"
            elif status[0] is "D":
                st = "мряка"
            hours = (weather.get_reference_time('date') + timedelta(hours=diff)).hour
            if hours is 0 or hours is 12:
                sticker = '🕛'
            elif hours is 3 or hours is 15:
                sticker = '🕒'
            elif hours is 6 or hours is 18:
                sticker = '🕕'
            elif hours is 9 or hours is 21:
                sticker = '🕘'
            if hours < 10:
                hours = '0'+str(hours)
            if (weather.get_reference_time('date') + timedelta(hours=diff)).day is (datetime.now() + timedelta(days=1, hours=diff)).day or \
                    (weather.get_reference_time('date') + timedelta(hours=diff)).day is (datetime.now() + timedelta(days=2, hours=diff)).day and \
                    (weather.get_reference_time('date') + timedelta(hours=diff)).hour is 0:
                f += sticker+" "+str(hours)+":00 - "+str(temp)+"°C, "+st+"\n"
        bot.send_message(cid, f)
    elif c.data == '2days':
        f = 'Прогноз погоди на '+str(dd2)+'.'+str(dm2)+' у м. '+str(dict2.get(cid))+':\n'
        sticker = ''
        for weather in weather_list:
            temp = round(weather.get_temperature('celsius')['temp'], 1)
            status = weather.get_status()
            if status[0] is "M" or status[0] is "F":
                st = "туман"
            elif status[0] is "C" and status[1] is "l" and status[2] is "e":
                st = "чисте небо"
            elif status[0] is "C" and status[1] is "l" and status[2] is "o":
                st = "хмарно"
            elif status[0] is "S":
                st = "сніг"
            elif status[0] is "R":
                st = "дощ"
            elif status[0] is "H":
                st = "імла"
            elif status[0] is "D":
                st = "мряка"
            hours = (weather.get_reference_time('date') + timedelta(hours=diff)).hour
            if hours is 0 or hours is 12:
                sticker = '🕛'
            elif hours is 3 or hours is 15:
                sticker = '🕒'
            elif hours is 6 or hours is 18:
                sticker = '🕕'
            elif hours is 9 or hours is 21:
                sticker = '🕘'
            if hours < 10:
                hours = '0'+str(hours)
            if (weather.get_reference_time('date') + timedelta(hours=diff)).day is (datetime.now() + timedelta(days=2, hours=diff)).day or \
                    (weather.get_reference_time('date') + timedelta(hours=diff)).day is (datetime.now() + timedelta(days=3, hours=diff)).day and \
                    (weather.get_reference_time('date') + timedelta(hours=diff)).hour is 0:
                f += sticker+" "+str(hours)+":00 - "+str(temp)+"°C, "+st+"\n"
        bot.send_message(cid, f)
    elif c.data == '3days':
        f = 'Прогноз погоди на '+str(dd3)+'.'+str(dm3)+' у м. '+str(dict2.get(cid))+':\n'
        sticker = ''
        for weather in weather_list:
            temp = round(weather.get_temperature('celsius')['temp'], 1)
            status = weather.get_status()
            if status[0] is "M" or status[0] is "F":
                st = "туман"
            elif status[0] is "C" and status[1] is "l" and status[2] is "e":
                st = "чисте небо"
            elif status[0] is "C" and status[1] is "l" and status[2] is "o":
                st = "хмарно"
            elif status[0] is "S":
                st = "сніг"
            elif status[0] is "R":
                st = "дощ"
            elif status[0] is "H":
                st = "імла"
            elif status[0] is "D":
                st = "мряка"
            hours = (weather.get_reference_time('date') + timedelta(hours=diff)).hour
            if hours is 0 or hours is 12:
                sticker = '🕛'
            elif hours is 3 or hours is 15:
                sticker = '🕒'
            elif hours is 6 or hours is 18:
                sticker = '🕕'
            elif hours is 9 or hours is 21:
                sticker = '🕘'
            if hours < 10:
                hours = '0'+str(hours)
            if (weather.get_reference_time('date') + timedelta(hours=diff)).day is (datetime.now() + timedelta(days=3, hours=diff)).day or \
                    (weather.get_reference_time('date') + timedelta(hours=diff)).day is (datetime.now() + timedelta(days=4, hours=diff)).day and \
                    (weather.get_reference_time('date') + timedelta(hours=diff)).hour is 0:
                f += sticker+" "+str(hours)+":00 - "+str(temp)+"°C, "+st+"\n"
        bot.send_message(cid, f)
    elif c.data == '4days':
        f = 'Прогноз погоди на '+str(dd4)+'.'+str(dm4)+' у м. '+str(dict2.get(cid))+':\n'
        sticker = ''
        for weather in weather_list:
            temp = round(weather.get_temperature('celsius')['temp'], 1)
            status = weather.get_status()
            if status[0] is "M" or status[0] is "F":
                st = "туман"
            elif status[0] is "C" and status[1] is "l" and status[2] is "e":
                st = "чисте небо"
            elif status[0] is "C" and status[1] is "l" and status[2] is "o":
                st = "хмарно"
            elif status[0] is "S":
                st = "сніг"
            elif status[0] is "R":
                st = "дощ"
            elif status[0] is "H":
                st = "імла"
            elif status[0] is "D":
                st = "мряка"
            hours = (weather.get_reference_time('date') + timedelta(hours=diff)).hour
            if hours is 0 or hours is 12:
                sticker = '🕛'
            elif hours is 3 or hours is 15:
                sticker = '🕒'
            elif hours is 6 or hours is 18:
                sticker = '🕕'
            elif hours is 9 or hours is 21:
                sticker = '🕘'
            if hours < 10:
                hours = '0'+str(hours)
            if (weather.get_reference_time('date') + timedelta(hours=diff)).day is (datetime.now() + timedelta(days=4, hours=diff)).day or \
                    (weather.get_reference_time('date') + timedelta(hours=diff)).day is (datetime.now() + timedelta(days=5, hours=diff)).day and \
                    (weather.get_reference_time('date') + timedelta(hours=diff)).hour is 0:
                f += sticker+" "+str(hours)+":00 - "+str(temp)+"°C, "+st+"\n"
        bot.send_message(cid, f)
    elif c.data == 'donate':
        bot.send_message(cid, '5375414111089099')
        bot.send_sticker(cid, 'CAACAgIAAxkBAAIfwV40nQ47oLUvQFrX1Aj0R1pwYp_YAAIHBAACxKtoC9Qdpn8YTk3lGAQ')


if __name__ == '__main__':
    bot.polling(none_stop=True)
