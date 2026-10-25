# Writes data/: the schemas in data/schemas.json (voluptuous schemas as
# JSON nodes, which oracle.py turns into voluptuous objects and
# mini_voluptuous.kara reads as they are), the configuration documents
# under data/configs/, the files and directories IsFile, IsDir and
# PathExists look at under data/files/, and the jobs in data/jobs.jsonl.
import json
import os

UNDEF = object()


# ------------------------------------------------------------ nodes
def T(name):
    return {"op": "type", "name": name}


def D(*pairs):
    return {"op": "dict", "keys": [[k, v] for k, v in pairs]}


def L(*items):
    return {"op": "list", "items": list(items)}


def V(op, **kw):
    n = {"op": op}
    for k, v in kw.items():
        if v is not UNDEF:
            n[k] = v
    return n


def marker(kind, name, msg=None, default=UNDEF, group=None):
    n = {"op": kind, "name": name}
    if msg is not None:
        n["msg"] = msg
    if default is not UNDEF:
        n["default"] = default
    if group is not None:
        n["group"] = group
    return n


def Req(name, msg=None, default=UNDEF):
    return marker("required", name, msg, default)


def Opt(name, msg=None, default=UNDEF):
    return marker("optional", name, msg, default)


def Rem(name):
    return marker("remove", name)


def Excl(name, group, msg=None):
    return marker("exclusive", name, msg, group=group)


def Incl(name, group, msg=None, default=UNDEF):
    return marker("inclusive", name, msg, default, group=group)


EXTRA = {"op": "extra"}


def Any(*vs, msg=None, required=False):
    n = {"op": "any", "of": list(vs)}
    if msg is not None:
        n["msg"] = msg
    if required:
        n["required"] = True
    return n


def All(*vs, msg=None, required=False):
    n = {"op": "all", "of": list(vs)}
    if msg is not None:
        n["msg"] = msg
    if required:
        n["required"] = True
    return n


def SomeOf(vs, min_valid=None, max_valid=None, msg=None):
    n = {"op": "someof", "of": list(vs)}
    if min_valid is not None:
        n["min"] = min_valid
    if max_valid is not None:
        n["max"] = max_valid
    if msg is not None:
        n["msg"] = msg
    return n


def Maybe(v, msg=None):
    return V("maybe", of=v, msg=msg if msg is not None else UNDEF)


def Msg(v, text):
    return {"op": "msg", "of": v, "text": text}


def M(op, msg=None, **kw):
    n = {"op": op}
    n.update({k: v for k, v in kw.items() if v is not UNDEF})
    if msg is not None:
        n["msg"] = msg
    return n


def Coerce(t, msg=None):
    return M("coerce", msg, type=t)


def Match(p, msg=None):
    return M("match", msg, pattern=p)


def Replace(p, s, msg=None):
    return M("replace", msg, pattern=p, sub=s)


def Range(min=UNDEF, max=UNDEF, min_included=True, max_included=True, msg=None):
    n = M("range", msg, min=min, max=max)
    if not min_included:
        n["min_included"] = False
    if not max_included:
        n["max_included"] = False
    return n


def Clamp(min=UNDEF, max=UNDEF, msg=None):
    return M("clamp", msg, min=min, max=max)


def Length(min=UNDEF, max=UNDEF, msg=None):
    return M("length", msg, min=min, max=max)


def Datetime(fmt=UNDEF, msg=None):
    return M("datetime", msg, format=fmt)


def Date(fmt=UNDEF, msg=None):
    return M("date", msg, format=fmt)


def In(c, msg=None):
    return M("in", msg, container=c)


def NotIn(c, msg=None):
    return M("notin", msg, container=c)


def Contains(item, msg=None):
    return M("contains", msg, item=item)


def ExactSequence(vs, msg=None):
    return M("exactsequence", msg, of=vs)


def Unordered(vs, msg=None):
    return M("unordered", msg, of=vs)


def Unique(msg=None):
    return M("unique", msg)


def Equal(t, msg=None):
    return M("equal", msg, target=t)


def Number(precision=UNDEF, scale=UNDEF, msg=None):
    return M("number", msg, precision=precision, scale=scale)


def Simple(op, msg=None):
    return M(op, msg)


Lower = {"op": "lower"}
Upper = {"op": "upper"}
Capitalize = {"op": "capitalize"}
Title = {"op": "title"}
Strip = {"op": "strip"}
SELF = {"op": "self"}


def DefaultTo(v):
    return {"op": "defaultto", "value": v}


def SetTo(v):
    return {"op": "setto", "value": v}


def Literal(v):
    return {"op": "literal", "value": v}


def Lit(v):
    # a literal schema value that would otherwise read as a node
    return {"op": "lit", "value": v}


# ------------------------------------------------------------ schemas
schemas = []


def schema(name, node, required=False, extra="prevent"):
    schemas.append({"name": name, "schema": node, "required": required, "extra": extra})


def extend(name, base, node, required=None, extra=None):
    s = {"name": name, "extend": base, "with": node}
    if required is not None:
        s["required"] = required
    if extra is not None:
        s["extra"] = extra
    schemas.append(s)


ENTITY = r"^[a-z_]+\.[a-z0-9_]+$"
DURATION = r"^\d{2}:\d{2}:\d{2}$"
byte = All(T("int"), Range(min=0, max=255))

