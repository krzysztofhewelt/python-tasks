# Program pobierający pierwiastki a, b, c od użytkownika i oblicza pierwiastki równania
```python
import math


class FunkcjaKwadratora:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def delta(self):
        return self.b * self.b - 4 * self.a * self.c

    def obliczPierwiastkiRownania(self):
        if self.a == 0 and self.b > 0:
            return {"x0": self.pierwiastekZero()}

        if self.a == 0 and self.b == 0:
            return {"x": self.c}

        if self.delta() > 0:
            return {"x1": self.pierwiastekPierwszy(), "x2": self.pierwiastekDrugi()}
        else:
            return "Delta < 0! Nie można obliczyć pierwiastków równania."

    def pierwiastekZero(self):
        return -self.b / self.c

    def pierwiastekPierwszy(self):
        return (-self.b - math.sqrt(self.delta())) / 2 * self.a

    def pierwiastekDrugi(self):
        return (-self.b + math.sqrt(self.delta())) / 2 * self.a


try:
    a = int(input("Podaj współczynnik a: "))
    b = int(input("Podaj współczynnik b: "))
    c = int(input("Podaj współczynnik c: "))

    rownanie = FunkcjaKwadratora(a, b, c)
    print(rownanie.obliczPierwiastkiRownania())
except ValueError:
    print("Współczynniki muszą być liczbami!")

```

# Poligony, obiektowo
Zadanie domowe: dorobić metody do klasy Points: obliczanie odległości miedzy punktami oraz pola
```python
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, point):
        dx = pow(point.x - self.x, 2)
        dy = pow(point.y - self.y, 2)
        return math.sqrt(dx + dy)

    def __str__(self):
        return f"(x = {self.x}; y = {self.y})"


# tutaj dorobić te metody distance i area
class Points:
    def __init__(self, *points):
        self.points = list(points)[:]

    def append(self, x, y):
        point = Point(x, y)
        self.points.append(point)

    def distance(self):
        suma = 0
        for index, element in enumerate(self.points):
            if index + 1 < len(self.points):
                suma += self.points[index + 1].dist(self.points[index])
        return suma

    def area(self):
        suma = 0
        for index, element in enumerate(self.points):
            if index + 1 < len(self.points):
                suma += self.points[index].x * self.points[index + 1].y - self.points[index + 1].x * self.points[index].y

        return abs(2 * suma)

    def __str__(self):
        text = ""
        for point in self.points:
            text += point.__str__() + "\n"

        return text


poly = Points()
poly.append(5, 5)
poly.append(10, 15)
poly.append(15, 20)
poly.append(25, 30)
print(poly)
print("Odległość między punktami:", poly.distance())
print("Pole polygonu:", poly.area())
```

# Rozszerzenie poniższego programu o obliczanie pola
```python
import math

a = (5, 5)
b = (10, 15)
c = (15, 20)
d = (25, 30)

e = (1, 1)
f = (1, 2)
g = (2, 2)
h = (2, 1)


def oblicz_odleglosc(*args):
    suma = 0
    for index, element in enumerate(args):
        if index + 1 < len(args):
            suma += math.sqrt(pow(args[index + 1][0] - args[index][0], 2) + pow(args[index + 1][1] - args[index][1], 2))

    return suma


def oblicz_pole(*args):
    suma = 0
    for index, element in enumerate(args):
        if index + 1 < len(args):
            suma += args[index][0] * args[index + 1][1] - args[index + 1][0] * args[index][1]

    return abs(2 * suma)

print("odleglosc:", oblicz_odleglosc(a, b, c, d))
print("pole:", oblicz_pole(a, b, c, d))
print("pole drugie:", oblicz_pole(e, f, g, h))
```

# Program obliczający odległość między wieloma punktami
```python
import math

a = (5, 5)
b = (10, 15)
c = (15, 20)
d = (25, 30)


def oblicz_odleglosc(*args):
    suma = 0
    for index, element in enumerate(args):
        if index + 1 < len(args):
            suma += math.sqrt(pow(args[index+1][0] - args[index][0], 2) + pow(args[index+1][1] - args[index][1], 2))

    return suma


print(oblicz_odleglosc(a, b, c, d))
```


# Program obliczający odległość między dwoma punktami
```python
import math

a = (1, 2)
b = (3, 4)

def oblicz_odleglosc(a, b):
    return math.sqrt(pow(b[0] - a[0], 2) + pow(b[1] - a[1], 2))

print(oblicz_odleglosc(a, b))
```


# Program obliczący silnię z liczby n
```python
def silnia(n: int):
    if n <= 1:
        return 1
    else:
        return n * silnia(n - 1)

print(silnia(5))
```

