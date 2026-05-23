import telebot
import requests
from bs4 import BeautifulSoup
import time
import threading
import os
from flask import Flask

# --- КОНФИГ ---
BOT_TOKEN = "8874309956:AAGpGixsd_ogvrIR-naW3tn2PKbt63VybUg"
CHAT_ID = 8231750590
URL = "https://funpay.com/lots/2418/"
COOKIES = {"golden_key": "G6d5o1b334e2faeg5j1zh9b3x2b0v85v"}
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

bot = telebot.TeleBot(BOT_TOKEN)
limits = {"13": 20.0, "21": 30.0}
sent_lots = set()

# --- МИНИ-СЕРВЕР ДЛЯ RENDER ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# --- СКАНЕР ---
def scanner():
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update(COOKIES)
    
    while True:
        try:
            r = session.get(URL, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            lots = soup.find_all('a', class_='tc-item')
            
            current_lot_links = set()
            for lot in lots:
                try:
                    link = "https://funpay.com" + lot['href']
                    current_lot_links.add(link)
                    price = float(lot.find('div', class_='tc-price').text.replace('₽', '').replace(' ', '').strip())
                    title = lot.find('div', class_='tc-desc-text').text.upper()
                    
                    match = ("13" in title and price <= limits['13']) or ("21" in title and price <= limits['21'])
                    if match and link not in sent_lots:
                        msg = f"‼️ НАЙДЕНО!\n{title.strip()}\n💰 Цена: {price}₽\n🔗 {link}"
                        bot.send_message(CHAT_ID, msg)
                        sent_lots.add(link)
                except: continue
            sent_lots.intersection_update(current_lot_links)
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(5)

# --- ЗАПУСК ---
if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start() # Запуск веб-сервера
    threading.Thread(target=scanner, daemon=True).start() # Запуск сканера
    bot.infinity_polling()
    
