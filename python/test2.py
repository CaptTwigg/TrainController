# import requests
#
# response = requests.get("http://orteil.dashnet.org/cookieclicker/img/")
#
# list = response.text.split("<a href=\"")
#
# for i in range(6, len(list), 1):
#     name = list[i].split("\">")[0]
#     img = requests.get("http://orteil.dashnet.org/cookieclicker/img/" + name)
#     with open('/Users/mackerbook/Dropbox/Arduino/train/firstTrain/python/CCImg/' + name, 'wb') as f:
#         f.write(img.content)


print(bin(0b111 >> 6 ^ 0b111))
