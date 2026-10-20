# Writes data/: jobs.tsv, the list of calls and programs mini_random runs,
# and the files the programs read.
import os

FILES = {}


def put(path, text):
    FILES[path] = text


J = []


def job(title):
    J.append(f"job\t{title}")


def op(*fields):
    J.append("\t".join(str(f) for f in fields))


# ------------------------------------------------------------ seeding
job("seeding from ints, floats, str and bytes")
for v in ["0", "1", "42", "-42", "4294967295", "4294967296", "123456789012345678901234567890",
          "-99999999999999999999999999999999999999", "2_026"]:
    op("seed", "int", v)
op("random", 3)
for v in ["3.5", "-1.5", "0.1", "1e300", "-0.0", "inf", "5e-324", "2.0"]:
    op("seed", "float", v)
for v in ["hello", "", "checkout-load-2026-10", "a much longer seed string than the others, over one block"]:
    op("seed", "str", v)
for v in ["", "00", "deadbeef", "73746174696f6e2d3037"]:
    op("seed", "bytes", v)
op("seed", "str", "hello", 1)
op("seed", "str", "", 1)
op("seed", "bytes", "68656c6c6f", 1)
op("seed", "list", "1,2")
op("random", 2)

job("random() and getrandbits()")
op("seed", "int", 2024)
op("random", 8)
for k in [0, 1, 7, 31, 32, 33, 48, 62, 63, 64, 65, 100, 128, 200, -1]:
    op("getrandbits", k)
for n in [0, 1, 3, 4, 5, 8, 16, -2]:
    op("randbytes", n)

job("randrange() and randint()")
op("seed", "int", 7)
for args in [["10"], ["1", "7"], ["0", "100", "5"], ["100", "0", "-7"], ["-10", "10"],
             ["0", "1"], ["5", "5"], ["5"], ["0"], ["-3"], ["10", "1"], ["0", "10", "0"],
             ["0", "10", "-1"], ["10", "-", "2"], ["2.5"], ["1", "2.5"], ["1", "10", "1.5"],
             ["1000000000000000000000000000000"], ["-1000000000000", "1000000000000"],
             ["0", "10000000000000000000000", "3"], ["9223372036854775807"],
             ["18446744073709551616", "18446744073709551626"], ["1_000"]]:
    op("randrange", *args)
for args in [["1", "6"], ["1", "6"], ["0", "0"], ["-5", "5"], ["6", "1"], ["1", "1e3"],
             ["1", "100000000000000000000"]]:
    op("randint", *args)

job("choice(), shuffle() and sample()")
op("seed", "str", "deck")
cards = ",".join(r + s for s in "SHDC" for r in "A23456789TJQK")
op("choice", "red,green,blue")
op("choice", "solo")
op("choice", "")
op("shuffle", "a,b,c,d,e,f,g,h")
op("shuffle", "")
op("shuffle", "x")
op("shuffle", cards)
op("sample", "red,green,blue,cyan,magenta", 3)
op("sample", "red,green,blue,cyan,magenta", 5)
op("sample", "red,green,blue,cyan,magenta", 0)
op("sample", "red,green,blue", 4)
op("sample", "red,green,blue", -1)
op("sample", "range:100", 5)
op("sample", "range:10", 10)
op("sample", "range:1000000", 6)
op("sample", "range:30", 6)
op("sample", "range:30", 7)
op("sample", "range:60", 25)
op("sample", cards, 13)
op("sample", "red,blue", 5, "4,2")
op("sample", "red,blue", 6, "4,2")
op("sample", "red,blue", 7, "4,2")
op("sample", "red,blue,green", 2, "4,2")
op("sample", "red,blue", 1, "-1,0")
op("sample", "a,b,c", 3, "0,3,0")

job("choices()")
op("seed", "int", 99)
op("choices", "heads,tails", "-", "-", 10)
op("choices", "a,b,c", "10,5,1", "-", 12)
op("choices", "a,b,c", "-", "10,15,16", 12)
op("choices", "a,b,c", "0.5,0.25,0.25", "-", 6)
op("choices", "a,b,c", "1,2", "-", 3)
op("choices", "a,b", "1,2", "1,3", 3)
op("choices", "a,b", "0,0", "-", 3)
op("choices", "a,b", "-1,0.5", "-", 3)
op("choices", "a,b", "1,inf", "-", 3)
op("choices", "", "-", "-", 1)
op("choices", "", "-", "-", 0)
op("choices", "", "", "-", 1)
op("choices", "x", "-", "-", 4)
op("choices", "a,b,c", "-", "-", 0)

