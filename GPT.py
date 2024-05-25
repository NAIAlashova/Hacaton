import requests
import logging
from creds import get_creds

logging.basicConfig(level=logging.DEBUG, filename='log.txt', format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")

def ask_gpt(collection):
    url = f"https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    iam_token, folder_id = get_creds()
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'}
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 200},
        "messages": []}
    data["messages"].append({
        "role": 'user',
        "text": collection})
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            result = f"Status code {response.status_code}."
            logging.error(f'Status code {response.status_code}.\n')
            return result
        result = response.json()['result']['alternatives'][0]['message']['text']
    except Exception:
        result = "Произошла непредвиденная ошибка. Подробности см. в журнале."
        logging.error(f'{Exception}\n')
    return result

def count_tokens(text):
    iam_token, folder_id = get_creds()
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'}
    len_tokens = requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize",
        json={"modelUri": f"gpt://{folder_id}/yandexgpt/latest", "text": text},
        headers=headers)
    return len(len_tokens.json()['tokens'])
