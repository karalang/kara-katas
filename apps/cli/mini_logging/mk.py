# Writes data/: the service's logging configurations, some broken
# ones, the log files a previous run left behind, and run.txt, the
# script of what the service logs from startup to shutdown.
import json, os, shutil

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data/config/broken")
os.makedirs("data/logs")


def put(path, obj):
    with open(path, "w") as f:
        if isinstance(obj, str):
            f.write(obj)
        else:
            json.dump(obj, f, indent=2)
            f.write("\n")


# What yesterday's run left in the access log and its backups.
put("data/logs/access.log", "".join(
    f"14/Oct/2026:23:5{i}:0{i} r-09{i}{i} GET /api/health 200 17B 0.4ms\n" for i in range(6)))
put("data/logs/access.log.1", "14/Oct/2026:22:00:00 r-0800 GET /api/products 200 5123B 9.1ms\n")
put("data/logs/access.log.2", "14/Oct/2026:21:00:00 r-0700 GET /api/products 200 5123B 8.7ms\n")
put("data/logs/db.log", "yesterday's database log, which mode 'w' replaces\n")
put("data/logs/audit.log", "2026-10-14 audit trail that a failed reload truncates\n")

base = {
    "version": 1,
    "formatters": {
        "plain": {"format": "%(asctime)s %(levelname)-8s %(name)s: %(message)s"},
        "access": {
            "format": "{asctime} {request_id} {message}",
            "style": "{",
            "datefmt": "%d/%b/%Y:%H:%M:%S",
            "defaults": {"request_id": "-"},
        },
        "json": {
            "format": '{"t": "$asctime", "lvl": "$levelname", "logger": "${name}", "msg": "$message"}',
            "style": "$",
        },
        "db": {"format": "%(relativeCreated)8d ms %(levelname).1s %(name)-12s|%(message)s"},
    },
    "filters": {"app_only": {"name": "app"}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "plain",
            "filters": ["app_only"],
            "stream": "ext://sys.stdout",
        },
        "errors": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "json",
            "stream": "ext://sys.stderr",
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "data/logs/access.log",
            "maxBytes": 400,
            "backupCount": 2,
            "formatter": "access",
            "encoding": "utf-8",
        },
        "db_file": {
            "class": "logging.FileHandler",
            "filename": "data/logs/db.log",
            "mode": "w",
            "formatter": "db",
            "encoding": "utf-8",
        },
        "buffer": {
            "class": "logging.handlers.MemoryHandler",
            "capacity": 3,
            "flushLevel": "ERROR",
            "target": "db_file",
        },
    },
    "loggers": {
        "app.http.access": {"handlers": ["access_file"], "level": "INFO", "propagate": False},
        "app.db": {"handlers": ["buffer"], "level": "DEBUG"},
    },
    "root": {"level": "INFO", "handlers": ["console", "errors"]},
}
put("data/config/base.json", base)

verbose = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "brace": {"format": "{asctime}.{msecs:03.0f} {levelname:<8} [{name:>15}] {message}", "style": "{", "datefmt": "%H:%M:%S"},
        "db": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s", "datefmt": "%a %d %b %H:%M:%S"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "brace", "stream": "ext://sys.stdout"},
        "db_file": {"class": "logging.FileHandler", "filename": "data/logs/db.log", "formatter": "db", "encoding": "utf-8"},
        "trash": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "app": {"level": "DEBUG"},
        "app.db": {"handlers": ["db_file"], "propagate": False},
        "stripe": {"level": "WARNING", "handlers": ["trash"], "propagate": False},
    },
    "root": {"level": "WARNING", "handlers": ["console"]},
}
put("data/config/verbose.json", verbose)

