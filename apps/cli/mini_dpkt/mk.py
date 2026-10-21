"""Writes data/: three captures (a classic pcap, a pcapng file and a
big-endian nanosecond pcap) of an office network's traffic, a file that
is not a capture, and the job list. The frames are built with the copy
of dpkt in dpkt/, with addresses from the documentation ranges."""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import dpkt  # noqa: E402
from dpkt import arp, dhcp, dns, ethernet, icmp, icmp6, ip, ip6, ntp, pcap, pcapng, tcp, udp  # noqa: E402

DATA = os.path.join(HERE, "data")


def mac(s):
    return bytes(int(x, 16) for x in s.split(":"))


def ip4(s):
    return bytes(int(x) for x in s.split("."))


def ip6a(s):
    import socket
    return socket.inet_pton(socket.AF_INET6, s)


GW_MAC = mac("02:00:5e:00:00:01")
PC_MAC = mac("02:1a:2b:3c:4d:5e")
NAS_MAC = mac("02:1a:2b:00:00:09")
BCAST = mac("ff:ff:ff:ff:ff:ff")
PC = ip4("192.0.2.10")
GW = ip4("192.0.2.1")
DNS_SRV = ip4("192.0.2.53")
NTP_SRV = ip4("192.0.2.123")
WEB = ip4("203.0.113.80")
FAR = ip4("198.51.100.7")
PC6 = ip6a("2001:db8::10")
GW6 = ip6a("2001:db8::1")
DNS6 = ip6a("2001:db8::53")


def eth(src, dst, payload, etype=None):
    e = ethernet.Ethernet(src=src, dst=dst, data=payload)
    if etype is not None:
        e.type = etype
    return e


def v4(src, dst, payload, p, ident=0, ttl=64, df=False):
    pkt = ip.IP(src=src, dst=dst, p=p, id=ident, ttl=ttl, data=payload)
    if df:
        pkt.df = 1
    return pkt


def udp4(src, dst, sport, dport, payload, ident=0):
    u = udp.UDP(sport=sport, dport=dport, data=payload)
    u.ulen = 8 + len(payload)
    return v4(src, dst, u, 17, ident)


def tcp4(src, dst, sport, dport, seq, ack, flags, payload=b"", opts=b"", win=64240, ident=0):
    t = tcp.TCP(sport=sport, dport=dport, seq=seq, ack=ack, flags=flags, win=win, opts=opts, data=payload)
    t.off = (20 + len(opts)) // 4
    return v4(src, dst, t, 6, ident, df=True)


def dns_query(qid, name, qtype):
    d = dns.DNS(id=qid, op=dns.DNS_RD)
    d.qd = [dns.DNS.Q(name=name, type=qtype)]
    return bytes(d)


def rr(name, rtype, ttl, **kw):
    r = dns.DNS.RR(name=name, type=rtype, ttl=ttl)
    for k, v in kw.items():
        setattr(r, k, v)
    return r


def dns_answer(qid, name, qtype, an, ns=(), ar=()):
    d = dns.DNS(id=qid, op=dns.DNS_QR | dns.DNS_RD | dns.DNS_RA)
    d.qd = [dns.DNS.Q(name=name, type=qtype)]
    d.an = list(an)
    d.ns = list(ns)
    d.ar = list(ar)
    return bytes(d)


def dhcp_msg(op, xid, msgtype, yiaddr=0, siaddr=0, extra=()):
    opts = [(dhcp.DHCP_OPT_MSGTYPE, bytes([msgtype]))]
    opts.extend(extra)
    d = dhcp.DHCP(op=op, xid=xid, chaddr=PC_MAC + b"\x00" * 10, yiaddr=yiaddr, siaddr=siaddr, opts=opts)
    d.flags = 0x8000
    return bytes(d)


