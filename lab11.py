import telebot
import re
import requests
import json
bot = telebot.TeleBot("1156430009:AAEHtciDJ5PdEzbe0MVnvd9qv_DiG1DohSk")
GLOBAL_OPERATION_TYPE = ''
GLOBAL_OPERATION_CURRENCY = ''
GLOBAL_OPERATION_CURRENCY_CODE = ''

def load_exchange(code):
    URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json&valcode=' + code.upper();
    curr = json.loads(requests.get(URL).text)
    if(curr):
        return curr[0]['rate'];
    return 0;

def fromUah(value, currency):
    global GLOBAL_OPERATION_CURRENCY, GLOBAL_OPERATION_CURRENCY_CODE
    result = round(float(value) * load_exchange(currency), 2);
    res_string = str(value) + GLOBAL_OPERATION_CURRENCY_CODE + ' = ' + str(result) + '₴'
    return res_string;

def toUah(value, currency):
    global GLOBAL_OPERATION_CURRENCY, GLOBAL_OPERATION_CURRENCY_CODE
    result = round(float(value) / load_exchange(currency), 2);
    res_string = str(value) + '₴ = ' + str(result) + GLOBAL_OPERATION_CURRENCY_CODE;
    return res_string;


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def RepresentsFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


start_buttons = {
 "uah_to_usd": "Конвертувати гривні в долари",
 "uah_to_eur": "Конвертувати гривні в євро",
 "eur_to_uah": "Конвертувати євро в гривні",
 "usd_to_uah": "Конвертувати долари в гривні",
}

start_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
start_keyboard.row(start_buttons["uah_to_usd"], start_buttons["uah_to_eur"])
start_keyboard.row(start_buttons["eur_to_uah"], start_buttons['usd_to_uah'])
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Вітаю, " + message.chat.first_name, reply_markup=start_keyboard)

@bot.message_handler(content_types=['text'])
def handle_text(message):
 global GLOBAL_OPERATION_TYPE
 global GLOBAL_OPERATION_CURRENCY
 global GLOBAL_OPERATION_CURRENCY_CODE
 if message.text == start_buttons["uah_to_usd"]:
    GLOBAL_OPERATION_TYPE = 'to'
    GLOBAL_OPERATION_CURRENCY = 'usd'
    GLOBAL_OPERATION_CURRENCY_CODE = '$'
    bot.send_message(message.chat.id, 'Вкажіть суму у гривні яку бажаєте конвертувати до долларів:')
 elif message.text == start_buttons["uah_to_eur"]:
     GLOBAL_OPERATION_TYPE = 'to'
     GLOBAL_OPERATION_CURRENCY = 'eur'
     GLOBAL_OPERATION_CURRENCY_CODE = '€'
     bot.send_message(message.chat.id, 'Вкажіть суму у гривні яку бажаєте конвертувати до євро:')
 elif message.text == start_buttons["eur_to_uah"]:
     GLOBAL_OPERATION_TYPE = 'from'
     GLOBAL_OPERATION_CURRENCY = 'eur'
     GLOBAL_OPERATION_CURRENCY_CODE = '€'
     bot.send_message(message.chat.id, 'Вкажіть суму у євро яку бажаєте конвертувати до гривні:')
 elif message.text == start_buttons["usd_to_uah"]:
     GLOBAL_OPERATION_TYPE = 'from'
     GLOBAL_OPERATION_CURRENCY = 'usd'
     GLOBAL_OPERATION_CURRENCY_CODE = '$'
     bot.send_message(message.chat.id, 'Вкажіть суму у долларах яку бажаєте конвертувати до гривні:')
 elif RepresentsInt(message.text) or RepresentsFloat(message.text):
     if(GLOBAL_OPERATION_TYPE == 'to'):
         bot.send_message(message.chat.id, toUah(message.text, GLOBAL_OPERATION_CURRENCY))
     elif(GLOBAL_OPERATION_TYPE == 'from'):
         bot.send_message(message.chat.id, fromUah(message.text, GLOBAL_OPERATION_CURRENCY))

     bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=start_keyboard)
 else:
     bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=start_keyboard)

bot.polling()