broken = {
    "no_version": {"handlers": {"console": {"class": "logging.StreamHandler"}}},
    "version_two": {"version": 2},
    "percent_brace": {
        "version": 1,
        "formatters": {"plain": {"format": "{levelname} {message}"}},
        "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "plain"}},
    },
    "bad_style": {"version": 1, "formatters": {"plain": {"format": "%(message)s", "style": "%%"}}},
    "dollar_no_fields": {"version": 1, "formatters": {"tpl": {"format": "%(message)s", "style": "$"}}},
    "brace_conversion": {"version": 1, "formatters": {"x": {"format": "{message!x}", "style": "{"}}},
    "brace_spec": {"version": 1, "formatters": {"x": {"format": "{levelname:<8q} {message}", "style": "{"}}},
    "bare_dollar": {"version": 1, "formatters": {"x": {"format": "$levelname costs $5", "style": "$"}}},
    "bad_level": {
        "version": 1,
        "handlers": {
            "audit": {"class": "logging.FileHandler", "filename": "data/logs/audit.log", "mode": "w"},
            "console": {"class": "logging.StreamHandler", "level": "VERBOSE"},
        },
    },
    "bad_class": {
        "version": 1,
        "handlers": {"rotating": {"class": "logging.handlers.RotatingHandler", "filename": "data/logs/x.log"}},
    },
    "bad_kwarg": {
        "version": 1,
        "handlers": {
            "access_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "data/logs/access.log",
                "max_bytes": 1000,
            }
        },
    },
    "bad_target": {
        "version": 1,
        "handlers": {"buf": {"class": "logging.handlers.MemoryHandler", "capacity": 10, "target": "missing"}},
    },
    "bad_flush_level": {
        "version": 1,
        "handlers": {"buf": {"class": "logging.handlers.MemoryHandler", "capacity": 10, "flushLevel": "LOUD"}},
    },
    "bad_formatter_ref": {
        "version": 1,
        "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "fancy"}},
    },
    "bad_ref": {
        "version": 1,
        "formatters": {"short": {"format": "$levelname $name: $message", "style": "$"}},
        "handlers": {"console2": {"class": "logging.StreamHandler", "formatter": "short", "stream": "ext://sys.stdout"}},
        "loggers": {"app.db": {"handlers": ["console2", "nope"]}},
    },
}
for name, cfg in broken.items():
    put(f"data/config/broken/{name}.json", cfg)

final = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"plain": {"format": "%(levelname)s %(name)s: %(message)s"}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "plain", "stream": "ext://sys.stdout"},
        "buffer": {"class": "logging.handlers.MemoryHandler", "capacity": 100, "target": "console"},
    },
    "loggers": {"app.http": {"handlers": ["buffer"], "propagate": False}},
    "root": {"level": "INFO", "handlers": ["console"]},
}
put("data/config/final.json", final)

run = []
def r(*lines):
    run.extend(lines)

r("# shop-api: a web service's logging from startup to shutdown.",
  "# Fields are separated by ' | '. Message arguments are s: (str),",
  "# i: (int) and f: (float); x:key=value is an `extra` field.",
  "",
  "# Nothing is configured yet, so only the last-resort handler runs.",
  "log app | INFO | starting shop-api %s | s:2.4.1",
  "log app | WARNING | config file %r not found, using defaults | s:/etc/shop/shop.toml",
  "tick 250",
  "basic | level=INFO",
  "log app | INFO | listening on port %d | i:8080",
  "log app.http | DEBUG | not shown: the root logger is at INFO",
  "basic | level=DEBUG | stream=stdout | format=%(levelname)s %(message)s",
  "log app.http | DEBUG | not shown either: the second basicConfig did nothing",
  "tick 1000",
  "basic | force | level=DEBUG | stream=stdout | format=%(asctime)s %(levelname)-8s %(name)s %(message)s",
  "log app.http | DEBUG | shown: force replaced the handler",
  "getlogger app.cache.redis",
  "log app.cache.redis | INFO | connected to %s:%d | s:10.0.0.7 | i:6379",
  "log urllib3.connectionpool | DEBUG | Starting new HTTPS connection (%d): %s:%s | i:1 | s:payments.example | i:443",
  "log app | INFO | %-6s|%6s|%06.2f|%+d|%x|%X|%o|%5.1f%% | s:ab | s:cd | f:3.14159 | i:42 | i:255 | i:48879 | i:8 | f:99.5",
  "log app | INFO | %r %r %r %.3s | s:it's | s:say \"hi\" | i:-7 | s:truncated",
  "tree",
  "",
  "tick 1500",
  "config | data/config/base.json",
  "tree",
  "enabled app.db",
  "enabled app.http.access",
  "enabled app",
  )
