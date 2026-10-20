# The oracle: a bookshop service on Starlette 1.6.0, driven straight through
# ASGI. Run it from the app directory, after mk.py, with PYTHONHASHSEED=0 (a
# 405's Allow header joins a set, so its order is the set's):
#     PYTHONHASHSEED=0 python3 -s -P oracle.py > expected.out
import asyncio
import json
import math
import os
import sys
import uuid
from urllib.parse import unquote

from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse, Response
from starlette.routing import Host, Mount, NoMatchFound, Route, Router, compile_path
from starlette.datastructures import MutableHeaders
from starlette._utils import get_route_path

assert os.environ.get("PYTHONHASHSEED") == "0", "run with PYTHONHASHSEED=0"

BOOKS = {}
NEXT = [1]
STOCK = {"DUNE-HB": 4, "LHOD-PB": 0}
RATES = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 149.5}


def add_book(title, author, price, tags):
    bid = NEXT[0]
    NEXT[0] += 1
    BOOKS[bid] = {"id": bid, "title": title, "author": author, "price": price, "tags": tags}
    return BOOKS[bid]


add_book("Dune", "Frank Herbert", 9.99, ["sci-fi", "classic"])
add_book("The Left Hand of Darkness", "Ursula K. Le Guin", 12.5, ["sci-fi"])
add_book("Cien años de soledad", "Gabriel García Márquez", 15, ["classic", "magic-realism"])


class OutOfStock(Exception):
    def __init__(self, sku):
        self.sku = sku


async def body_json(request):
    try:
        return await request.json()
    except ValueError:
        raise HTTPException(400, "Body must be valid JSON")


def check_fields(data, partial):
    errors = []
    for key in data:
        if key not in ("title", "author", "price", "tags"):
            errors.append(f"unknown field {key!r}")
    for key in ("title", "author"):
        if key in data or not partial:
            v = data.get(key)
            if not isinstance(v, str) or not v.strip():
                errors.append(f"{key} is required")
    if "price" in data:
        p = data["price"]
        if isinstance(p, bool) or not isinstance(p, (int, float)) or p < 0:
            errors.append("price must be a non-negative number")
    if "tags" in data:
        t = data["tags"]
        if not isinstance(t, list) or not all(isinstance(x, str) for x in t):
            errors.append("tags must be a list of strings")
    return errors


async def homepage(request):
    return PlainTextResponse("Bookshop API\n")


async def list_books(request):
    q = request.query_params
    items = list(BOOKS.values())
    author = q.get("author")
    if author:
        items = [b for b in items if b["author"].lower() == author.lower()]
    for tag in q.getlist("tag"):
        items = [b for b in items if tag in b["tags"]]
    try:
        limit = int(q.get("limit", "10"))
        offset = int(q.get("offset", "0"))
    except ValueError:
        raise HTTPException(400, "limit and offset must be integers")
    if limit < 0 or offset < 0:
        raise HTTPException(400, "limit and offset must not be negative")
    return JSONResponse({"total": len(items), "items": items[offset : offset + limit]})


async def create_book(request):
    data = await body_json(request)
    if not isinstance(data, dict):
        raise HTTPException(422, "Expected a JSON object")
    errors = check_fields(data, False)
    if errors:
        return JSONResponse({"errors": errors}, status_code=422)
    book = add_book(data["title"].strip(), data["author"].strip(), data.get("price", 0), data.get("tags", []))
    location = request.url_for("book", book_id=book["id"])
    return JSONResponse(book, status_code=201, headers={"Location": str(location)})


async def get_book(request):
    bid = request.path_params["book_id"]
    if bid not in BOOKS:
        raise HTTPException(404, f"Book {bid} not found")
    return JSONResponse(BOOKS[bid])


async def update_book(request):
    bid = request.path_params["book_id"]
    if bid not in BOOKS:
        raise HTTPException(404, f"Book {bid} not found")
    data = await body_json(request)
    if not isinstance(data, dict):
        raise HTTPException(422, "Expected a JSON object")
    errors = check_fields(data, True)
    if errors:
        return JSONResponse({"errors": errors}, status_code=422)
    book = BOOKS[bid]
    for key, value in data.items():
        book[key] = value.strip() if isinstance(value, str) else value
    return JSONResponse(book)


