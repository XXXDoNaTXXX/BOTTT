#username: KNU_MF41_ilyaD_PZ4_bot
#name: ToyStore

import telebot as telebot
import sqlite3
from telebot import types

TOKEN = '1891625688:AAHD6H6xg0GqRD8DVD0ZE0cLAAyt3cQHdxs'
bot = telebot.TeleBot(TOKEN)

class BOT:
    def setup(self):
        self.db = sqlite3.connect('server.db')
        self.sql = self.db.cursor()
        self.sql.execute("SELECT * FROM toy")
        self.result = self.sql.fetchall()
        self.sql.execute("SELECT * FROM limitation")
        limitations = self.sql.fetchall()
        self.map_limit = {}
        for i in limitations:
            self.map_limit[int(i[0])] = i[2]

    def all_toys(self):
        self.sql.execute("SELECT * FROM toy")
        result = self.sql.fetchall()

    def update_by_type(self, type_):
        if type_ == "любой тип":
            return

        new_result = []
        for i in self.result:
            if i[2] == type_:

                new_result.append(i)
        self.result = new_result

    def update_by_manuf(self, manuf_):
        if manuf_ == "любая страна":
            return

        new_result = []
        for i in self.result:
            if i[1] == manuf_:
                new_result.append(i)

        self.result = new_result

    def update_by_sex(self, sex_):
        if sex_ == "любой пол":
            return

        new_result = []
        for i in self.result:
            if self.map_limit[int(i[3])] == sex_ or self.map_limit[int(i[3])] =="М&Ж":

                new_result.append(i)
        self.result = new_result

    def get_result(self):
        return self.result

    def get_mp(self):
        return self.map_limit

@bot.message_handler(content_types=['text'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЗдесь вы можете просмортеть различные игрушки для детей!".format(message.from_user,
                                                                                        bot.get_me()),
                     parse_mode='html')

    B = BOT()
    B.setup()
    get_type(B, message)


def get_type(B, message):  # получаем фамилию
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # наша клавиатура
    item1 = types.KeyboardButton("любой тип")
    item2 = types.KeyboardButton('настольные')
    item3 = types.KeyboardButton('конструкторы')
    item4 = types.KeyboardButton('мягкие игрушки')
    item5 = types.KeyboardButton('куклы')
    item6 = types.KeyboardButton('машинки')

    keyboard.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.from_user.id, text='Укажите тип игрушки.', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_county, B)

def get_county(message, B):
    B.update_by_type(message.text)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # наша клавиатура
    item1 = types.KeyboardButton("любая страна")
    item2 = types.KeyboardButton("Украина")
    item3 = types.KeyboardButton("Россия")
    item4 = types.KeyboardButton("Китай")

    keyboard.add(item1, item2, item3, item4)
    bot.send_message(message.from_user.id, text='Укажите страну производителя.', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_sex, B)

def get_sex(message, B):
    B.update_by_manuf(message.text)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # наша клавиатура
    item1 = types.KeyboardButton("любой пол")
    item2 = types.KeyboardButton("М")
    item3 = types.KeyboardButton("Ж")
    keyboard.add(item1, item2, item3)
    bot.send_message(message.from_user.id, text='Вы хотите посмотреть игрушки для мальчика или девочки?', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_res, B)

def get_res(message, B):
    B.update_by_sex(message.text)
    mp = B.get_mp()
    bot.send_message(message.from_user.id, "Игрушки которые подходят под ваши требования: ")
    if len(B.get_result()) == 0:
        bot.send_message(message.from_user.id, "С такими параметрами игрушки не найдены!")
    for i in B.get_result():
        bot.send_message(message.from_user.id, "Игрушка: \n    Название: " + i[0] + "\n    Производитель: " + i[1] + "\n    Тип игрушки: " + i[2] + "\n    Пол: " + mp[i[3]])

    bot.register_next_step_handler(message, welcome)

if __name__ == "__main__":

    bot.polling(none_stop=True)
