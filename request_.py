import requests

params = requests.post(url="https://ejarima.uz/oz/search-admin/passport",
                       params={
                           "serial": "AB",
                           "number": "6567997"
                       }
                       )
print(params.json())
