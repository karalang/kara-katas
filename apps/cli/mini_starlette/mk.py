# Writes data/: route templates for compile_path, url_path_for calls, and
# the HTTP requests a bookshop service built on Starlette receives, one per
# file, read in name order. Run it from the app directory.
import os
import shutil

if os.path.isdir("data"):
    shutil.rmtree("data")
os.makedirs("data/requests")

paths = [
    "/",
    "/books",
    "/books/{book_id:int}",
    "/books/{book_id:int}/price/{currency}",
    "/users/{username}",
    "/users/{username:str}/repos/{repo}",
    "/files/{path:path}",
    "/rates/{rate:float}",
    "/orders/{order_id:uuid}",
    "/static/{path:path}",
    "/a.b/c+d/{x}",
    "/v1.0/(legacy)/{item}",
    "/price/$/{amount:float}",
    "/tilde~/{x}#frag",
    "/{a}{b}",
    "/{a}-{b:int}-{c}",
    "/{x}/{x}",
    "/{x}/{y}/{x}/{y}",
    "/{x:int}/{x:float}",
    "/{name:slug}",
    "/{name:Int}",
    "/{1bad}/{good}",
    "/{bad-name}",
    "/{:int}",
    "/{_private}/{CamelCase9}",
    "/{a:path}/{b:path}",
    "/space here/{x}",
    "/café/{x}",
    "/brace{/{x}",
    "/brace}/{x}",
    "{subdomain}.shop.example",
    "{subdomain}.shop.example:8080",
    "api.shop.example",
    "{a}.{b}.example",
    "{tenant:int}.example",
    "localhost:{port}",
    "",
    "/{x:str}",
    "/q?{x}",
    "/*.{ext}",
]
with open("data/paths.txt", "w") as f:
    for p in paths:
        f.write(p + "\n")

# name|key=type:value|...
urlfor = [
    "homepage",
    "books",
    "book|book_id=int:3",
    "book|book_id=str:12",
    "book|book_id=int:0",
    "book|book_id=int:-1",
    "book|book_id=str:x",
    "book|book_id=str:007",
    "book",
    "book|book_id=int:3|extra=str:y",
    "book|id=int:3",
    "update_book|book_id=int:9",
    "delete_book|book_id=int:9",
    "create_book",
    "price|book_id=int:2|currency=str:EUR",
    "price|currency=str:EUR|book_id=int:2",
    "price|book_id=int:2|currency=str:a/b",
    "price|book_id=int:2|currency=str:",
    "price|book_id=int:2|currency=int:5",
    "price|book_id=int:2|currency=str:café au lait",
    "rate|rate=float:1.5",
    "rate|rate=float:0.1",
    "rate|rate=float:0.2",
    "rate|rate=float:3",
    "rate|rate=int:3",
    "rate|rate=float:0",
    "rate|rate=float:1e-7",
    "rate|rate=float:123456789.125",
    "rate|rate=float:1e22",
    "rate|rate=float:-1.0",
    "rate|rate=float:-0.0",
    "rate|rate=float:nan",
    "rate|rate=float:inf",
    "rate|rate=str:2.50",
    "rate|rate=str:abc",
    "order|order_id=str:12345678-1234-5678-1234-567812345678",
    "files|path=str:docs/guide/intro.md",
    "files|path=str:",
    "files|path=str:/etc/passwd",
    "files|path=str:a b/c?d#e",
    "echo",
    "teapot",
    "admin",
    "admin|path=str:/users/7",
    "admin|path=str:users/7",
    "admin|path=str:",
    "admin|path=str:x|extra=int:1",
    "admin:home",
    "admin:user|uid=int:7",
    "admin:user|uid=int:-7",
    "admin:user",
    "admin:reports",
    "admin:tools:tool|tool=str:hammer",
    "admin:tools|path=str:saw",
    "admin:tools:tool",
    "admin:nothing",
    "admin:",
    "home",
    "user|uid=int:7",
    "static|path=str:css/site.css",
    "static|path=str:/css/site.css",
    "static:anything|path=str:x",
    "tenant|path=str:/stats|tenant=str:acme",
    "tenant|tenant=str:acme|path=str:/",
    "tenant|path=str:/",
    "tenant:home|tenant=str:acme",
    "tenant:stats|tenant=str:globex",
    "tenant:stats",
    "tenant:home|tenant=str:a/b",
    "tenant:missing|tenant=str:acme",
    "stock|sku=str:DUNE-HB",
    "cache|key=str:greeting",
    "search",
    "missing",
    "missing|a=int:1|b=str:2",
]
with open("data/urlfor.txt", "w") as f:
    for u in urlfor:
        f.write(u + "\n")

