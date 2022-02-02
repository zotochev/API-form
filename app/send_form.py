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


# @dataclass
# class QuizFields:
#     first: str
#     second: str
#     third: str
#     fourth: str
#     fifth: str
# 
# 
# @dataclass
# class FormFields:
#     name: str
#     gender: str
#     birth_day: str
#     quiz: QuizFields


def main_2():
    quiz = {
                'first': "1Hello",
                'second': "2World",
                'third': "3World",
                'fourth': "4World",
                'fifth': "5World",
            }

    form = {
                "name": "John Doe",
                "gender": True,
                # YYYY-MM-DD
                "birth_day": "1990-04-07",
                "quiz": quiz,
            }

    file_name = "test_pic.jpeg"
    url = 'http://localhost:8000/api/form'

    files = {
                'form': json.dumps(form),
                'file': (file_name, open(file_name, 'rb'), 'image/jpeg'),
            }

    r = requests.post(url, files=files)

    print(r)
    print(r.headers)
    print(r.ok)
    print(f'|{r.text}|')


if __name__ == "__main__":
    main_2()
