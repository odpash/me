import telebot
import json
from aiogram import types
import os
import re

all_keys = {'0': 'private_key',
            '1': 'adress',
            '2': 'sum',
            '3': 'xx',
            '4': 'timer',
            '5': 'listing',
            '6': 'pamp',
            '7': 'contract',
            '8': 'lang',
            '9': 'status'}


# coding utf-8
def parse_txt_file(filename):
    if filename == 'config.txt':
        f = open(filename, mode='r', encoding='UTF-8').read().split('\n')
        sl = {}
        for i in f:
            try:
                i = i.split(':')
                sl[i[0]] = i[1].strip()
            except:
                pass
        return sl
    else:
        return json.loads(open(filename, mode='r', encoding='UTF-8').read().replace("'", '"'))


token = '1851044696:AAHFM9l6hSTlX30uO09T9Ro_2DSLBiWCEt4'  # Bot username: olegpash_profile_bot
bot = telebot.TeleBot(token)


@bot.callback_query_handler(func=lambda
        c: 'ch_t_' in c.data or 'ch_r_' in c.data or 'ch_x_' in c.data)
def process_callback_button5(callback_query: types.CallbackQuery):
    user_cmd = callback_query.data
    config_data = parse_txt_file('config.txt')
    lang = get_lang(user_cmd)
    if '_p_' in user_cmd:
        command = 'pamp'
    else:
        command = 'listing'
    if '_t_' in user_cmd:
        command_2 = 't_btn_'
    elif '_r_' in user_cmd:
        command_2 = 'r_btn_'
    else:
        command_2 = 'x_btn_'
    command_2 += lang
    if os.path.exists(str(callback_query.from_user.id) + '.txt'):

        c_f = parse_txt_file(str(callback_query.from_user.id) + '.txt')
        c_f[command] = config_data[command_2]
        with open(str(callback_query.from_user.id) + '.txt', 'w', encoding='UTF-8') as file:
            file.write(str(c_f))
        file.close()
        bot.answer_callback_query(callback_query.id)
        bot.send_message(callback_query.from_user.id, config_data[f'ok_text_{lang}'])


@bot.callback_query_handler(func=lambda
        c: 'sell_btn_' in c.data)
def process_callback_button5(callback_query: types.CallbackQuery):
    user_cmd = callback_query.data
    config_data = parse_txt_file('config.txt')
    answer = 'НАЖАТА КНОПКА ПРОДАТЬ!'
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, answer)


def start_pump(message):
    if os.path.exists(str(message.from_user.id) + '.txt'):

        f = parse_txt_file(str(message.from_user.id) + '.txt')
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
    if '7_edit' not in user_cmd and '6_edit' not in user_cmd:
        f = parse_txt_file(str(callback_query.from_user.id) + '.txt')
        f['status'] = user_cmd[0]
        file_new = open(str(callback_query.from_user.id) + '.txt', 'w', encoding='UTF-8')
        file_new.write(str(f))
        file_new.close()
        bot.answer_callback_query(callback_query.id)
        bot.send_message(callback_query.from_user.id, answer)
    else:
        if '7_edit' in user_cmd:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(config_data[f't_btn_{current_language}'],
                                                  callback_data=f'ch_t_p_btn_{current_language}'),
                       )
            markup.add(types.InlineKeyboardButton(config_data[f'r_btn_{current_language}'],
                                                  callback_data=f'ch_r_p_btn_{current_language}'),
                       )
            markup.add(types.InlineKeyboardButton(config_data[f'x_btn_{current_language}'],
                                                  callback_data=f'ch_x_p_btn_{current_language}'),
                       )
            bot.answer_callback_query(callback_query.id)
            bot.send_message(callback_query.from_user.id, answer, reply_markup=[markup])
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(config_data[f'r_btn_{current_language}'],
                                                  callback_data=f'ch_r_l_btn_{current_language}'),
                       )
            markup.add(types.InlineKeyboardButton(config_data[f'x_btn_{current_language}'],
                                                  callback_data=f'ch_x_l_btn_{current_language}'),
                       )
            bot.answer_callback_query(callback_query.id)
            bot.send_message(callback_query.from_user.id, answer, reply_markup=[markup])


