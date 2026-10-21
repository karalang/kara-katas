"""Reference output for mini_dpkt: runs data/jobs.txt against the copy of
dpkt in dpkt/ and prints what each job shows."""
import io
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import dpkt  # noqa: E402
from dpkt import dhcp, dns, ethernet, http, icmp, icmp6, ip, ip6, ntp, pcap, pcapng, ssl, tcp, udp  # noqa: E402
from dpkt.utils import inet_to_str, mac_to_str  # noqa: E402

DATA = os.path.join(HERE, "data")


def err(e):
    return "error: %s: %s" % (type(e).__name__, e)


def fmt_ts(ts):
    if isinstance(ts, float):
        return "%.6f" % ts
    return str(ts)


def open_capture(name):
    f = open(os.path.join(DATA, name), "rb")
    return f, pcap.UniversalReader(f)


def frames_of(name):
    f, r = open_capture(name)
    out = list(r)
    f.close()
    return out


# ---- info and list

def job_info(name):
    try:
        f, r = open_capture(name)
    except ValueError as e:
        print(err(e))
        return
    frames = list(r)
    f.close()
    print("format: %s" % type(r).__module__.split(".")[-1])
    print("datalink: %d" % r.datalink())
    print("snaplen: %d" % r.snaplen)
    print("frames: %d" % len(frames))
    if frames:
        print("first: %s" % fmt_ts(frames[0][0]))
        print("last: %s" % fmt_ts(frames[-1][0]))
    print("captured bytes: %d" % sum(len(b) for _, b in frames))


def addr_port(a, p):
    s = inet_to_str(a)
    if ":" in s:
        return "[%s]:%d" % (s, p)
    return "%s:%d" % (s, p)


def describe_l4(src, dst, pkt):
    """One line for whatever sits on top of an IPv4 or IPv6 header."""
    d = pkt.data
    if isinstance(d, tcp.TCP):
        return "%s > %s TCP [%s] seq=%d ack=%d win=%d len=%d" % (
            addr_port(src, d.sport), addr_port(dst, d.dport), tcp.tcp_flags_to_str(d.flags),
            d.seq, d.ack, d.win, len(d.data))
    if isinstance(d, udp.UDP):
        return "%s > %s UDP len=%d" % (addr_port(src, d.sport), addr_port(dst, d.dport), len(d.data))
    head = "%s > %s" % (inet_to_str(src), inet_to_str(dst))
    if isinstance(d, icmp.ICMP):
        s = "%s ICMP type=%d code=%d" % (head, d.type, d.code)
        if isinstance(d.data, icmp.ICMP.Echo):
            s += " echo id=%d seq=%d" % (d.data.id, d.data.seq)
        elif isinstance(d.data, icmp.ICMP.Unreach):
            q = d.data.data
            s += " about %s > %s proto %d" % (inet_to_str(q.src), inet_to_str(q.dst), q.p)
        return s
    if isinstance(d, icmp6.ICMP6):
        s = "%s ICMP6 type=%d code=%d" % (head, d.type, d.code)
        if isinstance(d.data, icmp6.ICMP6.Echo):
            s += " echo id=%d seq=%d" % (d.data.id, d.data.seq)
        return s
    return "%s proto %d, %d bytes not decoded" % (head, getattr(pkt, "p", 0), len(d))


def describe(buf):
    try:
        e = ethernet.Ethernet(buf)
    except dpkt.UnpackError as x:
        return err(x)
    pre = ""
    if hasattr(e, "vlan_tags"):
        pre = "vlan %d pri %d: " % (e.vlanid, e.priority)
    d = e.data
    if isinstance(d, dpkt.Packet) and type(d).__name__ == "ARP":
        if d.op == 1:
            return pre + "ARP who-has %s tell %s" % (inet_to_str(d.tpa), inet_to_str(d.spa))
        return pre + "ARP %s is-at %s" % (inet_to_str(d.spa), mac_to_str(d.sha))
    if isinstance(d, ip.IP):
        s = "IP "
        if d.mf or d.offset:
            s += "frag id=%d off=%d mf=%d " % (d.id, d.offset * 8, d.mf)
        return pre + s + describe_l4(d.src, d.dst, d)
    if isinstance(d, ip6.IP6):
        s = "IP6 "
        if d.all_extension_headers:
            s += "ext=%s " % ",".join(type(h).__name__ for h in d.all_extension_headers)
        return pre + s + describe_l4(d.src, d.dst, d)
    return pre + "ethertype 0x%04x, %d bytes not decoded" % (e.type, len(d))