reqs = []


def req(name, method, target, headers=(), body="", host="bookshop.test"):
    lines = [f"{method} {target} HTTP/1.1"]
    if host is not None:
        lines.append(f"Host: {host}")
    for h in headers:
        lines.append(h)
    reqs.append((name, "\r\n".join(lines) + "\r\n\r\n" + body))


def js(name, method, target, body, headers=(), **kw):
    req(name, method, target, ["Content-Type: application/json", f"Content-Length: {len(body.encode())}"] + list(headers), body, **kw)


APP = "Origin: https://app.example.com"

# the basics
req("home", "GET", "/")
req("home-head", "HEAD", "/")
req("home-post", "POST", "/")
req("home-query", "GET", "/?utm_source=mail&utm_campaign=fall")
req("books", "GET", "/books")
req("books-slash", "GET", "/books/")
req("books-slash-query", "GET", "/books/?author=frank%20herbert")
req("books-author", "GET", "/books?author=Frank+Herbert")
req("books-author-case", "GET", "/books?author=URSULA%20K.%20LE%20GUIN")
req("books-tag", "GET", "/books?tag=classic")
req("books-two-tags", "GET", "/books?tag=classic&tag=sci-fi")
req("books-no-match", "GET", "/books?tag=poetry")
req("books-limit", "GET", "/books?limit=1&offset=1")
req("books-limit-spaces", "GET", "/books?limit=%202%20")
req("books-limit-plus", "GET", "/books?limit=+2")
req("books-limit-underscore", "GET", "/books?limit=1_0")
req("books-limit-bad", "GET", "/books?limit=ten")
req("books-limit-double-underscore", "GET", "/books?limit=1__0")
req("books-limit-negative", "GET", "/books?limit=-1")
req("books-offset-past", "GET", "/books?offset=10")
req("books-blank-param", "GET", "/books?author=&tag")
req("books-last-wins", "GET", "/books?author=nobody&author=Frank%20Herbert")
req("books-head", "HEAD", "/books")
req("books-put", "PUT", "/books")
req("books-delete", "DELETE", "/books")
req("books-options", "OPTIONS", "/books")
req("book-1", "GET", "/books/1")
req("book-3", "GET", "/books/3")
req("book-leading-zero", "GET", "/books/003")
req("book-missing", "GET", "/books/42")
req("book-not-int", "GET", "/books/dune")
req("book-negative", "GET", "/books/-1")
req("book-trailing-slash", "GET", "/books/2/")
req("book-patch-method", "TRACE", "/books/2")
req("book-options", "OPTIONS", "/books/2")