job("continuous distributions")
op("seed", "int", 12345)
op("uniform", 4, 1, 10)
op("uniform", 2, 10, 1)
op("uniform", 2, "2.5", "2.5")
op("triangular", 4)
op("triangular", 4, 0, 10, 2)
op("triangular", 4, 10, 0, 7)
op("triangular", 2, 3, 3, 3)
op("triangular", 2, 3, 3)
op("triangular", 2, 1, 5, 9)
op("normalvariate", 5, 0, 1)
op("normalvariate", 3, 100, 15)
op("gauss", 5, 0, 1)
op("gauss", 3, 170, 9)
op("lognormvariate", 4, 0, "0.5")
op("expovariate", 4)
op("expovariate", 4, "0.25")
op("expovariate", 2, -2)
op("expovariate", 1, 0)
op("vonmisesvariate", 4, 0, 4)
op("vonmisesvariate", 3, "3.14", "0.5")
op("vonmisesvariate", 2, 1, 0)
op("vonmisesvariate", 3, -10, 50)
op("paretovariate", 4, 3)
op("paretovariate", 1, 0)
op("weibullvariate", 4, 1, "1.5")
op("weibullvariate", 2, 2, 0)

job("gamma, beta and binomial")
op("seed", "str", "gamma")
for a, b in [("0.01", 1), ("0.1", 1), ("0.5", 1), ("0.9", 1), (1, 1), (2, 1), (20, 1), (200, 1), ("2.5", "0.5")]:
    op("gammavariate", 3, a, b)
op("gammavariate", 1, 0, 1)
op("gammavariate", 1, 1, -1)
op("betavariate", 4, 3, 3)
op("betavariate", 3, "0.5", "0.5")
op("betavariate", 2, 1, 1)
op("betavariate", 1, -1, 1)
for n, p in [(1, "0.5"), (1, "0.9"), (10, "0.5"), (15, "0.6"), (100, "0.75"), (100, "0.05"),
             (1000, "0.3"), (1000000, "0.001"), (50, "0.999"), (20, 0), (20, 1), (0, "0.5"),
             (-1, "0.5"), (5, "1.5"), (5, "-0.1"), (100000, "0.5"), (37, "0.27")]:
    op("binomialvariate", 4, n, p)

job("getstate() and setstate()")
op("seed", "int", 5)
op("state")
op("random", 2)
op("gauss", 1, 0, 1)
op("save")
op("state")
op("random", 3)
op("gauss", 1, 0, 1)
op("restore")
op("random", 3)
op("gauss", 1, 0, 1)
op("getrandbits", 640)
for _ in range(10):
    op("getrandbits", 2000)
op("state")
op("restore")
op("state")
op("badstate", "index", 625)
op("badstate", "index", 624)
op("random", 1)
op("badstate", "index", 0)
op("random", 1)
op("badstate", "version", 2)
op("random", 1)
op("badstate", "version", 4)
op("badstate", "size", 0)
op("gauss", 1, 0, 1)
op("restore")
op("badstate", "gauss", 7)
op("gauss", 2, 0, 1)
op("seed", "int", 5)
op("gauss", 1, 0, 1)

job("python -m random")
op("seed", "int", 8675309)
for argv in [[], ["-c", "rock", "paper", "scissors"], ["--choice", "heads", "tails"], ["-i", "6"],
             ["--integer", "20"], ["--int", "100"], ["--integer=5"], ["-i5"], ["-f", "2.5"],
             ["--float", "1e3"], ["--f", "2"], ["-f", "nan"], ["-f", "inf"], ["6"], ["2.5"],
             ["pizza tacos ramen"], ["red", "green", "blue"], ["--", "-5"], ["-2.5"], ["0"],
             ["-i", "0"], ["-i", "x"], ["-i", " 7 "], ["-i", "1_000"], ["-i", "0x10"],
             ["-i", "3", "-c", "a"], ["-c", "a", "-f", "1"], ["-c"], ["-i"], ["x", "-i"],
             ["--bogus"], ["--bogus", "a"], ["a", "-i", "3", "b"], ["a", "b", "-c", "x"],
             ["-c", "x", "y", "--", "z"], ["-f", "1", "2", "3"], ["--test", "3x"], ["--ch", "a", "b"],
             ["   "], [""], ["-h"], ["-i", "2", "-h", "--bogus"], ["-f", "-1"], ["-i", "4", "-i", "9"]]:
    op("cli", *argv)

# ------------------------------------------------------------ programs
job("program: load-test traffic generator")
op("program", "loadgen", "loadgen/checkout.conf")
op("program", "loadgen", "loadgen/search.conf")
job("program: A/B test bucketing")
op("program", "abtest", "abtest/experiments.conf", "abtest/users.txt")
job("program: retry backoff with jitter")
op("program", "backoff", "backoff/policy.conf")
job("program: reservoir sampling of a log")
op("program", "reservoir", "logs/app.log")
job("program: Monte Carlo project estimate")
op("program", "montecarlo", "project/tasks.csv")
job("program: tournament draw and Secret Santa")
op("program", "draw", "draw/players.txt", "draw/office.txt")
job("program: synthetic test data")
op("program", "synth", "synth/lists.txt")
job("program: weather station simulator")
op("program", "sensor", "sensor/station.conf")

