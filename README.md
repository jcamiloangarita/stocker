# STOCKER
Stocker is a python tool that uses ANN to predict the stock's close price for the next business day. Suggestions and contributions of all kinds are very welcome.

## Authors

* **Juan Camilo Gonzalez Angarita** - [jcamiloangarita](https://github.com/jcamiloangarita)
* **Moses Maalidefaa Tantuoyir**
* **Anthony Ibeme** 

See the full list of [contributors](https://github.com/jcamiloangarita/stocker/graphs/contributors) involved in this project.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Get pwptemp

* Users: Wheels for Python from [PyPI](https://pypi.python.org/pypi/stocker/) 
    * `pip install stocker`
* Developers: Source code from [github](https://github.com/jcamiloangarita/stocker)
    * `git clone https://github.com/jcamiloangarita/stocker`
    
## Quick use
```
>>> import stocker
>>> stocker.predict.tomorrow('AAPL')
[266.07, 1.276, '2019-11-11']
```
Notice that output = [predicted price, error(%), date of the next business day]