# creating and changing books
js("create", "POST", "/books", '{"title": "  Kindred ", "author": "Octavia E. Butler", "price": 11.0, "tags": ["sci-fi", "historical"]}')
req("create-then-get", "GET", "/books/4")
js("create-int-price", "POST", "/books", '{"title":"Piranesi","author":"Susanna Clarke","price":14}')
js("create-unicode", "POST", "/books", '{"title":"\\u00c9tranger","author":"Albert Camus","tags":["classique"],"price":7.25}')
js("create-raw-unicode", "POST", "/books", '{"title":"Норвежский лес","author":"Харуки Мураками","price":1e1}')
js("create-escapes", "POST", "/books", '{"title":"Tab\\there \\"quoted\\" back\\\\slash\\/","author":"A\\nB","price":0.1}')
js("create-duplicate-key", "POST", "/books", '{"title":"First","title":"Second","author":"Anon","price":1}')
js("create-missing", "POST", "/books", '{"title":"   ","price":-3,"tags":"poetry"}')
js("create-bool-price", "POST", "/books", '{"title":"T","author":"A","price":true}')
js("create-null-price", "POST", "/books", '{"title":"T","author":"A","price":null}')
js("create-tags-mixed", "POST", "/books", '{"title":"T","author":"A","tags":["ok",3]}')
js("create-not-object", "POST", "/books", '[1, 2, 3]')
js("create-string", "POST", "/books", '"just a string"')
js("create-bad-json", "POST", "/books", '{"title": "Unclosed"')
js("create-trailing-comma", "POST", "/books", '{"title": "T",}')
js("create-empty", "POST", "/books", '')
js("create-whitespace", "POST", "/books", '  \n {"title":"Spaced","author":"Out","price":2.5e-1} \n ')
js("create-trailing-garbage", "POST", "/books", '{"title":"T","author":"A"} x')
js("create-number-forms", "POST", "/books", '{"title":"N","author":"M","price":1.5E+2,"tags":[]}')
js("create-big-exp", "POST", "/books", '{"title":"N","author":"M","price":12345678901234567890e-10}')
js("create-leading-zero", "POST", "/books", '{"title":"N","author":"M","price":01}')
js("create-minus-zero-int", "POST", "/books", '{"title":"Z","author":"Z","price":-0}')
js("create-nested", "POST", "/books", '{"title":"Deep","author":"D","tags":["a"],"meta":{"x":[1,{"y":null}],"z":false}}')
req("list-after-creates", "GET", "/books?limit=20")
js("update", "PUT", "/books/1", '{"price": 10.49, "tags": ["sci-fi", "classic", "desert"]}')
js("update-patch", "PATCH", "/books/2", '{"title": "The Dispossessed"}')
js("update-bad", "PATCH", "/books/2", '{"price": "free", "author": ""}')
js("update-missing", "PUT", "/books/99", '{"price": 1}')
js("update-not-object", "PUT", "/books/1", 'null')
req("get-updated", "GET", "/books/1")
req("delete", "DELETE", "/books/3")
req("delete-again", "DELETE", "/books/3")
req("get-deleted", "GET", "/books/3")
req("price-eur", "GET", "/books/1/price/eur")
req("price-jpy", "GET", "/books/2/price/JPY")
req("price-unknown", "GET", "/books/1/price/xyz")
req("price-missing-book", "GET", "/books/77/price/USD")
req("price-quote", "GET", "/books/1/price/it%27s")

# converters
req("rate", "GET", "/rates/1.5")
req("rate-int", "GET", "/rates/2")
req("rate-tenth", "GET", "/rates/0.1")
req("rate-long", "GET", "/rates/0.30000000000000004")
req("rate-trailing-dot", "GET", "/rates/2.")
req("rate-exp", "GET", "/rates/1e5")
req("rate-zeros", "GET", "/rates/000.500")
req("order", "GET", "/orders/12345678-1234-5678-1234-567812345678")
req("order-upper-nodash", "GET", "/orders/ABCDEF0123456789ABCDEF0123456789")
req("order-mixed-dashes", "GET", "/orders/abcdef01-23456789-abcd-ef0123456789")
req("order-short", "GET", "/orders/1234")
req("order-delete", "DELETE", "/orders/12345678-1234-5678-1234-567812345678")
req("order-put", "PUT", "/orders/12345678-1234-5678-1234-567812345678")
req("order-post", "POST", "/orders/00000000-0000-0000-0000-000000000000")
req("files", "GET", "/files/docs/guide/intro.md")
req("files-empty", "GET", "/files/")
req("files-encoded", "GET", "/files/My%20Documents/r%C3%A9sum%C3%A9.pdf")
req("files-encoded-slash", "GET", "/files/a%2Fb")
req("files-dots", "GET", "/files/../../etc/passwd")
req("files-no-slash", "GET", "/files")
req("files-question", "GET", "/files/what%3F.txt")
req("files-hash", "GET", "/files/notes%23draft.txt")
req("files-bad-utf8", "GET", "/files/%FF%FEx")

