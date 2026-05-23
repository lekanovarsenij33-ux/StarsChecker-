import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import time
import threading
import os

# КОНФИГ
BOT_TOKEN = "8874309956:AAGpGixsd_ogvrIR-naW3tn2PKbt63VybUg"
CHAT_ID = 8231750590
URL = "https://funpay.com/lots/2418/"
COOKIES = {"golden_key": "G6d5o1b334e2faeg5j1zh9b3x2b0v85v"}
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

bot = telebot.TeleBot(BOT_TOKEN)
limits = {"13": 20.0, "21": 30.0} 
user_state = {}
sent_lots = set()

# (Здесь вставь остальной код из моего предыдущего сообщения с меню и сканером)
# ...
# В самом конце оставь:
if __name__ == "__main__":
    threading.Thread(target=scanner, daemon=True).start()
    bot.infinity_polling()
  
