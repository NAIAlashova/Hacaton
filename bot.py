import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import config
from creds import get_bot_token
from ds import execute_query, count_all_symbol
from GPT import ask_gpt, count_tokens

bot = telebot.TeleBot(get_bot_token())
execute_query(config.query1)
l = []

def ask(text, id):
    ans = ask_gpt(text)
    tokens = count_tokens(ans)
    execute_query(f'''INSERT INTO Requests (user_id, role, contents, tokens) VALUES ({id}, 'assistent', '{ans}', {tokens}) ;''')
    return ans
def right(message):
    if '/' in message.text:
        if 'logging' in message.text:
            handle_logging(message)
        elif 'about' in message.text:
            handle_about(message)
        elif 'help' in message.text:
            handle_help(message)
        elif 'start' in message.text:
            handle_start(message)
        elif 'name' in message.text:
            first(message)
        else:
            bot.send_message(message.chat.id, 'Непонятный запрос. Попробуйте пожалуйста заново.')
    else:
       pass

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, config.hi)
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, config.help)
@bot.message_handler(commands=['about'])
def handle_about(message):
    bot.send_message(message.chat.id, config.about)
@bot.message_handler(commands=['logging'])
def handle_logging(message):
    doc = open(config.LOGS, 'rb')
    doc = doc.read()
    bot.send_document(message.chat.id, doc)

markup1 = ReplyKeyboardMarkup(resize_keyboard=True)
markup1.add(KeyboardButton('мужское'))
markup1.add(KeyboardButton('женское'))
@bot.message_handler(commands=['name'])
def first(message):
    bot.send_message(message.chat.id, 'Если ты захочешь прекратить выбор имени, напиши команду /name.')
    if count_all_symbol(message.from_user.id) > 5000:
        bot.send_message(message.chat.id, 'К сожалению, у вас закончились токены. Я не смогу вам ответить.')
        return
    bot.send_message(message.chat.id, 'Какоге имя ты хочешь?', reply_markup=markup1)
    bot.register_next_step_handler(message, second)

markup2 = ReplyKeyboardMarkup(resize_keyboard=True)
markup2.add(KeyboardButton('греческое'))
markup2.add(KeyboardButton('римское'))
markup2.add(KeyboardButton('русское'))
markup2.add(KeyboardButton('английское'))
markup2.add(KeyboardButton('французское'))
markup2.add(KeyboardButton('испанское'))
def second(message):
    right(message)
    global l
    l.append(message.text[0:-2] + 'их')
    bot.send_message(message.chat.id, 'Какое происхождение у этого имени?', reply_markup=markup2)
    bot.register_next_step_handler(message, third)

markup3 = ReplyKeyboardMarkup(resize_keyboard=True)
markup3.add(KeyboardButton('Да'))
markup3.add(KeyboardButton('Нет'))
def third(message):
    right(message)
    global l
    l.append(message.text[0:-1]+'го')
    bot.send_message(message.chat.id, 'Есть у этого имени значение?', reply_markup=markup3)
    bot.register_next_step_handler(message, fourth)

def fourth(message):
    right(message)
    global l
    l.append(message.text)
    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Напиши это значение')
        bot.register_next_step_handler(message, last)
    else:
        last(message)

def last(message):
    right(message)
    global l
    text = f'Напиши 2 {l[0]} имени {l[1]} происхождения'
    if l[2] == 'Да':
        text += f'со значением {message.text}'
    tokens = count_tokens(text)
    execute_query(f'''INSERT INTO Requests (user_id, role, contents, tokens) VALUES ({message.from_user.id}, 'user', '{text}', {tokens});''')
    text += '. Не пиши никакого пояснительного текста.'
    bot.send_message(message.chat.id, ask(text, message.from_user.id))
    l = []


bot.infinity_polling()