# redirects
req("search-redirect", "GET", "/search?q=dune")
req("search", "GET", "/search/?q=DUNE")
req("search-empty", "GET", "/search/")
req("search-post-redirect", "POST", "/search")
req("old-catalog", "GET", "/old-catalog")
req("go", "GET", "/go?next=/books/1")
req("go-unicode", "GET", "/go?next=/caf%C3%A9%20menu?x=1%262")
req("go-absolute", "GET", "/go?next=https://evil.example/")
req("go-scheme-relative", "GET", "/go?next=//evil.example/")
req("go-default", "GET", "/go")
req("go-quote-chars", "GET", "/go?next=/a%22b%3Cc%3E%7Bd%7D%7Ce%5Ef%60g")
req("go-safe-chars", "GET", "/go?next=/x:y@z!$%26%27()*%2B,;=%25zz%5B%5D")
req("redirect-https-host", "GET", "/search", ["X-Test-Scheme: https"])
req("redirect-host-port", "GET", "/search", host="bookshop.test:8443")
req("redirect-bad-host", "GET", "/books/", host="localhost:abc")

# echo, cookies and headers
req("echo", "GET", "/echo?a=1&b=two&a=3", ["User-Agent: curl/8.5.0", "Accept: */*"])
req("echo-plus", "GET", "/echo?q=a+b%2Bc&empty=&flag")
req("echo-unicode-query", "GET", "/echo?name=Jos%C3%A9&bad=%E9")
req("echo-semicolon", "GET", "/echo?a=1;b=2")
req("echo-post", "POST", "/echo", ["Content-Type: text/plain", "Content-Length: 11"], "hello world")
req("echo-dup-headers", "GET", "/echo", ["X-Tag: one", "x-tag: two", "X-TAG: three"])
req("echo-cookies", "GET", "/echo", ["Cookie: session=alice:5; theme=dark;  lang = en ; =blank; novalue; quoted=\"a\\073b\\\"c\""])
req("echo-two-cookie-headers", "GET", "/echo", ["Cookie: a=1; b=2", "Cookie: b=3; c=4"])
req("echo-https", "GET", "/echo", ["X-Test-Scheme: https"])
req("echo-no-host", "GET", "/echo", host=None)
req("echo-delete", "DELETE", "/echo?id=4")
req("echo-options", "OPTIONS", "/echo")
js("login", "POST", "/login", '{"user": "alice"}')
js("login-unicode", "POST", "/login", '{"user": "Zoë Ånström"}')
js("login-missing", "POST", "/login", '{}')
js("login-spaces", "POST", "/login", '{"user": "bob smith"}')
req("login-get", "GET", "/login")
req("whoami", "GET", "/whoami", ["Cookie: session=alice:5"])
req("whoami-none", "GET", "/whoami")
req("whoami-quoted", "GET", "/whoami", ["Cookie: session=\"carol\\0729\""])
req("logout", "POST", "/logout")

# errors and handlers
req("teapot", "GET", "/teapot")
req("teapot-brew", "BREW", "/teapot")
req("teapot-delete", "DELETE", "/teapot")
req("boom", "GET", "/boom?n=4")
req("boom-zero", "GET", "/boom?n=0")
req("boom-bad", "GET", "/boom?n=four")
req("boom-negative", "GET", "/boom?n=-3")
req("stock", "GET", "/stock/DUNE-HB")
req("stock-out", "GET", "/stock/LHOD-PB")
req("stock-unknown", "GET", "/stock/NOPE")
req("cache", "GET", "/cache/greeting")
req("cache-hit", "GET", "/cache/greeting", ['If-None-Match: "greeting-v1"'])
req("cache-miss", "GET", "/cache/greeting", ['If-None-Match: "greeting-v0"'])
req("not-found", "GET", "/nope")
req("not-found-slash", "GET", "/nope/")
req("not-found-encoded", "GET", "/n%C3%B6pe%3Fq")
req("root-slashes", "GET", "//")

