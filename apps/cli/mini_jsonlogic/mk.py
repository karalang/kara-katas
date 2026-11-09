"""Writes data/ for mini_jsonlogic: the feature flags of a small web shop
written as JsonLogic rules, the users they are decided for, and a file of
single cases, each a rule and the data it runs on, that go through every
operation and the module's JavaScript-style coercions.

Every file is JSON; `cases.jsonl` holds one `[name, logic, data]` array
per line. No number in them is `-0`, NaN, an infinity or too big for an
i64 (README.md says why).

Run from this directory: python3 -s -P -B mk.py"""
import json
import os

FLAGS = {
    "new_checkout": {"and": [
        {"==": [{"var": "country"}, "NL"]},
        {">=": [{"var": "orders"}, 3]},
    ]},
    "beta_banner": {"in": [{"var": "plan"}, ["beta", "staff"]]},
    "free_shipping": {"or": [
        {">": [{"reduce": [{"var": "cart"},
                           {"+": [{"var": "accumulator"}, {"var": "current.price"}]},
                           0]}, 50]},
        {"==": [{"var": "plan"}, "gold"]},
    ]},
    "age_gate": {"<=": [18, {"var": "age"}, 120]},
    "needs_profile": {"missing_some": [2, ["email", "phone", "address.city"]]},
    "late_night": {"if": [
        {"<": [{"var": "hour"}, 6]}, True,
        {">=": [{"var": "hour"}, 22]}, True,
        False,
    ]},
    "bulk_buyer": {"some": [{"var": "cart"}, {">=": [{"var": "qty"}, 10]}]},
    "all_digital": {"all": [{"var": "cart"}, {"var": "digital"}]},
    "vip_email": {"in": ["@vip.", {"var": "email"}]},
}

USERS = [
    {"name": "ana", "country": "NL", "orders": 5, "plan": "gold", "age": 34,
     "email": "ana@vip.example.org", "hour": 23,
     "cart": [{"price": 20, "qty": 1, "digital": True},
              {"price": 12.5, "qty": 2, "digital": True}]},
    {"name": "bo", "country": "nl", "orders": "7", "plan": "beta", "age": "17",
     "phone": "", "hour": 9,
     "cart": [{"price": 40, "qty": 12, "digital": False},
              {"price": 15, "qty": 1}]},
    {"name": "cy", "country": "NL", "orders": 3.0, "plan": None, "age": 120,
     "email": "cy@example.org", "phone": "555-0100", "address": {"city": "Utrecht"},
     "hour": "5", "cart": []},
    {"name": "dee", "age": [42], "hour": None, "cart": "none"},
]

