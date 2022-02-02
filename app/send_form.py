import requests
import json


def main():
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

    file_name = "temp/test_pic.gif"
    url = 'http://localhost:8000/api/form'

    files = {
                'form': json.dumps(form),
                # 'file': (file_name, open(file_name, 'rb').read(), 'image/jpeg'),
                'file': open(file_name, 'rb').read(),
             }

    r = requests.post(url, files=files)

    print(r)
    print(r.headers)
    print(r.ok)
    print(f'|{r.text}|')


if __name__ == "__main__":
    main()
