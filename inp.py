#importing libraries
import requests

#Base line with the type of check
BASE = "http://127.0.0.1:5000/personal"

#sending image 
my_img = {'image': open('check.png', 'rb')}

#getting the details and converting into JSON
r = requests.post(BASE, files=my_img)
result = r.json()

#print the details
for key, value in result.items():
    print(key,":", value)