# A Home Assistant light platform, the way integrations declare
# PLATFORM_SCHEMA.
schema("ha_light", D(
    (Req("platform"), In(["hue", "mqtt", "template"])),
    (Req("name"), All(T("str"), Strip, Length(min=1, max=40))),
    (Opt("brightness", default=255), All(Coerce("int"), Range(min=0, max=255))),
    (Opt("color_temp"), All(T("int"), Range(min=153, max=500, msg="color_temp is in mireds, 153 to 500"))),
    (Opt("transition", default=1.0), All(Coerce("float"), Clamp(min=0, max=60))),
    (Excl("rgb_color", "color"), ExactSequence([byte, byte, byte])),
    (Excl("hs_color", "color"), ExactSequence([All(Coerce("float"), Range(min=0, max=360)),
                                               All(Coerce("float"), Range(min=0, max=100))])),
    (Excl("color_name", "color", msg="pick one way to give the color"), T("str")),
    (Incl("effect", "fx"), In(["colorloop", "random", "none"])),
    (Incl("effect_speed", "fx"), All(T("int"), Range(min=1, max=10))),
    (Opt("entity_id"), Match(r"^light\.[a-z0-9_]+$")),
    (Rem("friendly_name"), T("str")),
    (Opt("icon"), Match(r"^mdi:[a-z-]+$", msg="icons are mdi:<name>")),
))

extend("ha_light_zigbee", "ha_light", D(
    ("platform", In(["hue", "mqtt", "template", "zigbee"])),
    (Opt("brightness", default=128), All(Coerce("int"), Range(min=1, max=254))),
    (Req("area"), All(T("str"), Lower)),
))
extend("ha_light_lenient", "ha_light", D(), extra="allow")
extend("ha_light_tidy", "ha_light", D(), extra="remove")

state_trigger = D(
    (Req("platform"), "state"),
    (Req("entity_id"), Any(Match(ENTITY), [Match(ENTITY)])),
    (Opt("from"), T("str")),
    (Opt("to"), T("str")),
    (Opt("for"), Match(DURATION, msg="for is HH:MM:SS")),
)
time_trigger = D(
    (Req("platform"), "time"),
    (Req("at"), Datetime("%H:%M:%S")),
)
numeric_trigger = D(
    (Req("platform"), "numeric_state"),
    (Req("entity_id"), Match(ENTITY)),
    (Opt("above"), Coerce("float")),
    (Opt("below"), Coerce("float")),
)
sun_trigger = D(
    (Req("platform"), "sun"),
    (Req("event"), In(["sunrise", "sunset"])),
    (Opt("offset", default="00:00:00"), Match(r"^-?\d{2}:\d{2}:\d{2}$")),
)
service_action = D(
    (Req("service"), Match(r"^\w+\.\w+$")),
    (Opt("target"), D((Opt("entity_id"), Any(Match(ENTITY), [Match(ENTITY)])), (Opt("area_id"), T("str")))),
    (Opt("data", default={}), D((T("str"), T("object")))),
)
delay_action = D((Req("delay"), Match(DURATION)))
schema("ha_automation", D(
    (Req("alias"), All(T("str"), Length(min=1))),
    (Opt("description"), T("str")),
    (Opt("mode", default="single"), In(["single", "restart", "queued", "parallel"])),
    (Opt("max", default=10), All(T("int"), Range(min=1, max=100))),
    (Req("trigger"), All([Any(state_trigger, time_trigger, numeric_trigger, sun_trigger)], Length(min=1))),
    (Opt("condition", default=[]), [T("dict")]),
    (Req("action"), All([Any(service_action, delay_action, msg="an action is a service call or a delay")],
                        Length(min=1, msg="an automation needs an action"))),
))

upstream = D(
    ("name", Match(r"^[a-z][a-z0-9-]*$")),
    ("url", V("url")),
    (Opt("weight", default=1), All(T("int"), Range(min=1, max=100))),
    (Opt("backup", default=False), V("boolean")),
)
schema("web_server", D(
    ("listen", All(Coerce("int"), Range(min=1, max=65535))),
    ("host", Any("0.0.0.0", "::", Match(r"^(\d{1,3}\.){3}\d{1,3}$"), msg="host is an IPv4 address")),
    ("root", V("isdir")),
    (Opt("index", default="index.html"), T("str")),
    (Opt("public_url"), V("fqdnurl")),
    (Opt("tls"), D(
        ("cert", V("isfile")),
        ("key", V("isfile")),
        (Opt("protocols", default=["TLSv1.3"]), All([In(["TLSv1.2", "TLSv1.3"])], Unique())),
    )),
    ("upstreams", All([upstream], Length(min=1))),
    (Opt("log_dir"), V("pathexists")),
    (Opt("workers", default=4), All(T("int"), Range(min=1, max=64))),
    (Opt("gzip", default=True), V("boolean")),
), required=True)

schema("signup", D(
    (Req("email"), All(T("str"), Strip, Lower, V("email"))),
    (Req("username"), All(T("str"), Strip, Length(min=3, max=20),
                          Match(r"^[a-z0-9_]+$", msg="letters, digits and underscores only"))),
    (Req("password"), SomeOf([
        Match(r".*[A-Z]", msg="no uppercase letter"),
        Match(r".*[a-z]", msg="no lowercase letter"),
        Match(r".*\d", msg="no digit"),
        Match(r".*[^A-Za-z0-9]", msg="no symbol"),
        Length(min=12, msg="shorter than 12"),
    ], min_valid=4)),
    (Opt("birthday"), Date()),
    (Opt("website"), Maybe(V("url"))),
    (Opt("tags", default=[]), All([All(T("str"), Lower)], Unique(), Length(max=5))),
    (Req("terms", msg="you must accept the terms"), V("istrue")),
    (Opt("newsletter", default=False), V("boolean")),
    (Opt("referrer"), NotIn(["spam.example", "bot.example"])),
    (Opt("display_name"), All(T("str"), Strip, Title)),
))

