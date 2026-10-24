"""Writes data/jobs.txt: the client conversations mini_redispy plays.

Run: python3 -s -P -B mk.py"""
import os

JOBS = []


def esc(data):
    if isinstance(data, str):
        data = data.encode()
    out = []
    for b in data:
        c = chr(b)
        if 33 <= b < 127 and c not in "%":
            out.append(c)
        else:
            out.append(f"%{b:02X}")
    return "".join(out)


# ------------------------------------------------------------ RESP builders

def simple(s):
    return b"+" + s.encode() + b"\r\n"


def err(s):
    return b"-" + s.encode() + b"\r\n"


def num(n):
    return b":" + str(n).encode() + b"\r\n"


def bulk(v):
    if isinstance(v, str):
        v = v.encode()
    return b"$" + str(len(v)).encode() + b"\r\n" + v + b"\r\n"


NIL = b"$-1\r\n"
NIL_ARR = b"*-1\r\n"
OK = simple("OK")
QUEUED = simple("QUEUED")


def arr(items):
    out = b"*" + str(len(items)).encode() + b"\r\n"
    for it in items:
        out += enc(it)
    return out


def enc(it):
    if isinstance(it, bytes):
        return it
    if isinstance(it, str):
        return bulk(it)
    if isinstance(it, int):
        return num(it)
    if isinstance(it, list):
        return arr(it)
    if it is None:
        return NIL
    raise ValueError(it)


# RESP3
NULL3 = b"_\r\n"


def dbl(text):
    return b"," + text.encode() + b"\r\n"


def boolean(t):
    return b"#t\r\n" if t else b"#f\r\n"


def big(text):
    return b"(" + text.encode() + b"\r\n"


def verbatim(fmt, text):
    body = (fmt + ":" + text).encode()
    return b"=" + str(len(body)).encode() + b"\r\n" + body + b"\r\n"


def blob_err(text):
    body = text.encode()
    return b"!" + str(len(body)).encode() + b"\r\n" + body + b"\r\n"


def map3(pairs):
    out = b"%" + str(len(pairs)).encode() + b"\r\n"
    for k, v in pairs:
        out += enc(k) + enc(v)
    return out


def set3(items):
    out = b"~" + str(len(items)).encode() + b"\r\n"
    for it in items:
        out += enc(it)
    return out


def push(items):
    out = b">" + str(len(items)).encode() + b"\r\n"
    for it in items:
        out += enc(it)
    return out


def hello3(proto=3):
    return map3([
        ("server", "redis"), ("version", "7.4.1"), ("proto", proto),
        ("id", 14), ("mode", "standalone"), ("role", "master"), ("modules", []),
    ])


# ------------------------------------------------------------ jobs

class Job:
    def __init__(self, title, **client):
        self.lines = ["job " + title]
        opts = []
        for k, v in client.items():
            opts.append(f"{k}={tok(v)}")
        self.lines.append(" ".join(["client"] + list(opts)))
        JOBS.append(self)

    def reply(self, *units):
        for u in units:
            if u in ("@close", "@hang"):
                self.lines.append("reply " + u)
            else:
                self.lines.append("reply " + esc(u))
        return self

    def hs(self, n=2):
        """The two CLIENT SETINFO replies of a default handshake."""
        for _ in range(n):
            self.reply(OK)
        return self

    def call(self, text):
        self.lines.append("call " + text)
        return self

    def pipe(self, text):
        self.lines.append("pipe " + text)
        return self

    def bitfield(self, text):
        self.lines.append("bitfield " + text)
        return self

    def url(self, text):
        self.lines.append("url " + esc(text))
        return self


def tok(v):
    if v is None:
        return "N:"
    if v is True:
        return "T:"
    if v is False:
        return "F:"
    if isinstance(v, int):
        return f"i:{v}"
    if isinstance(v, float):
        return f"f:{v!r}"
    if isinstance(v, bytes):
        return "b:" + esc(v)
    return "s:" + esc(v)


def s(text):
    return "s:" + esc(text)


def b(data):
    return "b:" + esc(data)


# 1. strings
j = Job("strings")
j.hs()
j.reply(OK).call("set s:greeting s:hello")
j.reply(bulk("hello")).call("get s:greeting")
j.reply(NIL).call("get s:missing")
j.reply(OK).call("set s:session s:abc ex=i:30 nx=T:")
j.reply(NIL).call("set s:session s:abc px=i:1500 xx=T: keepttl=T:")
j.reply(bulk("abc")).call("set s:session s:def get=T:")
j.reply(OK).call("set s:counter i:10 ex=s:15")
j.call("set s:counter i:10 ex=f:1.5")
j.call("set s:counter i:10 px=s:15")
j.reply(OK).call("set s:stamp s:x exat=i:1700000000 pxat=i:1700000000123")
j.reply(num(11)).call("incr s:counter")
j.reply(num(16)).call("incrby s:counter i:5")
j.reply(num(14)).call("decrby s:counter i:2")
j.reply(num(13)).call("decr s:counter")
j.reply(bulk("13.75")).call("incrbyfloat s:counter f:0.75")
j.reply(num(11)).call("append s:greeting s:%20world")
j.reply(bulk("lo wo")).call("getrange s:greeting i:3 i:7")
j.reply(num(11)).call("setrange s:greeting i:6 s:WORLD")
j.reply(num(11)).call("strlen s:greeting")
j.reply(bulk("hello WORLD")).call("getdel s:greeting")
j.reply(OK).call("setex s:tmp i:60 s:v")
j.reply(OK).call("psetex s:tmp i:60000 s:v")
j.reply(num(1)).call("setnx s:lock s:me")
j.reply(num(0)).call("setnx s:lock s:you")
j.reply(OK).call("mset { s:a s:1 s:b s:2 s:c i:3 }")
j.reply(num(0)).call("msetnx { s:a s:9 s:d s:4 }")
j.reply(arr(["1", "2", None, "4"])).call("mget [ s:a s:b s:x ] s:d")
j.reply(arr(["1"])).call("mget s:a")
j.reply(err("ERR wrong number of arguments for 'mget' command")).call("mget [ ]")
j.reply(bulk("v")).call("getex s:tmp ex=i:5 px=i:5")
j.call("getex s:tmp ex=i:5 px=i:6 exat=i:7")
j.call("getex s:tmp ex=i:5 persist=T:")
j.reply(bulk("v")).call("getex s:tmp persist=T:")
j.reply(bulk("mytext")).call("lcs s:k1 s:k2")
j.reply(num(6)).call("lcs s:k1 s:k2 len=T:")

