import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import config
from creds import get_bot_token
from ds import execute_query, count_all_symbol
from GPT import ask_gpt, count_tokens

bot = telebot.TeleBot(get_bot_token())
execute_query(config.query1)
l = {}

def ask(text, id):
    ans = ask_gpt(text)
    tokens = count_tokens(ans)
    execute_query(f'''INSERT INTO Requests (user_id, role, contents, tokens) VALUES ({id}, 'assistent', '{ans}', {tokens}) ;''')
    return ans
def promt(l):
    if 'для' in l[1]:
        text = f'Придумай {l[-1]} '
        if l[-1] == '1':
            text += 'кличку '
        elif l[-1] == '2':
            text += 'клички '
        else:
            text += 'кличек '
        text += f'{l[0]} {l[1]}'
        if l[2] == 'Да':
            text += f' {l[3]} окраса'
    else:
        text = f'Придумай {l[-1]} {l[0]} '
        if l[-1] == '1':
            text += 'имя '
        elif l[-1] == '2':
            text += 'имени '
        else:
            text += 'имен '
        text += f'{l[1]} происхождения'
        if l[2] == 'Да':
            text += f' со значением {l[3]}'
    return text
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
markup1.add(KeyboardButton('для кошки'))
markup1.add(KeyboardButton('для собаки'))
markup1.add(KeyboardButton('для грызуна'))
@bot.message_handler(commands=['name'])
def first(message):
    global l
    bot.send_message(message.chat.id, 'Если ты захочешь прекратить выбор имени, напиши команду /name.')
    if count_all_symbol(message.from_user.id) > 5000:
        bot.send_message(message.chat.id, 'К сожалению, у вас закончились токены. Я не смогу вам ответить.')
        return
    bot.send_message(message.chat.id, 'Какое имя ты хочешь?', reply_markup=markup1)
    l[message.from_user.id] = []
    bot.register_next_step_handler(message, second)

markup2 = ReplyKeyboardMarkup(resize_keyboard=True)
markup2.add(KeyboardButton('греческое'))
markup2.add(KeyboardButton('римское'))
markup2.add(KeyboardButton('русское'))
markup2.add(KeyboardButton('английское'))
markup2.add(KeyboardButton('французское'))
markup2.add(KeyboardButton('испанское'))
markup2.add(KeyboardButton('японское'))
markup3 = ReplyKeyboardMarkup(resize_keyboard=True)
markup3.add(KeyboardButton('девочка'))
markup3.add(KeyboardButton('мальчик'))
def second(message):
    right(message)
    global l
    if not 'для' in message.text:
        l[message.from_user.id].append(message.text[0:-2] + 'их')
        bot.send_message(message.chat.id, 'Какое происхождение у этого имени?', reply_markup=markup2)
        bot.register_next_step_handler(message, third_for_people)
    else:
        l[message.from_user.id].append(message.text)
        bot.send_message(message.chat.id, 'Это мальчик или девочка?', reply_markup=markup3)
        bot.register_next_step_handler(message, third_for_pet)

markup4 = ReplyKeyboardMarkup(resize_keyboard=True)
markup4.add(KeyboardButton('Да'))
markup4.add(KeyboardButton('Нет'))
def third_for_people(message):
    right(message)
    global l
    l[message.from_user.id].append(message.text[0:-1]+'го')
    bot.send_message(message.chat.id, 'Есть у этого имени значение?', reply_markup=markup4)
    bot.register_next_step_handler(message, fourth_for_people)

def fourth_for_people(message):
    right(message)
    global l
    l[message.from_user.id].append(message.text)
    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Напиши это значение')
        bot.register_next_step_handler(message, last)
    else:
        last(message)

def third_for_pet(message):
    right(message)
    global l
    if 'д' in message.text:
        l[message.from_user.id].append(message.text[0:-1]+'и')
    else:
        l[message.from_user.id].append(message.text[0:-1] + 'а')
    bot.send_message(message.chat.id, 'Хочешь указать его окрас?', reply_markup=markup4)
    bot.register_next_step_handler(message, fourth_for_pet)

def fourth_for_pet(message):
    right(message)
    global l
    l[message.from_user.id].append(message.text)
    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Напиши его в родительном падеже')
        bot.register_next_step_handler(message, last)
    else:
        last(message)

markup5 = ReplyKeyboardMarkup(resize_keyboard=True)
markup5.add(KeyboardButton('1'))
markup5.add(KeyboardButton('2'))
markup5.add(KeyboardButton('5'))
def last(message):
    right(message)
    global l
    l[message.from_user.id].append(message.text)
    bot.send_message(message.chat.id, 'Сколько имен тебе нужно?', reply_markup=markup5)
    bot.register_next_step_handler(message, ans)

def ans(message):
    right(message)
    global l
    l[message.from_user.id].append(message.text)
    print(l)
    text = promt(l[message.from_user.id])
    print(text)
    tokens = count_tokens(text)
    execute_query(f'''INSERT INTO Requests (user_id, role, contents, tokens) VALUES ({message.from_user.id}, 'user', '{text}', {tokens});''')
    text += '. Не пиши никакого пояснительного текста.'
    bot.send_message(message.chat.id, ask(text, message.from_user.id))

bot.infinity_polling()