async def delete_book(request):
    bid = request.path_params["book_id"]
    if bid not in BOOKS:
        raise HTTPException(404, f"Book {bid} not found")
    del BOOKS[bid]
    return Response(status_code=204)


async def price_in(request):
    bid = request.path_params["book_id"]
    currency = request.path_params["currency"].upper()
    if bid not in BOOKS:
        raise HTTPException(404, f"Book {bid} not found")
    if currency not in RATES:
        raise HTTPException(400, f"Unknown currency {currency!r}")
    price = BOOKS[bid]["price"]
    return JSONResponse({"book": bid, "currency": currency, "price": price * RATES[currency]})


async def rate(request):
    r = request.path_params["rate"]
    return JSONResponse({"rate": r, "double": str(request.url_for("rate", rate=r * 2))})


async def order(request):
    oid = request.path_params["order_id"]
    if request.method == "DELETE":
        return Response(status_code=204, headers={"X-Order": str(oid)})
    if request.method == "POST" and oid.int == 0:
        raise HTTPException(409, "The nil order cannot be placed")
    return JSONResponse({"order": str(oid), "hex": oid.hex, "version": oid.version})


async def files(request):
    path = request.path_params["path"]
    return PlainTextResponse(f"file {path!r} ({len(path)} chars)\n")


async def search(request):
    q = request.query_params.get("q", "").lower()
    hits = [b["title"] for b in BOOKS.values() if q in b["title"].lower()]
    return JSONResponse({"q": q, "hits": hits})


async def old_catalog(request):
    return RedirectResponse(request.url_for("books"), status_code=301)


async def go(request):
    target = request.query_params.get("next", "/")
    if not target.startswith("/") or target.startswith("//"):
        raise HTTPException(400, "next must be a local path")
    return RedirectResponse(target, status_code=303)


async def echo(request):
    body = await request.body()
    return JSONResponse(
        {
            "method": request.method,
            "url": str(request.url),
            "base_url": str(request.base_url),
            "path": request.url.path,
            "query": [[k, v] for k, v in request.query_params.multi_items()],
            "query_string": str(request.query_params),
            "headers": [[k, v] for k, v in request.headers.items()],
            "cookies": request.cookies,
            "client": list(request.client),
            "body": body.decode("utf-8"),
        }
    )


async def login(request):
    data = await body_json(request)
    user = data.get("user") if isinstance(data, dict) else None
    if not isinstance(user, str) or not user:
        raise HTTPException(422, "user is required")
    response = JSONResponse({"ok": True, "user": user})
    response.set_cookie("session", f"{user}:{len(user)}", max_age=3600, httponly=True)
    response.set_cookie("prefs", "theme=dark; lang=en", path="/books", samesite="strict", secure=True)
    return response


async def logout(request):
    response = PlainTextResponse("bye\n")
    response.set_cookie("session", "", max_age=0)
    return response


async def whoami(request):
    session = request.cookies.get("session")
    if session is None:
        raise HTTPException(401, headers={"WWW-Authenticate": 'Cookie realm="shop"'})
    user, _, _ = session.partition(":")
    return JSONResponse({"user": user, "session": session})


async def teapot(request):
    if request.method == "BREW":
        return PlainTextResponse("brewing\n", status_code=202)
    raise HTTPException(418, headers={"X-Tea": "Earl Grey"})


