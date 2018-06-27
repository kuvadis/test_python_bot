import requests  
import datetime
import apixu

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

    def get_weather(self):
        request = requests.get('http://api.apixu.com/v1/current.json?key=425b2297a2544f15932120436182306&q=Belaja Zerkow')
        current_weather = request.json()['current']['temp_c']
        return current_weather


testbot = BotHandler('611929199:AAFuGI6_I0Rn4Pkf7NOtk6bApvNRX7l3Ses')
now = datetime.datetime.now()


def main():  
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']


        if now.hour == 10 or last_chat_text == 'погодв':
            weather = testbot.get_weather()
            testbot.send_message(last_chat_id, 'Привет, ' + last_chat_name + '. Погода на сегодня: ' + weather)

         new_offset = last_update_id + 1



if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()