# Program liczący średnią ważoną
```python
def srednia_wazona(oceny, wagi):
    licznik, mianownik = 0, 0
    for o, w in zip(oceny, wagi):
        licznik += o * w
        mianownik += w

    return licznik / mianownik


oceny = [2, 3, 4, 5]
wagi = [2, 5, 3, 4]
srednia = srednia_wazona(oceny, wagi)
print(srednia)
```

# Dowolna liczba argumentów
```python
# Dowolna liczb argumentów, i mieszanie * z **
# ** cpu="Intel, core=4
# * zwykłe argumenty

# mieszanie
def print_keyvalue_args(*args, **kvargs):
    txt = "values: "
    for value in args:
        txt += str(value) + " "

    txt += "\nkv:"

    for key, value in kvargs.items():
        txt += str(key) + " " + str(value) + " | "

    return txt


text = print_keyvalue_args(2, 3, 4, "ddd", cpu="Intel", core=4)
print(text)


# ala wskaźnik, oboetnie ile elementów, w postaci listy to jest
def sum(*args):
    suma = 0
    for x in args:
        suma += x
    return suma


z = sum(8, 5, 4, 1)
print(z)
```

# Funkcje
```python
def sum(x, y):
    return x + y

z = sum(8, 5)
print(z)
```

# Pętle for: string
```python
mystr = "Example text"

for char in mystr:
    print(char)
```

# Pętle for: dict
```python
mydict = {"imie": "Jan", "wiek": 13, "lubi-placki": True}

# dict
print()
for some in mydict:
    print(some)

print()
for key in mydict:
    print(key + ":", mydict[key])

print()
for key, value in mydict.items():
    print(key + ":", mydict[key])

print()
for some in mydict.items():
    print(some)
```


# Pętle for: lista, dict, tuple
```python
mylist = [1, 2, "3332"]
mytup = (3, 4, "5555")
mydict = {"imie": "Jan", "wiek": 13, "lubi-placki": 13}

print("Lista:")
for x in mylist:
    print(x)

print("\nKrotka:")
for x in mytup:
    print(x)

print("\nEnumerate:")
for i, value in enumerate(mytup):
    print(i, value, mytup[i])

print("\nZipowanie:")
myindex = ("a", "b", "c")
for abc, value in zip(myindex, mytup):
    print(abc, value)

myindex2 = ("1", "2", "3")
for abc, i123, value in zip(myindex, myindex2, mytup):
    print(abc, i123, value)
```

# Typy zmiennych i długości
```python
# typy iterowalne i prymitywne (string, int, itd.)
myint = 12
myfloat = 2.34
myfloat2 = 16.
mystring = "test"
mychar = 'g'
mylist = [1, 2, "3332"]
mytup = (3, 4, "5555")
mydict = {"imie": "Jan", "wiek": 13, "lubi-placki": 13}
mybool = True
mynull = None

print(myint, type(myint))
print(myfloat, type(myfloat))
print(mystring, type(mystring))
print(mychar, type(mychar))  # nie ma typu char
print(mylist, type(mylist))
print(mytup, type(mytup))
print(mydict, type(mydict))
print(myfloat2, type(myfloat2))
print(mybool, type(mybool))
print(mynull, type(mynull))

# te nie mają długości
# print(myint, len(myint))
# print(myfloat, len(myfloat))
# print(myfloat2, len(myfloat2))
# print(mybool, len(mybool))
# print(mynull, len(mynull))
print(mystring, len(mystring))
print(mychar, len(mychar))
print(mylist, len(mylist))
print(mytup, len(mytup))
print(mydict, len(mydict))

# silne typowanie Python, słabe typowanie w np. PHP, JS
# print("Hello " + myint)
print("Hello " + str(myint))

# konwersja
print("konwersja float na int", int(myfloat))
```


```python
# rozszerzenie
# funkcja policzy odleglosc miedzy wieloma punktami
import math

a = (5, 5)
b = (10, 15)
c = (15, 20)
d = (25, 30)

e = (1, 1)
f = (1, 2)
g = (2, 2)
h = (2, 1)


def oblicz_odleglosc(*args):
    suma = 0
    for index, element in enumerate(args):
        if index + 1 < len(args):
            suma += math.sqrt(pow(args[index+1][0] - args[index][0], 2) + pow(args[index+1][1] - args[index][1], 2))

    return suma


def oblicz_pole(*args):
    suma = 0
    for index, element in enumerate(args):
        if index + 1 < len(args):
            suma += args[index][0] * args[index+1][1] - args[index+1][0] * args[index][1]

    return abs(2 * suma)

print("odleglosc:", oblicz_odleglosc(a, b, c, d))
print("pole:", oblicz_pole(a, b, c, d))
print("pole drugie:", oblicz_pole(e, f, g, h))
#########################################

```