# 2. encoding of arguments
j = Job("argument encoding")
j.hs()
j.reply(OK).call("set s:i i:-42")
j.reply(OK).call("set s:f f:1.5")
j.reply(OK).call("set s:f f:0.1")
j.reply(OK).call("set s:f f:1e-05")
j.reply(OK).call("set s:f f:1e+16")
j.reply(OK).call("set s:f f:3.0")
j.reply(OK).call("set s:f f:-0.0")
j.reply(OK).call("set s:f f:123456789.125")
j.reply(OK).call("set s:f f:inf")
j.reply(OK).call("set s:big i:12345678901234567")
j.call("set s:flag T:")
j.call("set s:none N:")
j.call("set s:list [ s:a ]")
j.reply(OK).call("set b:bin%00key b:%00%01%FF%7F")
j.reply(OK).call("set s:caf%C3%A9 s:na%C3%AFve%20%E2%98%95")
j.reply(OK).call("set s:quote s:it's%20%22quoted%22")
j.reply(OK).call("execute_command s:SET s:raw s:v")
j.reply(OK).call("execute_command b:SET%20EX b:x")
j.reply(simple("PONG")).call("execute_command s:ping")

# 3. a big value goes out in pieces
j = Job("big values")
j.hs()
j.reply(OK).call("set s:blob r:x*7000")
j.reply(bulk("y" * 6500)).call("get s:blob")
j.reply(OK).call("mset { s:a r:z*5990 s:b s:short }")

# 4. keys
j = Job("keys")
j.hs()
j.reply(num(2)).call("delete s:a s:b s:c")
j.reply(num(1)).call("exists s:a")
j.reply(num(1)).call("expire s:a i:100")
j.reply(num(0)).call("expire s:a i:100 nx=T: xx=T: gt=T: lt=T:")
j.reply(num(1)).call("pexpire s:a i:2500 gt=T:")
j.reply(num(97)).call("ttl s:a")
j.reply(num(-2)).call("pttl s:gone")
j.reply(simple("string")).call("type s:a")
j.reply(simple("none")).call("type s:gone")
j.reply(OK).call("rename s:a s:a2")
j.reply(err("ERR no such key")).call("rename s:gone s:x")
j.reply(num(0)).call("renamenx s:a2 s:b")
j.reply(arr(["user:1", "user:2", "user:10"])).call("keys s:user:*")
j.reply(arr(["0", ["k1", "k2"]])).call("scan")
j.reply(arr(["17", ["user:1"]])).call("scan i:0 match=s:user:* count=i:100 _type=s:string")
j.reply(num(1)).call("copy s:a2 s:a3 destination_db=i:2 replace=T:")
j.reply(num(1)).call("persist s:a2")
j.reply(num(3)).call("unlink s:x s:y s:z")
j.reply(num(2)).call("touch s:x s:y")
j.reply(bulk("user:2")).call("randomkey")
j.reply(NIL).call("randomkey")
j.reply(bulk("embstr")).call("object s:encoding s:a2")
j.reply(num(5)).call("object s:refcount s:a2")

# 5. sort
j = Job("sort")
j.hs()
j.reply(arr(["3", "1", "2"])).call("sort s:ids")
j.reply(arr(["c", "b", "a"])).call("sort s:ids by=s:weight_* desc=T: alpha=T: start=i:0 num=i:3")
j.reply(arr(["alice", "30", "bob", "25"])).call("sort s:ids get=[ s:name_* s:age_* ] groups=T:")
j.call("sort s:ids get=s:name_* groups=T:")
j.call("sort s:ids start=i:2")
j.reply(num(3)).call("sort s:ids get=s:# store=s:sorted")
j.reply(arr([])).call("sort s:empty get=[ s:a s:b ] groups=T:")

# 6. hashes
j = Job("hashes")
j.hs()
j.reply(num(1)).call("hset s:user:1 s:name s:Ada")
j.reply(num(2)).call("hset s:user:1 mapping={ s:age i:36 s:lang s:en }")
j.reply(num(2)).call("hset s:user:1 s:k s:v items=[ s:x s:1 s:y s:2 ] mapping={ s:z s:3 }")
j.call("hset s:user:1")
j.reply(bulk("Ada")).call("hget s:user:1 s:name")
j.reply(arr(["name", "Ada", "age", "36", "lang", "en"])).call("hgetall s:user:1")
j.reply(arr([])).call("hgetall s:nobody")
j.reply(arr(["Ada", None])).call("hmget s:user:1 [ s:name s:email ]")
j.reply(arr(["Ada", "36"])).call("hmget s:user:1 s:name s:age")
j.reply(num(1)).call("hdel s:user:1 s:lang s:none")
j.reply(num(37)).call("hincrby s:user:1 s:age")
j.reply(bulk("37.5")).call("hincrbyfloat s:user:1 s:age f:0.5")
j.reply(arr(["name", "age"])).call("hkeys s:user:1")
j.reply(arr(["Ada", "37.5"])).call("hvals s:user:1")
j.reply(num(2)).call("hlen s:user:1")
j.reply(num(1)).call("hexists s:user:1 s:name")
j.reply(num(0)).call("hsetnx s:user:1 s:name s:Bob")
j.reply(arr(["age", "37.5", "name", "Ada"])).call("hrandfield s:user:1 count=i:2 withvalues=T:")
j.reply(num(3)).call("hstrlen s:user:1 s:name")
j.reply(arr(["0", ["name", "Ada", "age", "37.5"]])).call("hscan s:user:1 match=s:* count=i:10")
j.reply(arr(["0", ["name", "age"]])).call("hscan s:user:1 no_values=T:")
j.reply(arr(["0", ["name", "age"]])).call("hscan s:user:1 no_values=F:")
j.reply(arr(["0", []])).call("hscan s:empty")

# 7. lists
j = Job("lists")
j.hs()
j.reply(num(3)).call("lpush s:q s:a s:b s:c")
j.reply(num(5)).call("rpush s:q i:1 f:2.5")
j.reply(bulk("c")).call("lpop s:q")
j.reply(arr(["b", "a"])).call("lpop s:q count=i:2")
j.reply(NIL).call("rpop s:empty")
j.reply(arr(["2.5"])).call("rpop s:q i:1")
j.reply(arr(["1"])).call("lrange s:q i:0 i:-1")
j.reply(num(1)).call("llen s:q")
j.reply(bulk("1")).call("lindex s:q i:0")
j.reply(OK).call("lset s:q i:0 s:one")
j.reply(err("ERR index out of range")).call("lset s:q i:9 s:x")
j.reply(OK).call("ltrim s:q i:0 i:99")
j.reply(arr(["q", "one"])).call("blpop [ s:q s:r ] timeout=i:1")
j.reply(NIL_ARR).call("brpop s:q timeout=N:")
j.reply(num(2)).call("lpos s:q s:x")
j.reply(arr([2, 6])).call("lpos s:q s:x rank=i:-1 count=i:2 maxlen=i:100")
j.reply(bulk("one")).call("lmove s:q s:r")
j.reply(bulk("one")).call("lmove s:q s:r s:RIGHT s:LEFT")
j.reply(num(4)).call("linsert s:q s:BEFORE s:one s:zero")
j.reply(num(2)).call("lrem s:q i:0 s:x")