def job_list(name):
    for i, (ts, buf) in enumerate(frames_of(name), 1):
        print("%3d %s %s" % (i, fmt_ts(ts), describe(buf)))


def job_repr(name, nums):
    frames = frames_of(name)
    for n in nums:
        if n < 1 or n > len(frames):
            print("frame %d: no such frame (%d frames)" % (n, len(frames)))
            continue
        print("frame %d: %r" % (n, ethernet.Ethernet(frames[n - 1][1])))


def job_hexdump(name, nums):
    frames = frames_of(name)
    for n in nums:
        print("frame %d:" % n)
        print(dpkt.hexdump(frames[n - 1][1]))


# ---- application protocols

def udp_frames(name, ports):
    for i, (ts, buf) in enumerate(frames_of(name), 1):
        e = ethernet.Ethernet(buf)
        n = e.data
        if isinstance(n, (ip.IP, ip6.IP6)) and isinstance(n.data, udp.UDP):
            u = n.data
            if u.sport in ports or u.dport in ports:
                yield i, u


RTYPES = {1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 12: "PTR", 15: "MX", 16: "TXT", 28: "AAAA", 33: "SRV"}


def rr_text(r):
    t = r.type
    if t == dns.DNS_A:
        return inet_to_str(r.ip)
    if t == dns.DNS_AAAA:
        return inet_to_str(r.ip6)
    if t == dns.DNS_CNAME:
        return r.cname
    if t == dns.DNS_NS:
        return r.nsname
    if t == dns.DNS_MX:
        return "%d %s" % (r.preference[0], r.mxname)
    if t == dns.DNS_TXT:
        return " ".join('"%s"' % x for x in r.text)
    if t == dns.DNS_SOA:
        return "%s %s %d %d %d %d %d" % (r.mname, r.rname, r.serial, r.refresh, r.retry, r.expire, r.minimum)
    return repr(r.rdata)


def job_dns(name):
    for i, u in udp_frames(name, (53,)):
        d = dns.DNS(u.data)
        print("frame %d: id=0x%04x qr=%d opcode=%d aa=%d tc=%d rd=%d ra=%d rcode=%d" % (
            i, d.id, d.qr, d.opcode, d.aa, d.tc, d.rd, d.ra, d.rcode))
        for q in d.qd:
            print("  question %s %s" % (q.name, RTYPES.get(q.type, str(q.type))))
        for sect in ("an", "ns", "ar"):
            for r in getattr(d, sect):
                print("  %s %s %d %s %s" % (sect, r.name, r.ttl, RTYPES.get(r.type, str(r.type)), rr_text(r)))
        print("  %r" % d)


DHCP_TYPES = {1: "DISCOVER", 2: "OFFER", 3: "REQUEST", 5: "ACK", 6: "NAK", 7: "RELEASE"}
DHCP_OPTS = {1: "netmask", 3: "router", 6: "dns", 12: "hostname", 15: "domain", 51: "lease",
             53: "msgtype", 54: "server-id", 55: "params", 61: "client-id"}


def dhcp_opt(t, v):
    if t in (1, 3, 6, 54):
        return " ".join(inet_to_str(v[k:k + 4]) for k in range(0, len(v), 4))
    if t in (12, 15):
        return v.decode()
    if t == 51:
        return "%ds" % struct.unpack(">I", v)[0]
    if t == 53:
        return DHCP_TYPES[v[0]]
    if t == 55:
        return ",".join(DHCP_OPTS.get(x, str(x)) for x in v)
    return v.hex()