# the admin mount
req("admin-home", "GET", "/admin/")
req("admin-bare", "GET", "/admin")
req("admin-user", "GET", "/admin/users/7")
req("admin-user-bad", "GET", "/admin/users/x")
req("admin-reports-redirect", "GET", "/admin/reports?year=2026")
req("admin-reports", "GET", "/admin/reports/")
req("admin-tool", "GET", "/admin/tools/hammer")
req("admin-tools-root", "GET", "/admin/tools/")
req("admin-tool-slash", "GET", "/admin/tools/hammer/")
req("admin-post", "POST", "/admin/users/7")
req("admin-missing", "GET", "/admin/nothing")
req("admin-prefix", "GET", "/administrator")

# the static mount (a plain ASGI app)
req("static", "GET", "/static/css/site.css")
req("static-js", "GET", "/static/js/app.js")
req("static-missing", "GET", "/static/img/logo.png")
req("static-root", "GET", "/static/")
req("static-bare", "GET", "/static")
req("static-post", "POST", "/static/css/site.css")

# tenants by host
req("tenant", "GET", "/", host="acme.shop.example")
req("tenant-port", "GET", "/", host="acme.shop.example:8080")
req("tenant-stats", "GET", "/stats", host="globex.shop.example")
req("tenant-stats-slash", "GET", "/stats/", host="globex.shop.example")
req("tenant-missing", "GET", "/books", host="acme.shop.example")
req("tenant-upper", "GET", "/", host="ACME.shop.example")
req("tenant-nested", "GET", "/", host="a.b.shop.example")

# trusted hosts
req("host-www-redirect", "GET", "/books?x=1", host="shop.example")
req("host-www", "GET", "/", host="www.shop.example")
req("host-bad", "GET", "/", host="evil.example")
req("host-empty", "GET", "/", host="")
req("host-localhost", "GET", "/echo", host="localhost:8000")
req("host-suffix-trick", "GET", "/", host="evilshop.example")

# CORS
req("cors-simple", "GET", "/books/1", [APP])
req("cors-simple-other", "GET", "/books/1", ["Origin: https://admin.example.com"])
req("cors-disallowed", "GET", "/books/1", ["Origin: https://evil.example"])
req("cors-preflight", "OPTIONS", "/books", [APP, "Access-Control-Request-Method: POST", "Access-Control-Request-Headers: Content-Type, X-Request-Id"])
req("cors-preflight-no-headers", "OPTIONS", "/books/2", [APP, "Access-Control-Request-Method: DELETE"])
req("cors-preflight-bad-method", "OPTIONS", "/books", [APP, "Access-Control-Request-Method: PATCH"])
req("cors-preflight-bad-header", "OPTIONS", "/books", [APP, "Access-Control-Request-Method: GET", "Access-Control-Request-Headers: X-Secret"])
req("cors-preflight-bad-everything", "OPTIONS", "/books", ["Origin: https://evil.example", "Access-Control-Request-Method: PATCH", "Access-Control-Request-Headers: authorization,x-other", "Access-Control-Request-Private-Network: true"])
req("cors-preflight-private", "OPTIONS", "/books", [APP, "Access-Control-Request-Method: GET", "Access-Control-Request-Private-Network: true"])
req("cors-preflight-case", "OPTIONS", "/books", [APP, "Access-Control-Request-Method: get"])
req("cors-preflight-missing-route", "OPTIONS", "/nowhere", [APP, "Access-Control-Request-Method: GET"])
req("cors-options-no-request-method", "OPTIONS", "/books", [APP])
req("cors-on-404", "GET", "/nope", [APP])
req("cors-on-405", "PUT", "/books", [APP])
req("cors-on-redirect", "GET", "/search", [APP])
req("cors-on-500", "GET", "/boom?n=0", [APP])
req("cors-on-teapot", "GET", "/teapot", [APP])
req("cors-on-cookies", "POST", "/login", [APP, "Content-Type: application/json"], '{"user":"dave"}')
req("cors-vary-exists", "GET", "/cache/greeting", [APP])
req("cors-empty-origin", "GET", "/books/1", ["Origin: "])
req("cors-null-origin", "GET", "/books/1", ["Origin: null"])

for n, (name, text) in enumerate(reqs):
    with open("data/requests/%03d-%s.http" % (n, name), "w", newline="") as f:
        f.write(text)
print(len(paths), len(urlfor), len(reqs))