# 8. sets
j = Job("sets")
j.hs()
j.reply(num(3)).call("sadd s:tags s:red s:green s:blue")
j.reply(num(1)).call("srem s:tags s:green")
j.reply(arr(["red", "blue"])).call("smembers s:tags")
j.reply(arr([])).call("smembers s:none")
j.reply(num(1)).call("sismember s:tags s:red")
j.reply(arr([1, 0])).call("smismember s:tags [ s:red s:pink ]")
j.reply(num(2)).call("scard s:tags")
j.reply(arr(["red"])).call("sinter [ s:tags s:warm ]")
j.reply(arr(["red", "blue", "orange"])).call("sunion s:tags s:warm")
j.reply(arr(["blue"])).call("sdiff s:tags s:warm")
j.reply(bulk("blue")).call("spop s:tags")
j.reply(arr(["red"])).call("spop s:tags count=i:0")
j.reply(arr(["red", "red"])).call("srandmember s:tags i:-2")
j.reply(arr(["0", ["red"]])).call("sscan s:tags match=s:r*")
j.reply(num(1)).call("smove s:tags s:warm s:red")

# 9. sorted sets
j = Job("sorted sets")
j.hs()
j.reply(num(3)).call("zadd s:board { s:ada i:10 s:bob f:7.5 s:cy i:12 }")
j.call("zadd s:board { s:ada i:1 } nx=T: xx=T:")
j.call("zadd s:board { s:ada i:1 } gt=T: lt=T:")
j.call("zadd s:board { s:ada i:1 s:bob i:2 } incr=T:")
j.call("zadd s:board { s:ada i:1 } nx=T: gt=T:")
j.call("zadd s:board { }")
j.reply(bulk("11")).call("zadd s:board { s:ada i:1 } incr=T:")
j.reply(NIL).call("zadd s:board { s:ada i:1 } incr=T: xx=T: lt=T:")
j.reply(num(1)).call("zadd s:board { s:dee i:3 } ch=T: xx=T: gt=T:")
j.reply(arr(["bob", "ada", "cy"])).call("zrange s:board i:0 i:-1")
j.reply(arr(["bob", "7.5", "ada", "11", "cy", "12"])).call("zrange s:board i:0 i:-1 withscores=T:")
j.reply(arr(["cy", "12", "ada", "11"])).call("zrange s:board i:0 i:1 desc=T: withscores=T:")
j.reply(arr(["ada", "cy"])).call("zrange s:board s:(8 s:+inf byscore=T: offset=i:0 num=i:2")
j.reply(arr(["cy", "ada"])).call("zrange s:board s:+inf s:(8 byscore=T: desc=T: offset=i:0 num=i:2")
j.call("zrange s:board i:0 i:1 byscore=T: bylex=T:")
j.call("zrange s:board s:[a s:[z bylex=T: withscores=T:")
j.call("zrange s:board i:0 i:1 offset=i:1")
j.reply(arr(["ada", "11"])).call("zrangebyscore s:board s:-inf i:11 start=i:0 num=i:1 withscores=T:")
j.call("zrangebyscore s:board i:0 i:1 start=i:0")
j.reply(arr(["cy", "ada"])).call("zrevrange s:board i:0 i:1")
j.reply(bulk("7.5")).call("zscore s:board s:bob")
j.reply(NIL).call("zscore s:board s:nobody")
j.reply(bulk("inf")).call("zscore s:board s:infinite")
j.reply(bulk("-inf")).call("zscore s:board s:neg")
j.reply(bulk("9.5")).call("zincrby s:board f:2.0 s:bob")
j.reply(num(0)).call("zrank s:board s:bob")
j.reply(arr([0, "9.5"])).call("zrank s:board s:bob withscore=T:")
j.reply(NIL).call("zrank s:board s:nobody")
j.reply(num(1)).call("zrem s:board s:dee")
j.reply(num(3)).call("zcard s:board")
j.reply(num(2)).call("zcount s:board s:(9 s:+inf")
j.reply(arr(["bob", "9.5"])).call("zpopmin s:board")
j.reply(arr(["ada", "11", "cy", "12"])).call("zpopmin s:board i:2")
j.reply(arr([])).call("zpopmin s:empty")
j.reply(arr(["11", None])).call("zmscore s:board [ s:ada s:x ]")
j.call("zmscore s:board [ ]")
j.reply(arr(["0", ["ada", "11", "cy", "12"]])).call("zscan s:board")
j.reply(arr(["0", ["ada", "11"]])).call("zscan s:board score_cast_func=c:int")
j.reply(arr(["0", ["ada", "11.5"]])).call("zscan s:board score_cast_func=c:int")
j.reply(arr(["ada", "11"])).call("zrange s:board i:0 i:0 withscores=T: score_cast_func=c:int")
j.reply(num(4)).call("zunionstore s:out [ s:a s:b ]")
j.reply(num(4)).call("zunionstore s:out { s:a i:2 s:b f:0.5 } aggregate=s:max")
j.call("zunionstore s:out [ s:a ] aggregate=s:avg")

# 10. streams
j = Job("streams")
j.hs()
j.reply(bulk("1700000000000-0")).call("xadd s:events { s:type s:login s:user s:ada }")
j.reply(bulk("1700000000001-0")).call("xadd s:events { s:type s:logout } maxlen=i:1000")
j.reply(bulk("1700000000002-0")).call("xadd s:events { s:t i:1 } maxlen=i:10 approximate=F: limit=i:5 nomkstream=T: id=s:1700000000002-0")
j.reply(NIL).call("xadd s:events { s:t i:2 } minid=s:1699999999999-0 nomkstream=T:")
j.call("xadd s:events { s:t i:1 } maxlen=i:10 minid=s:0")
j.call("xadd s:events { }")
j.call("xadd s:events { s:t i:1 } maxlen=i:-1")
entries = [["1700000000000-0", ["type", "login", "user", "ada"]], ["1700000000001-0", ["type", "logout"]]]
j.reply(arr(entries)).call("xrange s:events")
j.reply(arr(entries[:1])).call("xrange s:events min=s:- max=s:+ count=i:1")
j.call("xrange s:events count=i:0")
j.reply(arr(entries[::-1])).call("xrevrange s:events")
j.reply(arr([["events", entries], ["audit", [["5-0", ["k", "v"]]]]])).call("xread { s:events s:0 s:audit s:$ } count=i:10 block=i:100")
j.reply(NIL_ARR).call("xread { s:events s:$ } block=i:0")
j.call("xread { s:events s:$ } block=i:-1")
j.call("xread { }")
j.reply(OK).call("xgroup_create s:events s:workers id=s:0 mkstream=T: entries_read=i:2")
j.reply(err("BUSYGROUP Consumer Group name already exists")).call("xgroup_create s:events s:workers")
j.reply(arr([["events", [entries[0], ["1700000000001-0", None]]]])).call("xreadgroup s:workers s:w1 { s:events s:> } count=i:2 noack=T:")
j.reply(num(1)).call("xack s:events s:workers s:1700000000000-0")
j.reply(num(2)).call("xlen s:events")
info = ["length", 2, "radix-tree-keys", 1, "groups", 1, "last-generated-id", "1700000000001-0",
        "first-entry", entries[0], "last-entry", entries[1]]