def job_dhcp(name):
    for i, u in udp_frames(name, (67, 68)):
        d = dhcp.DHCP(u.data)
        print("frame %d: op=%d xid=0x%08x client=%s yiaddr=%s siaddr=%s flags=0x%04x" % (
            i, d.op, d.xid, mac_to_str(d.chaddr), inet_to_str(struct.pack(">I", d.yiaddr)),
            inet_to_str(struct.pack(">I", d.siaddr)), d.flags))
        for t, v in d.opts:
            print("  option %d %s: %s" % (t, DHCP_OPTS.get(t, "?"), dhcp_opt(t, v)))
        print("  %r" % d)


def job_ntp(name):
    for i, u in udp_frames(name, (123,)):
        n = ntp.NTP(u.data)
        print("frame %d: li=%d v=%d mode=%d stratum=%d" % (i, n.li, n.v, n.mode, n.stratum))
        for f in ("update_time", "originate_time", "receive_time", "transmit_time"):
            sec, frac = struct.unpack(">II", getattr(n, f))
            if sec == 0 and frac == 0:
                print("  %s: unset" % f)
            else:
                print("  %s: %d.%06d" % (f, sec - 2208988800, frac * 1000000 >> 32))
        print("  %r" % n)


def tcp_segments(name):
    for i, (ts, buf) in enumerate(frames_of(name), 1):
        e = ethernet.Ethernet(buf)
        n = e.data
        if isinstance(n, ip.IP) and isinstance(n.data, tcp.TCP):
            yield i, n, n.data


def streams(name, port):
    """Payload of each direction of each connection on `port`, in seq order."""
    order = []
    segs = {}
    for i, n, t in tcp_segments(name):
        if t.sport != port and t.dport != port:
            continue
        key = (inet_to_str(n.src), t.sport, inet_to_str(n.dst), t.dport)
        if key not in segs:
            segs[key] = []
            order.append(key)
        if t.data:
            segs[key].append((t.seq, i, t.data))
    for key in order:
        parts = sorted(segs[key])
        yield key, [p[1] for p in parts], b"".join(p[2] for p in parts)


def job_http(name):
    for port in (80, 8080):
        for key, nums, data in streams(name, port):
            if not data:
                continue
            req = key[3] == port
            print("%s:%d > %s:%d %s, %d bytes from frames %s" % (
                key[0], key[1], key[2], key[3], "requests" if req else "responses", len(data),
                ",".join(map(str, nums))))
            while data:
                try:
                    m = http.Request(data) if req else http.Response(data)
                except dpkt.UnpackError as e:
                    print("  " + err(e))
                    break
                if req:
                    print("  %s %s HTTP/%s" % (m.method, m.uri, m.version))
                else:
                    print("  HTTP/%s %s %s" % (m.version, m.status, m.reason))
                for k, v in m.headers.items():
                    print("    %s: %r" % (k, v))
                print("    body %r" % m.body)
                print("    %r" % m)
                data = m.data


