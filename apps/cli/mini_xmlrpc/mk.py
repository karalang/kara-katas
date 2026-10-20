# Writes data/: the request bodies an XML-RPC service receives, one per
# file, read in name order. Run it from the app directory.
import os
import shutil

if os.path.isdir("data"):
    shutil.rmtree("data")
os.makedirs("data/requests")

reqs = []


def i(n):
    return "<value><int>%d</int></value>" % n


def s(t):
    return "<value><string>%s</string></value>" % t


def d(t):
    return "<value><double>%s</double></value>" % t


def b(v):
    return "<value><boolean>%s</boolean></value>" % v


def b64(t):
    return "<value><base64>%s</base64></value>" % t


def dt(t):
    return "<value><dateTime.iso8601>%s</dateTime.iso8601></value>" % t


def arr(*vs):
    return "<value><array><data>" + "".join(vs) + "</data></array></value>"


def st(*pairs):
    out = "<value><struct>"
    for k, v in pairs:
        out += "<member><name>%s</name>%s</member>" % (k, v)
    return out + "</struct></value>"


NIL = "<value><nil/></value>"


def call(name, *params, pretty=False):
    if pretty:
        body = "<?xml version='1.0'?>\n<methodCall>\n<methodName>%s</methodName>\n<params>\n" % name
        for p in params:
            body += "<param>\n%s\n</param>\n" % p
        return body + "</params>\n</methodCall>\n"
    return "<?xml version=\"1.0\"?><methodCall><methodName>%s</methodName><params>%s</params></methodCall>" % (
        name, "".join("<param>%s</param>" % p for p in params))


def mc(*calls):
    return arr(*[st(("methodName", s(n)), ("params", arr(*ps))) for n, *ps in calls])


def add(name, body):
    reqs.append((name, body))


