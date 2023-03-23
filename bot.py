import websocket
import json
import telebot
import threading

import botsecrets
import messagebuilder
import anekdot

# Получение секретов
HAMBART_ID = botsecrets.HAMBART_ID
BOT_TOKEN = botsecrets.BOT_TOKEN
CHAT_ID = botsecrets.CHAT_ID
KILLBOARD_URL = botsecrets.KILLBOARD_URL
KILLBOARD_START_MESSAGE = botsecrets.KILLBOARD_START_MESSAGE

killmail_count = 0

# ТГ бот
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    '''
    Только для получения ИД чата, чтобы бот работал на единственный чат
    '''
    bot.send_message(chat_id=message.chat.id,
                     text=message.chat.id)
    
def send_killmail(killmail_response):
    '''
    Отправляет сообщение о killmail
    '''
    bot.send_message(chat_id=CHAT_ID,
                     text=killmail_response)

def send_random_anekdot():
    '''
    Отправляет рандомный анекдот
    '''
    try:
        anekdot_response = anekdot.get_anekdot()
    except Exception as e:
        anekdot_response = "Анекдота не будет"
    
    bot.send_message(chat_id=CHAT_ID,
                     text=anekdot_response)

def log(message):
    '''
    Простое и красивое логирование
    '''
    print(f'✅ {message}')

def on_close(wsapp):
    '''
    При переподключении происходит закрытие коннекта,
      это значит, что коннект нужно восстановить заново
    '''
    log("OnClose!")
    main()

def on_message(wsapp, message):
    '''
    Реакция на новое событие от сервера WS
    '''
    log(f"OnMessage! ({killmail_count})")
    killmail_count += 1
    
    json_string = message
    json_dict = json.loads(json_string)

    response = messagebuilder.response(json_dict=json_dict)
    
    if response is not None:
        send_killmail(killmail_response=response)
        send_random_anekdot()
    else:
        print('response == None')

def on_open(wsapp):
    '''
    Событие при подключении к WS
    '''
    log("OnOpen!")
    wsapp.send(KILLBOARD_START_MESSAGE)

def run_zkillboard_ws():
    '''
    Запуск ZKB WS
    '''
    log("Run ZKillBoard websockets!")
    try:
        ws = websocket.WebSocketApp(url=KILLBOARD_URL,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_close=on_close)
        wst = threading.Thread(target=ws.run_forever)
        wst.start()
    except Exception as e:
        print(f"Error : ({e})")

# DEBUG ONLY
def run_telegram_bot():
    '''
    Запуск прослушку ТГ бота, чтобы найти ИД чата
    '''
    bot.infinity_polling()

def main():
    '''
    Запуск бота
    '''
    run_zkillboard_ws()

    # DEBUG ONLY
    # run_telegram_bot()

if __name__ == '__main__':
    main()