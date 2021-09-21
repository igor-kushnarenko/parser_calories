Parser of data on the calorie content in products
====
* Parser of data on the calorie content in products, from the site http://health-diet.ru/


Requirements
=====
* Python 3.x
* beautifulsoup4==4.10.0
* lxml==4.6.3
* requests==2.26.0


Download/Installation
====
* git clone https://github.com/igor-kushnarenko/parser_calories
* pip3 install -r requirements.txt --user

if pip3 is missing:
* apt-get install python3-setuptools
* easy_install3 pip
* pip3 install -r requirements.txt


Features
====
* Collects data from the site into documents separated by product type and saves it in json and csv formats

