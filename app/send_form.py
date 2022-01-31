import requests
import json


def main_1():
    file_name = "test_pic.jpeg"
    # files = {'file': (file_name, open(file_name, 'rb'), 'image/jpeg')}

    data = {'first': "Hello", 'second': "World"}

    form = {
                "name": "John Doe",
                "gender": True,
                "birth_day": "07.04.1990",
                "form": data,
            }

    response = requests.post('http://localhost:8000/api/form', data=json.dumps(form))

    print(response.status_code)
    print(response.text)


def main_2():
    quiz = {
                'first': "Hello",
                'second': "World"
            }

    form = {
                "name": "John Doe",
                "gender": True,
                "birth_day": "07.04.1990",
                "quiz": quiz,
            }

    file_name = "test_pic.jpeg"
    url = 'http://localhost:8000/api/form'

    files = {
                'form_my': json.dumps(data),
                'file': (file_name, open(file_name, 'rb'), 'image/jpeg'),
            }

    r = requests.post(url, files=files)
    print(r.text)


if __name__ == "__main__":
    main_2()
