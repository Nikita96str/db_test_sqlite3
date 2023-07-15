# db_test_sqlite3
Job done with sqlite3 library

Given a SQL database with tables:
1) Users(userId, age)
2) Purchases (purchaseId, userId, itemId, date)
3) Items (itemId, price).


You need to write SQL queries to calculate the following metrics:

(a) How much does he spend on average per month?
- users in the age range from 18 to 25 years old inclusive
- users in the age range from 26 to 35 years old inclusive
B) in which month of the year the revenue from users in the age range of 35+ is the largest
C) which product provides the largest contribution to revenue over the past year
D) top 3 products by revenue and their share in total revenue for any year