j.reply(arr(info)).call("xinfo_stream s:events")
info2 = ["length", 0, "groups", 0, "first-entry", None, "last-entry", None]
j.reply(arr(info2)).call("xinfo_stream s:empty")
full = ["length", 2, "entries", entries, "groups",
        [["name", "workers", "pel-count", 1,
          "consumers", [["name", "w1", "seen-time", 1700000000500, "pel-count", 1]]]]]
j.reply(arr(full)).call("xinfo_stream s:events full=T:")
j.reply(arr([["name", "workers", "consumers", 1, "pending", 1, "last-delivered-id", "1700000000001-0"]])).call("xinfo_groups s:events")
j.reply(arr([1, "1700000000001-0", "1700000000001-0", [["w1", "1"]]])).call("xpending s:events s:workers")
j.reply(arr([0, None, None, None])).call("xpending s:events s:idle")
j.reply(arr([["1700000000001-0", "w1", 4200, 1]])).call("xpending_range s:events s:workers s:- s:+ i:10")
j.reply(arr([])).call("xpending_range s:events s:workers s:- s:+ i:10 consumername=s:w1 idle=i:1000")
j.reply(arr([1, "1700000000001-0", "1700000000001-0", [["w1", "1"]]])).call("xpending_range s:events s:workers N: N: N:")
j.call("xpending_range s:events s:workers N: N: N: idle=i:5")
j.call("xpending_range s:events s:workers s:- N: i:10")
j.call("xpending_range s:events s:workers s:- s:+ i:-1")
j.reply(num(0)).call("xtrim s:events maxlen=i:100")
j.reply(num(1)).call("xtrim s:events minid=s:1700000000001-0 approximate=F: limit=i:10")
j.call("xtrim s:events")
j.reply(num(1)).call("xdel s:events s:1700000000000-0")
j.reply(arr([entries[1]])).call("xclaim s:events s:workers s:w2 i:1000 [ s:1700000000001-0 ] idle=i:5 time=i:1700000000999 retrycount=i:3 force=T:")
j.reply(arr(["1700000000001-0"])).call("xclaim s:events s:workers s:w2 i:1000 [ s:1700000000001-0 ] justid=T:")
j.call("xclaim s:events s:workers s:w2 i:-1 [ s:1-0 ]")
j.call("xclaim s:events s:workers s:w2 i:5 [ ]")
j.reply(arr(["0-0", [entries[1]], []])).call("xautoclaim s:events s:workers s:w2 i:1000 count=i:10")
j.reply(arr(["0-0", ["1700000000001-0"], []])).call("xautoclaim s:events s:workers s:w2 i:1000 justid=T:")
j.call("xautoclaim s:events s:workers s:w2 i:1000 count=i:-1")
j.call("xautoclaim s:events s:workers s:w2 i:-5")

# 11. server introspection
INFO = """# Server
redis_version:7.4.1
redis_mode:standalone
os:Linux 6.1.0 x86_64
arch_bits:64
uptime_in_seconds:86400
hz:10
executable:/usr/local/bin/redis-server

# Clients
connected_clients:3
maxmemory_policy:noeviction
mem_fragmentation_ratio:1.25

# Keyspace
db0:keys=12,expires=3,avg_ttl=0,subexpiry=0
db2:keys=1,expires=0,avg_ttl=0

# Commandstats
cmdstat_get:calls=40,usec=120,usec_per_call=3.00,rejected_calls=0,failed_calls=0
cmdstat_host:calls=1,usec=2
module:name=search,ver=21005,api=1,filters=0,usedby=[],using=[],options=[handle-io-errors]
module:name=ReJSON,ver=20609,api=1
listener0:name=tcp,bind=*,bind=-::*,port=6379
errorstat_ERR:count=2
latency_percentiles_usec_get:p50=1.003,p99=3.007,p99.9=10.015
loglevel:notice
tags:a,b,,c
weird line without colon
"""
j = Job("server")
j.hs()
j.reply(bulk(INFO)).call("info")
j.reply(bulk("# Keyspace\r\ndb0:keys=1,expires=0\r\n")).call("info s:keyspace")
j.reply(bulk("x:1\r\n")).call("info s:cpu s:memory")
j.reply(arr(["maxmemory", "0", "maxmemory-policy", "noeviction"])).call("config_get s:maxmemory*")
j.reply(arr([])).call("config_get s:nothing*")
j.reply(OK).call("config_set s:maxmemory s:100mb")
j.reply(simple("PONG")).call("ping")
j.reply(bulk("hi")).call("echo s:hi")
j.reply(num(12)).call("dbsize")
j.reply(arr(["1700000000", "123456"])).call("time")
CL = ("id=3 addr=127.0.0.1:50000 laddr=127.0.0.1:6379 fd=8 name= age=10 idle=0 flags=N db=0 "
      "sub=0 psub=0 multi=-1 qbuf=26 qbuf-free=20448 argv-mem=10 obl=0 oll=0 omem=0 tot-mem=22298 "
      "events=r cmd=client|list user=default lib-name=redis-py lib-ver=5.2.1\n"
      "id=4 addr=127.0.0.1:50002 laddr=127.0.0.1:6379 fd=9 name=worker=1 age=5 idle=5 flags=N db=2 "
      "sub=0 psub=0 multi=-1 qbuf=0 qbuf-free=0 argv-mem=0 obl=0 oll=0 omem=0 tot-mem=1800 "
      "events=r cmd=get user=default lib-name= lib-ver=\n")
j.reply(bulk(CL)).call("client_list")
j.reply(bulk(CL.split("\n")[0] + "\n")).call("client_list _type=s:normal client_id=[ s:3 s:4 ]")
j.call("client_list _type=s:bogus")
j.call("client_list client_id=s:3")
j.reply(bulk(CL.split("\n")[0] + "\n")).call("client_info")
j.reply(OK).call("client_setname s:worker")
j.reply(bulk("worker")).call("client_getname")
j.reply(NIL).call("client_getname")
j.reply(num(2)).call("client_kill_filter _type=s:NORMAL skipme=T: _id=i:3 addr=s:127.0.0.1:1 laddr=s:127.0.0.1:6379 user=s:bob maxage=i:60")
j.reply(OK).call("client_kill_filter skipme=F:")
j.call("client_kill_filter _type=s:replica")
j.call("client_kill_filter skipme=i:1")
j.call("client_kill_filter")
slow = [[14, "1700000000", 15000, ["KEYS", "*"], "127.0.0.1:50000", "worker"],
        [13, "1699999999", 12000, 42, ["SORT", "big"]]]