async def boom(request):
    n = int(request.query_params.get("n", "1"))
    return JSONResponse({"result": 100 // n})


async def stock(request):
    sku = request.path_params["sku"]
    if sku not in STOCK:
        raise HTTPException(404, f"Unknown SKU {sku}")
    if STOCK[sku] == 0:
        raise OutOfStock(sku)
    return JSONResponse({"sku": sku, "available": STOCK[sku]})


async def cache(request):
    key = request.path_params["key"]
    etag = f'"{key}-v1"'
    if request.headers.get("if-none-match") == etag:
        raise HTTPException(304, headers={"ETag": etag})
    return PlainTextResponse(f"value of {key}\n", headers={"ETag": etag, "Cache-Control": "max-age=60", "Vary": "Accept-Encoding"})


async def admin_home(request):
    return PlainTextResponse(f"admin home (root_path {request.scope['root_path']!r})\n")


async def admin_user(request):
    uid = request.path_params["uid"]
    return JSONResponse(
        {
            "uid": uid,
            "self": str(request.url_for("admin:user", uid=uid)),
            "home": str(request.url_for("admin:home")),
            "route_path": get_route_path(request.scope),
        }
    )


async def reports(request):
    return PlainTextResponse(f"reports for {request.query_params.get('year', 'all')}\n")


async def tool(request):
    return PlainTextResponse(f"tool {request.path_params['tool']} under {request.scope['root_path']}\n")


STATIC = {"/css/site.css": ("text/css", "body { margin: 0 }\n"), "/js/app.js": ("text/javascript", "console.log('hi');\n")}


async def static_app(scope, receive, send):
    path = get_route_path(scope)
    if scope["method"] not in ("GET", "HEAD"):
        response = PlainTextResponse("Method Not Allowed", status_code=405)
    elif path in STATIC:
        media, text = STATIC[path]
        response = Response(text, media_type=media)
    else:
        response = PlainTextResponse(f"no static file {path!r} under {scope['root_path']!r}", status_code=404)
    await response(scope, receive, send)


async def tenant_home(request):
    t = request.path_params["tenant"]
    return JSONResponse({"tenant": t, "home": str(request.url_for("tenant:home", tenant=t))})


async def tenant_stats(request):
    t = request.path_params["tenant"]
    return JSONResponse({"tenant": t, "orders": len(t) * 7})


async def not_found(request, exc):
    return JSONResponse({"detail": exc.detail, "path": request.url.path}, status_code=404)


async def out_of_stock(request, exc):
    return JSONResponse({"sku": exc.sku, "error": "out of stock"}, status_code=409, headers={"Retry-After": "120"})


class RequestIdMiddleware:
    def __init__(self, app):
        self.app = app
        self.count = 0

    async def __call__(self, scope, receive, send):
        self.count += 1
        rid = f"req-{self.count}"

        async def send_with_id(message):
            if message["type"] == "http.response.start":
                MutableHeaders(scope=message).append("X-Request-Id", rid)
            await send(message)

        await self.app(scope, receive, send_with_id)


tenant_router = Router(routes=[Route("/", tenant_home, name="home"), Route("/stats", tenant_stats, name="stats")])

routes = [
    Host("{tenant}.shop.example", app=tenant_router, name="tenant"),
    Route("/", homepage),
    Route("/books", list_books, name="books"),
    Route("/books", create_book, methods=["POST"]),
    Route("/books/{book_id:int}", get_book, name="book"),
    Route("/books/{book_id:int}", update_book, methods=["PUT", "PATCH"]),
    Route("/books/{book_id:int}", delete_book, methods=["DELETE"]),
    Route("/books/{book_id:int}/price/{currency}", price_in, name="price"),
    Route("/rates/{rate:float}", rate, name="rate"),
    Route("/orders/{order_id:uuid}", order, methods=["GET", "DELETE", "POST"], name="order"),
    Route("/files/{path:path}", files, name="files"),
    Route("/search/", search, name="search"),
    Route("/old-catalog", old_catalog),
    Route("/go", go),
    Route("/echo", echo, methods=["GET", "POST", "PUT", "PATCH", "DELETE"]),
    Route("/login", login, methods=["POST"]),
    Route("/logout", logout, methods=["POST"]),
    Route("/whoami", whoami),
    Route("/teapot", teapot, methods=["GET", "POST", "brew"]),
    Route("/boom", boom),
    Route("/stock/{sku}", stock, name="stock"),
    Route("/cache/{key}", cache, name="cache"),
    Mount(
        "/admin",
        name="admin",
        routes=[
            Route("/", admin_home, name="home"),
            Route("/users/{uid:int}", admin_user, name="user"),
            Route("/reports/", reports, name="reports"),
            Mount("/tools", name="tools", routes=[Route("/{tool}", tool, name="tool")]),
        ],
    ),
    Mount("/static", app=static_app, name="static"),
]

middleware = [
    Middleware(
        TrustedHostMiddleware,
        allowed_hosts=["bookshop.test", "*.shop.example", "www.shop.example", "localhost"],
    ),
    Middleware(
        CORSMiddleware,
        allow_origins=["https://app.example.com", "https://admin.example.com"],
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "X-Request-Id"],
        allow_credentials=True,
        expose_headers=["X-Request-Id", "Location"],
        max_age=300,
    ),
    Middleware(RequestIdMiddleware),
]

app = Starlette(routes=routes, middleware=middleware, exception_handlers={404: not_found, OutOfStock: out_of_stock})


def show_compile():
    print("# compile_path")
    with open("data/paths.txt") as f:
        for line in f:
            path = line.rstrip("\n")
            try:
                regex, fmt, convs = compile_path(path)
                cs = ", ".join(f"{k}={type(v).__name__}" for k, v in convs.items())
                print(f"{path!r} -> {regex.pattern!r} {fmt!r} [{cs}]")
            except (ValueError, AssertionError) as e:
                print(f"{path!r} -> ! {type(e).__name__}: {e}")


def parse_value(t):
    kind, _, v = t.partition(":")
    if kind == "int":
        return int(v)
    if kind == "float":
        return float(v)
    return v


def show_urlfor():
    print("# url_path_for")
    with open("data/urlfor.txt") as f:
        for line in f:
            parts = line.rstrip("\n").split("|")
            name = parts[0]
            params = {}
            for p in parts[1:]:
                k, _, v = p.partition("=")
                params[k] = parse_value(v)
            shown = ", ".join(f"{k}={v!r}" for k, v in params.items())
            try:
                url = app.url_path_for(name, **params)
                print(f"{name}({shown}) -> {str(url)!r} protocol={url.protocol!r} host={url.host!r}")
            except (NoMatchFound, AssertionError, ValueError) as e:
                print(f"{name}({shown}) -> ! {type(e).__name__}: {e}")


def show_routes():
    print("# routes")
    for r in routes:
        if isinstance(r, Route):
            print(repr(r))


def parse_request(raw):
    head, _, body = raw.partition(b"\r\n\r\n")
    lines = head.decode("latin-1").split("\r\n")
    method, target, _ = lines[0].split(" ")
    headers = []
    scheme = "http"
    for h in lines[1:]:
        k, _, v = h.partition(":")
        if k.lower() == "x-test-scheme":
            scheme = v.strip()
            continue
        headers.append((k.lower().encode("latin-1"), v.strip().encode("latin-1")))
    raw_path, _, query = target.partition("?")
    scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.4"},
        "http_version": "1.1",
        "method": method,
        "scheme": scheme,
        "path": unquote(raw_path),
        "raw_path": raw_path.encode("latin-1"),
        "query_string": query.encode("latin-1"),
        "root_path": "",
        "headers": headers,
        "client": ("203.0.113.9", 50123),
        "server": ("bookshop.test", 443 if scheme == "https" else 80),
    }
    return scope, body