@bot.callback_query_handler(func=lambda
        c: '1_btn' in c.data or '2_btn' in c.data or '3_btn' in c.data or '4_btn' in c.data or '5_btn'
           in c.data or '6_btn' in c.data or '7_btn' in c.data or '8_btn' in c.data)
def process_callback_button1(callback_query: types.CallbackQuery):
    user_cmd = callback_query.data
    current_language = get_lang(user_cmd)
    if not os.path.exists(str(callback_query.from_user.id) + '.txt'):
        with open(str(callback_query.from_user.id) + '.txt', 'w', encoding='UTF-8') as f:
            f.write(str({"private_key": "None",
                         "adress": "None",
                         "sum": "None",
                         "xx": "None",
                         "timer": "None",
                         "listing": "None",
                         "pamp": "None",
                         "contract": "None",
                         "lang": current_language,
                         "status": "0"}))
        f.close()
    user_data = parse_txt_file(str(callback_query.from_user.id) + '.txt')
    config_data = parse_txt_file('config.txt')
    params_in_list = [user_data['private_key'], user_data['adress'], user_data['sum'], user_data['xx'],
                      user_data['timer'], user_data['listing'], user_data['pamp'], user_data['contract']]
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
        markup.row(itembtna, itembtnb)
        markup.row(itembtnc, itembtnd)
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
        markup.row(btn_listing, btn_pump)
        markup.row(btn_settings, btn_manual, btn_support, btn_payment)
        bot.send_message(message.chat.id, answer, reply_markup=[markup])
    ######### listing and pump ############
    elif message.text == data['listing_button_English'] or message.text == data[
        'listing_button_فارسی'] or message.text == data[
        'listing_button_हिंदी'] or message.text == data['listing_button_中國人'] or message.text == data[
        'listing_button_Español']:
        if message.text == data['listing_button_فارسی']:
            lang = 'فارسی'
        elif message.text == data['listing_button_English']:
            lang = 'English'
        elif message.text == data['listing_button_हिंदी']:
            lang = 'हिंदी'
        elif message.text == data['listing_button_中國人']:
            lang = '中國人'
        elif message.text == data['listing_button_Español']:
            lang = 'Español'
        else:
            lang = 'error'
        answer = data[f'listing1_text_{lang}']
        if not os.path.exists(str(message.from_user.id) + '.txt'):
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


    elif message.text == data['pump_button_English'] or message.text == data['pump_button_فارسی'] or message.text == \
            data[
                'pump_button_हिंदी'] or message.text == data['pump_button_中國人'] or message.text == data[
        'pump_button_Español']:
        if message.text == data['pump_button_English']:
            lang = 'English'
        elif message.text == data['pump_button_فارسی']:
            lang = 'فارسی'
        elif message.text == data['pump_button_हिंदी']:
            lang = 'हिंदी'
        elif message.text == data['pump_button_中國人']:
            lang = '中國人'
        elif message.text == data['pump_button_Español']:
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
        markup.add(types.InlineKeyboardButton(data[f'param_7_{lang_now}'], callback_data=f'7_btn_{lang_now}'),
                   types.InlineKeyboardButton(data[f'param_8_{lang_now}'], callback_data=f'8_btn_{lang_now}'), )
        answer = data[f'choose_param_text_{lang_now}']
        bot.send_message(message.chat.id, answer, reply_markup=[markup])
    elif re.search(r'0x[a-fA-F0-9]{40}', message.text) is not None:
        start_pump(message)
    else:
        print(message.from_user.id)
        if os.path.exists(str(message.from_user.id) + '.txt'):
            f = parse_txt_file(str(message.from_user.id) + '.txt')
            if f['status'] != '0':
                f[all_keys[str(int(f['status']) - 1)]] = message.text
                f['status'] = '0'
                a = str(f)
                print(a)
                file = open(str(message.from_user.id) + '.txt', mode='w', encoding='UTF-8')
                file.write(a)
                file.close()
                bot.send_message(message.chat.id, data[f'ok_text_{f["lang"]}'])
            return
        try:

            if os.path.exists(str(message.from_user.id) + '.txt'):
                f = parse_txt_file(str(message.from_user.id) + '.txt')['lang']
                bot.send_message(message.chat.id, data[f'none_{f}'])
                return
        except:
            pass
        bot.send_message(message.chat.id, 'Unknown command. Please, write /start')


bot.polling()