def client_hello():
    body = struct.pack(">H", 0x0303) + bytes(range(32))
    body += b"\x20" + bytes(range(0x40, 0x60))
    suites = [0x0a0a, 0x1301, 0x1302, 0x1303, 0xc02b, 0xc02f, 0xc030, 0xcca8, 0x009c, 0x000a, 0x5600]
    body += struct.pack(">H", 2 * len(suites)) + b"".join(struct.pack(">H", s) for s in suites)
    body += b"\x01\x00"
    sni_name = b"www.example.com"
    sni = struct.pack(">HBH", len(sni_name) + 3, 0, len(sni_name)) + sni_name
    alpn = b"\x00\x0c\x02h2\x08http/1.1"
    groups = struct.pack(">H", 4) + struct.pack(">HH", 0x001d, 0x0017)
    versions = b"\x04\x03\x04\x03\x03"
    exts = [(0, sni), (16, alpn), (10, groups), (43, versions), (0x3a3a, b"")]
    ext = b"".join(struct.pack(">HH", t, len(d)) + d for t, d in exts)
    body += struct.pack(">H", len(ext)) + ext
    hs = b"\x01" + struct.pack(">I", len(body))[1:] + body
    return b"\x16\x03\x01" + struct.pack(">H", len(hs)) + hs


def server_hello():
    body = struct.pack(">H", 0x0303) + bytes(range(100, 132))
    body += b"\x20" + bytes(range(0x40, 0x60))
    body += struct.pack(">H", 0x1301) + b"\x00"
    exts = [(43, b"\x03\x04"), (51, struct.pack(">HH", 0x001d, 4) + b"\xaa\xbb\xcc\xdd")]
    ext = b"".join(struct.pack(">HH", t, len(d)) + d for t, d in exts)
    body += struct.pack(">H", len(ext)) + ext
    hs = b"\x02" + struct.pack(">I", len(body))[1:] + body
    rec = b"\x16\x03\x03" + struct.pack(">H", len(hs)) + hs
    ccs = b"\x14\x03\x03\x00\x01\x01"
    app = b"\x17\x03\x03\x00\x10" + bytes(range(16))
    return rec + ccs + app


