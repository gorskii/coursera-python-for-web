"""The task is to send a POST-request containing an Authorization header
with Basic auth method and base64-encoded login and password strings
to the specified endpoint.

Endpoint URL is https://datasend.webpython.graders.eldf.ru/submissions/1/

Then get new credentials and instructions from the response and follow
the instructions: make a PUT request to the same host, but the endpoint
is specified in 'path' attribute of the response.

The solution to the task is stored in the 'answer' attribute of the
final response. It should be written to a plain-text file named answer.txt.
"""

import requests

LOGIN = 'alladin'
PASSWORD = 'opensesame'
HOST = 'https://datasend.webpython.graders.eldf.ru/'
AUTH_ENDPOINT = 'submissions/1/'


if __name__ == '__main__':
    with requests.Session() as s:
        s.auth = (LOGIN, PASSWORD)
        res = s.post(HOST+AUTH_ENDPOINT)
        res.raise_for_status()
        data = res.json()
        path, login, password = data['path'], data['login'], data['password']

        s.auth = (login, password)
        res = s.put(HOST+path)
        res.raise_for_status()
        data = res.json()
        answer = data['answer']

    with open('answer.txt', 'w') as file:
        file.write(answer)