line = D(
    (Req("sku"), All(T("str"), Upper, Match(r"^[A-Z]{3}-\d{3}$"))),
    (Req("qty"), All(T("int"), Range(min=1))),
    (Req("unit_price"), All(T("str"), Number(scale=2))),
    (Opt("discount", default=0), All(Coerce("float"), Range(min=0, max=1, max_included=False))),
)
schema("invoice", D(
    (Req("number"), Match(r"^INV-\d{4}-\d{5}$")),
    (Req("issued"), Datetime("%Y-%m-%dT%H:%M:%SZ")),
    (Req("due"), Date()),
    (Req("currency"), In(["USD", "EUR", "GBP"])),
    (Req("customer"), D(
        (Req("name"), All(T("str"), Length(min=1))),
        (Opt("vat_id"), Match(r"^[A-Z]{2}[0-9A-Z]{8,12}$")),
        (Opt("email"), V("email")),
    )),
    (Req("lines"), All([line], Length(min=1))),
    (Opt("vat_rate", default=0.2), All(Coerce("float"), Range(min=0, max=0.25, min_included=False))),
    (Req("total"), All(T("str"), Number(precision=7, scale=2))),
    (Opt("notes"), Maybe(All(T("str"), Length(max=80)))),
    (Opt("paid", default=False), T("bool")),
))

service = D(
    (Excl("image", "source", msg="give image or build, not both"), Match(r"^[a-z0-9./-]+(:[\w.-]+)?$")),
    (Excl("build", "source", msg="give image or build, not both"),
     Any(T("str"), D((Req("context"), T("str")), (Opt("dockerfile"), T("str"))))),
    (Opt("ports"), [Any(T("int"), Match(r"^\d+:\d+$"), msg="ports are 8080 or 8080:80")]),
    (Opt("environment"), Any(
        D((Match(r"^[A-Z_][A-Z0-9_]*$"), Any(T("str"), T("int"), T("bool"), None))),
        [Match(r"^[A-Z_][A-Z0-9_]*=.*$")],
    )),
    (Opt("depends_on", default=[]), [T("str")]),
    (Opt("restart", default="no"), In(["no", "always", "on-failure", "unless-stopped"])),
    (Opt("replicas"), All(Coerce("int"), Range(min=0, max=20))),
    (Opt("command"), Any(T("str"), [T("str")])),
)
schema("compose", D(
    (Req("version"), All(Coerce("str"), In(["3.8", "3.9"]))),
    (Req("services"), All(D((Match(r"^[a-z][a-z0-9_-]*$"), service)), Length(min=1))),
    (Opt("volumes"), D((T("str"), Any(None, D((Opt("driver", default="local"), T("str"))))))),
    (Opt("networks"), D((T("str"), T("dict")))),
))

schema("menu", D(
    (Req("label"), All(T("str"), Length(min=1))),
    (Opt("action"), Match(r"^[a-z_]+(\.[a-z_]+)*$")),
    (Opt("shortcut"), Match(r"^(Ctrl|Alt|Shift)(\+(Ctrl|Alt|Shift))*\+[A-Z0-9]$")),
    (Opt("children", default=[]), [SELF]),
))

schema("feature_flags", D(
    (T("str"), Any(V("boolean"), D(
        (Req("rollout"), All(Coerce("int"), Range(min=0, max=100))),
        (Opt("groups", default=[]), [In(["staff", "beta", "everyone"])]),
        (Opt("until"), Date()),
    ))),
))

schema("sensor_reading", D(
    (Req("sensor"), Match(r"^[a-z]+-\d{3}$")),
    (Req("at"), Datetime()),
    (Req("celsius"), All(Coerce("float"), Range(min=-40, max=85))),
    (Opt("humidity"), All(Coerce("float"), Clamp(min=0, max=100))),
    (Opt("battery"), All(T("int"), Range(min=0, max=100))),
    (EXTRA, T("object")),
))

# ------------------------------------------------------------ the unit schemas
# One validator each, with the inputs that show what it does at its edges.
U = []


def unit(name, node, docs, required=False, extra="prevent"):
    schema(name, node, required, extra)
    U.append((name, docs))


unit("u_type_int", T("int"), [5, True, 5.0, "5", None])
unit("u_type_float", T("float"), [2.5, 2, "2.5"])
unit("u_type_str", T("str"), ["x", 1, [], {}])
unit("u_type_object", T("object"), [None, [1], {"a": 1}])
unit("u_literal", "on", ["on", "On", 1])
unit("u_literal_int", 1, [1, 1.0, True, "1", 2])
unit("u_literal_none", None, [None, 0, ""])
unit("u_list_any", [T("int"), T("str")], [[1, "a", 2], [1, 2.5], [], "ab", [None, None]])
unit("u_list_empty", [], [[], [1, "a"], [7], {}])
unit("u_list_nested_empty", D(("x", [])), [{"x": []}, {"x": [1, 2]}])
unit("u_list_of_dicts", [D(("id", T("int")))], [[{"id": 1}, {"id": "2"}, 3], [{"id": 1, "n": 2}]])
unit("u_typed_keys", D((T("str"), T("int"))), [{"a": 1, "b": 2}, {"a": "1"}, {}], required=True)
unit("u_match_key", D((Match(r"^x-"), T("str"))), [{"x-trace": "on"}, {"trace": "on"}, {}], required=True)
unit("u_required_all", D(("a", T("int")), (Opt("b"), T("int")), (Rem("c"), T("int"))),
     [{"a": 1}, {}, {"b": 1, "c": 2}, {"a": 1, "c": "x"}], required=True)
