import requests
import json

BASE_URL = 'https://api.hh.ru'


def get_countries(url):
    j = requests.get(f"{BASE_URL}{url}").json()
    # Загрузка JSON-строки в объект Python
    data = json.loads(json.dumps(j))
    # Получение списка имен объектов
    names_list = []
    for d in data:
        names_list.append((d['id'], d['name']))
    return names_list

def get_info(entity):
    j = requests.get(f"{BASE_URL}/dictionaries").json()
    # Загрузка JSON-строки в объект Python
    data = json.loads(json.dumps(j))
    # Получение списка имен объектов
    names_list = [(d['id'], d['name']) for d in data[entity]]
    return names_list

def get_currency():
    j = requests.get(f"{BASE_URL}/dictionaries").json()
    # Загрузка JSON-строки в объект Python
    data = json.loads(json.dumps(j))
    # Получение списка имен объектов
    names_list = [(d['code'], d['abbr']) for d in data["currency"]]
    return names_list
def auth():
    # client_id = "VQVJ5QBD7OJ2L58U2ET8M7O8CNNEQSUM3F6T2D7RM449KETARC92PRRODBDN28S0"
    # client_secret = "JDUG1I830GU1JHKGSOFBVQGH03TG51IS284HP4RC536RJ99BJ2LMVAEHDS0SMLRT"
    # # NO339LH7AML4HME1A7EPBD25P432HM64CT9ER92LBRRO9UNJO7F0DF4P7RNPM0FP
    # access_token = requests.post('https://hh.ru/oauth/token',
    #                              {'grant_type': 'authorization_code', 'client_id': client_id,
    #                               'client_secret': client_secret, 'code': '<CODE>'}).json()
    #
    # print(access_token)
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    # }
    # r = requests.get("https://hh.ru", headers=headers)
    # print(r)
    url = 'https://moscow.hh.ru/account/login'

    # Важно. По умолчанию requests отправляет вот такой
    # заголовок 'User-Agent': 'python-requests/2.22.0 ,  а это приводит к тому , что Nginx
    # отправляет 404 ответ. Поэтому нам нужно сообщить серверу, что запрос идет от браузера

    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

    # Создаем сессию и указываем ему наш user-agent
    session = requests.Session()
    r = session.get(url, headers={
        'User-Agent': user_agent_val
    })

    # Указываем referer. Иногда , если не указать , то приводит к ошибкам.
    session.headers.update({'Referer': url})

    # Хотя , мы ранее указывали наш user-agent и запрос удачно прошел и вернул
    # нам нужный ответ, но user-agent изменился на тот , который был
    # по умолчанию. И поэтому мы обновляем его.
    session.headers.update({'User-Agent': user_agent_val})

    # Получаем значение _xsrf из cookies
    _xsrf = session.cookies.get('_xsrf', domain=".hh.ru")

    # Осуществляем вход с помощью метода POST с указанием необходимых данных
    post_request = session.post(url, {
        'backUrl': 'https://spb.hh.ru/',
        'username': '515nonia515@gmail.com',
        'password': '228338118',
        '_xsrf': _xsrf,
        'remember': 'yes',
    })
    url = post_request.json()['redirectUrl']

    # Вход успешно воспроизведен и мы сохраняем страницу в html файл
    with open("hh_success.html", "w", encoding="utf-8") as f:
        f.write(post_request.text)

    return post_request.json()['redirectUrl']


def get_access_token(url, client_id, client_secret):
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    return response.json()["access_token"]
