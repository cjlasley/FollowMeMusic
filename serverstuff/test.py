import requests

body = {
"image" : "test"
}
response = requests.post("http://localhost:5000/upload", json = body )

print (response.text)