unit("u_extra", D(("id", T("int")), (EXTRA, T("object"))), [{"id": 1, "x": [1]}, {"id": "1", "y": 2}])
unit("u_extra_prevent", D(("id", T("int"))), [{"id": 1, "x": 1}, {"x": 1, "y": 2}])
unit("u_extra_allow", D(("id", T("int"))), [{"id": 1, "x": 1}], extra="allow")
unit("u_extra_remove", D(("id", T("int"))), [{"id": 1, "x": 1}, {"id": "1", "x": 1}], extra="remove")
unit("u_remove_then_type", D((Rem("x"), T("int")), (T("str"), T("int"))),
     [{"x": 1, "y": 2}, {"x": "a"}, {"y": "b"}])
unit("u_remove_key", D((Rem("debug"), T("bool")), ("name", T("str"))),
     [{"debug": True, "name": "a"}, {"debug": "yes", "name": "a"}, {"name": "a"}])
unit("u_defaults", D((Opt("a", default=1), T("int")), (Req("b", default="x"), T("str")),
                     (Opt("c", default=None), Maybe(T("int"))), (Opt("d", default="bad"), T("int"))),
     [{}, {"a": 2, "b": "y", "d": 3}, {"c": 5, "d": 4}])
unit("u_required_msg", D((Req("token", msg="a token is required"), T("str")), (Opt("x"), T("int"))),
     [{}, {"x": 1}, {"token": 5}])
unit("u_marker_msg", D((Req("port", msg="port must be an integer"), T("int"))),
     [{"port": "80"}, {"port": 80}, {"prot": 80}])
unit("u_exclusive", D((Excl("a", "g"), T("int")), (Excl("b", "g"), T("int")), (Excl("c", "h"), T("int")),
                      (Excl("d", "h", msg="c or d"), T("int"))),
     [{"a": 1}, {"a": 1, "b": 2}, {"a": 1, "b": 2, "c": 3, "d": 4}, {"c": 1, "d": "x"}])
unit("u_inclusive", D((Incl("user", "auth"), T("str")), (Incl("password", "auth"), T("str")),
                      (Incl("lat", "pos", msg="give lat and lon together"), T("float")),
                      (Incl("lon", "pos"), T("float"))),
     [{"user": "u", "password": "not-a-real-password"}, {"user": "u"}, {"lat": 1.5}, {"user": "u", "lat": 1.5}, {}])
unit("u_inclusive_default", D((Incl("x", "p", default=0), T("int")), (Incl("y", "p", default=0), T("int"))),
     [{}, {"x": 3}, {"x": 1, "y": 2}])
unit("u_nested_dict", D(("db", D(("host", T("str")), ("port", All(T("int"), Range(min=1)))))),
     [{"db": {"host": "h", "port": 5432}}, {"db": {"host": 1, "port": 0}}, {"db": "h:1"}, {"db": {}}],
     required=True)
unit("u_any", Any(T("int"), All(T("str"), Coerce("int"))), [3, "4", "four", None])
unit("u_any_msg", Any(T("int"), T("float"), msg="a number"), [3, 3.5, "3"])
unit("u_any_deepest", Any(D(("a", T("int"))), D(("a", D(("b", T("int")))))),
     [{"a": 1}, {"a": {"b": 2}}, {"a": {"b": "x"}}, {"a": "x"}])
unit("u_any_required", D(("v", Any(D(("x", T("int"))), D(("y", T("int"))), required=True))),
     [{"v": {}}, {"v": {"x": 1}}])
unit("u_any_not_required", D(("v", Any(D(("x", T("int"))), D(("y", T("int")))))), [{"v": {}}], required=True)
unit("u_all", All(T("str"), Strip, Length(min=2), Upper), ["  ab ", " a ", 5])
unit("u_all_msg", All(T("int"), Range(min=0), msg="a count"), [3, -1, "x"])
unit("u_someof_min", SomeOf([T("int"), Range(min=0), Range(max=9)], min_valid=3), [5, 15, -1, "x"])
unit("u_someof_max", SomeOf([Range(min=0), Range(max=9)], max_valid=1), [5, 15])
unit("u_someof_in_dict", D(("pin", SomeOf([Length(min=4), Length(max=6), Match(r"^\d+$")], min_valid=3))),
     [{"pin": "1234"}, {"pin": "12a"}, {"pin": 12}])
unit("u_maybe", Maybe(T("int")), [None, 1, "1"])
unit("u_maybe_msg", D(("n", Maybe(T("int"), msg="an int or null"))), [{"n": None}, {"n": "x"}])
unit("u_msg", Msg(All(T("int"), Range(min=1)), "a positive int"), [1, 0, "a"])
unit("u_msg_deep", D(("cfg", Msg(D(("a", D(("b", T("int"))))), "bad cfg"))),
     [{"cfg": {"a": {"b": "x"}}}, {"cfg": {"a": 1}}, {"cfg": 5}])
unit("u_coerce_int", Coerce("int"), ["12", " -7 ", "1_000", "3.5", 3.9, True, None, [1], "x"])
unit("u_coerce_float", Coerce("float"), ["2.5", " 3 ", "1e3", "-.5", 4, False, "two", None])
unit("u_coerce_str", Coerce("str"), [5, 2.5, None, True, [1, "a"], {"k": None}])
unit("u_coerce_bool", Coerce("bool"), [0, 1, "", "no", [], None])
unit("u_coerce_msg", Coerce("int", msg="whole numbers only"), ["1", "1.5"])
unit("u_boolean", V("boolean"), ["Yes", "off", "ENABLE", "maybe", 1, 0, None, [], [0], 2.5])
unit("u_istrue", V("istrue"), [True, 1, "x", [1], 0, "", [], None])
unit("u_isfalse", V("isfalse"), [False, 0, "", [], None, 1, "0"])
unit("u_match", Match(r"^\d{3}-\d{4}$"), ["555-1234", "5551234", 5551234, "555-12345"])
unit("u_match_msg", Match(r"(?i)^[a-z]+$", msg="letters only"), ["Abc", "ab1"])
unit("u_replace", All(T("str"), Replace(r"\s+", " "), Strip),
     ["  many   spaces\there ", "x"])