j.reply(arr(slow)).call("slowlog_get i:2")
j.reply(OK).call("execute_command s:SLOWLOG%20RESET")
j.reply(simple("Value at:0x7f00 refcount:1 encoding:embstr serializedlength:4 lru:123 lru_seconds_idle:7")).call("debug_object s:k")
acl = ["flags", ["on", "allkeys"], "passwords", ["5e88"], "commands", "+@all -debug -@dangerous",
       "keys", "~app:* ~cache:*", "channels", "&*", "selectors", [["commands", "-@all +get", "keys", "~x", "channels", ""]]]
j.reply(arr(acl)).call("acl_getuser s:app")
j.reply(arr(["flags", ["off"], "passwords", [], "commands", "-@all", "keys", "", "channels", ""])).call("acl_getuser s:off")
j.reply(NIL).call("acl_getuser s:nobody")
log = [["count", 1, "reason", "auth", "context", "toplevel", "object", "AUTH", "username", "bob",
        "age-seconds", "4.096", "client-info",
        "id=5 addr=127.0.0.1:50004 laddr=127.0.0.1:6379 fd=10 name= age=0 idle=0 flags=N db=0 sub=0 psub=0 ssub=0 multi=-1 qbuf=48 qbuf-free=20426 argv-mem=25 multi-mem=0 rbs=1024 rbp=0 obl=0 oll=0 omem=0 tot-mem=22322 events=r cmd=auth user=default redir=-1 resp=2"]]
j.reply(arr(log)).call("acl_log count=i:1")
j.reply(OK).call("acl_log")
j.call("acl_log count=s:1")
j.reply(OK).call("flushdb asynchronous=T:")
j.reply(OK).call("swapdb i:0 i:1")
mem = ["peak.allocated", 1048576, "total.allocated", 900000, "db.0", ["overhead.hashtable.main", 72, "overhead.hashtable.expires", 32],
       "fragmentation", "1.5", "keys.count", 3]
j.reply(arr(mem)).call("memory_stats")
j.reply(arr([["name", "search", "ver", 21005], ["name", "ReJSON", "ver", 20609]])).call("module_list")
nodes = ("07c37dfeb235213a872192d90877d0cd55635b91 127.0.0.1:30004@31004,host4.example hostname slave "
         "e7d1eecce10fd6bb5eb35b9f99a514335d9ba9ca 0 1426238317239 4 connected\n"
         "e7d1eecce10fd6bb5eb35b9f99a514335d9ba9ca 127.0.0.1:30001@31001 myself,master - 0 0 1 connected 0-5460 [5461->-292f8b] [93-<-8ab1]\n"
         "292f8b365bb7edb5e285caf0b7e6ddc7265d2f4f 127.0.0.1:30003@31003 master - 0 1426238318243 3 connected 10923-16383 7")
j.reply(bulk(nodes)).call("execute_command s:CLUSTER%20NODES")
j.reply(bulk("cluster_state:ok\r\ncluster_slots_assigned:16384\r\ncluster_known_nodes:6\r\n")).call("execute_command s:CLUSTER%20INFO")
cmd = [["get", 2, ["readonly", "fast"], 1, 1, 1, ["@read", "@string"], [], [], []],
       ["ping", -1, ["fast"], 0, 0, 0]]
j.reply(arr(cmd)).call("execute_command s:COMMAND")
j.reply(arr(["matches", [[[4, 7], [5, 8]], [[2, 3], [0, 1]]], "len", 6])).call("execute_command s:STRALGO s:LCS s:IDX idx=T:")
j.reply(arr(["matches", [[[4, 7], [5, 8], 4]], "len", 6])).call("execute_command s:STRALGO s:LCS s:IDX idx=T: withmatchlen=T:")
j.reply(num(6)).call("execute_command s:STRALGO s:LCS s:LEN len=T:")
j.reply(bulk("ab")).call("execute_command s:STRALGO s:LCS")
sm = ["name", "mymaster", "ip", "10.0.0.1", "port", "6379", "flags", "master", "num-slaves", "2",
      "quorum", "2", "down-after-milliseconds", "notanint", "last-ping-reply", "120"]
j.reply(arr([sm])).call("execute_command s:SENTINEL%20MASTERS")
j.reply(arr(sm[:8] + ["flags", "s_down,master,disconnected"])).call("execute_command s:SENTINEL%20MASTER s:mymaster")
j.reply(arr(["10.0.0.1", "6379"])).call("sentinel_get_master_addr_by_name s:mymaster")
j.reply(NIL_ARR).call("sentinel_get_master_addr_by_name s:none")
j.reply(arr([sm[:8]])).call("execute_command s:SENTINEL%20SLAVES s:mymaster")
j.reply(simple("RESET")).call("execute_command s:RESET")
j.reply(arr(["127.0.0.1", "6380"])).call("execute_command s:GEOHASH")
j.reply(num(1426238317)).call("execute_command s:CLIENT%20UNBLOCK i:5")
j.reply(arr(["read", "write"])).call("execute_command s:ACL%20CAT")
j.reply(bulk("ab12")).call("execute_command s:ACL%20GENPASS")
j.reply(num(1)).call("execute_command s:MODULE%20UNLOAD s:x")
j.reply(simple("Background saving started")).call("execute_command s:BGSAVE")

# 12. geo
j = Job("geo")
j.hs()
j.reply(num(2)).call("geoadd s:places [ f:13.361389 f:38.115556 s:Palermo f:15.087269 f:37.502669 s:Catania ]")
j.reply(num(0)).call("geoadd s:places [ f:13.361389 f:38.115556 s:Palermo ] xx=T: ch=T:")
j.call("geoadd s:places [ f:1.0 f:2.0 s:x ] nx=T: xx=T:")
j.call("geoadd s:places [ f:1.0 f:2.0 ]")
j.reply(arr([["13.36138933897018433", "38.11555639549629859"], None])).call("geopos s:places s:Palermo s:Nowhere")
j.reply(bulk("166.2742")).call("geodist s:places s:Palermo s:Catania unit=s:km")
j.reply(NIL).call("geodist s:places s:Palermo s:Nowhere")
j.call("geodist s:places s:a s:b unit=s:yd")
j.reply(arr(["sqc8b49rny0", "sqdtr74hyu0"])).call("geohash s:places s:Palermo s:Catania")
res = [["Palermo", "190.4424", 3479099956230698, ["13.36138933897018433", "38.11555639549629859"]],
       ["Catania", "56.4413", 3479447370796909, ["15.08726745843887329", "37.50266842333162032"]]]
