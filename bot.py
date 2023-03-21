import websocket
import json
import telebot

import botsecrets
import messagebuilder

# Получение секретов
HAMBART_ID = botsecrets.HAMBART_ID
BOT_TOKEN = botsecrets.BOT_TOKEN
CHAT_ID = botsecrets.CHAT_ID
KILLBOARD_URL = botsecrets.KILLBOARD_URL
KILLBOARD_START_MESSAGE = botsecrets.KILLBOARD_START_MESSAGE

# ТГ бот
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    '''
    Только для получения ИД чата, чтобы бот работал на единственный чат
    '''
    bot.send_message(chat_id=message.chat.id,
                     text=message.chat.id)

def log(message):
    '''
    Простое и красивое логирование
    '''
    print(f'✅ {message}')

def on_message(wsapp, message):
    '''
    Реакция на новое событие от сервера WS
    '''
    json_string = message
    json_dict = json.loads(json_string)

    killmail_id = json_dict['killmail_id']

    response = messagebuilder.response(json_dict=json_dict)
    if response is None:
        print(f">> killmail_id : {killmail_id} : ❌ No Hambart")
        return
    else:
        print(f">> killmail_id : {killmail_id} : 🟢 Hambart")

    bot.send_message(chat_id=CHAT_ID,
                     text=response)


def on_open(wsapp):
    '''
    Событие при подключении к WS
    '''
    log("Send killstream action message!")
    wsapp.send(KILLBOARD_START_MESSAGE)

def run_zkillboard_ws():
    '''
    Запуск ZKB WS
    '''
    log("Run ZKillBoard websockets!")
    ws = websocket.WebSocketApp(url=KILLBOARD_URL,
                                on_open=on_open,
                                on_message=on_message)
    ws.run_forever()

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