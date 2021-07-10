import telebot
import json
from aiogram import types
import os
import re

# coding utf-8
def parse_txt_file(filename):
    f = open(filename, mode='r', encoding='UTF-8').read().split('\n')
    sl = {}
    for i in f:
        try:
            i = i.split(':')
            sl[i[0]] = i[1].strip()
        except:
            pass
    return sl


token = 'ХУЙ ВАМ А НЕ ТОКЕН'  # Bot username: @Denis_D_testbot
bot = telebot.TeleBot(token)


@bot.callback_query_handler(func=lambda
        c: 'sell_btn_' in c.data)
def process_callback_button5(callback_query: types.CallbackQuery):
    user_cmd = callback_query.data
    config_data = parse_txt_file('config.txt')
    answer = 'НАЖАТА КНОПКА ПРОДАТЬ!'
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, answer)


def start_pump(message):
    if os.path.exists(str(message.chat.id) + '.txt'):
        print('+')
        f = open(str(message.chat.id) + '.txt', encoding='UTF-8').read().split('\n')
        while f[-1] == '':
            f = f[:len(f) - 1]
        for i in f:
            if 'lang' in i:
                current_language = i.split(': ')[1]
                break
        config_data = parse_txt_file('config.txt')
        answer = config_data[f'pump_process_text_{current_language}']
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(config_data[f'sell_btn_{current_language}'],
                                              callback_data=f'sell_btn_p_{current_language}'))
        bot.send_message(message.chat.id, answer, reply_markup=[markup])

@bot.callback_query_handler(func=lambda
        c: 'start_btn_' in c.data)
def process_callback_button5(callback_query: types.CallbackQuery):
    user_cmd = callback_query.data
    config_data = parse_txt_file('config.txt')
    current_language = get_lang(user_cmd)
    if '_l_' in user_cmd:  # ЛИСТИНГ
        answer = config_data[f'snip_text_{current_language}']
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(config_data[f'sell_btn_{current_language}'],
                                              callback_data=f'sell_btn_l_{current_language}'))
        bot.answer_callback_query(callback_query.id)
        bot.send_message(callback_query.from_user.id, answer, reply_markup=[markup])




def get_lang(user_cmd):
    print(user_cmd, 'fsdf')
    if 'English' in user_cmd:
        current_language = 'English'
    elif 'فارسی' in user_cmd:
        current_language = 'فارسی'
    elif 'हिंदी' in user_cmd:
        current_language = 'हिंदी'
    elif '中國人' in user_cmd:
        current_language = '中國人'
    elif 'Español' in user_cmd:
        current_language = 'Español'
    else:
        current_language = 'wtf'
    return current_language


@bot.callback_query_handler(func=lambda
        c: '-_l' in c.data or '-_p' in c.data)
def process_callback_button3(callback_query: types.CallbackQuery):
    user_cmd = callback_query.data
    config_data = parse_txt_file('config.txt')
    current_language = get_lang(user_cmd)
    answer = config_data[f'minus_info_{current_language}']
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, answer)


@bot.callback_query_handler(func=lambda
        c: '+_l' in c.data or '+_p' in c.data)
def process_callback_button4(callback_query: types.CallbackQuery):
    user_cmd = callback_query.data
    config_data = parse_txt_file('config.txt')
    current_language = get_lang(user_cmd)
    if '+_l' in user_cmd:  # ЛИСТИНГ
        answer = config_data[f'snip_prestart_text_{current_language}']
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(config_data[f'start_btn_{current_language}'],
                                              callback_data=f'start_btn_l_{current_language}'))
        bot.answer_callback_query(callback_query.id)
        bot.send_message(callback_query.from_user.id, answer, reply_markup=[markup])
    else:  # ПАМП
        answer = config_data[f'pump_prestart_text_{current_language}']
        bot.answer_callback_query(callback_query.id)
        bot.send_message(callback_query.from_user.id, answer)



@bot.callback_query_handler(func=lambda
        c: 'edit' in c.data)
