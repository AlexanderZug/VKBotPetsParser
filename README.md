# VKBotPetsParser
The Bot for VK, that helps to find pets in one of Moscow shelters.

![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/вконтакте-%232E87FB.svg?&style=for-the-badge&logo=vk&logoColor=white)
![](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)

## Deploy locally:

> Install Python(If it's not installed)<br>
> [Download Python3](https://www.python.org/downloads/)

Clone the repository:
```
git clone https://github.com/AlexanderZug/VKBotPetsParser.git
```

Install requirements:
```
pip3 install -r requirements.txt
```

Add your bot token and group id here in token_group_num.py:
```
TOKEN = ''
VK_GROUP_NUM = ''
```


Start programm:
```
cd bot
python3 main.py
```

> Technologies used in the project: Python3, beautifulsoup4, vk-api, requests.