j.reply(arr(res)).call("geosearch s:places longitude=i:15 latitude=i:37 radius=i:200 unit=s:km withdist=T: withcoord=T: withhash=T: sort=s:asc count=i:2 any=T:")
j.reply(arr([[r[0], r[1]] for r in res])).call("geosearch s:places member=s:Palermo radius=i:300 unit=s:KM withdist=T:")
j.reply(arr(["Palermo", "Catania"])).call("geosearch s:places member=s:Palermo longitude=i:0 latitude=i:0 width=i:400 height=i:400 unit=s:km")
j.reply(arr(["Catania"])).call("geosearch s:places longitude=i:15 latitude=i:37 radius=i:100 unit=s:km")
j.call("geosearch s:places radius=i:5")
j.call("geosearch s:places member=s:Palermo longitude=i:5 latitude=i:5 radius=i:5")
j.call("geosearch s:places member=s:Palermo")
j.call("geosearch s:places member=s:Palermo radius=i:5 unit=s:yd")
j.call("geosearch s:places member=s:Palermo radius=i:5 width=i:2 height=i:2")
j.call("geosearch s:places member=s:Palermo radius=i:5 sort=s:up")
j.call("geosearch s:places member=s:Palermo radius=i:5 any=T:")
j.reply(arr([["Palermo", "190.4424"]])).call("georadius s:places i:15 i:37 i:200 unit=s:km withdist=T: count=i:1 sort=s:DESC")
j.reply(num(2)).call("georadius s:places i:15 i:37 i:200 store=s:near")
j.call("georadius s:places i:15 i:37 i:200 unit=s:yd")
j.call("georadius s:places i:15 i:37 i:200 any=T:")
j.call("georadius s:places i:15 i:37 i:200 sort=s:asc")
j.call("georadius s:places i:15 i:37 i:200 store=s:a store_dist=s:b")

# 13. scripts, pub/sub, bits, hyperloglog
j = Job("scripts and pubsub")
j.hs()
j.reply(arr([1, 2, ["nested", None]])).call("eval s:return%20{1,2,{'nested',false}} i:0")
j.reply(bulk("v")).call("eval s:return%20redis.call('get',KEYS[1]) i:1 s:k s:extra")
j.reply(err("NOSCRIPT No matching script. Please use EVAL.")).call("evalsha s:e0e1f9fabfc9d4800c877a703b823ac0578ff8db i:0")
j.reply(bulk("e0e1f9fabfc9d4800c877a703b823ac0578ff8db")).call("script_load s:return%201")
j.reply(arr([1, 0])).call("script_exists s:e0e1 s:ffff")
j.reply(num(3)).call("publish s:news s:hello")
j.reply(arr(["news", 3, "sport", 0])).call("pubsub_numsub s:news s:sport")
j.reply(arr(["news"])).call("pubsub_channels")
j.reply(num(0)).call("setbit s:bits i:7 i:5")
j.reply(num(1)).call("setbit s:bits i:7 s:")
j.reply(num(1)).call("getbit s:bits i:7")
j.reply(num(4)).call("bitcount s:bits")
j.reply(num(2)).call("bitcount s:bits i:0 i:1 mode=s:BIT")
j.call("bitcount s:bits i:0")
j.reply(num(1)).call("bitop s:AND s:dest s:a s:b")
j.reply(num(7)).call("bitpos s:bits i:1 i:0")
j.reply(num(7)).call("bitpos s:bits i:1 i:0 i:-1 mode=s:BYTE")
j.call("bitpos s:bits i:2")
j.call("bitpos s:bits i:1 end=i:3")
j.reply(arr([1, 0, 255])).bitfield("s:bits | incrby s:u8 s:#0 i:1 | get s:i4 i:0 | set s:u8 i:8 i:255 | execute")
j.reply(arr([None, 3])).bitfield("s:bits default_overflow=s:fail | incrby s:u2 i:100 i:1 | overflow s:sat | incrby s:u2 i:102 i:1 overflow=s:Wrap | execute")
j.bitfield("s:bits default_overflow=s:WRAP | overflow s:wrap | get s:u8 i:0")
j.reply(num(1)).call("pfadd s:visits s:a s:b s:c")
j.reply(num(3)).call("pfcount s:visits")
j.reply(OK).call("pfmerge s:all s:visits s:other")

# 14. errors from the server
j = Job("server errors")
j.hs()
j.reply(err("WRONGTYPE Operation against a key holding the wrong kind of value")).call("get s:list")
j.reply(err("ERR value is not an integer or out of range")).call("incr s:name")
j.reply(err("NOSCRIPT No matching script")).call("evalsha s:abc i:0")
j.reply(err("READONLY You can't write against a read only replica.")).call("set s:a s:b")
j.reply(err("NOPERM User bob has no permissions to run the 'flushall' command")).call("execute_command s:FLUSHALL")
j.reply(err("OOM command not allowed when used memory > 'maxmemory'.")).call("set s:a s:b")
j.reply(err("EXECABORT Transaction discarded because of previous errors.")).call("execute_command s:EXEC")
j.reply(err("ERR Error loading the extension. Please check the server logs.")).call("execute_command s:MODULE%20LOAD s:x.so")
j.reply(err("ERR unknown command 'FOO', with args beginning with: ")).call("execute_command s:FOO")
j.reply(err("NOAUTH Authentication required.")).call("get s:a")
j.hs()
j.reply(err("LOADING Redis is loading the dataset in memory")).call("get s:a")
j.hs()
j.reply(err("ERR max number of clients reached")).call("get s:a")
j.hs()
j.reply(err("ERR")).call("get s:a")
j.reply(err("")).call("get s:a")
j.reply(b"?what\r\n").call("get s:a")
j.hs()
j.reply(b":12x\r\n").call("incr s:a")
j.hs()
j.reply(OK).call("ping")
j.reply(simple("PONGISH")).call("ping")

# 15. responses decoded to str
j = Job("decoded responses", decode=True)
j.hs()
j.reply(bulk("café")).call("get s:k")
j.reply(arr(["a", ["b", 3], None])).call("execute_command s:CUSTOM")
j.reply(bulk(b"\xffbad")).call("get s:bin")
j.hs()
j.reply(bulk(b"ok\xe2\x82")).call("get s:cut")
j.hs()
j.reply(bulk(b"x\xe2\x28\xa1")).call("get s:mid")
j.hs()
j.reply(arr(["name", "Ada", "age", "36"])).call("hgetall s:u")
j.reply(arr(["a", "b"])).call("smembers s:s")
j.reply(arr([[14, "1700000000", 15000, ["KEYS", "*"], "127.0.0.1:50000", "worker"]])).call("slowlog_get")
j.reply(simple("PONG")).call("ping")
j.reply(err("WRONGTYPE bad é")).call("get s:x")

# 16. str_if_bytes replaces bad UTF-8
j = Job("replacement characters")
j.hs()
j.reply(bulk(b"id=1 addr=x name=caf\xe9 age=1\n")).call("client_list")
j.reply(arr([bulk(b"a\xffb"), "1"])).call("config_get s:x")
j.reply(simple("ok")).call("script_load s:x")
j.reply(bulk(b"\xf0\x9f\x98")).call("script_load s:y")
j.reply(bulk(b"\xed\xa0\x80z")).call("script_load s:z")
j.reply(bulk(b"\xc0\xafq\xf8\x80")).call("script_load s:w")