def process_callback_button2(callback_query: types.CallbackQuery):
    user_cmd = callback_query.data
    config_data = parse_txt_file('config.txt')
    current_language = get_lang(user_cmd)
    answer = config_data[f'change_text_{current_language}']
    f = open(str(callback_query.from_user.id) + '.txt', encoding='UTF-8').read().split('\n')
    print(f)
    f[-1] = 'status: ' + user_cmd[0]
    file_new = open(str(callback_query.from_user.id) + '.txt', 'w', encoding='UTF-8')
    for i in f:
        file_new.write(i + '\n')
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, answer)


@bot.callback_query_handler(func=lambda
        c: '1_btn' in c.data or '2_btn' in c.data or '3_btn' in c.data or '4_btn' in c.data or '5_btn'
           in c.data or '6_btn' in c.data or '7_btn' in c.data)
def process_callback_button1(callback_query: types.CallbackQuery):
    user_cmd = callback_query.data
    current_language = get_lang(user_cmd)
    if not os.path.exists(str(callback_query.from_user.id) + '.txt'):
        with open(str(callback_query.from_user.id) + '.txt', 'w', encoding='UTF-8') as f:
            f.write('private_key: None\n')
            f.write('adress: None\n')
            f.write('sum: None\n')
            f.write('xx: None\n')
            f.write('timer: None\n')
            f.write('listing: None\n')
            f.write('pamp: None\n')
            f.write(f'lang: {current_language}\n')
            f.write('status: 0')
    user_data = parse_txt_file(str(callback_query.from_user.id) + '.txt')
    config_data = parse_txt_file('config.txt')
    params_in_list = [user_data['private_key'], user_data['adress'], user_data['sum'], user_data['xx'],
                      user_data['timer'], user_data['listing'], user_data['pamp']]
    answer = config_data[f'i_param_{user_cmd[0]}_{current_language}'] + ': ' + params_in_list[int(user_cmd[0]) - 1]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(config_data[f'edit_{current_language}'],
                                          callback_data=f'{user_cmd[0]}_edit_{current_language}'),
               )
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, answer, reply_markup=[markup])


@bot.message_handler()
def initialize(message):
    print(message.text)
    data = parse_txt_file('config.txt')
    ################### Screen #1 (start) #################
    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtna = types.KeyboardButton(data['NAME_lang1'])
        itembtnb = types.KeyboardButton(data['NAME_lang2'])
        itembtnc = types.KeyboardButton(data['NAME_lang3'])
        itembtnd = types.KeyboardButton(data['NAME_lang4'])
        itembtne = types.KeyboardButton(data['NAME_lang5'])
        markup.row(itembtna)
        markup.row(itembtnb)
        markup.row(itembtnc)
        markup.row(itembtnd)
        markup.row(itembtne)
        bot.send_message(message.chat.id, 'Choose language:', reply_markup=[markup])
    ################# Screen #2 part 1 (hi message + buttons) ###############

    elif message.text == data['NAME_lang1'] or message.text == data['NAME_lang2'] or message.text == data[
        'NAME_lang3'] or message.text == data['NAME_lang4'] or message.text == data['NAME_lang5']:
        message.text = message.text.split()[0]
        answer = data[f'hi_message_{message.text}']
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_settings = types.KeyboardButton(data[f'button_settings_{message.text}'])
        btn_manual = types.KeyboardButton(data[f'manual_button_{message.text}'])
        btn_support = types.KeyboardButton(data[f'support_button_{message.text}'])
        btn_payment = types.KeyboardButton(data[f'payment_button_{message.text}'])
        btn_pump = types.KeyboardButton(data[f'pump_button_{message.text}'])
        btn_listing = types.KeyboardButton(data[f'listing_button_{message.text}'])
        markup.row(btn_settings)
        markup.row(btn_manual)
        markup.row(btn_support)
        markup.row(btn_payment)
        markup.row(btn_pump)
        markup.row(btn_listing)
        bot.send_message(message.chat.id, answer, reply_markup=[markup])