def office():
    frames = []
    t = [1700000000.0]

    def add(frame, dt=0.015625):
        t[0] += dt
        frames.append((t[0], bytes(frame) if not isinstance(frame, bytes) else frame))

    # ARP for the gateway
    add(eth(PC_MAC, BCAST, arp.ARP(sha=PC_MAC, spa=PC, tha=b"\x00" * 6, tpa=GW)))
    add(eth(GW_MAC, PC_MAC, arp.ARP(op=arp.ARP_OP_REPLY, sha=GW_MAC, spa=GW, tha=PC_MAC, tpa=PC)))
    # DHCP discover and offer
    disc = dhcp_msg(dhcp.DHCP_OP_REQUEST, 0x3903f326, dhcp.DHCPDISCOVER, extra=[
        (dhcp.DHCP_OPT_PARAM_REQ, bytes([1, 3, 6, 15, 42])),
        (dhcp.DHCP_OPT_HOSTNAME, b"laptop-7"),
        (dhcp.DHCP_OPT_CLIENT_ID, b"\x01" + PC_MAC)])
    add(eth(PC_MAC, BCAST, udp4(ip4("0.0.0.0"), ip4("255.255.255.255"), 68, 67, disc)))
    offer = dhcp_msg(dhcp.DHCP_OP_REPLY, 0x3903f326, dhcp.DHCPOFFER, yiaddr=0xc000020a, siaddr=0xc0000201, extra=[
        (dhcp.DHCP_OPT_NETMASK, ip4("255.255.255.0")),
        (dhcp.DHCP_OPT_ROUTER, GW),
        (dhcp.DHCP_OPT_DNS_SVRS, DNS_SRV + ip4("192.0.2.54")),
        (dhcp.DHCP_OPT_DOMAIN, b"office.example"),
        (dhcp.DHCP_OPT_LEASE_SEC, struct.pack(">I", 86400)),
        (dhcp.DHCP_OPT_SERVER_ID, GW)])
    add(eth(GW_MAC, BCAST, udp4(GW, ip4("255.255.255.255"), 67, 68, offer, ident=0x4242)))
    # DNS: A with a CNAME, then MX and TXT
    add(eth(PC_MAC, GW_MAC, udp4(PC, DNS_SRV, 53001, 53, dns_query(0x1a2b, "www.example.com", dns.DNS_A), ident=101)))
    add(eth(GW_MAC, PC_MAC, udp4(DNS_SRV, PC, 53, 53001, dns_answer(0x1a2b, "www.example.com", dns.DNS_A, [
        rr("www.example.com", dns.DNS_CNAME, 3600, cname="web.example.com"),
        rr("web.example.com", dns.DNS_A, 300, ip=WEB),
    ], ns=[rr("example.com", dns.DNS_NS, 86400, nsname="ns1.example.com")],
        ar=[rr("ns1.example.com", dns.DNS_A, 86400, ip=ip4("198.51.100.53"))]), ident=7001)))
    add(eth(PC_MAC, GW_MAC, udp4(PC, DNS_SRV, 53002, 53, dns_query(0x1a2c, "example.com", dns.DNS_MX), ident=102)))
    mx = rr("example.com", dns.DNS_MX, 3600, mxname="mail.example.com")
    mx.preference = 10
    mx2 = rr("example.com", dns.DNS_MX, 3600, mxname="backup.mail.example.com")
    mx2.preference = 20
    add(eth(GW_MAC, PC_MAC, udp4(DNS_SRV, PC, 53, 53002, dns_answer(0x1a2c, "example.com", dns.DNS_MX, [
        mx, mx2,
        rr("example.com", dns.DNS_TXT, 3600, text=[b"v=spf1 mx -all", b"owner=office"]),
    ]), ident=7002)))
    add(eth(PC_MAC, GW_MAC, udp4(PC, DNS_SRV, 53003, 53, dns_query(0x1a2d, "nope.example.com", dns.DNS_A), ident=103)))
    nx = dns.DNS(id=0x1a2d, op=dns.DNS_QR | dns.DNS_RD | dns.DNS_RA | dns.DNS_RCODE_NXDOMAIN)
    nx.qd = [dns.DNS.Q(name="nope.example.com", type=dns.DNS_A)]
    nx.ns = [rr("example.com", dns.DNS_SOA, 900, mname="ns1.example.com", rname="hostmaster.example.com",
                serial=2024010101, refresh=7200, retry=3600, expire=1209600, minimum=300)]
    add(eth(GW_MAC, PC_MAC, udp4(DNS_SRV, PC, 53, 53003, bytes(nx), ident=7003)))
    # HTTP over TCP, the request and the response each in two segments
    mss = b"\x02\x04\x05\xb4\x04\x02\x08\x0a\x00\x00\x10\x00\x00\x00\x00\x00\x01\x03\x03\x07"
    cs, ss = 1000, 5000
    add(eth(PC_MAC, GW_MAC, tcp4(PC, WEB, 49152, 80, cs, 0, tcp.TH_SYN, opts=mss, ident=201)))
    add(eth(GW_MAC, PC_MAC, tcp4(WEB, PC, 80, 49152, ss, cs + 1, tcp.TH_SYN | tcp.TH_ACK,
                                 opts=b"\x02\x04\x05\xb4\x01\x01\x04\x02\x01\x03\x03\x08", win=65160, ident=0)))
    add(eth(PC_MAC, GW_MAC, tcp4(PC, WEB, 49152, 80, cs + 1, ss + 1, tcp.TH_ACK, ident=202)))
    req = (b"GET /docs/index.html?lang=en HTTP/1.1\r\nHost: www.example.com\r\n"
           b"User-Agent: curl/8.5.0\r\nAccept: */*\r\nAccept: text/html\r\n\r\n")
    add(eth(PC_MAC, GW_MAC, tcp4(PC, WEB, 49152, 80, cs + 1, ss + 1, tcp.TH_ACK, req[:40], ident=203)))
    add(eth(PC_MAC, GW_MAC, tcp4(PC, WEB, 49152, 80, cs + 41, ss + 1, tcp.TH_ACK | tcp.TH_PUSH, req[40:], ident=204)))
    add(eth(GW_MAC, PC_MAC, tcp4(WEB, PC, 80, 49152, ss + 1, cs + 1 + len(req), tcp.TH_ACK, ident=1)))
    resp = (b"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nTransfer-Encoding: chunked\r\n"
            b"Set-Cookie: a=1\r\nSet-Cookie: b=2\r\nServer: nginx\r\n\r\n"
            b"17\r\n<html><body>Docs</body>\r\n7\r\n</html>\r\n0\r\n\r\n")
    add(eth(GW_MAC, PC_MAC, tcp4(WEB, PC, 80, 49152, ss + 1, cs + 1 + len(req), tcp.TH_ACK, resp[:100], ident=2)))
    add(eth(GW_MAC, PC_MAC, tcp4(WEB, PC, 80, 49152, ss + 101, cs + 1 + len(req), tcp.TH_ACK | tcp.TH_PUSH,
                                 resp[100:], ident=3)))
    add(eth(PC_MAC, GW_MAC, tcp4(PC, WEB, 49152, 80, cs + 1 + len(req), ss + 1 + len(resp),
                                 tcp.TH_ACK | tcp.TH_FIN, ident=205)))
    add(eth(GW_MAC, PC_MAC, tcp4(WEB, PC, 80, 49152, ss + 1 + len(resp), cs + 2 + len(req),
                                 tcp.TH_ACK | tcp.TH_FIN, ident=4)))
    # TLS hellos
    ch = client_hello()
    add(eth(PC_MAC, GW_MAC, tcp4(PC, WEB, 49153, 443, 777, 9000, tcp.TH_ACK | tcp.TH_PUSH, ch, ident=206)))
    sh = server_hello()
    add(eth(GW_MAC, PC_MAC, tcp4(WEB, PC, 443, 49153, 9000, 777 + len(ch), tcp.TH_ACK | tcp.TH_PUSH, sh, ident=5)))
    # ping, then a traceroute probe answered with port unreachable
    echo = icmp.ICMP(type=icmp.ICMP_ECHO, data=icmp.ICMP.Echo(id=0x0b0b, seq=1, data=b"abcdefghijklmnop"))
    add(eth(PC_MAC, GW_MAC, v4(PC, FAR, echo, 1, ident=301)))
    reply = icmp.ICMP(type=icmp.ICMP_ECHOREPLY, data=icmp.ICMP.Echo(id=0x0b0b, seq=1, data=b"abcdefghijklmnop"))
    add(eth(GW_MAC, PC_MAC, v4(FAR, PC, reply, 1, ident=9001, ttl=57)))
    probe = udp4(PC, FAR, 40000, 33434, b"\x00" * 12, ident=302)
    probe.ttl = 1
    probe_b = bytes(probe)
    unreach = icmp.ICMP(type=icmp.ICMP_UNREACH, code=icmp.ICMP_UNREACH_PORT,
                        data=icmp.ICMP.Unreach(data=probe_b[:28]))
    add(eth(GW_MAC, PC_MAC, v4(FAR, PC, unreach, 1, ident=9002, ttl=57)))
    # NTP
    req_ntp = ntp.NTP(flags=0x23, transmit_time=b"\xe9\x0f\x55\x00\x00\x00\x00\x00", id=b"\x00" * 4,
                      update_time=b"\x00" * 8, originate_time=b"\x00" * 8, receive_time=b"\x00" * 8)
    add(eth(PC_MAC, GW_MAC, udp4(PC, NTP_SRV, 123, 123, bytes(req_ntp), ident=401)))
    rep_ntp = ntp.NTP(flags=0x24, stratum=2, interval=3, precision=0xe9, delay=0x84, dispersion=0x3327,
                      id=ip4("198.51.100.123"), update_time=b"\xe9\x0f\x54\x80\x11\x22\x33\x44",
                      originate_time=b"\xe9\x0f\x55\x00\x00\x00\x00\x00",
                      receive_time=b"\xe9\x0f\x55\x00\x40\x00\x00\x00",
                      transmit_time=b"\xe9\x0f\x55\x00\x40\x10\x00\x00")
    add(eth(GW_MAC, PC_MAC, udp4(NTP_SRV, PC, 123, 123, bytes(rep_ntp), ident=402)))
    # syslog from the NAS on VLAN 100
    msg = b"<14>Nov 14 22:13:20 nas backup: job nightly finished, 2.1 GB"
    inner = bytes(udp4(ip4("192.0.2.9"), ip4("192.0.2.5"), 514, 514, msg, ident=500))
    tag = struct.pack(">HH", (3 << 13) | 100, ethernet.ETH_TYPE_IP)
    add(mac("02:00:00:00:00:05") + NAS_MAC + struct.pack(">H", ethernet.ETH_TYPE_8021Q) + tag + inner)
    # IPv6: ping, an MLDv2 report behind a hop-by-hop header, DNS
    e6 = icmp6.ICMP6(type=128, data=icmp6.ICMP6.Echo(id=7, seq=1, data=b"ping6"))
    p6 = ip6.IP6(src=PC6, dst=GW6, nxt=58, hlim=64, data=e6)
    p6.plen = len(bytes(e6))
    add(eth(PC_MAC, GW_MAC, p6, ethernet.ETH_TYPE_IP6))
    mld = b"\x8f\x00\x00\x00\x00\x00\x00\x01" + b"\x04\x00\x00\x00" + ip6a("ff02::fb")
    hbh = b"\x3a\x00\x05\x02\x00\x00\x01\x00"
    mp = ip6.IP6(src=ip6a("fe80::1a:2bff:fe3c:4d5e"), dst=ip6a("ff02::16"), nxt=0, hlim=1)
    ph = struct.pack(">16s16sxBH", mp.src, mp.dst, 58, len(mld))
    cks = icmp6.ICMP6(type=143, data=mld[4:])
    cks.sum = dpkt.in_cksum_done(dpkt.in_cksum_add(dpkt.in_cksum_add(0, ph), mld))
    body = bytes(cks)
    mp.plen = len(hbh) + len(body)
    head = mac("33:33:00:00:00:16") + PC_MAC + struct.pack(">H", ethernet.ETH_TYPE_IP6)
    add(head + bytes(mp)[:40] + hbh + body)
    q6 = udp.UDP(sport=53010, dport=53, data=dns_query(0x2b3c, "www.example.com", dns.DNS_AAAA))
    q6.ulen = 8 + len(q6.data)
    p6 = ip6.IP6(src=PC6, dst=DNS6, nxt=17, hlim=64, data=q6)
    p6.plen = q6.ulen
    add(eth(PC_MAC, GW_MAC, p6, ethernet.ETH_TYPE_IP6))
    a6 = udp.UDP(sport=53, dport=53010, data=dns_answer(0x2b3c, "www.example.com", dns.DNS_AAAA, [
        rr("www.example.com", dns.DNS_AAAA, 300, ip6=ip6a("2001:db8:80::80")),
        rr("www.example.com", dns.DNS_AAAA, 300, ip6=ip6a("2001:db8:80::1:0:0:81"))]))
    a6.ulen = 8 + len(a6.data)
    p6 = ip6.IP6(src=DNS6, dst=PC6, nxt=17, hlim=64, data=a6)
    p6.plen = a6.ulen
    add(eth(GW_MAC, PC_MAC, p6, ethernet.ETH_TYPE_IP6))
    # a datagram in two fragments
    big = udp.UDP(sport=50000, dport=9000, data=bytes((i * 7) & 0xff for i in range(60)))
    big.ulen = 68
    whole = bytes(v4(PC, FAR, big, 17, ident=0x7777))
    payload = whole[20:]
    f1 = ip.IP(src=PC, dst=FAR, p=17, id=0x7777, data=payload[:32])
    f1.mf = 1
    f2 = ip.IP(src=PC, dst=FAR, p=17, id=0x7777, data=payload[32:])
    f2.offset = 4
    add(eth(PC_MAC, GW_MAC, f1))
    add(eth(PC_MAC, GW_MAC, f2))
    # a segment whose checksums are wrong
    bad = tcp4(PC, WEB, 49154, 80, 4242, 0, tcp.TH_SYN, ident=207)
    bb = bytearray(bytes(eth(PC_MAC, GW_MAC, bad)))
    bb[24] ^= 0xff
    bb[50] ^= 0x01
    add(bytes(bb))
    # LLDP, which dpkt does not decode
    lldp = b"\x02\x07\x04" + GW_MAC + b"\x04\x04\x05ge1\x06\x02\x00\x78\x00\x00"
    add(bytes(ethernet.Ethernet(src=GW_MAC, dst=mac("01:80:c2:00:00:0e"), type=0x88cc, data=lldp)))
    # a frame cut short by the snap length
    full = bytes(eth(PC_MAC, GW_MAC, tcp4(PC, WEB, 49155, 443, 1, 1, tcp.TH_ACK, b"x" * 40, ident=208)))
    return frames, {len(frames): (full[:40], len(full))}