# [name, logic, data]
CASES = [
    # Literals and the shape of a rule.
    ["literal", 42, None],
    ["literal list", [1, {"var": "a"}, "x"], {"a": True}],
    ["two keys is data", {"var": "a", "cat": "b"}, {"a": 1}],
    ["empty object", {}, None],
    ["unknown op", {"frobnicate": [1]}, None],
    ["dotted unknown", {"no.such": [1]}, None],
    ["dotted known", {"cat.x": [1]}, None],

    # var.
    ["var path", {"var": "user.address.city"}, {"user": {"address": {"city": "Leiden"}}}],
    ["var default", {"var": ["user.zip", "00000"]}, {"user": {}}],
    ["var whole", {"var": ""}, {"a": [1, 2]}],
    ["var null key", {"var": None}, [3]],
    ["var index", {"var": 1}, ["a", "b", "c"]],
    ["var index path", {"var": "items.1.name"}, {"items": [{"name": "x"}, {"name": "y"}]}],
    ["var float index", {"var": 1.0}, ["a", "b"]],
    ["var fraction", {"var": [1.5, "none"]}, ["a", "b"]],
    ["var true index", {"var": True}, ["a", "b"]],
    ["var negative", {"var": [-1, "none"]}, ["a", "b"]],
    ["var string index", {"var": "1"}, "hello"],
    ["var length", {"var": "tags.length"}, {"tags": ["a", "b", "c"]}],
    ["var text length", {"var": "word.length"}, {"word": "naïve"}],
    ["var padded index", {"var": ["01", "nope"]}, ["a", "b"]],
    ["var into number", {"var": ["a.b", "d"]}, {"a": 5}],
    ["var number on object", {"var": [0, "d"]}, {"0": "zero"}],
    ["var null value", {"var": ["a", "d"]}, {"a": None}],
    ["var too many", {"var": ["a", 1, 2]}, {"a": 1}],

    # Equality: the loose kind and the strict kind.
    ["eq num str", {"==": [1, "1"]}, None],
    ["eq num str space", {"==": [1, " 1 "]}, None],
    ["eq bool str", {"==": [True, "1"]}, None],
    ["eq str bool", {"==": ["0", False]}, None],
    ["eq null null", {"==": [None, None]}, None],
    ["eq null zero", {"==": [None, 0]}, None],
    ["eq list str", {"==": [[1, 2], "1,2"]}, None],
    ["eq list list", {"==": [[1], [1]]}, None],
    ["eq list num", {"==": [[7], 7]}, None],
    ["eq obj str", {"==": [{"var": "o"}, "[object Object]"]}, {"o": {"a": 1}}],
    ["object is an op", {"==": [{"a": 1}, "[object Object]"]}, None],
    ["eq float int", {"==": [2.0, 2]}, None],
    ["eq underscore", {"==": [1000, "1_000"]}, None],
    ["ne", {"!=": [1, "2"]}, None],
    ["strict int float", {"===": [1, 1.0]}, None],
    ["strict bool int", {"===": [True, 1]}, None],
    ["strict num str", {"===": [1, "1"]}, None],
    ["strict lists", {"===": [[1, [2]], [1, [2]]]}, None],
    ["strict not", {"!==": [1, "1"]}, None],

    # Ordering, with the three-argument between.
    ["lt", {"<": [1, 2]}, None],
    ["lt str num", {"<": ["10", 9]}, None],
    ["lt strings", {"<": ["apple", "banana"]}, None],
    ["lt str list", {"<": ["a", ["b"]]}, None],
    ["lt nulls", {"<": [None, None]}, None],
    ["lt null str", {"<": [None, "x"]}, None],
    ["lt objects", {"<": [{}, 1]}, None],
    ["between", {"<": [1, 5, 10]}, None],
    ["between edge", {"<=": [1, 1, 1]}, None],
    ["between null", {"<": [1, 2, None]}, None],
    ["gt", {">": ["b", "a"]}, None],
    ["ge mixed", {">=": [2, "2.0"]}, None],
    ["gt nan", {">": ["abc", 0]}, None],

    # Truth.
    ["not empty list", {"!": [[]]}, None],
    ["not list", {"!": [[0]]}, None],
    ["not object", {"!": {}}, None],
    ["double bang", {"!!": ["0"]}, None],
    ["bang zero float", {"!": 0.0}, None],
    ["and", {"and": [1, "a", [], "b"]}, None],
    ["and all", {"and": [1, "a", True]}, None],
    ["and empty", {"and": []}, None],
    ["or", {"or": [0, "", "x", "y"]}, None],
    ["or none", {"or": [0, False]}, None],
    ["if chain", {"if": [False, 1, None, 2, "x", 3, 4]}, None],
    ["if no else", {"if": [False, 1]}, None],
    ["if bare", {"if": True}, None],
    ["ternary", {"?:": [{"var": "ok"}, "yes", "no"]}, {"ok": [0]}],

    # Arithmetic.
    ["add ints", {"+": [1, 2, 3]}, None],
    ["add strs", {"+": ["1", "2.5"]}, None],
    ["add bools", {"+": [True, True]}, None],
    ["add null", {"+": [None, 4]}, None],
    ["add empty", {"+": []}, None],
    ["add junk", {"+": [1, "one"]}, None],
    ["add infinity", {"+": [1, "Infinity"]}, None],
    ["add inf", {"+": [1, "inf"]}, None],
    ["add list", {"+": [[2], 3]}, None],
    ["mul", {"*": [2, "3", 0.5]}, None],
    ["mul bool", {"*": [True, False]}, None],
    ["minus", {"-": [10, 4]}, None],
    ["negate", {"-": "7"}, None],
    ["negate null b", {"-": [5, None]}, None],
    ["negate bool", {"-": [True]}, None],
    ["div", {"/": [7, 2]}, None],
    ["div exact", {"/": [8, 4]}, None],
    ["div zero", {"/": [1, 0]}, None],
    ["div float zero", {"/": [1.5, 0]}, None],
    ["div nan zero", {"/": ["x", 0]}, None],
    ["mod", {"%": [7, 3]}, None],
    ["mod negative", {"%": [-7, 3]}, None],
    ["mod float", {"%": [-7.5, 2]}, None],
    ["mod float divisor", {"%": [7, -2.5]}, None],
    ["mod zero", {"%": [1, 0]}, None],
    ["mod float zero", {"%": [1.0, 0]}, None],
    ["mod exact neg", {"%": [-4.0, 2]}, None],
    ["min", {"min": [3, "1", 2]}, None],
    ["min first", {"min": [1, 1.0, True]}, None],
    ["max bool", {"max": [True, 0]}, None],
    ["max nan first", {"max": ["x", 5]}, None],
    ["max nan later", {"max": [5, "x", 9]}, None],
    ["min empty", {"min": []}, None],
    ["tiny", {"*": [0.1, 0.00001]}, None],
    ["big float", {"*": [12345678, 1e9, 10]}, None],
    ["third", {"/": [1, 3]}, None],

    # Strings.
    ["cat", {"cat": ["I love ", {"var": "x"}, "!"]}, {"x": "pie"}],
    ["cat coerce", {"cat": [1, 2.5, None, True, False, [1, [2, 3]], {"var": "o"}]}, {"o": {"k": 1}}],
    ["cat float", {"cat": [{"/": [1, 3]}, " ", 1e21, " ", 0.1, " ", 1e-7, " ", 100.0]}, None],
    ["cat precision", {"cat": [{"*": [123456789, 1000000, 10]}]}, None],
    ["substr", {"substr": ["jsonlogic", 4]}, None],
    ["substr neg", {"substr": ["jsonlogic", -5]}, None],
    ["substr len", {"substr": ["jsonlogic", 1, 3]}, None],
    ["substr neg len", {"substr": ["jsonlogic", 4, -2]}, None],
    ["substr past", {"substr": ["abc", 10, 2]}, None],
    ["substr far neg", {"substr": ["abc", -10]}, None],
    ["substr nan", {"substr": ["abc", "x", "y"]}, None],
    ["substr unicode", {"substr": ["naïve café", -4, 3]}, None],
    ["substr float", {"substr": ["abcdef", 1.9, 2.9]}, None],
    ["substr number", {"substr": [12345, 1, 2]}, None],
    ["in str", {"in": ["Spring", "Springfield"]}, None],
    ["in str num", {"in": [1, "a1b"]}, None],
    ["in list", {"in": ["b", ["a", "b"]]}, None],
    ["in list loose", {"in": [1, [True]]}, None],
    ["in list nested", {"in": [[1], [[1], 2]]}, None],
    ["in other", {"in": ["a", {"var": "o"}]}, {"o": {"a": 1}}],

    # Lists.
    ["merge", {"merge": [[1, 2], 3, [[4]], None]}, None],
    ["merge empty", {"merge": []}, None],
    ["map", {"map": [{"var": "xs"}, {"*": [{"var": ""}, 2]}]}, {"xs": [1, 2, 3]}],
    ["map not list", {"map": [{"var": "xs"}, 1]}, {"xs": "abc"}],
    ["map no logic", {"map": [[1, 2]]}, None],
    ["filter", {"filter": [{"var": "xs"}, {">": [{"var": ""}, 1]}]}, {"xs": [0, 1, 2, 3]}],
    ["filter short", {"filter": [[1]]}, None],
    ["reduce", {"reduce": [{"var": "xs"}, {"+": [{"var": "current"}, {"var": "accumulator"}]}, 0]}, {"xs": [1, 2, 3]}],
    ["reduce raw init", {"reduce": [[], 1, {"+": [1, 1]}]}, None],
    ["reduce not list", {"reduce": [5, 1, "init"]}, None],
    ["reduce context", {"reduce": [[1, 2], {"var": "current"}]}, None],
    ["reduce empty", {"reduce": []}, None],
    ["all", {"all": [[1, 2, 3], {">": [{"var": ""}, 0]}]}, None],
    ["all empty", {"all": [[], True]}, None],
    ["some", {"some": [{"var": "xs"}, {"==": [{"var": ""}, "b"]}]}, {"xs": ["a", "b"]}],
    ["none", {"none": [[1, 2], {">": [{"var": ""}, 5]}]}, None],
    ["none not list", {"none": ["xs", True]}, None],
    ["some short", {"some": [[1]]}, None],

    # missing and missing_some.
    ["missing", {"missing": ["a", "b", "c.d"]}, {"a": 1, "c": {"d": ""}}],
    ["missing list", {"missing": [["x", "y"]]}, {"y": 0}],
    ["missing number", {"missing": [0, 2]}, ["here", None]],
    ["missing some", {"missing_some": [1, ["a", "b"]]}, {"b": 2}],
    ["missing some short", {"missing_some": [2, ["a", "b", "c"]]}, {"b": 2}],
    ["missing some junk", {"missing_some": ["two", ["a"]]}, {}],
    ["missing some no list", {"missing_some": [1, "a"]}, None],
    ["missing in if", {"if": [{"missing": "x"}, "need x", "ok"]}, {"x": False}],

    # log writes the value and returns it.
    ["log", {"log": {"cat": ["café ", 3.0]}}, None],
    ["log object", {"+": [1, {"log": {"var": "o.n"}}]}, {"o": {"n": 2}}],
    ["log nothing", {"log": []}, None],
    ["log special", {"log": [{"/": [{"+": [1, "Infinity"]}, 1]}]}, None],
]

os.makedirs("data", exist_ok=True)
with open("data/flags.json", "w", encoding="utf-8", newline="") as fh:
    json.dump(FLAGS, fh, indent=2)
    fh.write("\n")
with open("data/users.json", "w", encoding="utf-8", newline="") as fh:
    json.dump(USERS, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
with open("data/cases.jsonl", "w", encoding="utf-8", newline="") as fh:
    for case in CASES:
        fh.write(json.dumps(case, ensure_ascii=False) + "\n")
