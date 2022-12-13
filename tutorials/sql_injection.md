# SQL Injection

### 1. Use SQL injection to login as "user1" without knowing the password.
> Through social engineering you found out that the email of user1 is user1@email.com
- Open the application (http://localhost:8080) in a browser
- Click on "Sign In" to get to the login form
- But you are not able to login because the password is missing
- Try to insert SQL syntax like `'` into the email field
- See how the application behaves
- The application returns an error with useful information
- Use these information to do an SQL injection attack
> A default query usually looks like the following:
```sql
SELECT * FROM accounts WHERE email = '[email]' AND password = '[password]';
```
> Words in brackets [word] are replaced by input parameters
> Putting `'` into the email field and nothing into the password field would lead to the following query :
```sql
 SELECT * FROM accounts WHERE email = ''' AND password = '[password]';
```
> `'''` is an incorrect SQL syntax and the application returns an error
- Find a way to manipulate the query, so that the statement is always true despite the given password
> You can use `#` to comment a line of an SQL statement <br/>
> Putting `' #` into the email field and nothing into the password field would lead to the following query :
```sql
 SELECT * FROM accounts WHERE email = '' #' AND password = '[password]';
```
> Everything after `#` is now a comment and the executed query would look like this:
```sql
 SELECT * FROM accounts WHERE email = ''
```

- Now try to login as "user1" without the password

<br/>

### 2. Repair the application, so that it is not possible to login without the password anymore.

- Take a look at 
    - [backend/src/accounts_me.py](../backend/src/accounts_me.py)
    - [backend/src/auth_login.py](../backend/src/auth_login.py)
    - [backend/src/auth_register.py](../backend/src/auth_register.py)
    - [backend/src/posts_create.py](../backend/src/posts_create.py)
- There are SQL statements which use the given input to store or load data
- The user input is neither escaped nor validated which means that you can manipulate the query
- One way of preventing SQL injection is using prepared statements
> In the given application prepared statements can look like this:
```python
cur.execute("""SELECT * FROM `table` WHERE `column` LIKE %s;""", (value))
```

- Replace all queries with a prepared statement 
- Now try to login as "user1" without the password like before