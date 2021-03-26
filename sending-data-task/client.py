"""The task is to send a POST-request containing an Authorization header
with Basic auth method and base64-encoded login and password strings
to the specified endpoint.

Endpoint URL is https://datasend.webpython.graders.eldf.ru/submissions/1/
"""

import requests

LOGIN = 'alladin'
PASSWORD = 'opensesame'
URL = 'https://datasend.webpython.graders.eldf.ru/submissions/1/'


def auth():
    credentials = (LOGIN, PASSWORD)
    return requests.post(url=URL, auth=credentials)


if __name__ == '__main__':
    response = auth()
    print(response.status_code, response.json())
