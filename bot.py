import requests

TOKEN = '8484771005:AAELMKkpBUTCBygG_DOg93Wj0DJQVmYJcCU'
TG_BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
KURS_URL = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/'

def get_updates(offset: int | None, limit: int = 100):
    url = f'{TG_BASE_URL}/getUpdates'
    params = {
        'offset': offset,
        'limit': limit
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        
        
        return response.json()['result']
    

def send_message(chat_id, text):
    url = f"{TG_BASE_URL}/sendMessage"
    params={
        'chat_id': chat_id,
        'text' : text
    }
    
    requests.get(url, params=params)

def get_usd_rate(summa):
    data = requests.get(KURS_URL).json()
    for item in data:
        if item["Ccy"] == "USD":
            kurs = float(item["Rate"])
            natija = summa / kurs
            return f"{summa:,.0f} so‘m ≈ {natija:,.2f} USD "

def get_euro_rate(summa):
    data = requests.get(KURS_URL).json()
    for item in data:
        if item["Ccy"] == "EUR":
            kurs = float(item["Rate"])
            natija = summa / kurs
            return f"{summa:,.0f} so‘m ≈ {natija:,.2f} EURO"

def get_rubl_rate(summa):
    data = requests.get(KURS_URL).json()
    for item in data:
        if item["Ccy"] == "RUB":
            kurs = float(item["Rate"])
            natija = summa / kurs
            return f"{summa:,.0f} so‘m ≈ {natija:,.2f}  RUBL"

def main():
    offset = None
    limit = 100

    while True:
        for update in get_updates(offset, limit):
            message = update['message']
            chat_id = message['chat']['id']
            
            if 'text' in message:
                text = message['text']

                if text == '/start':
                    send_message(chat_id, "👋 Salom!\nSo‘mni USD yoki EUR ga  va Rubl ga aylantiradigon botga xush kelibsiz!\nSummani kiriting. ")
                elif text.isdigit():
                    summa = int(text)
                    usd_text = get_usd_rate(summa)
                    eur_text = get_euro_rate(summa)
                    rub_text = get_rubl_rate(summa)

                    javob = f"{usd_text}\n{eur_text}\n{rub_text}"
                    send_message(chat_id, javob)
            
            
            offset = update['update_id'] + 1 


main()                    