put("jobs.tsv", "\n".join(J) + "\n")

put("loadgen/checkout.conf", """# checkout service, Black Friday rehearsal
seed = checkout-load-2026-10
rate = 12.5
requests = 300
error_rate = 0.02
endpoint GET /api/cart 5 3.2 0.35
endpoint POST /api/cart/items 3 3.6 0.40
endpoint GET /api/products 8 2.9 0.30
endpoint POST /api/checkout 1 4.8 0.55
endpoint GET /healthz 1 0.4 0.10
""")
put("loadgen/search.conf", """# search, steady traffic
seed = search-steady
rate = 40
requests = 200
error_rate = 0.005
endpoint GET /search 9 3.9 0.6
endpoint GET /suggest 6 2.3 0.25
""")

put("abtest/experiments.conf", """# name rollout variants weights
new-checkout 0.25 control,treatment 50,50
pricing-page 1.0 A,B,C 34,33,33
dark-mode 0.10 on 1
""")
first = ["ada", "bo", "chen", "dara", "eli", "fatima", "gus", "hana", "ivan", "jun", "kofi", "lena",
         "mo", "nia", "omar", "priya", "quinn", "ravi", "sara", "tomas"]
users = []
for i in range(120):
    users.append(f"u{1000 + i * 37}-{first[i % len(first)]}")
put("abtest/users.txt", "\n".join(users) + "\n")

put("backoff/policy.conf", """seed = 7
base = 0.1
cap = 10.0
attempts = 8
clients = 3
""")

levels = ["INFO"] * 14 + ["DEBUG"] * 5 + ["WARN"] * 3 + ["ERROR"] * 2
paths = ["/api/cart", "/api/products", "/api/checkout", "/login", "/healthz", "/search"]
log = []
x = 17
for i in range(220):
    x = (x * 1103515245 + 12345) % 2147483648
    lv = levels[x % len(levels)]
    p = paths[(x >> 8) % len(paths)]
    ms = 5 + (x >> 12) % 900
    h, m, s = 9 + i // 3600, (i * 13 // 60) % 60, (i * 13) % 60
    msg = {"INFO": f"request {p} 200 {ms}ms", "DEBUG": f"cache lookup {p} hit={x % 2 == 0}",
           "WARN": f"slow request {p} {ms * 3}ms", "ERROR": f"upstream timeout {p} after 30000ms"}[lv]
    log.append(f"2026-10-20T{h:02d}:{m:02d}:{s:02d}Z {lv:<5} {msg}")
put("logs/app.log", "\n".join(log) + "\n")

put("project/tasks.csv", """task,track,optimistic,likely,pessimistic
API design,A,2,3,6
Database schema,A,3,5,10
Payment integration,A,5,8,20
Frontend shell,B,4,6,9
Checkout UI,B,5,7,14
Accessibility pass,B,1,2,5
Load testing,final,2,3,7
Security review,final,1,3,8
Launch,final,1,1,2
""")

put("draw/players.txt", """Aiko Tanaka|Kyoto FC
Ben Okafor|Lagos United
Carla Mendes|Porto Azul
Dmitri Volkov|Neva Stars
Eun-ji Park|Busan Waves
Farid Haddad|Beirut Cedars
Greta Lind|Malmo Blue
Hugo Lefevre|Lyon Rouge
Isla McKay|Leith Thistle
Jonas Weber|Rhine Rovers
Kavya Rao|Chennai Lions
Luis Ortega|Andes FC
Maya Cohen|Haifa Port
Nils Berg|Bergen Fjord
Olu Adeyemi|Lagos United
Priya Nair|Chennai Lions
""")
put("draw/office.txt", """Alex|ops
Bea|ops
Cyrus|eng
Dana|eng
Emre|eng
Fen|design
Gita|design
Hal|sales
Ines|sales
""")

put("synth/lists.txt", """first: Olivia Liam Emma Noah Ava Mateo Sofia Kenji Amara Lucas Zara Diego Mei Arjun Nora
last: Smith Garcia Nguyen Okoro Muller Rossi Kim Patel Silva Cohen Ivanova Haddad
city: Lisbon:5 Toronto:4 Nairobi:3 Osaka:3 Austin:2 Reykjavik:1
tag: beta newsletter vip mobile churn-risk referral
""")

put("sensor/station.conf", """seed = station-07
hours = 24
base_temp = 12.0
swing = 6.0
wind_scale = 6.0
wind_shape = 2.0
wind_dir = 250
wind_kappa = 2.5
rain_chance = 0.3
loss = 0.05
""")

for path, text in FILES.items():
    full = os.path.join("data", path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)
