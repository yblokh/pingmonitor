import ping3
import time
import requests
import logging

LOG_FILE = 'pingmonitor.log'

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace these values with your actual chat_id, message, and bot_api_key
chat_id = "Telegram chat id"
bot_api_key = "Your Telegram bot api key"
message = ""

def send_telegram_message(chat_id, message, bot_api_key):
    url = f"https://api.telegram.org/bot{bot_api_key}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")

def check_host(host, status_dict):
    result = ping3.ping(host)
    if result is False:
        logging.info(f"{host} is not resolved!")

    elif result is not None:
        if status_dict[host]['status'] != 'up':
            if status_dict[host]['status'] == 'down':
                message = host+" is up!"
                logging.info(f"{message}")
                send_telegram_message(chat_id, message, bot_api_key)

            status_dict[host]['status'] = 'up'
            status_dict[host]['down_counter'] = 0
    else:
        if status_dict[host]['status'] != 'down':
            status_dict[host]['status'] = 'down'
            status_dict[host]['down_counter'] += 1

        if status_dict[host]['status'] == 'down':
            status_dict[host]['down_counter'] += 1
            #logging.warning(f"{ host} is down! (Attempt: {str(status_dict[host]['down_counter'])})")

        if status_dict[host]['down_counter'] == 3:
            message = host+" is down!"
            logging.warning(f"{message}")
            send_telegram_message(chat_id, message, bot_api_key) 

def read_hosts_from_file(file_path):
    with open(file_path, 'r') as file:
        hosts = [line.strip() for line in file.readlines()]
    return hosts

if __name__ == "__main__":
    hosts = read_hosts_from_file('hosts.txt')
    logging.info(f"{hosts}")
    host_status = {host: {'status': 'unknown', 'down_counter': 0} for host in hosts}
    while True:
        for host in hosts:
            check_host(host, host_status)
        time.sleep(15)  # Check every 15 seconds
