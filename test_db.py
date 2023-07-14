'''У вас SQL база с таблицами:
1) Users(userId, age)
2) Purchases (purchaseId, userId, itemId, date)
3) Items (itemId, price).


Напишите SQL запросы для расчета следующих метрик:

А) какую сумму в среднем в месяц тратит:
- пользователи в возрастном диапазоне от 18 до 25 лет включительно
- пользователи в возрастном диапазоне от 26 до 35 лет включительно
Б) в каком месяце года выручка от пользователей в возрастном диапазоне 35+ самая большая
В) какой товар обеспечивает дает наибольший вклад в выручку за последний год
Г) топ-3 товаров по выручке и их доля в общей выручке за любой год
'''

import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# проверка связи
cursor.execute('''PRAGMA foreign_keys=on''')  

# создание таблиц
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
    userId INT Primary Key,
    age INT)''' )
cursor.execute('''CREATE TABLE IF NOT EXISTS Purchases (
    purchaseId INT,
    userId INT, 
    itemId INT Primary Key,
    date TEXT,
    FOREIGN KEY (userId) REFERENCES Users (userId))''' )
cursor.execute('''CREATE TABLE IF NOT EXISTS Items (
    itemId INT ,
    price INT,
    FOREIGN KEY (itemId) REFERENCES Purchases (itemId))''' )

# наполняем таблицы 
cursor.execute('''INSERT INTO Users (userId, age) 
    VALUES (1, 23),
    (2, 46),
    (3, 62),
    (4, 21),
    (5, 27),
    (6, 24),
    (7, 34),
    (8, 29),
    (9, 42),
    (10, 56),
    (11, 34),
    (12, 45),
    (13, 27),
    (14, 57);''')
cursor.execute('''INSERT INTO Purchases (purchaseId, userId, itemId, date) 
    VALUES (31, 3, 456, "18.02.23"),
    (32, 7, 184, "21.03.23"),
    (33, 1, 465, "07.05.23"),
    (34, 4, 267, "14.02.23"),
    (35, 2, 123, "05.04.23"),
    (36, 6, 361, "28.01.23"),
    (37, 8, 403, "12.03.23"),
    (38, 5, 075, "10.02.23"),
    (39, 10, 533, "11.02.23"),
    (40, 9, 565, "05.03.23"),
    (41, 13, 68, "22.03.22"),
    (42, 14, 63, "03.02.22"),
    (43, 11, 47, "30.08.21"),
    (44, 12, 52, "05.11.21");''')
cursor.execute('''INSERT INTO Items (itemId, price) 
    VALUES (47, 219),
    (52, 500),
    (63, 299),
    (68, 189),
    (075, 499),
    (123, 249),
    (184, 329),
    (267, 199),
    (361, 449),
    (403, 299),
    (456, 179),
    (465, 229),
    (533, 479),
    (565, 149);''')

# выводим выборку
# А) какую сумму в среднем в месяц тратит:
def average_price_func(min_age, max_age):
    cursor.execute('SELECT userId FROM Users WHERE age>=(?) AND age<=(?)',[min_age, max_age])
    data = cursor.fetchall()
    userId_data = []
    for tuple_data in data:
        for userId in tuple_data:
            userId_data.append(userId)
    or_userId = " OR userId == (?)" * (len(userId_data)-1)

    cursor.execute('SELECT itemId FROM Purchases WHERE userId == (?)'+or_userId, userId_data)
    data = cursor.fetchall()

    itemId_data = []
    for tuple_data in data:
        for userId in tuple_data:
            itemId_data.append(userId)
    or_itemId = " OR itemId == (?)" * (len(itemId_data)-1)
    # print(itemId_data)

    cursor.execute('SELECT AVG(price) FROM Items WHERE itemId == (?)'+or_itemId, itemId_data)
    average_price = cursor.fetchall()
    average_price = round(average_price[0][0], 2)
    print(f'''А) В среднем в месяц тратят пользователи 
    в возрастном диапазоне от {min_age} до {max_age} лет включительно:''',average_price,'\n')

# - пользователи в возрастном диапазоне от 18 до 25 лет включительно
average_price_func(18,25)
# - пользователи в возрастном диапазоне от 26 до 35 лет включительно
average_price_func(26,35)

# Б) в каком месяце года выручка от пользователей в возрастном диапазоне 35+ самая большая?
# Выборка по всем таблицам
cursor.execute('''SELECT Users.userId, Users.age, Purchases.purchaseId, 
Purchases.itemId, Purchases.date, Items.price
FROM Users 
INNER JOIN Purchases 
ON Users.userId = Purchases.userId
INNER JOIN Items 
ON Purchases.itemId = Items.itemId''')

data = cursor.fetchall()
# print(data)

# Создаем общую таблицу
cursor.execute('''CREATE TABLE IF NOT EXISTS All_data 
(userId INT Primary Key,
age INT,
purchaseId INT,
itemId INT,
date TEXT, 
price INT)''' )
cursor.execute('''INSERT INTO All_data 
SELECT Users.userId, Users.age, Purchases.purchaseId, 
Purchases.itemId, Purchases.date, Items.price
FROM Users 
INNER JOIN Purchases 
ON Users.userId = Purchases.userId
INNER JOIN Items 
ON Purchases.itemId = Items.itemId''' )

# Добавление столбца mounth и year в новую таблицу
cursor.execute('ALTER TABLE All_data ADD COLUMN mounth INT')
cursor.execute('ALTER TABLE All_data ADD COLUMN year INT')

cursor.execute('''SELECT date, itemId FROM All_data''')
date_itemId = cursor.fetchall()
itemId_mounth = {}
for tuple_data in date_itemId:
    date = tuple_data[0]
    itemId = tuple_data[1]
    date = date.replace(date[:date.find('.')+1],'')
    mounth = date.replace(date[date.find('.'):],'')
    year = date.replace(date[:date.find('.')+1],'')
    itemId_mounth[itemId] = [int(mounth), int('20'+year)] 
# print('itemId_mounth', itemId_mounth)

for itemId in itemId_mounth:
    cursor.execute('''UPDATE All_data SET mounth = (?) WHERE itemId == (?)''',[itemId_mounth[itemId][0],itemId])
    cursor.execute('''UPDATE All_data SET year = (?) WHERE itemId == (?)''',[itemId_mounth[itemId][1],itemId])

cursor.execute('SELECT mounth FROM All_data WHERE age>=35' )
data = cursor.fetchall()
# print(data)

# Вычисляем самый прибыльный месяц в году
this_year = 2023
monthly_income = {}
for int_mounth in range(1,13):
    cursor.execute('SELECT SUM(price) FROM All_data WHERE age>=35 AND mounth == (?) AND year == (?)', [int_mounth, this_year] )
    data = cursor.fetchall()
    income = data[0][0]
    if income is None:
        income = 0
    monthly_income[int_mounth] = income
# print(monthly_income)

best_mounth = 0
best_income = 0
for mounth in monthly_income:
    if monthly_income[mounth] > best_income:
        best_income = monthly_income[mounth]
        best_mounth = mounth

print(f'''Б) В {best_mounth} месяце {this_year} года выручка, которая составила {best_income} рублей, 
от пользователей в возрастном диапазоне 35+ является наибольшей.\n''')

# В) какой товар обеспечивает дает наибольший вклад в выручку за последний год?
cursor.execute('SELECT MAX(price) FROM All_data WHERE year == (?)', [this_year])
data = cursor.fetchall()
max_price = data[0][0]
# print(max_price)

cursor.execute('SELECT itemId FROM All_data WHERE year == (?) AND price == (?)', [this_year, max_price])
data = cursor.fetchall()
itemId_data = data[0][0]

print(f'В) Товар с номером {itemId_data} обеспечивает наибольший вклад в выручку за {this_year} год\n')

# Г) топ-3 товаров по выручке и их доля в общей выручке за любой год
cursor.execute('SELECT price, itemId, year FROM All_data WHERE year == (?) ORDER BY price', [this_year])
data = cursor.fetchall()
top_list = []
for num in range(1,4):
    top = data[len(data)-num]
    top = list(top)
    top_list.append(top)
# print(top_list)

item_dict = {}

# Доля в общей выручке 1 товара 
item_1 = top_list[0]
cursor.execute('SELECT SUM(price) FROM All_data WHERE year == (?)', [item_1[2]])
all_price = cursor.fetchall()[0][0]
market_share1 = item_1[0] / (all_price / 100) 
market_share1 = round(market_share1, 2)
item_1.append(market_share1)
item_dict[1] = item_1

# Доля в общей выручке 2 товара 
item_2 = top_list[1]
cursor.execute('SELECT SUM(price) FROM All_data WHERE year == (?)', [item_2[2]])
all_price = cursor.fetchall()[0][0]
market_share2 = item_2[0] / (all_price / 100) 
market_share2 = round(market_share2, 2)
item_2.append(market_share2)
item_dict[2] = item_2

# Доля в общей выручке 3 товара 
item_3 = top_list[2]
cursor.execute('SELECT SUM(price) FROM All_data WHERE year == (?)', [item_3[2]])
all_price = cursor.fetchall()[0][0]
market_share3 = item_3[0] / (all_price / 100) 
market_share3 = round(market_share3, 2)
item_3.append(market_share3)
item_dict[3] = item_3

# Общий вывод Топ-3 товаров
print(f'Г) Топ-3 товаров по доходу и их доля в общей выручке за {this_year} год:')
for item in item_dict:
    print(f'''Топ-{item} товар принес компании {item_dict[item][0]} рублей. 
    Доля в общей выручке товара под номером {item_dict[item][1]} составила {item_dict[item][3]}%''')



# Вывод всех данных таблицы
cursor.execute('SELECT * FROM All_data')
data = cursor.fetchall()
# print(data)