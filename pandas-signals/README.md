# Pandas, Signals

Solved task from: https://github.com/Xaeian/LabPython/blob/main/pd.md.

Used modules:
* numpy
* pandas
* matplotlib

## .ini parser features
* supports sections, arrays and comments (``# comment`` and ``; another comment``)
* guesses the types of variables
* get value of the given element

Example .ini files included.

## How to use .ini parser
1. Create an IniReader object and give path to the .ini file 
```python
configFileReader = IniReader('config.ini')
```

2. Display parsed file...
```python
configFileReader.display_file()
```

3. ... or get value by key element:
```python
configFileReader.get('ip')
```

4. You can get parsed data in dictionary and modify it:
```python
data = configFileReader.get_parsed_data()
data['test'] = 'example string'
```

## Example IniReader output
```commandline
Get few elements:
192.168.0.1
3306

Print parsed .ini file and dictionary:
{'test': 'a', 'valid_also': 'test', 'first_section': {'ip': '192.168.0.1', 'port': 3306, 'one': 1, 'five': 5, 'seven': 5.5, 'animal': 'BIRD'}, 'second_section': {'path': '/usr/local/bin', 'URL': 'http://www.example.com/~username'}, 'third_section': {'phpversion': [5.0, 5.1, 5.2, 5.3], 'urls': 'http://svn.php.net'}}
test = a
valid_also = test
[first_section]
ip = 192.168.0.1
port = 3306
one = 1
five = 5
seven = 5.5
animal = BIRD

[second_section]
path = /usr/local/bin
URL = http://www.example.com/~username

[third_section]
phpversion = [5.0, 5.1, 5.2, 5.3]
urls = http://svn.php.net
```