# Writes the inputs under data/.
import os
os.makedirs("data", exist_ok=True)

headers = r'''sid=abc123; theme=dark
 a=1 ;b=2;   c=3 
quoted="hello world"; esc="a\"b\\c\012d"
chips="\303\251t\303\251"
k=v; Path=/; Domain=example.com; Max-Age=3600; Secure; HttpOnly; SameSite=Lax
k=v; expires=Wed, 21 Oct 2026 07:28:00 GMT; path=/docs
k=v; expires=Thursday, 22-Oct-2026 07:28:00 GMT
k=v; expires=Wed, 21 Oct 2026 07:28 GMT
Path=/; k=v
k=v; Domain
k=v; $Path=/x; $Version=1
k=v; $Foo=1
$Version=1; k=v
a<b=1; c=2
a=1; c d=2
a=1 b=2
k=v; comment=hello there
k=[1,2]; m={x:1}
k=a=b=c
k
;;a=1
k=v; secure=1; httponly
=v
a=1; a=2; A=3
x="unterminated; y=2
w=1;	tab=2
'''
open("data/headers.txt", "w").write(headers)

jar = '''at 1760000000
resp https://shop.example.com/catalog/shoes/index.html
Set-Cookie: sid=s1; Path=/; Secure; HttpOnly; SameSite=Lax
Set-Cookie: cart=3 items; Max-Age=600
Set-Cookie: lang=de; Domain=.example.com; Path=/
Set-Cookie: trk=1; Domain=tracker.net
Set-Cookie: wide=1; Domain=com
Set-Cookie: promo="10% off"; Expires=Fri, 10 Oct 2025 08:00:00 GMT
Set-Cookie: banner=summer; Expires=Wed, 21 Oct 2026 07:28:00 GMT; Path=/catalog
Set-Cookie: views=7; Path=/catalog/shoes/; Priority=High
req https://shop.example.com/catalog/shoes/item.html
req https://shop.example.com/catalog/
req https://shop.example.com/catalogue
req http://shop.example.com/catalog/shoes/x
req https://blog.example.com/
req https://example.com/
req https://evil-example.com/
resp http://shop.example.com/login
Set-Cookie: sid=hijack; Path=/; Secure
Set-Cookie: csrf=t0k; Path=/login
Set-Cookie: lang=fr; Domain=example.com; Path=/
dump
at 1760000500
req https://shop.example.com/catalog/shoes/item.html
at 1760000700
req https://shop.example.com/catalog/shoes/item.html
resp https://shop.example.com/logout
Set-Cookie: sid=; Path=/; Max-Age=0
Set-Cookie: lang=x; Domain=example.com; Path=/; Max-Age=-1
Set-Cookie: banner=autumn; Path=/catalog; Max-Age=abc
Set-Cookie: views; Path=/catalog/shoes/
Set-Cookie: <bad>=1
dump
at 1792531681
req https://shop.example.com/catalog/shoes/item.html
dump
'''
open("data/jar.txt", "w").write(jar)
