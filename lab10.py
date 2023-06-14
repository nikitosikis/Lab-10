import json
import pyaudio
import requests
import vosk


model = vosk.Model('vosk-model-small-ru-0.4')
response = requests.get('https://randomuser.me/api/')
data = json.loads(response.content)

record = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=16000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


#Сохранение фото
def save_pic():
    response = requests.get("https://randomuser.me/api/")
    dct = response.text.replace('[', '')
    dct = dct.replace(']', '')
    dct = json.loads(dct)
    pic_URL = requests.get(dct['results']['picture']['large'])
    out = open('img.jpg', 'wb')
    out.write(pic_URL.content)
    out.close()
    print('Фотография пользователя сохранена')

#Сказать имя пользователя
def name():
    response = requests.get("https://randomuser.me/api/")
    dct = response.text.replace('[', '')
    dct = dct.replace(']', '')
    dct = json.loads(dct)
    print(dct)
    print('Имя пользователя: ' + dct['results']['name']['title'] + '. ' + dct['results']['name']['first'] + ' ' + dct['results']['name']['last'])


# Страна пользователя
def country():
    response = requests.get("https://randomuser.me/api/")
    dct = response.text.replace('[', '')
    dct = dct.replace(']', '')
    dct = json.loads(dct)
    print('Страна проживания: ' + dct['results']['location']['country'])

#Часовой пояс пользователя
def timezone():
    response = requests.get("https://randomuser.me/api/")
    dct = response.text.replace('[', '')
    dct = dct.replace(']', '')
    dct = json.loads(dct)
    print('Часовой пояс: ' + dct['results']['location']['timezone']['offset'] + '; Описание пояса: ' + dct['results']['location']['timezone']['description'])




for text in listen():
    if 'часовой пояс' in text:
        timezone()
    elif 'страна' in text:
        country()
    elif 'сохранить' in text:
        save_pic()
    elif 'имя' in text:
        name()
    elif 'выход' in text:
        break
    else:
        print('Не удалось распознать команду')