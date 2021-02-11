import telebot
from config import TOKEN, keys
from extention import ConversionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n' \
           ' <имя валюты цену которой хотите узнать> <имя валюты в которой надо узнать цену первой валюты> ' \
           '<количество первой валюты> \
\n посмотреть доступные валюты /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConversionException('Некорректный ввод.')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)

    except ConversionException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)