# 17. RESP3
j = Job("resp3 types", proto=3)
j.reply(hello3())
j.hs()
j.reply(OK).call("set s:a s:1")
j.reply(bulk("1")).call("get s:a")
j.reply(NULL3).call("get s:missing")
j.reply(dbl("3.14")).call("execute_command s:CUSTOM")
j.reply(dbl("inf")).call("execute_command s:CUSTOM")
j.reply(dbl("-1e10")).call("execute_command s:CUSTOM")
j.reply(dbl("nan")).call("execute_command s:CUSTOM")
j.reply(boolean(True)).call("execute_command s:CUSTOM")
j.reply(boolean(False)).call("execute_command s:CUSTOM")
j.reply(big("3492890328409238509324850943850943825024385")).call("execute_command s:CUSTOM")
j.reply(big("-12")).call("execute_command s:CUSTOM")
j.reply(verbatim("txt", "Some string")).call("execute_command s:CUSTOM")
j.reply(set3(["b", "a", "c"])).call("smembers s:s")
j.reply(set3([])).call("smembers s:none")
j.reply(map3([("name", "Ada"), ("age", "36")])).call("hgetall s:u")
j.reply(map3([])).call("hgetall s:none")
j.reply(arr([["bob", dbl("7.5")], ["ada", dbl("11")]])).call("zrange s:board i:0 i:-1 withscores=T:")
j.reply(dbl("7.5")).call("zscore s:board s:bob")
j.reply(arr(["ada", dbl("11")])).call("zpopmin s:board")
j.reply(map3([("events", [["1-0", ["a", "1"]]]), ("audit", [["2-0", ["b", "2"]]])])).call("xread { s:events s:0 s:audit s:0 }")
j.reply(NULL3).call("xread { s:events s:$ } block=i:10")
j.reply(map3([("events", [["1-0", ["a", "1"]]])])).call("xreadgroup s:g s:c { s:events s:> }")
j.reply(map3([("maxmemory", "0"), ("appendonly", "no")])).call("config_get s:*")
j.reply(push(["message", "news", "hello"]) + bulk("v")).call("get s:a")
j.reply(push(["invalidate", ["a"]]) + num(5)).call("incr s:n")
j.reply(push(["pmessage", "n*", "news", "x"]) + push(["message", "a", "b"]) + OK).call("set s:a s:2")
j.reply(b"|1\r\n+key-popularity\r\n%0\r\n" + bulk("v")).call("get s:a")
j.hs(0)
j.reply(hello3())
j.hs()
j.reply(blob_err("SYNTAX invalid syntax")).call("execute_command s:CUSTOM")
j.reply(blob_err("NOSCRIPT x")).call("execute_command s:CUSTOM")
cmd3 = [["get", 2, set3(["readonly", "fast"]), 1, 1, 1, set3(["@read"]), [], [map3([("flags", set3(["RO"]))])], []]]
j.reply(arr(cmd3)).call("execute_command s:COMMAND")
j.reply(arr([map3([("count", 1), ("reason", "auth"), ("age-seconds", dbl("4.5"))])])).call("acl_log")
j.reply(OK).call("acl_log")
j.reply(map3([("len", 6), ("matches", [])])).call("execute_command s:STRALGO s:LCS s:IDX")
j.reply(bulk("ab")).call("execute_command s:STRALGO s:LCS")
j.reply(arr([map3([("name", "workers"), ("pending", 1)])])).call("xinfo_groups s:events")
j.reply(arr([map3([("name", "w1"), ("pending", 0)])])).call("execute_command s:XINFO%20CONSUMERS s:events s:workers")
j.reply(map3([("length", 1), ("first-entry", ["1-0", ["a", "1"]]), ("last-entry", ["1-0", ["a", "1"]])])).call("xinfo_stream s:events")
j.reply(map3([("length", 1), ("entries", [["1-0", ["a", "1"]]]), ("groups", [map3([("name", "g")])])])).call("xinfo_stream s:events full=T:")
j.reply(map3([("name", "mymaster"), ("port", "6379"), ("quorum", "2"), ("flags", "master,s_down"), ("ip", "10.0.0.1")])).call("execute_command s:SENTINEL%20MASTER s:mymaster")
j.reply(map3([("peak.allocated", 100), ("db.0", map3([("overhead.hashtable.main", 72)]))])).call("memory_stats")
j.reply(map3([("flags", ["on"]), ("passwords", []), ("commands", "+@all"), ("keys", "~*"), ("channels", "&*"), ("selectors", [map3([("commands", "+get"), ("keys", "~a")])])])).call("acl_getuser s:app")
j.reply(arr([dbl("1.5"), NULL3])).call("zmscore s:board [ s:a s:b ]")
j.reply(bulk("1.5")).call("geodist s:p s:a s:b")

j = Job("resp3 null bulk", proto=3)
j.reply(hello3())
j.hs()
j.reply(NIL).call("get s:a")

j = Job("resp3 handshake", proto=3, decode=True)
j.reply(hello3())
j.hs()
j.reply(map3([("a", "1")])).call("hgetall s:h")
j.reply(set3(["x", "y"])).call("smembers s:s")

j = Job("resp3 wrong version", proto=3)
j.reply(hello3(2))
j.call("get s:a")
j.reply(err("NOPROTO unsupported protocol version"))
j.call("get s:a")

j = Job("resp3 with password", proto=3, password="s3cret")
j.reply(hello3())
j.hs()
j.reply(OK).call("ping")

j = Job("resp3 with username", proto=3, username="app", password="s3cret", client_name="worker-1", db=2)
j.reply(hello3())
j.reply(OK)
j.hs()
j.reply(OK)
j.reply(simple("PONG")).call("ping")

# 18. connection set-up
j = Job("auth", password="s3cret")
j.reply(OK)
j.hs()
j.reply(simple("PONG")).call("ping")

j = Job("auth with username", username="app", password="s3cret")
j.reply(OK)
j.hs()
j.reply(simple("PONG")).call("ping")

j = Job("auth fallback", username="app", password="s3cret")
j.reply(err("ERR wrong number of arguments for 'auth' command"))
j.reply(OK)
j.hs()
j.reply(simple("PONG")).call("ping")

j = Job("auth refused", password="nope")
j.reply(err("WRONGPASS invalid username-password pair or user is disabled."))
j.call("ping")
j.reply(simple("NOTOK"))
j.call("ping")
j.reply(err("ERR AUTH <password> called without any password configured for the default user. Are you sure your configuration is correct?"))
j.call("ping")
j.reply(err("ERR invalid password"))
j.call("ping")

j = Job("client name and db", client_name="worker-1", db=3)
j.reply(OK)
j.hs()
j.reply(OK)
j.reply(simple("PONG")).call("ping")

j = Job("bad client name", client_name="worker 1")
j.reply(simple("NO"))
j.call("ping")
j.reply(err("ERR Client names cannot contain spaces, newlines or special characters."))
j.call("ping")

j = Job("bad db", db=99)
j.hs()
j.reply(err("ERR DB index is out of range"))
j.call("ping")
j.hs()
j.reply(simple("NOPE"))
j.call("ping")