reqs = [("GET", "/api/products", 200, 5123, "12.34"), ("GET", "/api/products/42", 200, 811, "3.07"),
        ("POST", "/api/cart", 201, 96, "18.91"), ("GET", "/api/cart", 200, 412, "4.2"),
        ("DELETE", "/api/cart/7", 204, 0, "6.66"), ("GET", "/favicon.ico", 404, 9, "0.31"),
        ("POST", "/api/checkout", 502, 37, "1504.88"), ("GET", "/api/products?page=2", 200, 4980, "11.1"),
        ("GET", "/api/health", 200, 17, "0.38"), ("PUT", "/api/profile", 200, 233, "27.02"),
        ("GET", "/api/orders", 200, 2048, "15.51"), ("GET", "/robots.txt", 200, 24, "0.29")]
for k, (m, p, s, b, ms) in enumerate(reqs):
    extra = "" if k in (5, 8) else f" | x:request_id=r-{1001 + k}"
    r(f"tick {137 * (k + 1)}",
      f"log app.http.access | INFO | %s %s %d %dB %sms | s:{m} | s:{p} | i:{s} | i:{b} | f:{ms}{extra}")
    if k == 3:
        r("log app.db | DEBUG | SELECT * FROM products WHERE id = %d | i:42",
          "log app.db.pool | DEBUG | checked out connection %d of %d | i:3 | i:10",
          "log app.db | INFO | migration %s applied | s:0042_add_index")
    if k == 6:
        r("log app.db | ERROR | deadlock detected, retrying (%d/%d) | i:1 | i:3",
          "log app.db | DEBUG | ROLLBACK")
r("log app.http.access | INFO | %s %s | s:GET | x:name=oops",
  "log app.http.access | INFO | %s %s | s:GET | x:message=oops",
  "log urllib3.connectionpool | WARNING | Retrying (%s) after connection broken | s:Retry(total=2)",
  "log app | WARNING | low disk space: %d%% free | i:7",
  "log app.cache.redis | WARNING | evicted %d keys | i:1200",
  "log stripe.http | WARNING | slow response from %s | s:api.stripe.example",
  "log stripe.http | ERROR | charge %s failed: card_declined | s:ch_3P",
  "log app.payments | WARNING | charge %s declined, asking the customer | s:ch_3P",
  "",
  "level app.db | WARNING",
  "enabled app.db.pool",
  "log app.db.pool | INFO | pool resized to %d | i:20",
  "log app.db | WARNING | replica lag %d s | i:12",
  "level app.db | DEBUG",
  "disable | WARNING",
  "log app.payments | WARNING | not shown: logging.disable(WARNING)",
  "log app.payments | ERROR | refund %s failed | s:re_9",
  "disable | NOTSET",
  "addlevel | 25 | NOTICE",
  "log app.payments | NOTICE | payout %s scheduled | s:po_77",
  "log app.payments | 15 | not shown: level 15 is below the root's INFO",
  "level app.payments | 15",
  "log app.payments | 15 | shown? the logger allows it, but console is at INFO",
  "log app.payments | 35 | level 35 has no name",
  "tree",
  "",
  "tick 2000",
  "config | data/config/verbose.json",
  "tree",
  "log app | DEBUG | app is enabled again",
  "log app.http | INFO | %s requests in the last minute | i:12",
  "log app.http.access | INFO | %s %s %d | s:GET | s:/api/after-reload | i:200 | x:request_id=r-2001",
  "log app.db | INFO | vacuum finished in %.2f s | f:4.567",
  "log app.db.pool | WARNING | connection %d reset | i:4",
  "log stripe | ERROR | not shown: stripe goes to a NullHandler",
  "log app.payments | 15 | reset by the reload, so INFO is the effective level",
  "log app.payments | NOTICE | NOTICE survives the reload",
  "",
  "# Reloads that fail part way.",
  )
for name in broken:
    r(f"tick 100", f"config | data/config/broken/{name}.json",
      f"log app.db | WARNING | after {name}", f"log app | WARNING | after {name}")
r("tree", "",
  "tick 3000",
  "config | data/config/final.json",
  "log app.http | INFO | buffered %d | i:1",
  "log app | WARNING | not buffered",
  "log app.http | ERROR | buffered %d, and ERROR is the default flush level | i:2",
  "log app.http | INFO | buffered %d, still in the buffer at exit | i:3",
  "tree",
  "shutdown",
  "files",
  )
put("data/run.txt", "\n".join(run) + "\n")