######### listing and pump ############
    elif message.text == data['param_6_فارسی'] or message.text == data['param_6_English'] or message.text == data[
        'param_6_हिंदी'] or message.text == data['param_6_中國人'] or message.text == data['param_6_Español']:
        if message.text == data['param_6_فارسی']:
            lang = 'فارسی'
        elif message.text == data['param_6_English']:
            lang = 'English'
        elif message.text == data['param_6_हिंदी']:
            lang = 'हिंदी'
        elif message.text == data['param_6_中國人']:
            lang = '中國人'
        elif message.text == data['param_6_Español']:
            lang = 'Español'
        else:
            lang = 'error'
        answer = data[f'listing1_text_{lang}']
        if not os.path.exists(str(message.chat.id) + '.txt'):
            answer += '\nERROR_NOT_REGISTERED'
        else:
            f = open(str(message.chat.id) + '.txt', 'r', encoding='UTF-8').read()
            end_idx = f.index('lang')
            answer += '\n' + f[:end_idx]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(data[f'yes_text_{lang}'], callback_data=f'+_l_{lang}'),
                   types.InlineKeyboardButton(data[f'no_text_{lang}'], callback_data=f'-_l_{lang}')
                   )
        bot.send_message(message.chat.id, answer, reply_markup=[markup])


    elif message.text == data['param_7_فارسی'] or message.text == data['param_7_English'] or message.text == data[
        'param_7_हिंदी'] or message.text == data['param_7_中國人'] or message.text == data['param_7_Español']:
        if message.text == data['param_7_فارسی']:
            lang = 'فارسی'
        elif message.text == data['param_7_English']:
            lang = 'English'
        elif message.text == data['param_7_हिंदी']:
            lang = 'हिंदी'
        elif message.text == data['param_7_中國人']:
            lang = '中國人'
        elif message.text == data['param_7_Español']:
            lang = 'Español'
        else:
            lang = 'error'
        answer = data[f'pamp1_text_{lang}']
        if not os.path.exists(str(message.chat.id) + '.txt'):
            answer += '\nERROR_NOT_REGISTERED'
        else:
            f = open(str(message.chat.id) + '.txt', 'r', encoding='UTF-8').read()
            end_idx = f.index('lang')
            answer += '\n' + f[:end_idx]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(data[f'yes_text_{lang}'], callback_data=f'+_p_{lang}'),
                   types.InlineKeyboardButton(data[f'no_text_{lang}'], callback_data=f'-_p_{lang}')
                   )
        bot.send_message(message.chat.id, answer, reply_markup=[markup])


