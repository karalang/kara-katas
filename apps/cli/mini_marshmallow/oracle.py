# Runs data/jobs.tsv through marshmallow 4.3.1 (the marshmallow/ package
# next to this file, unchanged) and prints what it did.
# mini_marshmallow.kara must print the same bytes.
#
# The schemas are described in data/schemas.json; this file turns each
# description into a Schema class the way an application would write it,
# with the hooks, methods and field functions below.
import datetime
import enum
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from marshmallow import Schema, ValidationError, fields, validate  # noqa: E402
from marshmallow import post_dump, post_load, pre_dump, pre_load, validates, validates_schema  # noqa: E402
from marshmallow.constants import missing  # noqa: E402

OUT = []


def emit(s):
    OUT.append(s)


def read(rel):
    with open(os.path.join(HERE, "data", rel), encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------- printing

def key_order(k):
    return (0, k, "") if isinstance(k, int) else (1, 0, k)


def show(v):
    if isinstance(v, dict):
        items = sorted(v.items(), key=lambda kv: key_order(kv[0]))
        return "{" + ", ".join(show(k) + ": " + show(x) for k, x in items) + "}"
    if isinstance(v, list):
        return "[" + ", ".join(show(x) for x in v) + "]"
    if isinstance(v, tuple):
        if len(v) == 1:
            return "(" + show(v[0]) + ",)"
        return "(" + ", ".join(show(x) for x in v) + ")"
    if v is missing:
        return "<missing>"
    return repr(v)


# ------------------------------------------------- what the app defines

def slugify(s):
    out = "".join(c if c.isascii() and c.isalnum() else "-" for c in s.lower())
    return "-".join(p for p in out.split("-") if p)


def half_even(x):
    return int(round(x))


FIELD_FUNCS = {
    "strip": lambda v: v.strip() if isinstance(v, str) else v,
    "lower": lambda v: v.lower() if isinstance(v, str) else v,
    "upper": lambda v: v.upper() if isinstance(v, str) else v,
    "split_commas": lambda v: [p.strip() for p in v.split(",")],
    "cents": lambda v: half_even(v * 100),
}


def v_even(value):
    if value % 2:
        raise ValidationError("Must be even.")


def v_not_blank(value):
    if not value.strip():
        raise ValidationError("Must not be blank.")


VALIDATORS = {"even": v_even, "not_blank": v_not_blank}

CALLABLES = {"new_list": lambda: []}


def to_cents(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValidationError("Not a whole number of cents.") from None


FUNCTIONS = {
    "word_count": lambda obj: len(obj.get("body", "").split()),
    "price_cents": lambda obj: obj.get("price_cents"),
    "to_cents": to_cents,
    "upper_first": lambda obj: obj["first"].upper(),
}

CANON = ["firstName", "lastName", "fullName", "born", "CODE", "tagList", "price", "note"]


def m_display_name(self, obj):
    return obj["username"] + " <" + obj["email"] + ">"


def m_full_name(self, obj):
    return (obj.get("first", "") + " " + obj.get("last", "")).strip()


def m_split_name(self, value):
    parts = value.split()
    if not parts:
        return {}
    return {"given": parts[0], "family": parts[-1]}


METHODS = {"display_name": m_display_name, "full_name": m_full_name, "split_name": m_split_name}


def h_check_username(self, value, data_key):
    if value in ("root", "admin", "system"):
        raise ValidationError(value + " is reserved.")


def h_check_title(self, value, data_key):
    if "banned" in value.lower():
        raise ValidationError("Title contains a banned word.")


def h_unwrap(self, data, **kw):
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    return data


def h_unwrap_many(self, data, **kw):
    if isinstance(data, dict) and "items" in data:
        return data["items"]
    return data


def h_drop_none(self, data, **kw):
    return {k: v for k, v in data.items() if v is not None}


def h_passwords_match(self, data, **kw):
    if data.get("password") != data.get("confirm"):
        raise ValidationError("Passwords do not match.", "confirm")


def h_adult_admin(self, data, **kw):
    if data.get("role") == "admin" and (data.get("age") or 0) < 18:
        raise ValidationError({"role": ["Admins must be adults."], "age": ["Too young for admin."]})


def h_ship_after_placed(self, data, **kw):
    if "ship_by" in data and "placed" in data and data["ship_by"] < data["placed"].date():
        raise ValidationError("Cannot ship before the order is placed.", "ship_by")


def h_compute_total(self, data, **kw):
    total = 0.0
    for item in data.get("items", []):
        total += item.get("qty", 1) * item.get("price", 0.0)
    data["total"] = total
    return data


def h_add_links(self, data, original, **kw):
    data["href"] = "/orders/" + str(original["id"])
    return data


def h_date_order(self, data, **kw):
    if "ends" in data and "starts" in data and data["ends"] <= data["starts"]:
        raise ValidationError("ends must be after starts.", "ends")


def h_add_slug(self, data, **kw):
    data["slug"] = slugify(data["title"])
    return data


def h_default_title(self, obj, **kw):
    obj = dict(obj)
    obj.setdefault("title", "Untitled")
    return obj


def h_total_size(self, data, **kw):
    total = data.get("size", 0)
    for c in data.get("children", []):
        total += c.get("total", 0)
    data["total"] = total
    return data


def h_unique_skus(self, data, **kw):
    if not isinstance(data, list):
        return
    skus = [d.get("sku") for d in data if isinstance(d, dict)]
    dups = sorted({s for s in skus if s is not None and skus.count(s) > 1})
    if dups:
        raise ValidationError("Duplicate SKUs: " + ", ".join(dups) + ".")


def h_sale_needs_stock(self, data, **kw):
    if "sale" in data.get("tags", []) and data.get("stock", 0) == 0:
        raise ValidationError("Items on sale must be in stock.", "stock")


def h_envelope(self, data, many, **kw):
    if many:
        return {"data": data, "count": len(data)}
    return {"data": data}


def h_lower_keys(self, data, **kw):
    if not isinstance(data, dict):
        return data
    out = {}
    for k, v in data.items():
        name = k
        for c in CANON:
            if c.lower() == k.lower():
                name = c
                break
        out[name] = v
    return out


def h_stamp(self, data, original, **kw):
    data["source_keys"] = sorted(original.keys())
    return data


def h_number_items(self, data, **kw):
    if isinstance(data, list):
        for i, d in enumerate(data):
            d["n"] = i
    return data


def h_fail_banned(self, data, **kw):
    if data.get("kind") == "banned":
        raise ValidationError("Banned kind.", "kind")
    return data


HOOKS = {
    "check_username": h_check_username, "check_title": h_check_title, "unwrap": h_unwrap,
    "unwrap_many": h_unwrap_many, "drop_none": h_drop_none, "passwords_match": h_passwords_match,
    "adult_admin": h_adult_admin, "ship_after_placed": h_ship_after_placed,
    "compute_total": h_compute_total, "add_links": h_add_links, "date_order": h_date_order,
    "add_slug": h_add_slug, "default_title": h_default_title, "total_size": h_total_size,
    "unique_skus": h_unique_skus, "sale_needs_stock": h_sale_needs_stock, "envelope": h_envelope,
    "lower_keys": h_lower_keys, "stamp": h_stamp, "number_items": h_number_items,
    "fail_banned": h_fail_banned,
}

# ----------------------------------------------- descriptions to classes

ENUM_TYPES = {}
SCHEMAS = {}
DESCS = {}


def default_of(v):
    if isinstance(v, dict) and "$fn" in v:
        return CALLABLES[v["$fn"]]
    return v


def tz_of(minutes):
    if minutes == 0:
        return datetime.timezone.utc
    return datetime.timezone(datetime.timedelta(minutes=minutes))


def make_validator(spec):
    if isinstance(spec, str):
        return VALIDATORS[spec]
    name, args = spec
    args = dict(args)
    if name == "Regexp":
        return validate.Regexp(args.pop("regex"), args.pop("flags", 0), **args)
    if name == "Equal":
        return validate.Equal(args.pop("comparable"), **args)
    if name in ("OneOf", "ContainsOnly"):
        return getattr(validate, name)(args.pop("choices"), **args)
    if name in ("NoneOf", "ContainsNoneOf"):
        return getattr(validate, name)(args.pop("iterable"), **args)
    return getattr(validate, name)(**args)


COMMON = ["required", "allow_none", "data_key", "attribute", "load_only", "dump_only", "error_messages"]


def make_field(spec):
    kind = spec["type"]
    kw = {k: spec[k] for k in COMMON if k in spec}
    if "load_default" in spec:
        kw["load_default"] = default_of(spec["load_default"])
    if "dump_default" in spec:
        kw["dump_default"] = default_of(spec["dump_default"])
    if "validate" in spec:
        kw["validate"] = [make_validator(v) for v in spec["validate"]]
    if "pre_load" in spec:
        kw["pre_load"] = [FIELD_FUNCS[f] for f in spec["pre_load"]]
    if "post_load" in spec:
        kw["post_load"] = [FIELD_FUNCS[f] for f in spec["post_load"]]
    for k in ("strict", "as_string", "allow_nan", "relative", "absolute", "schemes", "require_tld",
              "truthy", "falsy", "format", "precision", "only", "exclude", "many", "unknown"):
        if k in spec:
            kw[k] = spec[k]
    if "timezone" in spec:
        kw["timezone"] = tz_of(spec["timezone"])
    if "default_timezone" in spec:
        kw["default_timezone"] = tz_of(spec["default_timezone"])
    if kind == "List":
        return fields.List(make_field(spec["inner"]), **kw)
    if kind == "Tuple":
        return fields.Tuple([make_field(s) for s in spec["tuple_fields"]], **kw)
    if kind == "Dict":
        keys = make_field(spec["keys"]) if "keys" in spec else None
        values = make_field(spec["values"]) if "values" in spec else None
        return fields.Dict(keys=keys, values=values, **kw)
    if kind == "Nested":
        nested = spec["nested"]
        if isinstance(nested, dict):
            nested = {k: make_field(s) for k, s in nested.items()}
        return fields.Nested(nested, **kw)
    if kind == "Pluck":
        return fields.Pluck(spec["nested"], spec["field_name"], **kw)
    if kind == "Enum":
        by_value = spec.get("by_value", False)
        if isinstance(by_value, dict):
            by_value = make_field(by_value)
        return fields.Enum(ENUM_TYPES[spec["enum"]], by_value=by_value, **kw)
    if kind == "Constant":
        return fields.Constant(spec["constant"], **kw)
    if kind == "Method":
        return fields.Method(spec.get("serialize"), spec.get("deserialize"), **kw)
    if kind == "Function":
        ser = FUNCTIONS[spec["serialize"]] if "serialize" in spec else None
        de = FUNCTIONS[spec["deserialize"]] if "deserialize" in spec else None
        return fields.Function(ser, de, **kw)
    return getattr(fields, kind)(**kw)


DECORATORS = {"pre_load": pre_load, "post_load": post_load, "pre_dump": pre_dump, "post_dump": post_dump}


def wrap(fn):
    def hook(self, *args, **kwargs):
        return fn(self, *args, **kwargs)
    return hook


def build_schema(desc):
    """Builds the class, or returns the error building it raised."""
    base = SCHEMAS[desc["base"]] if "base" in desc else Schema
    attrs = {}
    for name, spec in desc["fields"]:
        attrs[name] = make_field(spec)
    for h in desc.get("hooks", []):
        fn = wrap(HOOKS[h["fn"]])
        tag = h["tag"]
        if tag == "validates":
            fn = validates(*h["field_names"])(fn)
        elif tag == "validates_schema":
            fn = validates_schema(pass_collection=h.get("pass_collection", False),
                                  pass_original=h.get("pass_original", False),
                                  skip_on_field_errors=h.get("skip_on_field_errors", True))(fn)
        elif tag == "pre_dump":
            fn = pre_dump(pass_collection=h.get("pass_collection", False))(fn)
        else:
            fn = DECORATORS[tag](pass_collection=h.get("pass_collection", False),
                                 **({"pass_original": True} if h.get("pass_original") else {}))(fn)
        attrs[h["fn"]] = fn
    for name, spec in desc["fields"]:
        for k in ("serialize", "deserialize"):
            if spec["type"] == "Method" and k in spec:
                attrs[spec[k]] = METHODS[spec[k]]
    if "meta" in desc:
        attrs["Meta"] = type("Meta", (), dict(desc["meta"]))
    if "error_messages" in desc:
        attrs["error_messages"] = desc["error_messages"]
    return type(desc["name"], (base,), attrs)


def load_schemas():
    spec = json.loads(read("schemas.json"))
    for name, members in spec["enums"].items():
        ENUM_TYPES[name] = enum.Enum(name, [(m, v) for m, v in members])
    for desc in spec["schemas"]:
        DESCS[desc["name"]] = desc
        try:
            SCHEMAS[desc["name"]] = build_schema(desc)
        except ValueError as e:
            SCHEMAS[desc["name"]] = e


# --------------------------------------------------------------- jobs

def ctor_args(opts):
    kw = dict(opts)
    for k in ("only", "exclude", "load_only", "dump_only"):
        if k in kw:
            kw[k] = tuple(kw[k])
    return kw


def call_args(opts):
    return dict(opts)


def instance(name, opts):
    cls = SCHEMAS[name]
    if isinstance(cls, Exception):
        raise cls
    return cls(**ctor_args(opts))


def show_error(e):
    emit("! " + type(e).__name__ + ": " + str(e))


def show_load(err):
    emit("errors " + show(err.messages))
    emit("valid " + show(err.valid_data))


def docs(name):
    return read("docs/" + name + ".jsonl").splitlines()


def run_load(cols):
    kind, name, ctor, call, docname = cols
    try:
        s = instance(name, json.loads(ctor))
    except ValueError as e:
        show_error(e)
        return
    kw = call_args(json.loads(call))
    for line in docs(docname):
        emit("> " + line)
        data = json.loads(line)
        if kind == "validate":
            emit("validate " + show(s.validate(data, **{k: v for k, v in kw.items() if k != "unknown"})))
            continue
        try:
            result = s.load(data, **kw)
        except ValidationError as err:
            show_load(err)
            continue
        emit("ok " + show(result))
        if kind == "roundtrip":
            many = kw.get("many")
            emit("= " + json.dumps(s.dump(result, many=many)))


def run_dump(cols):
    _, name, ctor, call, loader, lcall, docname = cols
    try:
        s = instance(name, json.loads(ctor))
    except ValueError as e:
        show_error(e)
        return
    ld = instance(loader, {})
    lkw = call_args(json.loads(lcall))
    kw = call_args(json.loads(call))
    for line in docs(docname):
        emit("> " + line)
        try:
            obj = ld.load(json.loads(line), **lkw)
        except ValidationError as err:
            emit("skipped " + show(err.messages))
            continue
        emit("= " + json.dumps(s.dump(obj, **kw)))


def run_init(cols):
    _, name, ctor = cols
    try:
        s = instance(name, json.loads(ctor))
    except ValueError as e:
        show_error(e)
        return
    emit("fields " + ", ".join(s.fields))
    emit("load " + ", ".join(s.load_fields))
    emit("dump " + ", ".join(s.dump_fields))


def main():
    load_schemas()
    for line in read("jobs.tsv").splitlines():
        if line.startswith("== "):
            emit(line)
            continue
        cols = line.split("\t")
        emit("-- " + " ".join(cols[:4]))
        if cols[0] in ("load", "validate", "roundtrip"):
            run_load(cols)
        elif cols[0] == "dump":
            run_dump(cols)
        else:
            run_init(cols)
    sys.stdout.write("\n".join(OUT) + "\n")


main()