async def run_one(scope, body):
    sent = []
    messages = [{"type": "http.request", "body": body, "more_body": False}]

    async def receive():
        if messages:
            return messages.pop(0)
        return {"type": "http.disconnect"}

    async def send(message):
        sent.append(message)

    error = None
    try:
        await app(scope, receive, send)
    except Exception as e:
        error = e
    return sent, error


def show_requests():
    print("# requests")
    for name in sorted(os.listdir("data/requests")):
        with open(os.path.join("data/requests", name), "rb") as f:
            raw = f.read()
        scope, body = parse_request(raw)
        q = scope["query_string"].decode("latin-1")
        print(f"== {name[:-5]}")
        print(f"> {scope['method']} {scope['path']!r}" + (f" ?{q}" if q else ""))
        sent, error = asyncio.run(run_one(scope, body))
        for m in sent:
            if m["type"] == "http.response.start":
                print(f"< {m['status']}")
                for k, v in m["headers"]:
                    print(f"< {k.decode('latin-1')}: {v.decode('latin-1')}")
            elif m["type"] == "http.response.body":
                b = m.get("body", b"")
                if b:
                    print(f"| {b.decode('utf-8')!r}")
        if error is not None:
            print(f"! raised {type(error).__name__}: {error}")


show_compile()
show_urlfor()
show_routes()
show_requests()