j = Job("old server", lib_name="my-app", lib_version=None)
j.reply(err("ERR unknown subcommand 'SETINFO'. Try CLIENT HELP."))
j.reply(simple("PONG")).call("ping")

j = Job("no client info", lib_name=None, lib_version=None)
j.reply(simple("PONG")).call("ping")

j = Job("handshake drops", lib_name="x", lib_version=None)
j.reply("@close")
j.call("ping")
j.reply(OK)
j.reply(simple("PONG")).call("ping")

# 19. connections that fail
j = Job("closed by server")
j.hs()
j.reply(OK).call("set s:a s:1")
j.reply("@close").call("get s:a")
j.hs()
j.reply(bulk("1")).call("get s:a")
j.reply(b"$5\r\nab").call("get s:a")

j = Job("timeouts")
j.hs()
j.reply("@hang").call("get s:a")
j.hs()
j.reply(bulk("1")).call("get s:a")

j = Job("retry on timeout", retry_on_timeout=True)
j.hs()
j.reply("@hang")
j.hs()
j.reply(bulk("1")).call("get s:a")
j.reply("@hang")
j.hs()
j.reply("@hang").call("get s:a")
j.hs()
j.reply("@close")
j.call("get s:a")

j = Job("stale data")
j.hs()
j.reply(OK + OK).call("set s:a s:1")
j.hs()
j.reply(bulk("1")).call("get s:a")
j.reply(bulk("1") + num(7)).call("get s:a")
j.hs()
j.reply(OK + OK)
j.call("get s:a")

# 20. pipelines
j = Job("pipeline")
j.hs()
j.pipe("begin transaction=F:")
j.call("set s:a s:1")
j.call("incr s:a")
j.call("hgetall s:h")
j.call("zrange s:z i:0 i:-1 withscores=T:")
j.reply(OK, num(2), arr(["f", "v"]), arr(["m", "1.5"]))
j.pipe("execute")
j.call("set s:a s:x")
j.call("incr s:a")
j.call("get s:a")
j.reply(OK, err("ERR value is not an integer or out of range"), bulk("x"))
j.pipe("execute")
j.call("set s:a s:x")
j.call("incr s:a")
j.call("get s:a")
j.reply(OK, err("ERR value is not an integer or out of range"), bulk("x"))
j.pipe("execute raise_on_error=F:")
j.pipe("execute")
j.call("set s:k r:v*6100")
j.call("set s:k2 s:w")
j.reply(OK, OK)
j.pipe("execute")
j.bitfield("s:bits | incrby s:u8 i:0 i:1 | execute")
j.call("mget [ ]")
j.reply(arr([1]), err("ERR wrong number"))
j.pipe("execute")
j.pipe("end")

j = Job("transaction")
j.hs()
j.pipe("begin")
j.call("set s:a s:1")
j.call("incr s:a")
j.call("smembers s:s")
j.call("set s:b s:2 get=T:")
j.reply(OK, QUEUED, QUEUED, QUEUED, QUEUED, arr([OK, 2, ["x", "y"], None]))
j.pipe("execute")
j.call("set s:a s:x")
j.call("incr s:a")
j.reply(OK, QUEUED, QUEUED, arr([OK, err("ERR value is not an integer or out of range")]))
j.pipe("execute")
j.call("set s:a s:x")
j.call("incr s:a")
j.reply(OK, QUEUED, QUEUED, arr([OK, err("ERR value is not an integer or out of range")]))
j.pipe("execute raise_on_error=F:")
j.call("get s:a")
j.call("get s:b")
j.reply(OK, err("ERR wrong number of arguments for 'get' command"), QUEUED,
        err("EXECABORT Transaction discarded because of previous errors."))
j.pipe("execute")
j.call("get s:a")
j.reply(OK, QUEUED, NIL_ARR)
j.pipe("execute")
j.call("get s:a")
j.call("get s:b")
j.reply(OK, QUEUED, QUEUED, arr(["1"]))
j.pipe("execute")
j.hs()
j.call("get s:a")
j.reply(err("ERR MULTI calls can not be nested"), QUEUED, arr(["1"]))
j.pipe("execute raise_on_error=F:")
j.hs()
j.call("ping")
j.reply(OK, QUEUED, err("EXECABORT Transaction discarded"))
j.pipe("execute")
j.pipe("execute")
j.pipe("end")

j = Job("watch")
j.hs()
j.pipe("begin")
j.reply(OK).pipe("watch s:balance")
j.reply(bulk("100")).call("get s:balance")
j.pipe("multi")
j.pipe("multi")
j.call("set s:balance i:90")
j.reply(OK, QUEUED, arr([OK]))
j.pipe("execute")
j.reply(OK).pipe("watch s:balance")
j.reply(OK).pipe("unwatch")
j.pipe("unwatch")
j.reply(OK).pipe("watch s:balance")
j.pipe("multi")
j.call("set s:balance i:80")
j.reply(OK, QUEUED, NIL_ARR)
j.pipe("execute")
j.reply(OK).pipe("watch s:a s:b")
j.reply(OK)
j.pipe("reset")
j.call("get s:a")
j.pipe("multi")
j.reply(OK).pipe("watch s:c")
j.reply(OK).pipe("reset")
j.reply(OK).pipe("watch s:a")
j.reply("@close")
j.hs()
j.reply(OK)
j.call("get s:a")
j.pipe("reset")
j.reply(OK).pipe("watch s:a")
j.pipe("multi")
j.call("incr s:a")
j.reply("@close")
j.hs()
j.reply(OK)
j.pipe("execute")
j.pipe("end")

# 21. URLs
j = Job("urls")
for u in [
    "redis://localhost",
    "redis://localhost:6380/2",
    "redis://:secret@cache.internal:6379/0",
    "redis://app:p%40ss%3Aword@10.0.0.5:7000",
    "rediss://user@secure.example.com/5?ssl_check_hostname=false",
    "unix:///var/run/redis.sock?db=3",
    "unix://user:pw@/tmp/r.sock",
    "redis://h/1?db=4",
    "redis://h/x",
    "redis://h/?socket_timeout=2.5&socket_connect_timeout=1&health_check_interval=30",
    "redis://h?socket_keepalive=no&retry_on_timeout=yes&max_connections=10",
    "redis://h?socket_keepalive=&decode_responses=True&client_name=my%20app",
    "redis://h?db=abc",
    "redis://h?max_connections=1.5",
    "redis://h?timeout=fast",
    "redis://[::1]:6379/0",
    "redis://h?a=1&a=2&b",
    "http://localhost:6379",
    "redis://h:99999",
    "redis://h:abc",
    "REDIS://h",
    "redis://h/%2F2",
    "redis://h?retry_on_error=x",
    "redis://H.Example.COM",
]:
    j.url(u)

os.makedirs("data", exist_ok=True)
with open(os.path.join("data", "jobs.txt"), "w") as f:
    for job in JOBS:
        f.write("\n".join(job.lines) + "\n")
