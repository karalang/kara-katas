# Writes data/: an access log a small web shop's front end wrote over
# an afternoon, the user agents in it, and jobs.tsv, the jobs
# mini_uaparser runs. Everything is fixed, so the files never change.
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "curl/8.4.0",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "python-requests/2.31.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Dalvik/2.1.0 (Linux; U; Android 11; Redmi Note 8 Pro MIUI/V12.5.4.0.RGGMIXM)",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/118.0.5993.92 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 14; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0",
    "Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; chromeframe/11.0.696.57)",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Wget/1.21.4",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 OPR/79.0.4195.76",
    "-",
    "",
]

PATHS = ["/", "/products", "/products/42", "/cart", "/checkout", "/api/stock?sku=17",
         "/robots.txt", "/static/app.js", "/static/site.css", "/login", "/search?q=lamp",
         "/sitemap.xml", "/favicon.ico", "/products/7", "/api/price?sku=3"]
STATUS = [200, 200, 200, 304, 200, 404, 200, 301, 200, 500, 200, 302, 200, 403]


def log_lines():
    lines = []
    seed = 12345
    for n in range(160):
        seed = (seed * 1103515245 + 12345) % 2147483648
        ua = (seed >> 8) % len(UAS)
        path = PATHS[(seed >> 4) % len(PATHS)]
        status = STATUS[(seed >> 12) % len(STATUS)]
        size = "-" if status in (304, 301, 302) else str(200 + (seed >> 3) % 9000)
        ip = "%s.%d" % (["192.0.2", "198.51.100", "203.0.113"][n % 3], 1 + (seed >> 6) % 250)
        minute = 14 * 60 + n // 3
        stamp = "21/Oct/2026:%02d:%02d:%02d +0000" % (minute // 60, minute % 60, (n * 17) % 60)
        method = "POST" if path in ("/cart", "/checkout", "/login") and n % 2 else "GET"
        ref = "-" if n % 4 else "https://shop.example/"
        lines.append('%s - - [%s] "%s %s HTTP/1.1" %d %s "%s" "%s"'
                     % (ip, stamp, method, path, status, size, ref, UAS[ua]))
        if n % 37 == 5:
            lines.append("%s - - [%s] \"\\x16\\x03\\x01\" 400 -" % (ip, stamp))
    return lines


def jobs():
    j = []
    for i in range(len(UAS)):
        j.append(["parse", str(i)])
    j.append(["report"])
    for i in (0, 3, 6, 9, 13, 20, 21):
        j.append(["ua", str(i)])
        j.append(["os", str(i)])
        j.append(["device", str(i)])
    j.append(["cache"])
    # the javascript overrides, which are deprecated
    j.append(["ua_js", "0", "js_user_agent_family=Iron"])
    j.append(["ua_js", "0", "js_user_agent_family=Iron|js_user_agent_v1=31|js_user_agent_v3="])
    j.append(["ua_js", "0", "js_user_agent_family="])
    j.append(["ua_js", "0", "js_user_agent_v1=99"])
    j.append(["ua_js", "15", "js_user_agent_string=" + UAS[0]])
    j.append(["ua_js", "15", "js_user_agent_string=" + UAS[5]])
    j.append(["ua_js", "15", "js_user_agent_string=" + UAS[0]])
    j.append(["ua_js", "0", "js_user_agent_string=" + UAS[0]])
    j.append(["ua_js", "15", "js_user_agent_family=Chromium|js_user_agent_v1=11|js_user_agent_string=" + UAS[0]])
    j.append(["parse_js", "2", "js_user_agent_family=cURL|js_user_agent_v2=4"])
    j.append(["parse_js", "2", "js_user_agent_v2=4|js_user_agent_family=cURL"])
    j.append(["os_js", "2", "js_user_agent_family=cURL"])
    j.append(["cache"])
    # the entry order of a cached result follows the first call
    j.append(["os", "7"])
    j.append(["clear"])
    j.append(["os", "7"])
    j.append(["parse", "7"])
    j.append(["device", "17"])
    j.append(["parse", "17"])
    j.append(["parse", "17"])
    # pretty printing
    for args in (["Chrome", "120", "0", "6099"], ["Firefox", "3", "5", "b4"], ["Safari", "17", "1", "~"],
                 ["curl", "8", "~", "~"], ["Other", "~", "~", "~"], ["X", "~", "2", "~"], ["X", "~", "~", "3"],
                 ["X", "1", "", "rc1"], ["Opera", "", "", ""]):
        j.append(["pretty_ua"] + args)
        j.append(["pretty"] + args)
    for args in (["Windows", "10", "~", "~", "~"], ["Mac OS X", "10", "15", "7", "~"], ["iOS", "17", "1", "~", "~"],
                 ["Android", "4", "4", "w", "~"], ["Linux", "~", "~", "~", "9"], ["Other", "~", "~", "~", "~"],
                 ["Symbian OS", "9", "2", "", ""]):
        j.append(["pretty_os"] + args)
    for i in (0, 3, 15, 16):
        j.append(["pretty_parse", str(i)])
    # the backwards-compatible entry points
    j.append(["jsov", "15", UAS[0], "~", "~", "~", "~"])
    j.append(["jsov", "15", "~", "~", "~", "~", "~"])
    j.append(["jsov", "0", "~", "Iron", "31", "~", ""])
    j.append(["jsov", "0", "~", "", "31", "~", "~"])
    j.append(["jsov", "21", "~", "~", "~", "~", "~"])
    j.append(["filters", UAS[0], UAS[0], "Iron", "~", "", "7"])
    j.append(["filters", UAS[0], "~", "~", "~", "~", "~"])
    j.append(["filters", "", "", "", "0", "~", "x"])
    # match spans of single parsers
    for kind, idx, ua in (("ua", "2", "~"), ("ua", "0", "GeoEvent Server 10"), ("ua", "1", "ArcGIS Pro 3.1.2.41833"),
                          ("ua", "1", "ArcGIS Pro"), ("os", "0", "~"), ("device", "0", "~"),
                          ("ua", "2", "ArcGIS Client Using WinInet")):
        j.append(["spans", kind, idx, ua])
    # filling the cache past its size clears it
    j.append(["clear"])
    j.append(["fill", "150"])
    j.append(["cache"])
    j.append(["fill", "49"])
    j.append(["cache"])
    j.append(["ua_js", "15", "js_user_agent_string=" + UAS[8]])
    j.append(["cache"])
    j.append(["ua_js", "15", "js_user_agent_string=" + UAS[8]])
    j.append(["cache"])
    j.append(["fill", "260"])
    j.append(["cache"])
    j.append(["parse", "0"])
    j.append(["cache"])
    return j


os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "access.log"), "w", encoding="utf-8", newline="\n") as f:
    for line in log_lines():
        f.write(line + "\n")
with open(os.path.join(DATA, "agents.txt"), "w", encoding="utf-8", newline="\n") as f:
    for ua in UAS:
        f.write(ua + "\n")
with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8", newline="\n") as f:
    for job in jobs():
        f.write("\t".join(job) + "\n")