# arithmetic
add("add-ints", call("math.add", i(2), i(3), pretty=True))
add("add-floats", call("math.add", d("0.1"), d("0.2")))
add("add-int-float", call("math.add", i(1), d("2.5")))
add("add-bools", call("math.add", b(1), b(1)))
add("add-strings", call("math.add", s("foo"), s("bar")))
add("add-lists", call("math.add", arr(i(1), s("x")), arr(d("2"))))
add("add-bytes", call("math.add", b64("aGVs"), b64("bG8=")))
add("add-int-str", call("math.add", i(1), s("x")))
add("add-str-int", call("math.add", s("x"), i(1)))
add("add-list-int", call("math.add", arr(), i(1)))
add("add-bytes-str", call("math.add", b64("AA=="), s("x")))
add("add-dicts", call("math.add", st(), st()))
add("add-date-int", call("math.add", dt("20260101T00:00:00"), i(1)))
add("add-overflow", call("math.add", i(2147483647), i(1)))
add("add-negative-edge", call("math.add", i(-2147483647), i(-1)))
add("add-arity-low", call("math.add", i(1)))
add("add-arity-none", call("math.add"))
add("add-arity-high", call("math.add", i(1), i(2), i(3)))
add("div-ints", call("math.div", i(7), i(2)))
add("div-thirds", call("math.div", i(1), i(3)))
add("div-zero", call("math.div", i(1), i(0)))
add("div-float-zero", call("math.div", d("1.5"), i(0)))
add("div-by-float-zero", call("math.div", i(1), d("-0.0")))
add("div-strings", call("math.div", s("6"), i(3)))
add("div-inf", call("math.div", d("inf"), d("2")))
add("sum-ints", call("math.sum", arr(i(1), i(2), i(3), b(1))))
add("sum-floats", call("math.sum", arr(d("0.1"), d("0.2"), d("0.3"), d("1e16"), d("1"), d("-1e16"))))
add("sum-mixed", call("math.sum", arr(i(1), d("0.1"), i(2), b(1), d("0.7"))))
add("sum-empty", call("math.sum", arr()))
add("sum-bytes", call("math.sum", b64("AQID")))
add("sum-strings", call("math.sum", arr(s("a"), s("b"))))
add("sum-float-then-str", call("math.sum", arr(d("1.5"), s("a"))))
add("sum-int-then-list", call("math.sum", arr(i(1), arr())))
add("sum-not-iterable", call("math.sum", i(5)))
add("sum-dict", call("math.sum", st(("a", i(1)))))
# text
add("join-list", call("text.join", s(", "), arr(s("a"), s("b"), s("c"))))
add("join-string", call("text.join", s("-"), s("abc")))
add("join-dict-keys", call("text.join", s("+"), st(("x", i(1)), ("y", i(2)))))
add("join-bad-item", call("text.join", s(","), arr(s("a"), i(2))))
add("join-not-iterable", call("text.join", s(","), d("1.5")))
add("join-int-sep", call("text.join", i(1), arr()))
add("join-bytes-sep", call("text.join", b64("LQ=="), arr(b64("YQ=="), b64("Yg=="))))
add("join-bytes-sep-str", call("text.join", b64("LQ=="), arr(s("a"))))
add("split-comma", call("text.split", s("a,b,,c"), s(",")))
add("split-whitespace", call("text.split", s("  a b\tc\n"), NIL))
add("split-empty-sep", call("text.split", s("abc"), s("")))
add("split-int-sep", call("text.split", s("abc"), i(1)))
add("split-bytes", call("text.split", b64("YSBi"), b64("IA==")))
add("split-bytes-str", call("text.split", b64("YSBi"), s(" ")))
add("split-int", call("text.split", i(5), s(",")))
# the store
add("kv-put-config", call("kv.put", s("config"), st(("retries", i(3)), ("timeout", d("2.5")), ("hosts", arr(s("a.example"), s("b.example"))))))
add("kv-put-blob", call("kv.put", s("logo"), b64("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")))
add("kv-put-when", call("kv.put", s("deployed"), dt("20260315T09:30:00")))
add("kv-put-int-key", call("kv.put", i(7), s("seven")))
add("kv-get", call("kv.get", s("config")))
add("kv-get-blob", call("kv.get", s("logo")))
add("kv-get-missing", call("kv.get", s("nope")))
add("kv-keys", call("kv.keys"))
add("kv-keys-arg", call("kv.keys", i(1)))
add("kv-pop", call("kv.pop", s("deployed")))
add("kv-pop-again", call("kv.pop", s("deployed")))
add("kv-keys-after", call("kv.keys"))
# bytes and lengths
add("concat", call("blob.concat", arr(b64("SGVsbG8s"), b64("IHdvcmxk"), b64("IQ=="))))
add("concat-long", call("blob.concat", arr(*[b64("AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8=") for _ in range(4)])))
add("concat-empty", call("blob.concat", arr()))
add("concat-str", call("blob.concat", arr(b64("YQ=="), s("b"))))
add("concat-string", call("blob.concat", s("ab")))
add("size-str", call("blob.size", s("héllo")))
add("size-bytes", call("blob.size", b64("AAEC\nAwQF")))
add("size-list", call("blob.size", arr(i(1), i(2))))
add("size-int", call("blob.size", i(12)))
add("size-date", call("blob.size", dt("20260101T00:00:00")))
# dates
add("shift-day", call("time.shift", dt("20261231T23:59:30"), i(1), i(45)))
add("shift-back", call("time.shift", dt("20240301T00:00:00"), i(-1), i(0)))
add("shift-leap", call("time.shift", dt("19000228T12:00:00"), i(1), i(-43200)))
add("shift-far", call("time.shift", dt("20260115T08:00:00"), i(36500), i(86399)))
add("shift-bool-days", call("time.shift", dt("20260115T08:00:00"), b(1), b(0)))
add("shift-overflow", call("time.shift", dt("99991231T12:00:00"), i(1), i(0)))
add("shift-underflow", call("time.shift", dt("00010101T00:00:00"), i(0), i(-1)))
add("shift-str-days", call("time.shift", dt("20260115T08:00:00"), s("1"), i(0)))
add("shift-int-when", call("time.shift", i(5), i(1), i(0)))
add("shift-str-when", call("time.shift", s("x"), i(1), i(0)))
add("shift-bytes-when", call("time.shift", b64(""), i(1), i(0)))
add("date-short-fields", call("echo", dt("2026012T3:4:5")))
add("date-lowercase-t", call("echo", dt("20260102t03:04:05")))
add("date-feb-30", call("echo", dt("20260230T00:00:00")))
add("date-leap-day", call("echo", dt("20240229T00:00:00"), dt("19000229T00:00:00")))
add("date-second-60", call("echo", dt("20260102T03:04:60")))
add("date-leading-space", call("echo", dt(" 20260102T03:04:05")))
add("date-trailing-space", call("echo", dt("20260102T03:04:05 ")))
add("date-dashes", call("echo", dt("2026-01-02T03:04:05")))
add("date-year-zero", call("echo", dt("00000102T03:04:05")))
add("date-hour-24", call("echo", dt("20260102T24:00:00")))
# what echo sends back
add("echo-mixed", call("echo", i(42), s("tab\there &amp; &lt;there&gt;"), d("-0.0"), d("1e300"), d("1.5e-7"), b(0), arr(), st()))
add("echo-nested", call("echo", st(("user", st(("name", s("Ana")), ("roles", arr(s("admin"), s("ops"))))), ("tags", arr(arr(i(1)), arr())))))
add("echo-nil", call("echo", i(1), NIL))
add("echo-nil-nested", call("echo", arr(NIL)))
add("echo-i8", call("echo", "<value><i8>5000000000</i8></value>"))
add("echo-i8-small", call("echo", "<value><i8>-17</i8></value>", "<value><i4>  +9 </i4></value>", "<value><i2>1_000</i2></value>"))
add("echo-untyped", call("echo", "<value>  plain text </value>", "<value></value>", "<value/>"))
add("echo-entities", call("echo", s("&lt;&#65;&#x42;&amp;&gt;&quot;&apos;"), s("<![CDATA[<raw> & stuff]]>"), s("a<!-- note -->b")))
add("echo-namespaced", '<?xml version="1.0"?><ex:methodCall xmlns:ex="urn:x"><ex:methodName>echo</ex:methodName><ex:params><ex:param><ex:value><ex:int>5</ex:int></ex:value></ex:param><ex:param><ex:value><ex:array><ex:data><ex:value><ex:boolean>1</ex:boolean></ex:value></ex:data></ex:array></ex:value></ex:param></ex:params></ex:methodCall>')
add("echo-dup-keys", call("echo", st(("a", i(1)), ("b", i(2)), ("a", i(3)))))
add("echo-member-no-name", call("echo", "<value><struct><member><value><int>1</int></value></member><member><value><int>2</int></value></member></struct></value>"))
add("echo-member-no-value", call("echo", "<value><struct><member><name>a</name></member></struct></value>"))
add("echo-member-list-key", call("echo", "<value><struct><member><value><array><data/></array></value></member><member><value><int>2</int></value></member></struct></value>"))
add("echo-whitespace", call("echo", i(1), arr(i(2), s("x")), pretty=True).replace("<int>", "\n  <int>").replace("</data>", "\n</data>"))
add("echo-unknown-tag", call("echo", "<value><decimal>1.5</decimal></value>"))
add("echo-ignored-tag", call("echo", "<value><int>1</int><note>x</note></value>"))
add("echo-bad-bool", call("echo", b("2")))
add("echo-bad-int", call("echo", "<value><int>12px</int></value>"))
add("echo-bad-double", call("echo", d("1.5e")))
add("echo-double-forms", call("echo", d(" 1_0.25 "), d("-Infinity"), d("NaN"), d("1e400"), d(".5"), d("7")))
add("echo-base64-padding", call("echo", b64("YWJj\nZGVm\n"), b64("YQ"), b64("YW=Jj")))
add("echo-base64-short", call("echo", b64("YWJjZ")))
add("echo-float-text", call("echo", "<value><float>2.0</float></value>", "<value><double>123456789012345678</double></value>"))
add("echo-long-string", call("echo", s("x" * 3 + "é中\U0001F600")))
add("echo-many-params", call("echo", *[i(n) for n in range(1, 13)]))
# introspection
add("list-methods", call("system.listMethods"))
add("method-help", call("system.methodHelp", s("math.add")))
add("method-help-system", call("system.methodHelp", s("system.multicall")))
add("method-help-unknown", call("system.methodHelp", s("nope")))
add("method-help-int", call("system.methodHelp", i(3)))
add("method-help-list", call("system.methodHelp", arr()))
add("method-help-arity", call("system.methodHelp"))
add("method-signature", call("system.methodSignature", s("math.add")))
add("list-methods-arity", call("system.listMethods", i(1)))
# multicall
add("multicall", call("system.multicall", mc(("math.add", i(1), i(2)), ("kv.get", s("config")), ("kv.get", s("gone")), ("math.div", i(1), i(0)), ("nope",))))
GOOD = st(("methodName", s("math.add")), ("params", arr(i(1), i(1))))
for kind, bad in [("no-params", st(("methodName", s("math.add")))), ("no-name", st(("params", arr()))),
                  ("list", arr()), ("string", s("x")), ("int", i(4)), ("nil", NIL), ("bytes", b64("YQ==")),
                  ("double", d("1"))]:
    add("multicall-shape-" + kind, call("system.multicall", arr(GOOD, bad)))
