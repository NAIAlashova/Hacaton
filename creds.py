import json
import logging
import time
from datetime import datetime
import requests
from config import IAM_TOKEN_PATH, FOLDER_ID_PATH, BOT_TOKEN_PATH

logging.basicConfig(filename='log.txt', level=logging.INFO, format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")
def create_new_token():
    metadata_url = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
    headers = {"Metadata-Flavor": "Google"}
    try:
        response = requests.get(metadata_url, headers=headers)
        if response.status_code == 200:
            token_data = response.json()
            token_data['expires_at'] = time.time() + token_data['expires_in']
            with open(IAM_TOKEN_PATH, "w") as token_file:
                json.dump(token_data, token_file)
            logging.info("Получен new iam_token\n")
            return response.json()
        else:
            logging.error(f"Ошибка получения iam_token. Статус-код: {response.status_code}\n")
    except Exception as e:
        logging.error(f"Ошибка получения iam_token: {e}\n")
def get_creds():
    try:
        with open(IAM_TOKEN_PATH, 'r') as f:
            expiration = datetime.strptime(json.load(f)["expires_at"][:26], "%Y-%m-%dT%H:%M:%S.%f")
        if expiration < datetime.now():
            logging.info("Срок годности iam_token истёк")
            create_new_token()
    except:
        create_new_token()
    with open(FOLDER_ID_PATH, 'r') as f:
        folder_id = f.read().strip()
    with open(IAM_TOKEN_PATH, 'r') as f:
        iam_token = json.load(f)["access_token"]
    return iam_token, folder_id
def get_bot_token():
    with open(BOT_TOKEN_PATH, 'r') as f:
        return f.read().strip()