def write_pcap(path, frames, cut):
    with open(path, "wb") as f:
        w = pcap.Writer(f, snaplen=65535)
        for ts, frame in frames:
            w.writepkt(frame, ts=ts)
        for _, (data, n) in cut.items():
            ts = frames[-1][0] + 0.25
            sec = int(ts)
            usec = int(round(ts % 1 * 1e6))
            f.write(struct.pack("<IIII", sec, usec, len(data), n) + data)


def opt(code, data):
    return pcapng.PcapngOptionLE(code=code, data=data)


def capture_ng(path):
    """An Edge browser's keep-alive connection, from a pcapng file."""
    shb = pcapng.SectionHeaderBlockLE(opts=[
        opt(pcapng.PCAPNG_OPT_COMMENT, b"office uplink, after lunch"),
        opt(pcapng.PCAPNG_OPT_SHB_HARDWARE, b"x86_64"),
        opt(pcapng.PCAPNG_OPT_SHB_OS, b"Linux 6.8"),
        opt(pcapng.PCAPNG_OPT_SHB_USERAPPL, b"dumpcap (Wireshark) 4.2.2"),
        opt(pcapng.PCAPNG_OPT_ENDOFOPT, b"")])
    idb = pcapng.InterfaceDescriptionBlockLE(snaplen=262144, opts=[
        opt(pcapng.PCAPNG_OPT_IF_NAME, b"eth0"),
        opt(pcapng.PCAPNG_OPT_IF_TSRESOL, b"\x06"),
        opt(pcapng.PCAPNG_OPT_ENDOFOPT, b"")])
    cs, ss = 300, 70000
    req1 = b"GET /api/status HTTP/1.1\r\nHost: api.example.com\r\nConnection: keep-alive\r\n\r\n"
    body1 = b'{"status":"ok","uptime":86400}'
    resp1 = (b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: %d\r\n\r\n" % len(body1)) + body1
    req2 = (b"POST /api/jobs HTTP/1.1\r\nHost: api.example.com\r\nContent-Type: application/json\r\n"
            b"Content-Length: 13\r\n\r\n{\"job\":\"tar\"}")
    resp2 = b"HTTP/1.1 204 No Content\r\nServer: api\r\n\r\n"
    req3 = b"HEAD /api/jobs/9 HTTP/1.1\r\nHost: api.example.com\r\n\r\n"
    resp3 = b"HTTP/1.1 404 Not Found\r\nContent-Length: 9\r\n\r\n"
    segs = [
        (PC, WEB, 52000, 8080, cs, ss, tcp.TH_ACK | tcp.TH_PUSH, req1 + req2[:30], "first request"),
        (WEB, PC, 8080, 52000, ss, cs + len(req1) + 30, tcp.TH_ACK | tcp.TH_PUSH, resp1, None),
        (PC, WEB, 52000, 8080, cs + len(req1) + 30, ss + len(resp1), tcp.TH_ACK | tcp.TH_PUSH,
         req2[30:] + req3, None),
        (WEB, PC, 8080, 52000, ss + len(resp1), cs + len(req1) + len(req2) + len(req3), tcp.TH_ACK | tcp.TH_PUSH,
         resp2 + resp3, "two responses in one segment"),
        (PC, WEB, 52000, 8080, cs + len(req1) + len(req2) + len(req3), ss + len(resp1) + len(resp2) + len(resp3),
         tcp.TH_RST | tcp.TH_ACK, b"", "reset by the client"),
    ]
    with open(path, "wb") as f:
        f.write(bytes(shb))
        f.write(bytes(idb))
        ts = 1700003600 * 1000000 + 120000
        for k, (s, d, sp, dp, sq, ak, fl, pl, comment) in enumerate(segs):
            frame = bytes(eth(PC_MAC if s == PC else GW_MAC, GW_MAC if s == PC else PC_MAC,
                              tcp4(s, d, sp, dp, sq, ak, fl, pl, ident=600 + k)))
            opts = []
            if comment:
                opts = [opt(pcapng.PCAPNG_OPT_COMMENT, comment.encode()), opt(pcapng.PCAPNG_OPT_ENDOFOPT, b"")]
            ts += 31250 * (k + 1)
            epb = pcapng.EnhancedPacketBlockLE(ts_high=ts >> 32, ts_low=ts & 0xffffffff, pkt_data=frame, opts=opts)
            f.write(bytes(epb))
            if k == 1:
                # an interface statistics block, which the reader skips
                f.write(bytes(pcapng.PcapngBlockLE(type=5)))


def nano(path):
    """Two syslog datagrams in a big-endian, nanosecond pcap."""
    with open(path, "wb") as f:
        f.write(bytes(pcap.FileHdr(magic=pcap.TCPDUMP_MAGIC_NANO, snaplen=262144, linktype=1)))
        for k, (ns, msg) in enumerate([(123456789, b"<11>router: link down eth1"),
                                       (500000000, b"<13>router: link up eth1")]):
            frame = bytes(eth(GW_MAC, NAS_MAC, udp4(GW, ip4("192.0.2.9"), 514, 514, msg, ident=800 + k)))
            f.write(struct.pack(">IIII", 1700007200 + k, ns, len(frame), len(frame)) + frame)


JOBS = """# mini_dpkt jobs
info office.pcap
info capture.pcapng
info nano.pcap
info notes.txt
list office.pcap
list capture.pcapng
list nano.pcap
repr office.pcap 1 3 5 6 8 12 14 19 22 24 25 27 28 29 31 33 34 36 37 38
hexdump office.pcap 1 26
dns office.pcap
dhcp office.pcap
ntp office.pcap
http office.pcap
http capture.pcapng
tls office.pcap
checksums office.pcap
stats office.pcap
ngblocks capture.pcapng
build
errors
summary
"""


def main():
    if os.path.exists(DATA):
        shutil.rmtree(DATA)
    os.makedirs(DATA)
    frames, cut = office()
    write_pcap(os.path.join(DATA, "office.pcap"), frames, cut)
    capture_ng(os.path.join(DATA, "capture.pcapng"))
    nano(os.path.join(DATA, "nano.pcap"))
    with open(os.path.join(DATA, "notes.txt"), "w") as f:
        f.write("captures from the office uplink, kept for a week\n")
    with open(os.path.join(DATA, "jobs.txt"), "w") as f:
        f.write(JOBS)


main()