##########################!!!!!############################
    #############  Screen #3 part 1 (Manual) ################
    elif message.text == data['manual_button_English']:
        answer = data['manual_text_English']
        bot.send_message(message.chat.id, answer)
    elif message.text == data['manual_button_فارسی']:
        answer = data['manual_text_فارسی']
        bot.send_message(message.chat.id, answer)
    elif message.text == data['manual_button_हिंदी']:
        answer = data['manual_text_हिंदी']
        bot.send_message(message.chat.id, answer)
    elif message.text == data['manual_button_中國人']:
        answer = data['manual_text_中國人']
        bot.send_message(message.chat.id, answer)
    elif message.text == data['manual_button_Español']:
        answer = data['manual_text_Español']
        bot.send_message(message.chat.id, answer)

        #############  Screen #3 part 2 (Support) ################
    elif message.text == data['support_button_English']:
        answer = data['support_text_English']
        bot.send_message(message.chat.id, answer)
    elif message.text == data['support_button_فارسی']:
        answer = data['support_text_فارسی']
        bot.send_message(message.chat.id, answer)
    elif message.text == data['support_button_हिंदी']:
        answer = data['support_text_हिंदी']
        bot.send_message(message.chat.id, answer)
    elif message.text == data['support_button_中國人']:
        answer = data['support_text_中國人']
        bot.send_message(message.chat.id, answer)
    elif message.text == data['support_button_Español']:
        answer = data['support_text_Español']
        bot.send_message(message.chat.id, answer)

    #############  Screen #3 part 3 (Payment) #############
    elif message.text == data['payment_button_English']:
        answer = data['payment_text_English']
        bot.send_message(message.chat.id, answer)
    elif message.text == data['payment_button_فارسی']:
        answer = data['payment_text_فارسی']
        bot.send_message(message.chat.id, answer)
    elif message.text == data['payment_button_हिंदी']:
        answer = data['payment_text_हिंदी']
        bot.send_message(message.chat.id, answer)
    elif message.text == data['payment_button_中國人']:
        answer = data['payment_text_中國人']
        bot.send_message(message.chat.id, answer)
    elif message.text == data['payment_button_Español']:
        answer = data['payment_text_Español']
        bot.send_message(message.chat.id, answer)

    #############  Screen #3 part 4 (Settings) #############
    elif message.text == data['button_settings_English'] or message.text == data[
        'button_settings_فارسی'] or message.text == data['button_settings_हिंदी'] or message.text == \
            data['button_settings_中國人'] or message.text == data['button_settings_Español']:
        if message.text == data['button_settings_English']:
            lang_now = 'English'
        elif message.text == data['button_settings_فارسی']:
            lang_now = 'فارسی'
        elif message.text == data['button_settings_हिंदी']:
            lang_now = 'हिंदी'
        elif message.text == data['button_settings_中國人']:
            lang_now = '中國人'
        elif message.text == data['button_settings_Español']:
            lang_now = 'Español'
        else:
            lang_now = 'Error'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(data[f'param_1_{lang_now}'], callback_data=f'1_btn_{lang_now}'),
                   types.InlineKeyboardButton(data[f'param_2_{lang_now}'], callback_data=f'2_btn_{lang_now}')
                   )
        markup.add(types.InlineKeyboardButton(data[f'param_3_{lang_now}'], callback_data=f'3_btn_{lang_now}'),
                   types.InlineKeyboardButton(data[f'param_4_{lang_now}'], callback_data=f'4_btn_{lang_now}')
                   )
        markup.add(types.InlineKeyboardButton(data[f'param_5_{lang_now}'], callback_data=f'5_btn_{lang_now}'),
                   types.InlineKeyboardButton(data[f'param_6_{lang_now}'], callback_data=f'6_btn_{lang_now}')
                   )
        markup.add(types.InlineKeyboardButton(data[f'param_7_{lang_now}'], callback_data=f'7_btn_{lang_now}'), )
        answer = data[f'choose_param_text_{lang_now}']
        bot.send_message(message.chat.id, answer, reply_markup=[markup])
    elif re.search(r'0x[a-fA-F0-9]{40}', message.text) is not None:
        start_pump(message)
    else:
        if os.path.exists(str(message.chat.id) + '.txt'):
            print('+')
            f = open(str(message.chat.id) + '.txt', encoding='UTF-8').read().split('\n')
            while f[-1] == '':
                f = f[:len(f) - 1]
            f = f[-1].split(': ')
            if f[0] == 'status' and f[1] != '0':
                print('++')
                sss = f[1]
                c_f = open(str(message.chat.id) + '.txt', encoding='UTF-8').read().split('\n')
                c_f[int(f[1]) - 1] = c_f[int(f[1]) - 1].split(': ')[0] + ': ' + message.text
                while c_f[-1] == '':
                    c_f = c_f[:len(c_f) - 1]
                c_f[-1] = c_f[-1].split(': ')[0] + ': 0'
                with open(str(message.chat.id) + '.txt', 'w', encoding='UTF-8') as f:
                    for i in c_f:
                        if 'lang' in i:
                            language_now = i.split(': ')[1]
                        f.write(i + '\n')
                bot.send_message(message.chat.id, data[f'ok_text_{language_now}'])


bot.polling()
