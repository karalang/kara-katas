# Runs data/jobs.txt against the real statsd 0.9.0 daemon (node) and its
# real graphite backend, printing the same transcript the Kāra program
# prints. The daemon's ports are rewritten to fixed local ones, and the
# values that depend on the wall clock are normalized: flush timestamps
# become virtual ones (startup at T0, flush k at T0 + interval*(k+1)),
# millisecond timings become 0, timestamp_lag becomes 0, last_flush becomes
# the previous virtual flush time, and flush_length is the length of the
# previous normalized payload.
import os, re, socket, subprocess, sys, time

T0 = 1760000000
NODE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "realnode/node_modules/statsd/stats.js")
UDP, MGMT, GRAPHITE = 18125, 18126, 12003

out = []
proc = None
listener = socket.socket()
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(("127.0.0.1", GRAPHITE))
listener.listen(8)
state = {}

def read_flush():
    c, _ = listener.accept()
    buf = b""
    while True:
        d = c.recv(65536)
        if not d:
            break
        buf += d
    c.close()
    return buf.decode()

def normalize(payload):
    k = state["k"]
    ts = T0 + state["interval"] * (k + 1)
    prev = T0 + state["interval"] * k
    lines = []
    for line in payload.split("\n"):
        if line == "":
            continue
        key, val, _ = line.split(" ")
        base = key.split(";")[0]
        if (".graphiteStats.calculationtime" in base or ".processing_time" in base
                or ".graphiteStats.flush_time" in base or ".timestamp_lag" in base):
            val = "0"
        elif ".graphiteStats.last_flush" in base:
            val = str(prev)
        elif ".graphiteStats.flush_length" in base:
            val = str(state["last_len"])
        lines.append(f"{key} {val} {ts}")
    text = "\n".join(lines) + "\n"
    state["last_len"] = len(text)
    state["k"] = k + 1
    return text

def start(cfg):
    global proc
    if proc:
        proc.kill()
        proc.wait()
    text = open(os.path.join("data", cfg)).read()
    text = text.replace("port: 8125", f"port: {UDP}").replace("mgmt_port: 8126", f"mgmt_port: {MGMT}")
    text = text.replace("graphitePort: 2003", f"graphitePort: {GRAPHITE}")
    state["interval"] = int(re.search(r"flushInterval: (\d+)", text).group(1)) // 1000
    path = "/tmp/realstatsd-" + cfg
    open(path, "w").write(text)
    proc = subprocess.Popen(["node", NODE, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    state["k"] = 0
    state["last_len"] = 0
    normalize(read_flush())  # the silent first flush

TERM = {"counters": "END\n\n", "timers": "END\n\n", "gauges": "END\n\n", "delcounters": "END\n\n",
        "deltimers": "END\n\n", "delgauges": "END\n\n", "help": "\n\n", "health": "\n"}

def admin(cmd):
    s = socket.create_connection(("127.0.0.1", MGMT))
    s.sendall(cmd.encode())
    name = cmd.split(" ")[0]
    term = TERM.get(name, "ERROR\n")
    buf = b""
    closed = False
    s.settimeout(3)
    while True:
        try:
            d = s.recv(65536)
        except socket.timeout:
            break
        if not d:
            closed = True
            break
        buf += d
        if name != "quit" and buf.decode().endswith(term):
            break
    s.close()
    text = buf.decode()
    text = re.sub(r"(timestamp_lag'?: )-?\d+", r"\g<1>0", text)
    out.append(text)
    if closed:
        out.append("(connection closed)\n")

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for line in open("data/jobs.txt").read().split("\n"):
    if line == "" or line.startswith("#"):
        continue
    out.append(f"$ {line}\n")
    cmd, _, arg = line.partition(" ")
    if cmd == "config":
        start(arg)
    elif cmd == "send":
        udp.sendto(arg.replace("\\n", "\n").encode(), ("127.0.0.1", UDP))
        time.sleep(0.05)
    elif cmd == "admin":
        admin(arg)
    elif cmd == "flush":
        out.append(normalize(read_flush()))
    out.append("\n")
proc.kill()
sys.stdout.write("".join(out))
