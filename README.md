A Python parser for the CC-CEDICT Chinese-English dictionary
============================================================

[![Travis](https://img.shields.io/travis/rust-lang/rust.svg)](https://travis-ci.org/marcanuy/cedict_utils)
[![PyPI version](https://badge.fury.io/py/cedict-utils.svg)](https://badge.fury.io/py/cedict-utils)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Downloads](https://pepy.tech/badge/cedict-utils)](https://pepy.tech/project/cedict-utils)
[![Pypi](https://img.shields.io/pypi/v/nine.svg)](https://pypi.python.org/pypi/cedict-utils/)

----

A parser for the CC-CEDICT Chinese-English dictionary.

# Install

## PIP

https://pypi.org/project/cedict-utils/

~~~
pip install cedict-utils
~~~

# Usage

~~~ python
$ python
>>> from cedict_utils.cedict import CedictParser
>>> parser = CedictParser()
>>> entries = parser.parse()
>>> for e in entries:
...     print(e)
... 
..
龟缩 (龜縮) - gui1 suo1
龟背竹 (龜背竹) - gui1 bei4 zhu2
龟船 (龜船) - gui1 chuan2
..
>>> entries[200].simplified
'敦'
>>> entries[200].traditional
'㪟'
>>> entries[200].pinyin
'dun1'
>>> entries[200].raw_line
'㪟 敦 [dun1] /variant of 敦[dun1]/'
>>> entries[200].meanings
['variant of 敦[dun1]']
>>> 
~~~


## REPO

1. Create virtualenv.

~~~
python3 -m venv ~/.virtualenvs/cedict-utils
~~~

2. Activate venv.

~~~
source ~/.virtualenvs/cedict-utils/bin/activate
~~~

3. Install requirements.
   
~~~
pip install -r requirements.txt
~~~

## Dictionary

If you want to download a specific dictionary:

~~~
wget -O - https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.txt.gz | gunzip > data/cedict_ts.u8
~~~

Then 

~~~
>>> parser.read_file()
~~~


# Tests

Running tests

~~~
$ make test
pytest
================================================================ test session starts ================================================================
platform linux -- Python 3.6.8, pytest-3.2.3, py-1.4.34, pluggy-0.4.0
rootdir: /Development/cedict-utils, inifile:
collected 8 items                                                                                                                                    

tests/test_cedict.py ........

============================================================= 8 passed in 0.09 seconds ==============================================================
~~~

# Resources

- Cedict project https://www.mdbg.net/chinese/dictionary?page=cc-cedict
