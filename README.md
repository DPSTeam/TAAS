# Translate better, together.
# Translation as a service - 翻译即服务
Do you have mass translation tasks to do? TAAS can helps you with asynchronous translation tasks via the HTTP API.

# Usage
1. Make sure you already installed RabbitMQ and MongoDB on your computer.
2. Using pip3 install the following packages:
````sh
sudo pip3 install googletrans flask pika pymongo
````
3. Run TAAS consumer on background.
````sh
(python3 consumer.py > /dev/null) &
disown
````
4. (If you want) Run TAAS server over HTTP API.
````sh
(python3 api.py > /dev/null) &
````
If all these command execute successfully, you will see HTTP API over port 5000.

# Import/Export translation cache
TaaS allow you import and export translation data from database.
## Export translation for backup
* Execute
````sh
python3 exportTranslate.py
````
After that, you can see your translate database dump at ```translate_dump.json```.
## Import translation into database
* Execute
````sh
python3 importTranslate.py <filename>
````

# Dependency
* ```googletrans``` on pypi
* ```flask``` on pypi
* RabbitMQ
* MongoDB

# Author
"王万霖"<dgideas@outlook.com>

# License
See ```License```.