unit("u_replace_groups", All(T("str"), Replace(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1")),
     ["2024-07-02 and 2023-01-31", "none"])
unit("u_replace_named", All(T("str"), Replace(r"(?P<k>\w+)=(?P<v>\w*)", r"\g<v>:\g<k>")), ["a=1 b= c=3"])
unit("u_email", V("email"), ["ann@example.com", "a.b+c@mail.example.org", "\"odd user\"@example.com",
                             "no-at.example.com", "two@@example.com", "a@b", "a@b.c", "user@[192.168.0.1]",
                             "user@[300.1.1.1]", "a..b@example.com", ".a@example.com", "a@-x.com", "",
                             "a@example.com.", 5, "A@EXAMPLE.COM", "x@localhost", "x@host-name"])
unit("u_url", V("url"), ["http://example.com", "https://a.b/c?d#e", "ftp://files", "example.com",
                         "http://", "mailto:a@b.c", "//example.com/x", "  http://x.y", "HTTP://X", 5,
                         "http:/x", "c:\\path", "localhost:8080", "a1+b.c-d://h"])
unit("u_fqdnurl", V("fqdnurl"), ["http://example.com", "http://localhost:8080", "https://a.b", "x"])
unit("u_isfile", V("isfile"), ["data/files/tls/server.pem", "data/files/tls", "data/files/none.txt", "", None, 0])
unit("u_isdir", V("isdir"), ["data/files/www", "data/files/www/index.html", "data/nowhere", ""])
unit("u_pathexists", V("pathexists"), ["data/files/logs", "data/files/www/index.html", "data/x", "", None])
unit("u_isfile_msg", V("isfile", msg="no such certificate"), ["data/files/tls/missing.pem"])
unit("u_range", Range(min=1, max=10), [1, 10, 0, 11, 5.5, "5", None, True])
unit("u_range_open", Range(min=0, max=1, min_included=False, max_included=False), [0.5, 0, 1, -0.0])
unit("u_range_float", Range(min=0.5, max=2.5), [0.25, 3, 1])
unit("u_range_str", Range(min="b", max="m"), ["c", "a", "z", 5])
unit("u_range_msg", Range(max=100, msg="too big"), [101, "x"])
unit("u_clamp", Clamp(min=0, max=10), [-5, 5, 15, 2.5, "x"])
unit("u_clamp_float", Clamp(min=0.5), [0, 1, 0.25])
unit("u_length", Length(min=2, max=4), ["ab", "a", "abcde", [1, 2], {"a": 1}, 5, None])
unit("u_length_msg", Length(max=1, msg="one at most"), [[1, 2], 7])
unit("u_datetime", Datetime(), ["2024-07-02T10:20:30.123456Z", "2024-07-02T10:20:30Z", "2024-02-30T00:00:00.0Z", 5])
unit("u_datetime_fmt", Datetime("%d/%m/%Y %H:%M"), ["02/07/2024 09:05", "2/7/2024 9:05", "32/01/2024 00:00",
                                                       "02/07/2024 09:05 "])
unit("u_date", Date(), ["2024-02-29", "2023-02-29", "2024-2-9", "24-02-01", None])
unit("u_date_fmt", Date("%b %d %Y", msg="like Jul 02 2024"), ["Jul 02 2024", "jul 2 2024", "July 02 2024"])
unit("u_in", In(["red", "green", "blue"]), ["red", "Red", 1, None])
unit("u_in_numbers", In([3, 1, 2]), [1, 1.0, True, 4])
unit("u_in_mixed", In(["b", 2, "a", 10]), ["a", 3])
unit("u_in_msg", In(["a"], msg="only a"), ["b"])
unit("u_notin", NotIn(["root", "admin"]), ["ann", "root", 5])
unit("u_notin_mixed", NotIn([1, "x"]), ["x", 2])
unit("u_contains", Contains("b"), [["a", "b"], ["a"], "abc", "xyz", {"b": 1}, 5, None])
unit("u_contains_int", Contains(3), [[1, 2, 3], [3.0], "123", {"3": 1}])
unit("u_exact", ExactSequence([T("int"), T("str")]), [[1, "a"], [1], [1, 2], ["a", "b"], "ab", {"a": 1}])
unit("u_exact_msg", ExactSequence([T("int"), T("str")], msg="an id and a name"), [[1, 2], [1]])
unit("u_exact_in_dict", D(("pair", ExactSequence([T("int"), D(("k", T("str")))]))),
     [{"pair": [1, {"k": "v"}]}, {"pair": [1, {"k": 1}]}, {"pair": ["1", {}]}, {"pair": [1]}])
unit("u_unordered", Unordered([T("int"), T("str")]), [["a", 1], [1, 2], [1], [None, None], "ab", {"a": 1}])
unit("u_unordered_dicts", Unordered([D(("a", T("int"))), D(("b", T("int")))]), [[{"b": 1}, {"a": 2}], [{"a": 1}, {"a": 2}]])
unit("u_unique", Unique(), [[1, 2, 3], [1, 2, 1], ["a", "a", "a"], "abc", "hello", [1, True], [{"a": 1}], [[1], [1]], 5])
unit("u_unique_msg", Unique(msg="no repeats"), [[1, 1]])
unit("u_equal", Equal("yes"), ["yes", "no", ["yes"]])
unit("u_equal_list", Equal([1, "a"]), [[1, "a"], [1.0, "a"], [1]])
unit("u_number", Number(precision=6, scale=2), ["1234.56", "123.45", "1234.5", "12.345", "abc", " 0012.30 ", "1e2", 1234])
unit("u_number_scale", Number(scale=0), ["17", "17.0", "1E+3", "-0"])
unit("u_number_precision", Number(precision=3, msg="three digits"), ["1.23", "1.2", "0.00"])
unit("u_strings", D((Opt("l"), Lower), (Opt("u"), Upper), (Opt("c"), Capitalize), (Opt("t"), Title), (Opt("s"), Strip)),
     [{"l": "MiXeD", "u": "MiXeD", "c": "hELLO wORLD", "t": "hello o'neil 3rd-place", "s": "\t x \n"},
      {"l": 5, "u": None, "c": True, "t": [1], "s": 2.5}])
unit("u_defaultto", All(DefaultTo("n/a"), T("str")), [None, "x", 0])
unit("u_setto", D(("v", SetTo(42))), [{"v": "anything"}])
unit("u_literal_obj", Literal({"mode": "fast"}), [{"mode": "fast"}, {"mode": "slow"}, "fast"])
unit("u_self", D(("v", T("int")), (Opt("next"), Any(None, SELF))),
     [{"v": 1, "next": {"v": 2, "next": None}}, {"v": 1, "next": {"v": "2"}}, {"v": 1, "next": {"v": 2, "next": {"w": 3}}}])
unit("u_msg_self", Msg(D(("v", T("int")), (Opt("next"), SELF)), "bad link"), [{"v": 1, "next": {"v": 2}}, {"v": 1, "next": {"v": "x"}}])
unit("u_dict_type", D(("tags", T("dict")), ("list", T("list"))), [{"tags": {}, "list": []}, {"tags": [], "list": {}}])
unit("u_not_a_dict", D(("a", T("int"))), [[1], "a", None])
unit("u_none_value", D(("a", None)), [{"a": None}, {"a": 0}])
unit("u_any_key", D((Any("a", "b"), T("int"))), [{"a": 1, "b": 2}, {"c": 3}])
unit("u_any_key_required", D((Any("a", "b"), T("int"))), [{}, {"a": 1}], required=True)
unit("u_list_validator", All([T("int")], Length(min=1)), [[], [1], ["x"]])
unit("u_list_coerce", [Coerce("int")], [["1", 2, "x", "4"]])
unit("u_list_in_list", [[T("int")]], [[[1], [2, 3]], [[1], ["x"]], [1]])
unit("u_title_words", All(T("str"), Title, Replace(r"'S\b", "'s")), ["the cat's toy", "ACME CO."])

# ------------------------------------------------------------ files
FILES = {
    "files/tls/server.pem": "placeholder certificate for the validator, not a real one\n",
    "files/tls/server.key": "placeholder key for the validator, not a real one\n",
    "files/www/index.html": "<!doctype html>\n<title>it works</title>\n",
    "files/www/assets/app.css": "body { margin: 0 }\n",
    "files/logs/access.log": "",
}

# ------------------------------------------------------------ configuration documents
CONFIGS = {}

CONFIGS["lights/kitchen.json"] = {
    "platform": "hue", "name": "  Kitchen ceiling ", "brightness": "180", "color_temp": 370,
    "transition": "2.5", "entity_id": "light.kitchen_ceiling", "friendly_name": "Kitchen", "icon": "mdi:ceiling-light",
}
CONFIGS["lights/porch.json"] = {
    "platform": "mqtt", "name": "Porch", "rgb_color": [255, 140, 0], "effect": "colorloop", "effect_speed": 3,
    "transition": 90,
}
CONFIGS["lights/desk.json"] = {
    "platform": "hue", "name": "Desk", "rgb_color": [255, 255], "hs_color": [30, 80], "brightness": 300,
}
CONFIGS["lights/garden.json"] = {
    "platform": "zigbee", "name": "", "effect": "random", "color_temp": 100, "entity_id": "Light.Garden",
    "area": "Garden",
}
CONFIGS["lights/strip.json"] = {
    "platform": "template", "name": "LED strip", "hs_color": ["210", 101], "color_name": "blue",
    "icon": "mdi:led_strip", "effect_speed": 11,
}
CONFIGS["lights/hall.json"] = {
    "platform": "hue", "name": "Hall", "rgb_color": [10, 20, "30"], "brightness": "dim", "transition": "slow",
    "colour": "warm", "area": "hallway",
}
CONFIGS["lights/bulbs.json"] = [{"platform": "hue", "name": "Bulb"}]

CONFIGS["automations/lights_at_sunset.json"] = {
    "alias": "Porch lights at sunset",
    "trigger": [{"platform": "sun", "event": "sunset", "offset": "-00:30:00"}],
    "action": [{"service": "light.turn_on", "target": {"entity_id": "light.porch"}, "data": {"brightness": 200}}],
}
CONFIGS["automations/motion.json"] = {
    "alias": "Hall motion", "mode": "restart",
    "trigger": [{"platform": "state", "entity_id": ["binary_sensor.hall_motion", "binary_sensor.stairs"], "to": "on"}],
    "condition": [{"condition": "state", "entity_id": "sun.sun", "state": "below_horizon"}],
    "action": [{"service": "light.turn_on", "target": {"area_id": "hall"}}, {"delay": "00:02:00"},
               {"service": "light.turn_off", "target": {"area_id": "hall"}}],
}
CONFIGS["automations/broken_trigger.json"] = {
    "alias": "Freezer alarm",
    "trigger": [{"platform": "numeric_state", "entity_id": "sensor.freezer", "above": "-10"},
                {"platform": "state", "entity_id": "sensor.freezer_door", "for": "5 minutes"},
                {"platform": "time", "at": "25:00:00"},
                {"platform": "webhook", "webhook_id": "freezer"}],
    "action": [{"service": "notify.phone", "data": {"message": "Freezer warm"}}],
}
CONFIGS["automations/no_action.json"] = {
    "alias": "", "mode": "sometimes", "max": 0,
    "trigger": [],
    "action": [],
}
CONFIGS["automations/bad_action.json"] = {
    "alias": "Morning", "description": 7,
    "trigger": [{"platform": "time", "at": "07:00:00"}],
    "condition": {"condition": "time"},
    "action": [{"service": "light turn on"}, {"wait": "00:01:00"}, {"delay": "1m"}],
}

CONFIGS["sites/static.json"] = {
    "listen": "8080", "host": "0.0.0.0", "root": "data/files/www",
    "upstreams": [{"name": "api", "url": "http://127.0.0.1:9000"}],
    "log_dir": "data/files/logs",
}
CONFIGS["sites/tls.json"] = {
    "listen": 443, "host": "10.0.0.5", "root": "data/files/www", "public_url": "https://shop.example.com",
    "tls": {"cert": "data/files/tls/server.pem", "key": "data/files/tls/server.key", "protocols": ["TLSv1.2", "TLSv1.3"]},
    "upstreams": [{"name": "app-1", "url": "http://10.0.0.11:8000", "weight": 3},
                  {"name": "app-2", "url": "http://10.0.0.12:8000", "backup": "yes"}],
    "workers": 16, "gzip": "off",
}
CONFIGS["sites/broken.json"] = {
    "listen": 70000, "host": "localhost", "root": "data/files/www/index.html", "public_url": "http://intranet",
    "tls": {"cert": "data/files/tls/missing.pem", "key": "data/files/tls", "protocols": ["TLSv1.3", "TLSv1.3", "SSLv3"]},
    "upstreams": [{"name": "App", "url": "10.0.0.11:8000", "weight": 0}, {"url": "http://x"}],
    "log_dir": "data/files/missing", "workers": "8",
}
CONFIGS["sites/minimal.json"] = {"listen": 80, "root": "data/files/www"}
CONFIGS["sites/empty_upstreams.json"] = {
    "listen": 80, "host": "::", "root": "data/files/www", "upstreams": [], "index": None, "cache": True,
}

CONFIGS["compose/shop.json"] = {
    "version": 3.9,
    "services": {
        "web": {"image": "nginx:1.27", "ports": ["8080:80", 443], "depends_on": ["api"], "restart": "always"},
        "api": {"build": {"context": "./api", "dockerfile": "Dockerfile.prod"},
                "environment": {"DATABASE_URL": "postgres://db/shop", "WORKERS": 4, "DEBUG": False, "EMPTY": None},
                "replicas": "3", "command": ["gunicorn", "app:app"]},
        "db": {"image": "postgres:16-alpine", "environment": ["POSTGRES_DB=shop", "POSTGRES_PASSWORD=not-a-real-password"]},
    },
    "volumes": {"dbdata": None, "uploads": {"driver": "nfs"}, "cache": {}},
}
CONFIGS["compose/broken.json"] = {
    "version": "2",
    "services": {
        "Web": {"image": "nginx"},
        "worker": {"image": "app:latest", "build": "."},
        "queue": {"image": "redis:7", "ports": ["6379", 6379.5], "restart": "sometimes", "replicas": 50},
        "cron": {"build": {"dockerfile": "Dockerfile"}, "environment": {"lower_case": "x", "OK": [1]}},
        "proxy": {"environment": ["GOOD=1", "bad"], "command": 5, "healthcheck": {"test": "curl"}},
    },
    "volumes": {"data": {"driver": 5}},
}
CONFIGS["compose/no_services.json"] = {"version": "3.8", "services": {}, "networks": {"front": {}, "back": "bridge"}}

CONFIGS["menus/editor.json"] = {
    "label": "File",
    "children": [
        {"label": "New", "action": "file.new", "shortcut": "Ctrl+N"},
        {"label": "Open recent", "children": [
            {"label": "notes.md", "action": "file.open_recent"},
            {"label": "More", "children": [{"label": "Clear list", "action": "file.clear_recent"}]},
        ]},
        {"label": "Save as", "action": "file.save_as", "shortcut": "Ctrl+Shift+S"},
    ],
}
CONFIGS["menus/broken.json"] = {
    "label": "Edit",
    "children": [
        {"label": "Undo", "action": "edit.undo", "shortcut": "Ctrl+z"},
        {"label": "Find", "children": [
            {"label": "", "action": "find"},
            {"label": "Replace", "children": [{"action": "edit.replace"}, "separator"]},
        ]},
        {"label": "Paste", "action": "Edit.Paste", "shortcut": "Cmd+V", "children": {}},
    ],
}

CONFIGS["flags/prod.json"] = {
    "new_checkout": {"rollout": "25", "groups": ["beta", "staff"], "until": "2024-12-31"},
    "dark_mode": "on",
    "legacy_search": False,
    "fast_cart": {"rollout": 100},
}
CONFIGS["flags/broken.json"] = {
    "new_checkout": {"rollout": 120, "groups": ["vip"]},
    "dark_mode": "sometimes",
    "beta_banner": {"until": "2024-13-01"},
}

CONFIGS["signups/batch.json"] = [
    {"email": "  Ann.Lee@Example.COM ", "username": "ann_lee", "password": "Correct-Horse-9", "terms": True,
     "birthday": "1990-04-12", "website": "https://ann.example.com", "tags": ["Python", "rust"],
     "display_name": "  ann lee "},
    {"email": "bob@example", "username": "Bob!", "password": "password", "terms": False, "tags": ["a", "A"]},
    {"email": "carol@example.org", "username": "cc", "password": "NotARealPassw0rd", "terms": "yes",
     "newsletter": "nope", "website": None, "referrer": "spam.example"},
    {"username": "dave_1977", "password": "short1A!", "birthday": "1977-02-30", "website": "dave.example.com",
     "tags": ["a", "b", "c", "d", "e", "f"], "terms": 1},
    {"email": "erin@example.net", "username": "  erin  ", "password": 12345678901234, "terms": True,
     "tags": "music", "display_name": 5},
]

CONFIGS["invoices/2024-00117.json"] = {
    "number": "INV-2024-00117", "issued": "2024-07-02T09:30:00Z", "due": "2024-08-01", "currency": "EUR",
    "customer": {"name": "Acme GmbH", "vat_id": "DE123456789", "email": "billing@acme.example"},
    "lines": [{"sku": "abc-001", "qty": 3, "unit_price": "19.99"},
              {"sku": "XYZ-042", "qty": 1, "unit_price": "250.00", "discount": "0.1"}],
    "total": "29497.00", "notes": "Thank you for your business",
}
CONFIGS["invoices/2024-00118.json"] = {
    "number": "INV-24-118", "issued": "2024-07-02 09:30", "due": "2024-07-32", "currency": "eur",
    "customer": {"name": "", "vat_id": "de123", "phone": "+49 30 1234567"},
    "lines": [{"sku": "ab-1", "qty": 0, "unit_price": "19.9"}, {"sku": "XYZ-042", "qty": "2", "unit_price": 250},
              {"qty": 1, "unit_price": "1.00", "discount": 1}],
    "vat_rate": 0, "total": "1234567.891", "paid": "no",
}
CONFIGS["invoices/2024-00119.json"] = {
    "number": "INV-2024-00119", "issued": "2024-07-03T23:59:59Z", "due": "2024-08-02", "currency": "GBP",
    "customer": {"name": "Smith & Sons"}, "lines": [], "total": "0.00",
    "notes": "x" * 90, "vat_rate": "0.3",
}

CONFIGS["sensors/readings.json"] = [
    {"sensor": "temp-001", "at": "2024-07-02T10:00:00.000000Z", "celsius": "21.5", "humidity": 104, "battery": 87,
     "firmware": "1.2.0"},
    {"sensor": "temp-002", "at": "2024-07-02T10:00:00Z", "celsius": 90, "humidity": "-3"},
    {"sensor": "Temp-3", "at": "2024-07-02T10:00:00.5Z", "celsius": "warm", "battery": 101},
    {"at": "2024-07-02T10:00:00.250Z", "celsius": -40, "battery": 0},
]

# ------------------------------------------------------------ jobs
jobs = []


def file_job(schema_name, path):
    jobs.append({"schema": schema_name, "file": "configs/" + path})


for p in ["kitchen", "porch", "desk", "garden", "strip", "hall", "bulbs"]:
    file_job("ha_light", f"lights/{p}.json")
for p in ["kitchen", "garden", "hall"]:
    file_job("ha_light_zigbee", f"lights/{p}.json")
for p in ["hall", "kitchen"]:
    file_job("ha_light_lenient", f"lights/{p}.json")
    file_job("ha_light_tidy", f"lights/{p}.json")
for p in ["lights_at_sunset", "motion", "broken_trigger", "no_action", "bad_action"]:
    file_job("ha_automation", f"automations/{p}.json")
for p in ["static", "tls", "broken", "minimal", "empty_upstreams"]:
    file_job("web_server", f"sites/{p}.json")
for p in ["shop", "broken", "no_services"]:
    file_job("compose", f"compose/{p}.json")
for p in ["editor", "broken"]:
    file_job("menu", f"menus/{p}.json")
for p in ["prod", "broken"]:
    file_job("feature_flags", f"flags/{p}.json")
# each signup, invoice line and sensor reading on its own
jobs.append({"schema": "signup", "file": "configs/signups/batch.json", "each": True})
for p in ["2024-00117", "2024-00118", "2024-00119"]:
    file_job("invoice", f"invoices/{p}.json")
jobs.append({"schema": "sensor_reading", "file": "configs/sensors/readings.json", "each": True})
# Schema.infer from one document, then the others checked against it
jobs.append({"infer": "configs/lights/kitchen.json",
             "check": ["configs/lights/porch.json", "configs/lights/kitchen.json"]})
jobs.append({"infer": "configs/compose/shop.json", "check": ["configs/compose/broken.json"]})
jobs.append({"infer": "configs/menus/editor.json", "check": ["configs/menus/broken.json"]})

for name, docs in U:
    for d in docs:
        jobs.append({"schema": name, "data": d})

# ------------------------------------------------------------ write
def write(path, text):
    full = os.path.join("data", path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", newline="\n") as f:
        f.write(text)


if os.path.exists("data"):
    import shutil
    shutil.rmtree("data")
for p, t in FILES.items():
    write(p, t)
for p, doc in CONFIGS.items():
    write("configs/" + p, json.dumps(doc, indent=2) + "\n")
write("schemas.json", "[\n" + ",\n".join(json.dumps(s) for s in schemas) + "\n]\n")
write("jobs.jsonl", "".join(json.dumps(j) + "\n" for j in jobs))
print(f"{len(schemas)} schemas, {len(CONFIGS)} documents, {len(jobs)} jobs")
