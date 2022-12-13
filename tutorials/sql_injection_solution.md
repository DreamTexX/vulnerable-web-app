# SQL Injection

### 1. Use SQL injection to login as "user1" without knowing the password.

- Write `user1@email.com' #` into the email text field
- Leave the password field empty
- You are now able to login without the password
- The query is the following:
```sql
SELECT id FROM accounts WHERE email LIKE 'user1@email.com' #' OR TRUE AND password LIKE '';
```
- This leads to this query:
```sql
SELECT id FROM accounts WHERE email LIKE 'user1@email.com'
```

<br/>

### 2. Repair the application, so that is not possible anymore to login without the password.
> Solutions branch: fix-sql-injections <br/>
> All corresponding files with SQL statements should use prepared statements to escape the input
-----

- file: [backend/src/accounts_me.py](../backend/src/accounts_me.py)
- the code needs to be changed at line 15 and 16

current code:
```python 
cur.execute(f"""SELECT `id`, `email`, `username` FROM `accounts` WHERE `id` = {session["id"]}""")
```

replace with the following code:
```python 
cur.execute(f"""SELECT `id`, `email`, `username` FROM `accounts` WHERE `id` = %s""", (session["id"],))
```

-----

- file: [backend/src/auth_login.py](../backend/src/auth_login.py)
- the code needs to be changed at line 17 and 18

current code:
```python 
cur.execute(f"""SELECT `id` FROM `accounts` WHERE `email` LIKE '{email}' AND `password` LIKE '{password}';""")
```

replace with the following code:
```python 
cur.execute(f"""SELECT `id` FROM `accounts` WHERE `email` LIKE %s AND `password` LIKE %s;""", (email, password))
```

-----

- file: [backend/src/auth_register.py](../backend/src/auth_register.py)
- the code needs to be changed at line 26, 27 and 33, 34

current code:
```python 
cur.execute(f"""SELECT `email`, `username` FROM `accounts` WHERE `email` LIKE '{email}' OR `username` LIKE '{username}';""")

// ...

cur.execute(f"""INSERT INTO `accounts` (`email`, `username`, `password`) VALUES ('{email}', '{username}', '{password}');""")
```

replace with the following code:
```python 
cur.execute(f"""SELECT `email`, `username` FROM `accounts` WHERE `email` LIKE %s OR `username` LIKE %s;""", (email, username))

// ...

cur.execute(f"""INSERT INTO `accounts` (`email`, `username`, `password`) VALUES (%s, %s, %s);""", (email, username, password))
```

-----

- file: [backend/src/posts_create.py](../backend/src/posts_create.py)
- the code needs to be changed at line 19, 20 and 22, 23

current code:
```python 
cur.execute(f"""INSERT INTO `posts` (`content`, `author_id`) VALUES ('{content}', '{author_id}');""")

// ...

cur.execute(f"""SELECT `posts`.`id`, `posts`.`content`, `accounts`.`username`, `posts`.`created_at` FROM `posts` INNER JOIN `accounts` ON `accounts`.`id` = `posts`.`author_id` WHERE `posts`.`id` = {cur.lastrowid}""")
```

replace with the following code:
```python 
cur.execute(f"""INSERT INTO `posts` (`content`, `author_id`) VALUES (%s, %s);""", (content, author_id))

// ...

cur.execute(f"""SELECT `posts`.`id`, `posts`.`content`, `accounts`.`username`, `posts`.`created_at` FROM `posts` INNER JOIN `accounts` ON `accounts`.`id` = `posts`.`author_id` WHERE `posts`.`id` = %s""", (cur.lastrowid,))
```

-----
