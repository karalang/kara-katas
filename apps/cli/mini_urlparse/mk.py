# Writes the inputs under data/.
import os
os.makedirs("data", exist_ok=True)

urls = [
    "http://www.python.org/doc/#frag",
    "HTTPS://User:Pa%20ss@WWW.Example.COM:8443/a/b;p=1/c;q=2?x=1&y=2#top",
    "https://example.com:443",
    "http://[::1]:8080/path",
    "http://[FE80::822A:A8FF:FE49:470C%tESt]:1234/keys",
    "http://[2001:db8::7]/c=GB?objectClass?one",
    "http://[::ffff:192.0.2.1]/",
    "http://[v1.fe80::a+en1]/",
    "http://[192.0.2.1]/",
    "http://[::1/",
    "http://::1]/",
    "http://x[::1]/",
    "http://[::1]x/",
    "http://[1:2:3:4:5:6:7:8:9]/",
    "http://[vz.x]/",
    "http://host:port/",
    "http://host:99999/",
    "http://host:/",
    "http://host:0080/",
    "http://user@host",
    "http://user:@host",
    "http://:pw@host",
    "http://a@b@c/d",
    "ftp://ftp.is.co.za/rfc/rfc1808.txt",
    "mailto:John.Doe@example.com",
    "news:comp.infosystems.www.servers.unix",
    "tel:+1-816-555-1212",
    "telnet://192.0.2.16:80/",
    "urn:oasis:names:specification:docbook:dtd:xml:4.1.2",
    "file:///etc/hosts",
    "file:/etc/hosts",
    "file://localhost/c:/WINDOWS/clock.avi",
    "//www.example.com/path?q",
    "/just/a/path;params?query#frag",
    "relative/path",
    "path:with:colons",
    "1http://not-a-scheme/",
    "git+ssh://git@github.com/user/repo.git",
    "svn+ssh://svn.example.org/trunk",
    "sip:alice@atlanta.com;transport=tcp",
    "http://example.com/a;b;c/d;e?f#g#h",
    "http://example.com/?",
    "http://example.com/#",
    "http://example.com?#",
    "  \x01http://leading.example/  ",
    "ht\ttp://tab\n.exam\rple/",
    "HTTP://EXAMPLE.COM/%7Euser",
    "javascript:alert(1)",
    "data:text/plain;base64,SGVsbG8=",
    "http://example.com:8080:9090/",
    "http:///triple/slash",
    "http:",
    "",
]
with open("data/urls.txt", "w", newline="") as f:
    for u in urls:
        f.write(u.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r").replace("\x01", "\\x01") + "\n")

joins = """\
base http://a/b/c/d;p?q
g:h
g
./g
g/
/g
//g
?y
g?y
#s
g#s
g?y#s
;x
g;x
g;x?y#s
<empty>
.
./
..
../
../g
../..
../../
../../g
../../../g
../../../../g
/./g
/../g
g.
.g
g..
..g
./../g
./g/.
g/./h
g/../h
g;x=1/./y
g;x=1/../y
g?y/./x
g?y/../x
g#s/./x
g#s/../x
http:g
http://other/x/../y
https://a/b
base http://a/b/c/
d
../../../..
//
base https://shop.example.com/catalog/shoes/index.html?page=2
../bags/
item.html?id=7#reviews
/
mailto:x@y
#top
base mailto:a@b
c@d
base
anything
base file:///home/user/docs/
../music/song.mp3
base svn+ssh://svn.example.org/repo/trunk/src/
../../branches/x
base tel:+1
2
"""
open("data/joins.txt", "w").write(joins)

quotes = """\
abc def
/path/to/file name.txt
a+b=c&d
~user/_.-
100% sure?
caf\u00e9 cr\u00e8me
\u65e5\u672c\u8a9e/\u30c6\u30b9\u30c8
emoji \U0001F600!
%41%42%43
%7e%7E%zz%4
%C3%A9t%C3%A9
%E6%97%A5%E6%9C
%FF%C3(%80
%C3\u00e9%A9
%E0%80%AF
%ED%A0%80x
%F4%90%80%80
%C2%A0nbsp
a%2Bb+c
[]{}|\\^`"'<>
"""
open("data/quotes.txt", "w").write(quotes)

queries = """\
a=1&b=2&a=3
name=John+Doe&city=New%20York
empty=&flag&x=1
=nokey&k=
&&a=1&&
q=%E2%9C%93&lang=de-DE
x=1;y=2
plus=a%2Bb+c&eq=a=b=c
k=caf%C3%A9&bad=%FF
<empty>
"""
open("data/queries.txt", "w").write(queries)

log = """\
203.0.113.5 - - [15/Oct/2026:10:00:01 +0000] "GET /catalog/./shoes/../shoes/index.html?page=2&sort=price HTTP/1.1" 200 5120 "https://www.Google.com/search?q=running+shoes&hl=en" "Mozilla/5.0"
203.0.113.5 - - [15/Oct/2026:10:00:03 +0000] "GET /catalog/shoes/item.html?id=7&ref=list HTTP/1.1" 200 2048 "https://shop.example.com/catalog/shoes/index.html?page=2" "Mozilla/5.0"
198.51.100.23 - alice [15/Oct/2026:10:01:10 +0000] "POST /cart/add?id=7&qty=2 HTTP/1.1" 302 0 "https://shop.example.com:443/catalog/shoes/item.html?id=7" "curl/8.0"
198.51.100.23 - alice [15/Oct/2026:10:01:11 +0000] "GET /cart/ HTTP/1.1" 200 900 "-" "curl/8.0"
192.0.2.44 - - [15/Oct/2026:10:02:00 +0000] "GET /search?q=caf%C3%A9+cr%C3%A8me&q=t%C3%A9&page= HTTP/1.1" 200 3000 "http://bing.com/search?q=cafe" "Mozilla/5.0"
192.0.2.44 - - [15/Oct/2026:10:02:05 +0000] "GET /catalog/bags/../../catalog/bags/ HTTP/1.1" 200 4000 "https://SHOP.example.com/search?q=caf%C3%A9" "Mozilla/5.0"
192.0.2.99 - - [15/Oct/2026:10:03:00 +0000] "GET /static/%7Elogo.png HTTP/1.1" 304 0 "https://shop.example.com/" "Mozilla/5.0"
192.0.2.99 - - [15/Oct/2026:10:03:01 +0000] "GET //evil.example/phish HTTP/1.1" 404 0 "-" "Mozilla/5.0"
192.0.2.99 - - [15/Oct/2026:10:03:02 +0000] "GET /search?q=a%26b%3Dc&debug HTTP/1.1" 200 100 "https://news.ycombinator.com/item?id=1" "Mozilla/5.0"
203.0.113.5 - - [15/Oct/2026:10:04:00 +0000] "GET /catalog/shoes/index.html?sort=price&page=2 HTTP/1.1" 200 5120 "https://www.google.com/search?hl=en&q=running%20shoes" "Mozilla/5.0"
203.0.113.7 - - [15/Oct/2026:10:05:00 +0000] "GET /a/b/../../../../etc/passwd HTTP/1.1" 400 0 "http://[2001:db8::1]:8080/x" "scanner"
203.0.113.7 - - [15/Oct/2026:10:05:01 +0000] "GET /x HTTP/1.1" 400 0 "http://[::1/x" "scanner"
"""
open("data/access.log", "w").write(log)
