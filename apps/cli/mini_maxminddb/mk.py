"""Writes data/ for mini_maxminddb: MaxMind DB files built here from the
format specification (a GeoIP2-City-style database, a GeoLite2-Country-
and a GeoLite2-ASN-style one, a decoder test database with every data
type, and nine broken ones), an access log, a firewall policy and
data/jobs.txt, the commands the run executes. The networks and places
are test data, not real allocations.

Run from this directory: python3 -s -P -B mk.py"""
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
MARKER = b"\xab\xcd\xefMaxMind.com"


# ------------------------------------------------------------ addresses

def v4_int(s):
    a, b, c, d = (int(x) for x in s.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def v6_int(s):
    import ipaddress
    return int(ipaddress.IPv6Address(s))


def net_bits(net, ip_version):
    """The bits of a network in the tree, most significant first."""
    addr, plen = net.split("/")
    plen = int(plen)
    if ":" in addr:
        n, width = v6_int(addr), 128
    else:
        n, width = v4_int(addr), 32
        if ip_version == 6:
            width = 128
            plen += 96
    return [(n >> (width - 1 - i)) & 1 for i in range(plen)]


# ------------------------------------------------------------ data section

class T:
    """A value with an explicit MaxMind DB type."""
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value


def ctrl(type_num, size):
    out = bytearray()
    first = (type_num << 5) if type_num <= 7 else 0
    if size < 29:
        first |= size
        tail = b""
    elif size < 285:
        first |= 29
        tail = bytes([size - 29])
    elif size < 65821:
        first |= 30
        tail = struct.pack(">H", size - 285)
    else:
        first |= 31
        tail = struct.pack(">I", size - 65821)[1:]
    out.append(first)
    if type_num > 7:
        out.append(type_num - 7)
    out += tail
    return bytes(out)


def uint_bytes(n):
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return b


def pointer(p):
    if p < 2048:
        return bytes([0x20 | (p >> 8), p & 0xFF])
    if p < 526336:
        q = p - 2048
        return bytes([0x28 | (q >> 16), (q >> 8) & 0xFF, q & 0xFF])
    if p < 134744064:
        q = p - 526336
        return bytes([0x30 | (q >> 24), (q >> 16) & 0xFF, (q >> 8) & 0xFF, q & 0xFF])
    return bytes([0x38]) + struct.pack(">I", p)


def key_of(v):
    if isinstance(v, T):
        return ("T", v.kind, key_of(v.value) if v.kind in ("arr",) else repr(v.value))
    if isinstance(v, dict):
        return ("map", tuple((k, key_of(x)) for k, x in v.items()))
    if isinstance(v, list):
        return ("arr", tuple(key_of(x) for x in v))
    return (type(v).__name__, repr(v))


class Data:
    def __init__(self, dedup=True):
        self.buf = bytearray()
        self.cache = {}
        self.dedup = dedup

    def write(self, v):
        """Writes v at the end and returns its offset, or reuses an earlier
        copy through a pointer."""
        k = key_of(v)
        big = isinstance(v, (dict, list)) or (isinstance(v, str) and len(v.encode()) >= 3)
        if self.dedup and big and k in self.cache:
            off = len(self.buf)
            self.buf += pointer(self.cache[k])
            return off
        off = len(self.buf)
        self.emit(v)
        if big:
            self.cache.setdefault(k, off)
        return off

    def emit(self, v):
        b = self.buf
        if isinstance(v, T):
            kind, x = v.kind, v.value
            if kind == "u16":
                p = uint_bytes(x)
                b += ctrl(5, len(p)) + p
            elif kind == "u32":
                p = uint_bytes(x)
                b += ctrl(6, len(p)) + p
            elif kind == "u64":
                p = uint_bytes(x)
                b += ctrl(9, len(p)) + p
            elif kind == "u128":
                p = uint_bytes(x)
                b += ctrl(10, len(p)) + p
            elif kind == "i32":
                p = struct.pack(">i", x)
                if x >= 0:
                    p = p.lstrip(b"\x00")
                b += ctrl(8, len(p)) + p
            elif kind == "f32":
                b += ctrl(15, 4) + struct.pack(">f", x)
            elif kind == "raw":
                b += x
            else:
                raise ValueError(kind)
        elif isinstance(v, bool):
            b += ctrl(14, 1 if v else 0)
        elif isinstance(v, int):
            p = uint_bytes(v)
            b += ctrl(6 if v < 2**32 else 9, len(p)) + p
        elif isinstance(v, float):
            b += ctrl(3, 8) + struct.pack(">d", v)
        elif isinstance(v, str):
            p = v.encode()
            b += ctrl(2, len(p)) + p
        elif isinstance(v, bytes):
            b += ctrl(4, len(v)) + v
        elif isinstance(v, dict):
            b += ctrl(7, len(v))
            for k, x in v.items():
                self.write(k)
                self.write(x)
        elif isinstance(v, list):
            b += ctrl(11, len(v))
            for x in v:
                self.write(x)
        else:
            raise TypeError(type(v))


def plain(v):
    """A value written with no pointers, for the metadata."""
    d = Data(dedup=False)
    d.write(v)
    return bytes(d.buf)


# ------------------------------------------------------------ the tree

class Node:
    def __init__(self):
        self.kids = [None, None]


class Leaf:
    def __init__(self, data):
        self.data = data


class Alias:
    pass


def build(ip_version, record_size, inserts, metadata, aliases=True, data=None, raw_leaf=None):
    """inserts: (network, value) pairs. Returns the file bytes."""
    root = Node()
    data = data or Data()
    leaves = []
    ordered = sorted(enumerate(inserts), key=lambda p: (len(net_bits(p[1][0], ip_version)), p[0]))
    for _, (net, value) in ordered:
        bits = net_bits(net, ip_version)
        node = root
        for depth, bit in enumerate(bits):
            last = depth == len(bits) - 1
            child = node.kids[bit]
            if last:
                leaf = Leaf(value)
                leaves.append(leaf)
                node.kids[bit] = leaf
                break
            if child is None:
                child = Node()
                node.kids[bit] = child
            elif isinstance(child, Leaf):
                split = Node()
                split.kids = [child, Leaf(child.data)]
                leaves.append(split.kids[1])
                node.kids[bit] = split
                child = split
            node = child
    ipv4_root = None
    if ip_version == 6 and aliases:
        node = root
        for _ in range(96):
            if node.kids[0] is None:
                node.kids[0] = Node()
            node = node.kids[0]
        ipv4_root = node
        for net in ["::ffff:0:0/96", "2002::/16"]:
            bits = net_bits(net, 6)
            node = root
            for depth, bit in enumerate(bits):
                if depth == len(bits) - 1:
                    node.kids[bit] = Alias()
                    break
                if node.kids[bit] is None:
                    node.kids[bit] = Node()
                node = node.kids[bit]
    # number the nodes breadth first
    order = []
    number = {}
    queue = [root]
    while queue:
        n = queue.pop(0)
        number[id(n)] = len(order)
        order.append(n)
        for k in n.kids:
            if isinstance(k, Node) and id(k) not in number:
                queue.append(k)
    node_count = len(order)
    # the data section, in tree order
    offsets = {}
    for n in order:
        for k in n.kids:
            if isinstance(k, Leaf) and id(k) not in offsets:
                offsets[id(k)] = data.write(k.data)

    def value_of(k):
        if k is None:
            return node_count
        if isinstance(k, Alias):
            return number[id(ipv4_root)]
        if isinstance(k, Node):
            return number[id(k)]
        if raw_leaf is not None and raw_leaf(k.data) is not None:
            return raw_leaf(k.data)
        return node_count + 16 + offsets[id(k)]

    tree = bytearray()
    for n in order:
        a, b = value_of(n.kids[0]), value_of(n.kids[1])
        tree += records(record_size, a, b)
    meta = dict(metadata)
    meta["node_count"] = T("u32", node_count)
    md = {}
    for k in ["binary_format_major_version", "binary_format_minor_version", "build_epoch", "database_type", "description", "ip_version", "languages", "node_count", "record_size"]:
        if k in meta:
            md[k] = meta[k]
    for k in meta:
        if k not in md:
            md[k] = meta[k]
    return bytes(tree) + bytes(16) + bytes(data.buf) + MARKER + plain(md)


def records(record_size, a, b):
    if record_size == 24:
        return a.to_bytes(3, "big") + b.to_bytes(3, "big")
    if record_size == 28:
        return a.to_bytes(4, "big")[1:] + bytes([((a >> 24) << 4) | (b >> 24)]) + b.to_bytes(4, "big")[1:]
    if record_size == 32:
        return a.to_bytes(4, "big") + b.to_bytes(4, "big")
    # an unknown size: five bytes a node, written as 24-bit records
    return a.to_bytes(3, "big") + b.to_bytes(2, "big")


def metadata(db_type, ip_version, record_size, description, languages, epoch):
    return {
        "binary_format_major_version": T("u16", 2),
        "binary_format_minor_version": T("u16", 0),
        "build_epoch": T("u64", epoch),
        "database_type": db_type,
        "description": description,
        "ip_version": T("u16", ip_version),
        "languages": languages,
        "record_size": T("u16", record_size),
    }


# ------------------------------------------------------------ places

LANGS = ["de", "en", "es", "fr", "ja", "pt-BR", "ru", "zh-CN"]

CONTINENTS = {
    "AF": (6255146, {"de": "Afrika", "en": "Africa", "es": "África", "fr": "Afrique", "ja": "アフリカ", "pt-BR": "África", "ru": "Африка", "zh-CN": "非洲"}),
    "AS": (6255147, {"de": "Asien", "en": "Asia", "es": "Asia", "fr": "Asie", "ja": "アジア", "pt-BR": "Ásia", "ru": "Азия", "zh-CN": "亚洲"}),
    "EU": (6255148, {"de": "Europa", "en": "Europe", "es": "Europa", "fr": "Europe", "ja": "ヨーロッパ", "pt-BR": "Europa", "ru": "Европа", "zh-CN": "欧洲"}),
    "NA": (6255149, {"de": "Nordamerika", "en": "North America", "es": "Norteamérica", "fr": "Amérique du Nord", "ja": "北アメリカ", "pt-BR": "América do Norte", "ru": "Северная Америка", "zh-CN": "北美洲"}),
    "OC": (6255151, {"de": "Ozeanien", "en": "Oceania", "es": "Oceanía", "fr": "Océanie", "ja": "オセアニア", "pt-BR": "Oceania", "ru": "Океания", "zh-CN": "大洋洲"}),
    "SA": (6255150, {"de": "Südamerika", "en": "South America", "es": "Sudamérica", "fr": "Amérique du Sud", "ja": "南アメリカ", "pt-BR": "América do Sul", "ru": "Южная Америка", "zh-CN": "南美洲"}),
}

COUNTRIES = {
    "GB": (2635167, "EU", False, {"de": "Vereinigtes Königreich", "en": "United Kingdom", "es": "Reino Unido", "fr": "Royaume-Uni", "ja": "イギリス", "pt-BR": "Reino Unido", "ru": "Великобритания", "zh-CN": "英国"}),
    "FR": (3017382, "EU", True, {"de": "Frankreich", "en": "France", "es": "Francia", "fr": "France", "ja": "フランス共和国", "pt-BR": "França", "ru": "Франция", "zh-CN": "法国"}),
    "DE": (2921044, "EU", True, {"de": "Deutschland", "en": "Germany", "es": "Alemania", "fr": "Allemagne", "ja": "ドイツ連邦共和国", "pt-BR": "Alemanha", "ru": "Германия", "zh-CN": "德国"}),
    "PL": (798544, "EU", True, {"de": "Polen", "en": "Poland", "es": "Polonia", "fr": "Pologne", "ja": "ポーランド共和国", "pt-BR": "Polônia", "ru": "Польша", "zh-CN": "波兰"}),
    "IS": (2629691, "EU", False, {"de": "Island", "en": "Iceland", "es": "Islandia", "fr": "Islande", "ja": "アイスランド共和国", "pt-BR": "Islândia", "ru": "Исландия", "zh-CN": "冰岛"}),
    "JP": (1861060, "AS", False, {"de": "Japan", "en": "Japan", "es": "Japón", "fr": "Japon", "ja": "日本", "pt-BR": "Japão", "ru": "Япония", "zh-CN": "日本"}),
    "IN": (1269750, "AS", False, {"de": "Indien", "en": "India", "es": "India", "fr": "Inde", "ja": "インド", "pt-BR": "Índia", "ru": "Индия", "zh-CN": "印度"}),
    "BR": (3469034, "SA", False, {"de": "Brasilien", "en": "Brazil", "es": "Brasil", "fr": "Brésil", "ja": "ブラジル連邦共和国", "pt-BR": "Brasil", "ru": "Бразилия", "zh-CN": "巴西"}),
    "AU": (2077456, "OC", False, {"de": "Australien", "en": "Australia", "es": "Australia", "fr": "Australie", "ja": "オーストラリア", "pt-BR": "Austrália", "ru": "Австралия", "zh-CN": "澳大利亚"}),
    "CA": (6251999, "NA", False, {"de": "Kanada", "en": "Canada", "es": "Canadá", "fr": "Canada", "ja": "カナダ", "pt-BR": "Canadá", "ru": "Канада", "zh-CN": "加拿大"}),
    "US": (6252001, "NA", False, {"de": "USA", "en": "United States", "es": "Estados Unidos", "fr": "États-Unis", "ja": "アメリカ合衆国", "pt-BR": "Estados Unidos", "ru": "США", "zh-CN": "美国"}),
    "NG": (2328926, "AF", False, {"de": "Nigeria", "en": "Nigeria", "es": "Nigeria", "fr": "Nigeria", "ja": "ナイジェリア連邦共和国", "pt-BR": "Nigéria", "ru": "Нигерия", "zh-CN": "尼日利亚"}),
    "KE": (192950, "AF", False, {"de": "Kenia", "en": "Kenya", "es": "Kenia", "fr": "Kenya", "ja": "ケニア共和国", "pt-BR": "Quênia", "ru": "Кения", "zh-CN": "肯尼亚"}),
}

# city key: (geoname id, names, country, [(subdivision geoname, iso, names)],
#            postal or None, (lat, lon, radius, time zone, metro code or None))
CITIES = {
    "london": (2643743, {"de": "London", "en": "London", "es": "Londres", "fr": "Londres", "ja": "ロンドン", "pt-BR": "Londres", "ru": "Лондон", "zh-CN": "伦敦"}, "GB",
               [(6269131, "ENG", {"en": "England", "fr": "Angleterre", "de": "England"})], "EC1A", (51.5142, -0.0931, 10, "Europe/London", None)),
    "paris": (2988507, {"de": "Paris", "en": "Paris", "es": "París", "fr": "Paris", "ja": "パリ", "pt-BR": "Paris", "ru": "Париж", "zh-CN": "巴黎"}, "FR",
              [(3012874, "IDF", {"en": "Île-de-France", "fr": "Île-de-France"}), (2968815, "75", {"en": "Paris", "fr": "Paris"})], "75001", (48.8607, 2.3281, 20, "Europe/Paris", None)),
    "berlin": (2950159, {"de": "Berlin", "en": "Berlin", "es": "Berlín", "fr": "Berlin", "ja": "ベルリン", "ru": "Берлин", "zh-CN": "柏林"}, "DE",
               [(2950157, "BE", {"de": "Land Berlin", "en": "Land Berlin"})], "10117", (52.5196, 13.4069, 50, "Europe/Berlin", None)),
    "munich": (2867714, {"de": "München", "en": "Munich", "es": "Múnich", "fr": "Munich", "ja": "ミュンヘン", "ru": "Мюнхен", "zh-CN": "慕尼黑"}, "DE",
               [(2951839, "BY", {"de": "Bayern", "en": "Bavaria", "fr": "Bavière"})], "80331", (48.1374, 11.5755, 20, "Europe/Berlin", None)),
    "krakow": (3094802, {"de": "Krakau", "en": "Kraków", "fr": "Cracovie", "ja": "クラクフ", "pt-BR": "Cracóvia", "ru": "Краков"}, "PL",
               [(858787, "12", {"en": "Lesser Poland", "de": "Kleinpolen", "fr": "Petite-Pologne"})], "31-001", (50.0614, 19.9366, 100, "Europe/Warsaw", None)),
    "reykjavik": (3413829, {"de": "Reykjavík", "en": "Reykjavik", "fr": "Reykjavik", "ja": "レイキャヴィーク", "ru": "Рейкьявик", "zh-CN": "雷克雅未克"}, "IS",
                  [(3426182, "1", {"en": "Capital Region"})], "101", (64.1355, -21.8954, 50, "Atlantic/Reykjavik", None)),
    "tokyo": (1850147, {"de": "Tokio", "en": "Tokyo", "es": "Tokio", "fr": "Tokyo", "ja": "東京", "pt-BR": "Tóquio", "ru": "Токио", "zh-CN": "东京"}, "JP",
              [(1850144, "13", {"en": "Tokyo", "ja": "東京都"})], "100-0001", (35.6893, 139.6899, 5, "Asia/Tokyo", None)),
    "osaka": (1853909, {"de": "Osaka", "en": "Osaka", "fr": "Osaka", "ja": "大阪市", "ru": "Осака", "zh-CN": "大阪"}, "JP",
              [(1853904, "27", {"en": "Osaka", "ja": "大阪府"})], "530-0001", (34.6939, 135.5022, 10, "Asia/Tokyo", None)),
    "mumbai": (1275339, {"de": "Mumbai", "en": "Mumbai", "fr": "Bombay", "ja": "ムンバイ", "ru": "Мумбаи", "zh-CN": "孟买"}, "IN",
               [(1264418, "MH", {"en": "Maharashtra"})], "400001", (19.0728, 72.8826, 20, "Asia/Kolkata", None)),
    "sao_paulo": (3448439, {"de": "São Paulo", "en": "São Paulo", "es": "São Paulo", "fr": "São Paulo", "ja": "サンパウロ", "pt-BR": "São Paulo", "ru": "Сан-Паулу", "zh-CN": "圣保罗"}, "BR",
                  [(3448433, "SP", {"en": "São Paulo", "pt-BR": "São Paulo"})], "01000-000", (-23.5475, -46.6361, 100, "America/Sao_Paulo", None)),
    "sydney": (2147714, {"de": "Sydney", "en": "Sydney", "fr": "Sydney", "ja": "シドニー", "pt-BR": "Sydney", "ru": "Сидней", "zh-CN": "悉尼"}, "AU",
               [(2155400, "NSW", {"en": "New South Wales"})], "2000", (-33.8715, 151.2006, 50, "Australia/Sydney", None)),
    "toronto": (6167865, {"de": "Toronto", "en": "Toronto", "es": "Toronto", "fr": "Toronto", "ja": "トロント", "pt-BR": "Toronto", "ru": "Торонто", "zh-CN": "多伦多"}, "CA",
                [(6093943, "ON", {"en": "Ontario", "fr": "Ontario"})], "M5H", (43.6547, -79.3623, 20, "America/Toronto", None)),
    "new_york": (5128581, {"de": "New York City", "en": "New York", "es": "Nueva York", "fr": "New York", "ja": "ニューヨーク", "pt-BR": "Nova Iorque", "ru": "Нью-Йорк", "zh-CN": "纽约"}, "US",
                 [(5128638, "NY", {"en": "New York", "fr": "New York"})], "10001", (40.7506, -73.9971, 5, "America/New_York", 501)),
    "seattle": (5809844, {"de": "Seattle", "en": "Seattle", "fr": "Seattle", "ja": "シアトル", "ru": "Сиэтл", "zh-CN": "西雅图"}, "US",
                [(5815135, "WA", {"en": "Washington", "fr": "Washington"})], "98101", (47.6062, -122.3321, 10, "America/Los_Angeles", 819)),
    "lagos": (2332459, {"de": "Lagos", "en": "Lagos", "fr": "Lagos", "ja": "ラゴス", "ru": "Лагос", "zh-CN": "拉各斯"}, "NG",
              [(2332453, "LA", {"en": "Lagos"})], None, (6.4541, 3.3947, 200, "Africa/Lagos", None)),
    "nairobi": (184745, {"de": "Nairobi", "en": "Nairobi", "fr": "Nairobi", "ja": "ナイロビ", "ru": "Найроби", "zh-CN": "内罗毕"}, "KE",
                [(184742, "110", {"en": "Nairobi County"})], "00100", (-1.2833, 36.8167, 50, "Africa/Nairobi", None)),
}

# The city database's networks: (network, city key or None, country if
# no city, registered country, extra traits, represented country).
CITY_NETS = [
    ("81.2.69.0/24", "london", None, "GB", {}, None),
    ("81.2.69.160/27", "london", None, "GB", {}, None),
    ("81.2.70.0/23", None, "GB", "GB", {}, None),
    ("2.125.160.216/29", "london", None, "GB", {}, None),
    ("2001:db8:100::/40", "london", None, "GB", {}, None),
    ("89.160.20.112/28", "paris", None, "FR", {}, None),
    ("89.160.20.128/25", "paris", None, "FR", {}, None),
    ("2001:db8:200::/40", "paris", None, "FR", {}, None),
    ("5.83.124.0/22", "berlin", None, "DE", {}, None),
    ("5.83.128.0/20", "munich", None, "DE", {}, None),
    ("5.83.144.0/20", None, "DE", "DE", {}, None),
    ("2001:db8:300::/40", "berlin", None, "DE", {}, None),
    ("31.11.0.0/18", "krakow", None, "PL", {}, None),
    ("82.221.0.0/16", "reykjavik", None, "IS", {}, None),
    ("126.0.0.0/12", "tokyo", None, "JP", {}, None),
    ("126.16.0.0/12", "osaka", None, "JP", {}, None),
    ("2001:db8:400::/40", "tokyo", None, "JP", {}, None),
    ("2001:db8:401::/48", "osaka", None, "JP", {}, None),
    ("49.32.0.0/11", "mumbai", None, "IN", {}, None),
    ("177.32.0.0/14", "sao_paulo", None, "BR", {}, None),
    ("177.36.0.0/14", None, "BR", "BR", {}, None),
    ("1.128.0.0/11", "sydney", None, "AU", {}, None),
    ("2001:db8:500::/40", "sydney", None, "AU", {}, None),
    ("24.48.0.0/14", "toronto", None, "CA", {}, None),
    ("67.43.156.0/24", "new_york", None, "US", {}, None),
    ("67.43.157.0/24", "seattle", None, "US", {}, None),
    ("2001:db8:600::/40", "new_york", None, "US", {}, None),
    ("2001:db8:610::/44", "seattle", None, "US", {}, None),
    ("105.112.0.0/12", "lagos", None, "NG", {}, None),
    ("41.80.0.0/13", "nairobi", None, "KE", {}, None),
    # a block registered in the United States and used in Japan
    ("216.160.83.56/29", "tokyo", None, "US", {}, None),
    # an anycast resolver: a country and no city
    ("214.78.120.0/22", None, "US", "US", {"is_anycast": True}, None),
    # the US military in Germany
    ("214.1.0.0/16", "munich", None, "US", {}, ("US", "military")),
    # a satellite provider with no country at all
    ("2001:db8:700::/40", None, None, None, {"is_satellite_provider": True}, None),
]


def names(d):
    return {k: d[k] for k in LANGS if k in d}


def place_country(iso):
    gid, cont, eu, nm = COUNTRIES[iso]
    out = {"geoname_id": gid}
    if eu:
        out["is_in_european_union"] = True
    out["iso_code"] = iso
    out["names"] = names(nm)
    return out


def place_continent(iso):
    code = COUNTRIES[iso][1]
    gid, nm = CONTINENTS[code]
    return {"code": code, "geoname_id": gid, "names": names(nm)}


def city_record(city, country, registered, traits, represented):
    rec = {}
    if city is not None:
        gid, nm, iso, subs, postal, loc = CITIES[city]
        lat, lon, radius, tz, metro = loc
        rec["city"] = {"geoname_id": gid, "names": names(nm)}
        rec["continent"] = place_continent(iso)
        rec["country"] = place_country(iso)
        location = {"accuracy_radius": T("u16", radius), "latitude": lat, "longitude": lon}
        if metro is not None:
            location["metro_code"] = T("u16", metro)
        location["time_zone"] = tz
        rec["location"] = location
        if postal is not None:
            rec["postal"] = {"code": postal}
    elif country is not None:
        rec["continent"] = place_continent(country)
        rec["country"] = place_country(country)
    if registered is not None:
        rec["registered_country"] = place_country(registered)
    if represented is not None:
        r = place_country(represented[0])
        r["type"] = represented[1]
        rec["represented_country"] = r
    if city is not None:
        rec["subdivisions"] = [{"geoname_id": g, "iso_code": i, "names": names(n)} for g, i, n in CITIES[city][3]]
    if traits:
        rec["traits"] = dict(traits)
    return rec


def country_record(city, country, registered, represented):
    rec = {}
    iso = CITIES[city][2] if city is not None else country
    if iso is not None:
        rec["continent"] = place_continent(iso)
        rec["country"] = place_country(iso)
    if registered is not None:
        rec["registered_country"] = place_country(registered)
    if represented is not None:
        r = place_country(represented[0])
        r["type"] = represented[1]
        rec["represented_country"] = r
    return rec


ASN_NETS = [
    ("81.2.69.0/24", 64496, "Larkfield Telecom"),
    ("81.2.70.0/23", 64496, "Larkfield Telecom"),
    ("2.125.160.216/29", 64497, "Thames Broadband"),
    ("2001:db8:100::/40", 64496, "Larkfield Telecom"),
    ("89.160.20.0/24", 64498, "Seine Fibre"),
    ("5.83.124.0/22", 64499, "Spree Netz"),
    ("5.83.128.0/19", 64500, "Isar Kabel"),
    ("31.11.0.0/18", 64501, "Wisła Online"),
    ("82.221.0.0/16", 64502, "Geysir Hosting"),
    ("126.0.0.0/11", 64503, "Kanto Mobile"),
    ("2001:db8:400::/39", 64503, "Kanto Mobile"),
    ("49.32.0.0/11", 64504, "Arabian Sea Networks"),
    ("177.32.0.0/13", 64505, "Paulista Dados"),
    ("1.128.0.0/11", 64506, "Harbour Bridge Internet"),
    ("24.48.0.0/14", 64507, "Lakeshore Cable"),
    ("67.43.156.0/23", 64508, "Hudson Transit"),
    ("105.112.0.0/12", 64509, "Lagoon Mobile"),
    ("41.80.0.0/13", 64510, "Rift Valley Wireless"),
    ("214.78.120.0/22", 65551, "Anycast Resolver Collective"),
    ("214.1.0.0/16", 64511, ""),
    ("2001:db8:600::/40", 65536, "Hudson Transit v6"),
]


# ------------------------------------------------------------ the decoder test

def types_db():
    long29 = "x" * 40
    long285 = "Larkfield " * 40
    unicode = "ünïcödé 日本語 🚀"
    big_map = {"mapX": {"arrayX": [T("u32", 7), T("u32", 8), T("u32", 9)], "utf8_stringX": "hello"}}
    full = {
        "array": [T("u32", 1), T("u32", 2), T("u32", 3)],
        "boolean": True,
        "bytes": b"\x00\x00\x00*",
        "double": 42.123456,
        "float": T("f32", 1.1),
        "int32": T("i32", -268435456),
        "map": big_map,
        "uint128": T("u128", 1 << 120),
        "uint16": T("u16", 100),
        "uint32": T("u32", 268435456),
        "uint64": T("u64", 1152921504606846976),
        "utf8_string": "unicode! ☯ - ♫",
    }
    zeros = {
        "array": [],
        "boolean": False,
        "bytes": b"",
        "double": 0.0,
        "float": T("f32", 0.0),
        "int32": T("i32", 0),
        "map": {},
        "uint128": T("u128", 0),
        "uint16": T("u16", 0),
        "uint32": T("u32", 0),
        "uint64": T("u64", 0),
        "utf8_string": "",
    }
    maxes = {
        "double": float("inf"),
        "float": T("f32", float("-inf")),
        "int32": T("i32", 2147483647),
        "uint128": T("u128", (1 << 128) - 1),
        "uint16": T("u16", 65535),
        "uint32": T("u32", 4294967295),
        "uint64": T("u64", (1 << 64) - 1),
    }
    mins = {
        "double": -0.0,
        "float": T("f32", -1.5),
        "int32": T("i32", -2147483648),
        "nested": [[[]], {"a": [{"b": [True, False]}]}],
        "small": [T("i32", -1), T("i32", 1), T("f32", 3.4028234663852886e38), 1e-300, 2.5e-08],
    }
    strings = {"long29": long29, "long285": long285, "unicode": unicode, "quote": "it's \"quoted\"\n\ttab\\", "bytes": b"\x00\xff'\"\\\n abc"}
    d = Data()
    # a filler record so that later records sit beyond offset 2048 and
    # need two-byte pointers
    filler = {"filler": "f" * 2100}
    inserts = [
        ("1.1.1.0/24", filler),
        ("1.1.1.1/32", full),
        ("1.1.1.2/31", zeros),
        ("1.1.1.4/30", maxes),
        ("1.1.1.8/29", mins),
        ("1.1.1.16/28", strings),
        ("1.1.1.32/32", {"again": full, "map_again": big_map}),
        ("2001:db8::/64", {"v6": True, "uint16": T("u16", 6)}),
        ("2001:db8:0:1::/64", {"v6": True, "uint16": T("u16", 7)}),
        ("::1.1.1.64/122", {"ipv4_in_v6": "compat"}),
    ]
    return build(6, 24, inserts, metadata("MaxMind DB Decoder Test", 6, 24,
                                         {"en": "Test Database", "zh": "Test Database Chinese"}, ["en", "zh"], 1761264000), data=d)


# ------------------------------------------------------------ broken files

def broken():
    out = {}
    out["nometa.mmdb"] = bytes(range(256)) * 4
    good = build(4, 24, [("1.2.3.0/24", {"a": T("u32", 1)})], metadata("Broken", 4, 24, {"en": "x"}, ["en"], 1))
    # metadata that is an array
    tree_and_data = good[: good.rfind(MARKER)]
    out["metalist.mmdb"] = tree_and_data + MARKER + plain(["node_count", 1])
    # metadata without build_epoch
    md = metadata("Broken", 4, 24, {"en": "x"}, ["en"], 1)
    del md["build_epoch"]
    out["metamissing.mmdb"] = build(4, 24, [("1.2.3.0/24", {"a": T("u32", 1)})], md)
    # an unknown record size
    out["rec20.mmdb"] = build(4, 20, [("1.2.3.0/24", {"a": T("u32", 1)})], metadata("Broken", 4, 20, {"en": "x"}, ["en"], 1))
    # a data pointer past the end of the file
    out["corrupt.mmdb"] = build(4, 24, [("1.2.3.0/24", "tree"), ("1.2.4.0/24", {"a": T("u32", 1)})],
                                metadata("Broken", 4, 24, {"en": "x"}, ["en"], 1),
                                raw_leaf=lambda v: 0xFFFFF0 if v == "tree" else None)
    # a type number the decoder does not know (12, the data cache container)
    out["badtype.mmdb"] = build(4, 24, [("1.2.3.0/24", T("raw", bytes([0x01, 0x05]))), ("1.2.4.0/24", {"a": T("u32", 1)})],
                                metadata("Broken", 4, 24, {"en": "x"}, ["en"], 1))
    # a double four bytes long
    out["baddouble.mmdb"] = build(4, 24, [("1.2.3.0/24", {"d": T("raw", bytes([0x64]) + struct.pack(">f", 1.5))})],
                                  metadata("Broken", 4, 24, {"en": "x"}, ["en"], 1))
    # a pointer inside the data past the end of the file
    out["badptr.mmdb"] = build(4, 24, [("1.2.3.0/24", {"p": T("raw", bytes([0x38, 0x00, 0x10, 0x00, 0x00]))})],
                               metadata("Broken", 4, 24, {"en": "x"}, ["en"], 1))
    # a search tree too shallow for an address: 32 levels end on a node
    tree = bytearray()
    n = 34
    for i in range(33):
        tree += records(24, i + 1, i + 1)
    tree += records(24, n, n)
    data = Data()
    data.write({"never": True})
    md = metadata("Broken", 4, 24, {"en": "x"}, ["en"], 1)
    md["node_count"] = T("u32", n)
    out["shallow.mmdb"] = bytes(tree) + bytes(16) + bytes(data.buf) + MARKER + plain(md)
    return out


# ------------------------------------------------------------ the logs

class Lcg:
    def __init__(self, seed):
        self.s = seed

    def next(self):
        self.s = (self.s * 1103515245 + 12345) % 2147483648
        return self.s >> 8

    def below(self, n):
        return self.next() % n


def host_in(net, r):
    addr, plen = net.split("/")
    plen = int(plen)
    if ":" in addr:
        n = v6_int(addr) + r.below(1 << min(24, 128 - plen))
        parts = [(n >> (112 - 16 * i)) & 0xFFFF for i in range(8)]
        return ":".join(f"{p:x}" for p in parts)
    n = v4_int(addr) + r.below(1 << min(24, 32 - plen))
    return ".".join(str((n >> s) & 255) for s in (24, 16, 8, 0))


PATHS = ["/", "/catalog", "/catalog/search?q=maps", "/account/login", "/admin", "/api/v2/loans", "/static/app.js", "/feeds/new.xml"]


def access_log():
    r = Lcg(20261024)
    pool = [n[0] for n in CITY_NETS] + ["10.1.2.0/24", "192.168.7.0/24", "2001:db8:ffff::/48", "198.51.100.0/24"]
    lines = []
    for i in range(300):
        net = pool[r.below(len(pool))]
        ip = host_in(net, r)
        if r.below(9) == 0:
            ip = ip.upper() if ":" in ip else ip
        path = PATHS[r.below(len(PATHS))]
        status = [200, 200, 200, 304, 404, 403, 500][r.below(7)]
        size = 0 if status == 304 else 200 + r.below(40000)
        t = i * 11
        lines.append(f'{ip} - - [24/Oct/2026:09:{t // 60 % 60:02}:{t % 60:02} +0000] "GET {path} HTTP/1.1" {status} {size}')
    lines.insert(77, "not-an-ip - - [24/Oct/2026:09:14:07 +0000] \"GET / HTTP/1.1\" 400 0")
    lines.insert(150, "300.12.4.1 - - [24/Oct/2026:09:27:30 +0000] \"GET / HTTP/1.1\" 400 0")
    return "\n".join(lines) + "\n"


POLICY = """# geo policy for the admin panel, first match wins
deny country KP
deny represented military
allow asn 64496
deny continent AF
deny anycast
deny satellite
allow registered US
deny country IS
deny unknown
default allow
"""


# ------------------------------------------------------------ the jobs

def jobs():
    j = []
    for db in ["city", "country", "asn", "types"]:
        j.append(["meta", f"{db}.mmdb"])
    city_ips = ["81.2.69.142", "81.2.69.163", "81.2.70.1", "2.125.160.217", "89.160.20.115", "89.160.20.200", "5.83.125.10",
                "5.83.130.1", "5.83.150.9", "31.11.33.1", "82.221.4.4", "126.1.2.3", "126.20.0.1", "49.40.1.2", "177.33.4.5",
                "177.37.0.1", "1.128.9.9", "24.49.0.1", "67.43.156.7", "67.43.157.200", "105.113.0.9", "41.81.2.3",
                "216.160.83.58", "214.78.121.9", "214.1.33.33", "2001:db8:100::1", "2001:DB8:200:ab::1", "2001:db8:300:0:0:0:0:1",
                "2001:db8:401::5", "2001:db8:4ff::1", "2001:db8:600::1", "2001:db8:61f::1", "2001:db8:700::7", "::ffff:81.2.69.142",
                "2002:5153:4401::1", "10.0.0.1", "192.0.2.1", "::", "::1", "2001:db8:ffff::1", "8.8.8.8"]
    for ip in city_ips:
        j.append(["get", "city.mmdb", ip])
    for ip in ["81.2.69.142", "126.20.0.1", "214.1.33.33", "10.0.0.1", "2001:db8:100::1", "1.2.3.4.5", "01.2.3.4", "1::2::3", "", "2001:db8::g", "fe80::1:2:3:4:5:6:7"]:
        j.append(["get", "country.mmdb", ip])
    for ip in ["81.2.69.142", "5.83.140.1", "214.1.2.3", "2001:db8:600:1::1", "177.38.0.1", "8.8.8.8"]:
        j.append(["get", "asn.mmdb", ip])
    for ip in ["1.1.1.1", "1.1.1.3", "1.1.1.5", "1.1.1.9", "1.1.1.20", "1.1.1.32", "1.1.1.33", "1.1.1.66", "::1.1.1.66", "2001:db8::1", "2001:db8:0:1::1", "2001:db8:0:2::1"]:
        j.append(["get", "types.mmdb", ip])
    j.append(["dump", "asn.mmdb"])
    j.append(["dump", "country.mmdb"])
    j.append(["dump", "types.mmdb"])
    j.append(["networks", "city.mmdb"])
    for ip, loc in [("81.2.69.142", "en"), ("81.2.69.142", "fr,en"), ("89.160.20.115", "ja,en"), ("5.83.130.1", "de"), ("31.11.33.1", "pt-BR,ru"),
                    ("126.20.0.1", "zh-CN"), ("177.33.4.5", "es,pt-BR"), ("216.160.83.58", "en"), ("214.78.121.9", "en"), ("214.1.33.33", "en"),
                    ("2001:db8:700::7", "en"), ("67.43.156.7", "ru"), ("2001:db8:61f::1", "en"), ("5.83.150.9", "en"), ("105.113.0.9", "xx"),
                    ("10.0.0.1", "en"), ("2001:db8:ffff::1", "en"), ("::ffff:81.2.69.142", "en"), ("nonsense", "en")]:
        j.append(["city", "city.mmdb", ip, loc])
    for ip in ["81.2.69.142", "214.1.33.33", "10.0.0.1"]:
        j.append(["country", "country.mmdb", ip, "en"])
    j.append(["country", "city.mmdb", "81.2.69.142", "en"])
    j.append(["asn", "city.mmdb", "81.2.69.142", "en"])
    j.append(["city", "asn.mmdb", "81.2.69.142", "en"])
    for ip in ["81.2.69.142", "214.1.2.3", "2001:db8:600:1::1", "8.8.8.8"]:
        j.append(["asn", "asn.mmdb", ip, "en"])
    for bad in ["nometa", "metalist", "metamissing", "rec20", "corrupt", "badtype", "baddouble", "badptr", "shallow", "missing"]:
        j.append(["get", f"{bad}.mmdb", "1.2.3.4"])
    j.append(["get", "corrupt.mmdb", "1.2.4.4"])
    j.append(["get", "badtype.mmdb", "1.2.4.4"])
    j.append(["get", "country.mmdb", "2001:db8::1"])
    j.append(["annotate", "access.log"])
    j.append(["firewall", "policy.txt", "access.log"])
    return j


def main():
    os.makedirs(DATA, exist_ok=True)
    files = {}
    city_inserts = [(n, city_record(c, k, reg, tr, rep)) for n, c, k, reg, tr, rep in CITY_NETS]
    files["city.mmdb"] = build(6, 28, city_inserts, metadata("GeoIP2-City", 6, 28,
                                                            {"en": "Larkfield test City database", "fr": "Base de test des villes"}, LANGS, 1761264000))
    country_inserts = [(n, country_record(c, k, reg, rep)) for n, c, k, reg, tr, rep in CITY_NETS if ":" not in n]
    files["country.mmdb"] = build(4, 24, country_inserts, metadata("GeoLite2-Country", 4, 24,
                                                                  {"en": "Larkfield test Country database"}, LANGS, 1761177600))
    asn_inserts = [(n, {"autonomous_system_number": T("u32", a), "autonomous_system_organization": o} if o else {"autonomous_system_number": T("u32", a)})
                   for n, a, o in ASN_NETS]
    files["asn.mmdb"] = build(6, 32, asn_inserts, metadata("GeoLite2-ASN", 6, 32, {"en": "Larkfield test ASN database"}, ["en"], 1761091200))
    files["types.mmdb"] = types_db()
    files.update(broken())
    files["access.log"] = access_log().encode()
    files["policy.txt"] = POLICY.encode()
    files["jobs.txt"] = ("\n".join("\t".join(x) for x in jobs()) + "\n").encode()
    for name, b in files.items():
        with open(os.path.join(DATA, name), "wb") as f:
            f.write(b)
    with open(os.path.join(DATA, "files.txt"), "w") as f:
        f.write("\n".join(sorted(files)) + "\n")


main()
