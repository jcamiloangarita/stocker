[![PyPI version](https://badge.fury.io/py/stocker.svg)](https://badge.fury.io/py/stocker)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/jcamiloangarita/stocker/blob/master/LICENSE)
[![tests](https://github.com/jcamiloangarita/stocker/actions/workflows/tests.yml/badge.svg)](https://github.com/jcamiloangarita/stocker/actions/workflows/tests.yml)
[![Downloads](https://pepy.tech/badge/stocker)](https://pepy.tech/project/stocker)


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