def ext_text(t, d):
    if t == 0:
        n = struct.unpack(">H", d[3:5])[0]
        return "server_name %s" % d[5:5 + n].decode()
    if t == 16:
        names = []
        k = 2
        while k < len(d):
            names.append(d[k + 1:k + 1 + d[k]].decode())
            k += 1 + d[k]
        return "alpn %s" % ",".join(names)
    if t == 10:
        return "groups %s" % ",".join("0x%04x" % x for x in struct.unpack(">%dH" % ((len(d) - 2) // 2), d[2:]))
    if t == 43:
        if len(d) == 2:
            return "supported_versions 0x%04x" % struct.unpack(">H", d)[0]
        return "supported_versions %s" % ",".join(
            "0x%04x" % x for x in struct.unpack(">%dH" % ((len(d) - 1) // 2), d[1:]))
    if t == 51:
        return "key_share group 0x%04x, %d byte key" % (struct.unpack(">H", d[:2])[0], len(d) - 4)
    return "type 0x%04x, %d bytes" % (t, len(d))


def job_tls(name):
    for i, n, t in tcp_segments(name):
        if 443 not in (t.sport, t.dport) or not t.data:
            continue
        recs, used = ssl.tls_multi_factory(t.data)
        print("frame %d: %d records, %d of %d bytes" % (i, len(recs), used, len(t.data)))
        for r in recs:
            print("  record type=%d version=0x%04x length=%d" % (r.type, r.version, r.length))
            if r.type != 22:
                print("    %r" % r)
                continue
            h = ssl.TLSHandshake(r.data)
            print("    handshake %s, %d bytes" % (ssl.HANDSHAKE_TYPES[h.type][0], h.length))
            hello = h.data
            print("    %r" % hello)
            print("    session id %d bytes" % len(hello.session_id))
            if isinstance(hello, ssl.TLSClientHello):
                for c in hello.ciphersuites:
                    print("    suite 0x%04x %s kx=%s enc=%s mac=%s pfs=%s aead=%s" % (
                        c.code, c.name, c.kx, c.encoding, c.mac, c.pfs, c.aead))
            else:
                c = hello.ciphersuite
                print("    chosen 0x%04x %s" % (c.code, c.name))
            for et, ed in getattr(hello, "extensions", []):
                print("    extension %s" % ext_text(et, ed))


# ---- checksums and statistics

def job_checksums(name):
    good = 0
    for i, (ts, buf) in enumerate(frames_of(name), 1):
        e = ethernet.Ethernet(buf)
        n = e.data
        base = 14 + 4 * len(getattr(e, "vlan_tags", []))
        if isinstance(n, ip.IP):
            raw = bytes(buf[base:base + n.hl * 4])
            got = struct.unpack(">H", raw[10:12])[0]
            want = dpkt.in_cksum(raw[:10] + b"\x00\x00" + raw[12:])
            if got != want:
                print("frame %d: ip header checksum 0x%04x, should be 0x%04x" % (i, got, want))
            else:
                good += 1
            seg = bytes(buf[base + n.hl * 4:base + n.len])
            if len(seg) != n.len - n.hl * 4:
                print("frame %d: truncated, %d of %d bytes captured" % (i, len(seg), n.len - n.hl * 4))
                continue
            if n.mf or n.offset or n.p not in (6, 17):
                continue
            src, dst = n.src, n.dst
        elif isinstance(n, ip6.IP6):
            if n.p not in (6, 17, 58):
                continue
            ext = sum(h.length for h in n.all_extension_headers)
            seg = bytes(buf[base + 40 + ext:base + 40 + n.plen])
            src, dst = n.src, n.dst
        else:
            continue
        p = n.p
        at = {6: 16, 17: 6, 58: 2}[p]
        got = struct.unpack(">H", seg[at:at + 2])[0]
        zeroed = seg[:at] + b"\x00\x00" + seg[at + 2:]
        if len(src) == 4:
            ph = struct.pack(">4s4sxBH", src, dst, p, len(seg))
        else:
            ph = struct.pack(">16s16sxBH", src, dst, p, len(seg))
        want = dpkt.in_cksum_done(dpkt.in_cksum_add(dpkt.in_cksum_add(0, ph), zeroed))
        if p == 17 and want == 0:
            want = 0xffff
        label = {6: "tcp", 17: "udp", 58: "icmp6"}[p]
        if got != want:
            print("frame %d: %s checksum 0x%04x, should be 0x%04x" % (i, label, got, want))
        else:
            good += 1
    print("%d checksums correct" % good)


SERVICES = {53: "dns", 67: "dhcp", 68: "dhcp", 80: "http", 123: "ntp", 443: "https", 514: "syslog"}


def job_stats(name):
    eth_types = {}
    protos = {}
    services = {}
    talkers = {}
    for ts, buf in frames_of(name):
        e = ethernet.Ethernet(buf)
        n = e.data
        et = "0x%04x" % (e.vlan_tags[-1].type if hasattr(e, "vlan_tags") else e.type)
        eth_types[et] = eth_types.get(et, 0) + 1
        if isinstance(n, (ip.IP, ip6.IP6)):
            p = n.p
            protos[p] = protos.get(p, 0) + 1
            src = inet_to_str(n.src)
            talkers[src] = talkers.get(src, 0) + len(buf)
            if isinstance(n.data, (tcp.TCP, udp.UDP)):
                port = min(n.data.sport, n.data.dport)
                s = SERVICES.get(port, "port %d" % port)
                services[s] = services.get(s, 0) + 1
    print("ethertypes:")
    for k in sorted(eth_types):
        print("  %s %d" % (k, eth_types[k]))
    print("ip protocols:")
    for k in sorted(protos):
        print("  %d %s %d" % (k, ip.get_ip_proto_name(k), protos[k]))
    print("services:")
    for k in sorted(services, key=lambda s: (-services[s], s)):
        print("  %s %d" % (k, services[k]))
    print("talkers by bytes sent:")
    for k in sorted(talkers, key=lambda s: (-talkers[s], s)):
        print("  %s %d" % (k, talkers[k]))


# ---- pcapng blocks

def job_ngblocks(name):
    with open(os.path.join(DATA, name), "rb") as f:
        buf = f.read()
    off = 0
    while off + 8 <= len(buf):
        btype, blen = struct.unpack("<II", buf[off:off + 8])
        blk = buf[off:off + blen]
        if btype == pcapng.PCAPNG_BT_SHB:
            b = pcapng.SectionHeaderBlockLE(blk)
            print("SHB at %d: version %d.%d, %d bytes" % (off, b.v_major, b.v_minor, b.len))
        elif btype == pcapng.PCAPNG_BT_IDB:
            b = pcapng.InterfaceDescriptionBlockLE(blk)
            print("IDB at %d: linktype %d snaplen %d" % (off, b.linktype, b.snaplen))
        elif btype == pcapng.PCAPNG_BT_EPB:
            b = pcapng.EnhancedPacketBlockLE(blk)
            ts = (b.ts_high << 32) | b.ts_low
            print("EPB at %d: iface %d ts %d.%06d caplen %d" % (off, b.iface_id, ts // 1000000, ts % 1000000, b.caplen))
        else:
            b = pcapng.PcapngBlockLE(blk)
            print("block type %d at %d, %d bytes" % (btype, off, b.len))
        for o in b.opts:
            if o.code == pcapng.PCAPNG_OPT_COMMENT:
                print("  comment %r" % o.text)
            print("  %r" % o)
        off += blen


# ---- building packets

def show_built(label, frame):
    print("%s, %d bytes:" % (label, len(frame)))
    print(dpkt.hexdump(frame))
    print("  %r" % ethernet.Ethernet(frame))


def job_build():
    a = b"\x02\x00\x00\x00\x00\xaa"
    b = b"\x02\x00\x00\x00\x00\xbb"
    src = bytes([192, 0, 2, 20])
    dst = bytes([192, 0, 2, 30])
    # a DNS answer, packed with name compression
    d = dns.DNS(id=0x0102, op=dns.DNS_QR | dns.DNS_RD | dns.DNS_RA)
    d.qd = [dns.DNS.Q(name="printer.office.example", type=dns.DNS_A)]
    r1 = dns.DNS.RR(name="printer.office.example", type=dns.DNS_CNAME, ttl=60)
    r1.cname = "prn-2.office.example"
    r2 = dns.DNS.RR(name="prn-2.office.example", type=dns.DNS_A, ttl=60)
    r2.ip = bytes([192, 0, 2, 31])
    d.an = [r1, r2]
    packed = bytes(d)
    print("dns answer, %d bytes:" % len(packed))
    print(dpkt.hexdump(packed))
    back = dns.DNS(packed)
    print("  %r" % back)
    print("  same names: %s" % ([q.name for q in back.qd] + [r.name for r in back.an] ==
                                ["printer.office.example", "printer.office.example", "prn-2.office.example"]))
    # UDP, TCP and ICMP over IPv4, with every checksum computed on packing
    u = udp.UDP(sport=5353, dport=53, data=packed)
    u.ulen = 8 + len(packed)
    show_built("udp", bytes(ethernet.Ethernet(src=a, dst=b, data=ip.IP(src=src, dst=dst, p=17, ttl=32, data=u))))
    t = tcp.TCP(sport=40001, dport=22, seq=1, ack=2, flags=tcp.TH_ACK | tcp.TH_PUSH, win=501, data=b"SSH-2.0-x\r\n")
    show_built("tcp", bytes(ethernet.Ethernet(src=a, dst=b, data=ip.IP(src=src, dst=dst, p=6, id=7, data=t))))
    echo = icmp.ICMP(type=icmp.ICMP_ECHO, data=icmp.ICMP.Echo(id=1, seq=9, data=b"hello"))
    show_built("icmp", bytes(ethernet.Ethernet(src=a, dst=b, data=ip.IP(src=src, dst=dst, p=1, data=echo))))
    # IPv6 with an ICMPv6 echo, checksummed over the pseudo-header
    e6 = icmp6.ICMP6(type=129, data=icmp6.ICMP6.Echo(id=3, seq=4, data=b"pong"))
    p6 = ip6.IP6(src=b"\x20\x01\x0d\xb8" + b"\x00" * 11 + b"\x01", dst=b"\x20\x01\x0d\xb8" + b"\x00" * 11 + b"\x02",
                 nxt=58, hlim=255, data=e6)
    p6.plen = len(bytes(e6))
    show_built("icmp6", bytes(ethernet.Ethernet(src=a, dst=b, type=ethernet.ETH_TYPE_IP6, data=p6)))
    # a VLAN tag on top
    v = ethernet.Ethernet(src=a, dst=b, vlan_tags=[ethernet.VLANtag8021Q(id=42, pri=5)],
                          data=ip.IP(src=src, dst=dst, p=17, data=udp.UDP(sport=1, dport=2, ulen=8)))
    show_built("vlan", bytes(v))
    # write both capture formats and read them back
    out = os.path.join(DATA, "out")
    os.makedirs(out, exist_ok=True)
    frames = [(1700010000.25, bytes(ethernet.Ethernet(src=a, dst=b, data=ip.IP(src=src, dst=dst, p=17,
                                                                                 data=udp.UDP(sport=9, dport=9))))),
              (1700010000.5, bytes(ethernet.Ethernet(src=b, dst=a, data=ip.IP(src=dst, dst=src, p=1, data=echo)))),
              (1700010001.125, b"\x00" * 14)]
    with open(os.path.join(out, "built.pcap"), "wb") as f:
        w = pcap.Writer(f, snaplen=2048)
        for ts, fr in frames:
            w.writepkt(fr, ts=ts)
    with open(os.path.join(out, "built.pcapng"), "wb") as f:
        w = pcapng.Writer(f, snaplen=2048)
        for ts, fr in frames:
            w.writepkt(fr, ts=ts)
    for fn in ("built.pcap", "built.pcapng"):
        with open(os.path.join(out, fn), "rb") as f:
            raw = f.read()
        print("%s, %d bytes, starts:" % (fn, len(raw)))
        print(dpkt.hexdump(raw[:48]))
        with open(os.path.join(out, fn), "rb") as f:
            r = pcap.UniversalReader(f)
            got = list(r)
        print("  read back %d frames, snaplen %d" % (len(got), r.snaplen))
        for (ts, fr), (ts0, fr0) in zip(got, frames):
            print("  %s %d bytes %s" % (fmt_ts(ts), len(fr), "same" if fr == fr0 else "DIFFERENT"))


# ---- errors

def attempt(label, fn):
    try:
        v = fn()
        print("%s: %r" % (label, v))
    except (dpkt.Error, ssl.SSL3Exception, ValueError) as e:
        print("%s: %s" % (label, err(e)))


def set_v(v):
    p = ip.IP()
    p.v = v
    return p.v


def three_tags():
    return bytes(ethernet.Ethernet(vlan_tags=[ethernet.VLANtag8021Q(id=k) for k in (1, 2, 3)]))


def no_endofopt():
    return bytes(pcapng.SectionHeaderBlockLE(opts=[pcapng.PcapngOptionLE(code=1, data=b"x")]))


def bad_rr():
    d = dns.DNS()
    d.an = [dns.DNS.RR(name="x.example", type=99)]
    return bytes(d)


def mismatch_lengths():
    blk = bytearray(bytes(pcapng.SectionHeaderBlockLE()))
    blk[-4] ^= 4
    return pcapng.SectionHeaderBlockLE(bytes(blk))


def job_errors():
    hdr = b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
    attempt("ethernet from 2 bytes", lambda: ethernet.Ethernet(b"\x00\x01"))
    attempt("ip header length 16", lambda: ip.IP(b"\x44" + b"\x00" * 19))
    attempt("tcp data offset 4", lambda: tcp.TCP(b"\x00" * 12 + b"\x40\x02" + b"\x00" * 6))
    attempt("dns pointer to itself", lambda: dns.DNS(hdr + b"\xc0\x0c\x00\x01\x00\x01"))
    attempt("dns label length 0x80", lambda: dns.DNS(hdr + b"\x80abc\x00\x00\x01\x00\x01"))
    attempt("dns name cut short", lambda: dns.DNS(hdr + b"\x03ww"))
    attempt("dns rr type 99", lambda: dns.DNS(b"\x12\x34\x81\x00\x00\x00\x00\x01\x00\x00\x00\x00"
                                              b"\x01x\x00\x00\x63\x00\x01\x00\x00\x00\x3c\x00\x01\x00"))
    attempt("pack dns rr type 99", bad_rr)
    attempt("http method", lambda: http.Request(b"FETCH / HTTP/1.1\r\n\r\n"))
    attempt("http version", lambda: http.Request(b"GET / SPDY/3\r\n\r\n"))
    attempt("http header", lambda: http.Request(b"GET / HTTP/1.1\r\nBad Header: 1\r\n\r\n"))
    attempt("http chunk size", lambda: http.Response(b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\nzz\r\n"))
    attempt("http chunked body ends early",
            lambda: http.Response(b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n5\r\nhello\r\n"))
    attempt("http short body", lambda: http.Response(b"HTTP/1.1 200 OK\r\nContent-Length: 10\r\n\r\nabc"))
    attempt("http status line", lambda: http.Response(b"HTTP/1.1 OK\r\n\r\n"))
    attempt("tls record cut short", lambda: ssl.TLSRecord(b"\x16\x03\x03\x00\x10abc"))
    attempt("tls version bytes", lambda: ssl.tls_multi_factory(b"\x16\x09\x09\x00\x01\x00"))
    attempt("tls partial record", lambda: ssl.tls_multi_factory(b"\x17\x03\x03\x00\x02ab\x17\x03\x03\x00\x09abc"))
    attempt("tls handshake type 99", lambda: ssl.TLSHandshake(b"\x63\x00\x00\x00"))
    attempt("ip version 16", lambda: set_v(16))
    attempt("ip version 15", lambda: set_v(15))
    attempt("three vlan tags", three_tags)
    attempt("pcapng options without end", no_endofopt)
    attempt("pcapng length fields", mismatch_lengths)
    attempt("pcap reader on notes.txt", lambda: pcap.Reader(open(os.path.join(DATA, "notes.txt"), "rb")))
    attempt("pcapng reader on office.pcap", lambda: pcapng.Reader(open(os.path.join(DATA, "office.pcap"), "rb")))


def job_summary(counts):
    print("jobs: %d" % counts["jobs"])
    for name in ("office.pcap", "capture.pcapng", "nano.pcap"):
        fr = frames_of(name)
        print("%s: %d frames, %d bytes" % (name, len(fr), sum(len(b) for _, b in fr)))


def main():
    with open(os.path.join(DATA, "jobs.txt")) as f:
        lines = [x.strip() for x in f if x.strip() and not x.startswith("#")]
    counts = {"jobs": 0}
    for line in lines:
        parts = line.split()
        print("== " + line)
        counts["jobs"] += 1
        cmd, args = parts[0], parts[1:]
        if cmd == "info":
            job_info(args[0])
        elif cmd == "list":
            job_list(args[0])
        elif cmd == "repr":
            job_repr(args[0], [int(x) for x in args[1:]])
        elif cmd == "hexdump":
            job_hexdump(args[0], [int(x) for x in args[1:]])
        elif cmd == "dns":
            job_dns(args[0])
        elif cmd == "dhcp":
            job_dhcp(args[0])
        elif cmd == "ntp":
            job_ntp(args[0])
        elif cmd == "http":
            job_http(args[0])
        elif cmd == "tls":
            job_tls(args[0])
        elif cmd == "checksums":
            job_checksums(args[0])
        elif cmd == "stats":
            job_stats(args[0])
        elif cmd == "ngblocks":
            job_ngblocks(args[0])
        elif cmd == "build":
            job_build()
        elif cmd == "errors":
            job_errors()
        elif cmd == "summary":
            job_summary(counts)
        else:
            print("unknown job")


main()
