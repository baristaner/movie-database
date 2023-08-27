import requests

url = '/adddfilms'
data = {
    'title': 'Example Movie',
    'director': 'John Doe',
    'genre': 'Action',
    'review': 'Great movie!',
    'movie_img': 'example'
}

headers = {'Content-Type': 'application/json'}  
response = requests.post(url, json=data, headers=headers)
print(response.text)
