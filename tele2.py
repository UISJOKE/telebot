import telebot
import mysql.connector
bot = telebot.TeleBot('1168768704:AAH2x7fAGMWECBYPKxm7E9IPbp9cQWR8_yU')
db = mysql.connector.connect(
        host='localhost',
        user = 'root',
        passwd = 'root',
        port = '3306',
        database = 'telebot'
)
cursor = db.cursor()

#cursor.execute('CREATE TABLE users(nickname VARCHAR(255))')
#cursor.execute('CREATE DATABASE telebot')
#cursor.execute('SHOW DATABASES')
#for x in cursor:
 #       print(x)
#cursor.execute('SHOW TABLES')
#for x in cursor:
 #       print(x)
#cursor.execute('ALTER TABLE users ADD COLUMN (id INT AUTO_INCREMENT PRIMARY KEY , user_id INT UNIQUE)')
user_dict = {}


class User:
    def __init__(self, nickname):
        self.nickname = nickname


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, 'Введите свой никнейм: ')
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Введит название объявления: ')
        bot.register_next_step_handler(msg, process_name_board_step)


def process_name_board_step(message):
        chat_id = message.chat.id
        name_board = message.text
        user = user_dict[chat_id]
        user.name_board = name_board
        msg = bot.reply_to(message, 'Введите текст объявления: ')
        bot.register_next_step_handler(msg, process_text_board_step)


def process_text_board_step(message):
        chat_id = message.chat.id
        text_board = message.text
        user = user_dict[chat_id]
        user.text_board = text_board
        sql = 'INSERT INTO users (nickname,user_id,name_board,text_board) VALUES (%s, %s, %s, %s)'
        val = (user.nickname, chat_id, user.name_board, user.text_board)
        cursor.execute(sql, val)
        db.commit()

        bot.send_message(chat_id, 'Ваше объявление успешно добавлено!\n ' + user.nickname + '\n' + user.name_board + '\n' + user.text_board)



bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling(none_stop=True)