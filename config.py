HOME_DIR = '/home/student/Hacaton'

LOGS = f'{HOME_DIR}/log.txt'
DB_FILE = f'{HOME_DIR}/messages.db'

IAM_TOKEN_PATH = f'{HOME_DIR}/creds/iam_token.txt'
FOLDER_ID_PATH = f'{HOME_DIR}/creds/folder_id.txt'
BOT_TOKEN_PATH = f'{HOME_DIR}/creds/bot_token.txt'

query1 = '''CREATE TABLE IF NOT EXISTS 'Requests' (
id INTEGER PRIMARY KEY,
user_id INTEGER, 
role TEXT,
contents TEXT,
tokens INTEGER);'''

hi = 'Привет. Я - бот, придумывающий имена по твоим критериям. \nДля этого просто напиши команду /name.'
help = 'Что случилось? Если я тебя не понимаю, сорри. Такое бывает. Может быть, я сломался. Тогда тебе придётся подождать, пока меня не исправят.\nЕсли же у тебя кончились токены, то к сожалинию сейчас функции по их пополнению сейчас нет.'
about = 'Я - бот-генератор. Меня подключили к нейросети, и теперь я знаю почти все имена, что есть в интернете. \nУ меня есть лимит по токенам(символам текста запроса). Если вы привысите лимит, то я не буду вам писать.'