add("multicall-params", call("system.multicall", arr(st(("methodName", s("echo")), ("params", s("ab"))), st(("methodName", s("echo")), ("params", st(("k", i(1))))), st(("methodName", s("echo")), ("params", i(5))), st(("methodName", i(5)), ("params", arr())), st(("methodName", arr()), ("params", arr())))))
add("multicall-nested", call("system.multicall", mc(("system.multicall", mc(("math.add", i(2), i(2)))), ("kv.keys",))))
add("multicall-void", call("system.multicall", mc(("sys.void",), ("echo", NIL))))
add("multicall-dict", call("system.multicall", st(("methodName", s("x")))))
add("multicall-not-list", call("system.multicall", i(1)))
add("multicall-empty", call("system.multicall", arr()))
# the dispatcher's own failures
add("unknown-method", call("math.pow", i(2), i(8)))
add("method-spaces", call(" math.add ", i(1), i(2)))
add("method-escaped", call("math&amp;add", i(1)))
add("void", call("sys.void"))
add("no-method-name", "<?xml version='1.0'?><methodCall><params><param>%s</param></params></methodCall>" % i(1))
add("no-params", "<?xml version='1.0'?><methodCall><methodName>kv.keys</methodName></methodCall>")
add("response-params", "<?xml version='1.0'?><methodResponse><params><param>%s</param></params></methodResponse>" % i(1))
add("response-fault", "<?xml version='1.0'?><methodResponse><fault>%s</fault></methodResponse>" % st(("faultCode", i(7)), ("faultString", s("upstream said no"))))
add("response-fault-extra", "<?xml version='1.0'?><methodResponse><fault>%s</fault></methodResponse>" % st(("faultCode", s("E42")), ("faultString", s("odd")), ("retry", b(1))))
add("response-fault-short", "<?xml version='1.0'?><methodResponse><fault>%s</fault></methodResponse>" % st(("faultCode", i(1))))
add("response-fault-int", "<?xml version='1.0'?><methodResponse><fault>%s</fault></methodResponse>" % i(3))
add("response-fault-empty", "<?xml version='1.0'?><methodResponse><fault></fault></methodResponse>")
add("bare-value", "<?xml version='1.0'?>%s" % i(1))
add("other-root", "<rpc><call>x</call></rpc>")
add("xml-mismatched", "<methodCall><methodName>a</methodName><params></param></methodCall>")
add("xml-unclosed", "<methodCall>\n  <methodName>kv.keys</methodName>\n")
add("xml-junk", "<methodCall><methodName>kv.keys</methodName></methodCall>\n<!-- ok -->\n<again/>")
add("xml-empty", "")
add("crlf", call("text.split", s("a b"), s(" "), pretty=True).replace("\n", "\r\n"))

for k, (name, body) in enumerate(reqs):
    with open("data/requests/%03d-%s.xml" % (k + 1, name), "w", encoding="utf-8", newline="") as f:
        f.write(body)
