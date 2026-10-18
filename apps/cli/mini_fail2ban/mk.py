# The inputs of mini_fail2ban: a jail.local, the filters it names, and
# the logs they read. Run as a script, it writes them into data/; the
# oracle and gen_kara.py import FILES.
import os

FILES = {}

FILES["jail.local"] = """# Jails for web1: ban after repeated failures, longer each time.
[DEFAULT]
bantime  = 600
findtime = 600
maxretry = 5
ignoreip = 127.0.0.1/8 10.0.0.0/8 192.168.1.50
bantime.increment = true
bantime.maxtime = 3600

[sshd]
enabled  = true
filter   = sshd
logpath  = data/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled  = true
filter   = nginx-http-auth
logpath  = data/log/nginx/error.log
findtime = 120

[postfix-sasl]
enabled  = true
filter   = postfix-sasl
logpath  = data/log/mail.log
bantime  = 1800
; the relay network sends from here, so 127.0.0.1 is not ignored
ignoreip = 198.51.100.0/24

[apache-auth]
enabled = false
filter  = apache-auth
logpath = data/log/apache/error.log

[dovecot]
enabled = true
filter  = dovecot
logpath = data/log/mail.log

[vsftpd]
enabled = true
filter  = vsftpd
logpath = data/log/vsftpd.log
"""

FILES["filter.d/common.conf"] = r"""# Shared by the filters that read syslog lines.
[DEFAULT]
_daemon = \S*
__hostname = \S+
__pid_re = (?:\[\d+\])
__daemon_re = %(_daemon)s%(__pid_re)s?:
__prefix_line = %(__hostname)s %(__daemon_re)s\s+
"""

FILES["filter.d/sshd.conf"] = r"""[INCLUDES]
before = common.conf

[Definition]
_daemon = sshd
failregex = ^%(__prefix_line)sFailed (?:password|publickey) for (?:invalid user )?\S+ from <HOST> port \d+
            ^%(__prefix_line)sInvalid user \S+ from <HOST> port \d+$
            ^%(__prefix_line)sConnection closed by authenticating user \S+ <HOST> port \d+ \[preauth\]$
ignoreregex = for backup from
"""

FILES["filter.d/nginx-http-auth.conf"] = r"""# Basic-auth failures in nginx's error log.
[Definition]
failregex = ^\[error\] \d+#\d+: \*\d+ user "[^"]*":? (?:password mismatch|was not found in "[^"]*"), client: <HOST>, server: \S*, request: "[^"]*", host: "[^"]*"(?:, referrer: "[^"]*")?$
ignoreregex =
"""

FILES["filter.d/postfix-sasl.conf"] = r"""[INCLUDES]
before = common.conf

[Definition]
_daemon = postfix/(?:submission/)?smtp[ds]
failregex = ^%(__prefix_line)swarning: [-._\w]+\[<HOST>\]: SASL (?:LOGIN|PLAIN|(?:CRAM|DIGEST)-MD5) authentication failed(?:: [ A-Za-z0-9+/]*={0,2})?\s*$
"""

FILES["filter.d/vsftpd.conf"] = r"""[INCLUDES]
before = common.conf

[Definition]
_daemon = vsftpd
failregex = ^%(__prefix_line)s.*FAIL LOGIN: Client "<HOST>"$
"""

FILES["log/auth.log"] = """Oct 17 03:00:01 web1 sshd[2201]: Accepted publickey for deploy from 10.0.4.12 port 51022 ssh2: ED25519 SHA256:k3J9
Oct 17 03:00:15 web1 sshd[2210]: Failed password for root from 203.0.113.7 port 52144 ssh2
Oct 17 03:00:21 web1 sshd[2210]: Failed password for root from 203.0.113.7 port 52144 ssh2
Oct 17 03:00:40 web1 sshd[2214]: Invalid user admin from 198.51.100.23 port 40022
Oct 17 03:00:41 web1 sshd[2214]: Failed password for invalid user admin from 198.51.100.23 port 40022 ssh2
Oct 17 03:01:02 web1 sshd[2210]: Failed password for root from 203.0.113.7 port 52150 ssh2
Oct 17 03:01:30 web1 sshd[2219]: Failed password for root from 203.0.113.7 port 52160 ssh2
Oct 17 03:02:00 web1 CRON[2230]: pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)
Oct 17 03:02:11 web1 sshd[2240]: Failed password for backup from 192.0.2.88 port 33010 ssh2
Oct 17 03:02:30 web1 sshd[2241]: Failed password for root from 10.0.4.99 port 33012 ssh2
Oct 17 03:03:05 web1 sshd[2250]: Connection closed by authenticating user git 2001:db8::5 port 41000 [preauth]
Oct 17 03:03:06 web1 sshd[2251]: Connection closed by authenticating user git 2001:db8::5 port 41002 [preauth]
Oct 17 03:03:08 web1 sshd[2252]: Invalid user oracle from 2001:db8::5 port 41004
-- MARK -- the rotation left a line with no timestamp
Oct 17 03:05:00 web1 sshd[2260]: Failed publickey for deploy from 198.51.100.23 port 40100 ssh2
Oct 17 03:11:30 web1 sshd[2270]: Failed password for root from 203.0.113.7 port 52300 ssh2
Oct 17 03:12:00 web1 sshd[2271]: Failed password for root from 203.0.113.7 port 52302 ssh2
Oct 17 03:12:30 web1 sshd[2272]: Failed password for root from 203.0.113.7 port 52304 ssh2
Oct 17 03:13:10 web1 sshd[2280]: Failed password for invalid user test from 192.0.2.140 port 6000 ssh2
Oct 17 03:30:00 web1 sshd[2290]: Failed password for invalid user test from 192.0.2.140 port 6002 ssh2
Oct 17 03:30:05 web1 sshd[2291]: Received disconnect from 192.0.2.140 port 6002:11: Bye Bye [preauth]
Oct 17 03:45:00 web1 sshd[2300]: Failed password for root from 203.0.113.7 port 52400 ssh2
Oct 17 03:45:01 web1 sshd[2301]: Failed password for root from 203.0.113.7 port 52402 ssh2
Oct 17 03:45:02 web1 sshd[2302]: Failed password for root from 203.0.113.7 port 52404 ssh2
Oct 17 03:46:00 web1 sshd[2310]: Failed password for root from 203.0.113.7 port 52410 ssh2
"""

FILES["log/nginx/error.log"] = """2026/10/17 04:00:00 [notice] 812#812: signal process started
2026/10/17 04:00:10 [error] 812#812: *41 user "admin": password mismatch, client: 203.0.113.50, server: example.com, request: "GET /admin/ HTTP/1.1", host: "example.com"
2026/10/17 04:00:20 [error] 812#812: *42 user "admin": password mismatch, client: 203.0.113.50, server: example.com, request: "GET /admin/ HTTP/1.1", host: "example.com"
2026/10/17 04:00:30 [error] 812#812: *43 user "admin": password mismatch, client: 203.0.113.50, server: example.com, request: "GET /admin/ HTTP/1.1", host: "example.com"
2026/10/17 04:00:40 [error] 812#812: *44 user "root": password mismatch, client: 203.0.113.50, server: example.com, request: "GET /admin/ HTTP/1.1", host: "example.com"
2026/10/17 04:01:05 [error] 812#812: *45 user "jsmith" was not found in "/etc/nginx/.htpasswd", client: 198.51.100.7, server: example.com, request: "GET /reports/ HTTP/2.0", host: "example.com", referrer: "https://example.com/"
2026/10/17 04:01:30 [error] 812#812: *46 user "ops": password mismatch, client: 192.168.1.50, server: example.com, request: "GET /admin/ HTTP/1.1", host: "example.com"
2026/10/17 04:01:31 [error] 812#812: *47 user "ops": password mismatch, client: 192.168.1.51, server: example.com, request: "GET /admin/ HTTP/1.1", host: "example.com"
2026/10/17 04:02:50 [error] 812#812: *48 user "admin": password mismatch, client: 203.0.113.50, server: example.com, request: "POST /admin/login HTTP/1.1", host: "example.com"
2026/10/17 04:03:00 [error] 812#812: *49 user "admin": password mismatch, client: 203.0.113.50, server: example.com, request: "POST /admin/login HTTP/1.1", host: "example.com"
2026/10/17 04:03:01 [error] 812#812: *50 user "admin": password mismatch, client: 203.0.113.50, server: example.com, request: "POST /admin/login HTTP/1.1", host: "example.com"
2026/10/17 04:03:02 [error] 812#812: *51 user "admin": password mismatch, client: 203.0.113.50, server: example.com, request: "POST /admin/login HTTP/1.1", host: "example.com"
2026/10/17 04:03:03 [error] 812#812: *52 user "admin": password mismatch, client: 203.0.113.50, server: example.com, request: "POST /admin/login HTTP/1.1", host: "example.com"
2026/10/17 04:04:00 [error] 812#812: *53 user "guest": password mismatch, client: 2001:db8:4::9, server: example.com, request: "GET / HTTP/1.1", host: "example.com"
2026/10/17 04:04:01 [error] 812#812: *54 user "guest": password mismatch, client: 2001:db8:4::9, server: example.com, request: "GET / HTTP/1.1", host: "example.com"
2026/10/17 04:04:02 [error] 812#812: *55 user "guest": password mismatch, client: 2001:db8:4::9, server: example.com, request: "GET / HTTP/1.1", host: "example.com"
2026/10/17 04:04:03 [error] 812#812: *56 user "guest": password mismatch, client: 2001:db8:4::9, server: example.com, request: "GET / HTTP/1.1", host: "example.com"
2026/10/17 04:04:04 [error] 812#812: *57 user "guest": password mismatch, client: 2001:db8:4::9, server: example.com, request: "GET / HTTP/1.1", host: "example.com"
2026/10/17 04:05:00 [error] 812#812: *58 open() "/var/www/html/favicon.ico" failed (2: No such file or directory), client: 198.51.100.7, server: example.com, request: "GET /favicon.ico HTTP/1.1", host: "example.com"
2026/10/17 04:14:00 [error] 812#812: *59 user "admin": password mismatch, client: 203.0.113.50, server: example.com, request: "GET /admin/ HTTP/1.1", host: "example.com"
"""

FILES["log/mail.log"] = """Oct 17 05:00:00 mx1 postfix/smtpd[3001]: connect from unknown[192.0.2.200]
Oct 17 05:00:01 mx1 postfix/smtpd[3001]: warning: unknown[192.0.2.200]: SASL LOGIN authentication failed: UGFzc3dvcmQ6
Oct 17 05:00:03 mx1 postfix/smtpd[3001]: warning: unknown[192.0.2.200]: SASL LOGIN authentication failed: UGFzc3dvcmQ6
Oct 17 05:00:05 mx1 postfix/smtpd[3001]: warning: unknown[192.0.2.200]: SASL LOGIN authentication failed: UGFzc3dvcmQ6
Oct 17 05:00:07 mx1 postfix/smtpd[3001]: warning: unknown[192.0.2.200]: SASL PLAIN authentication failed:
Oct 17 05:00:09 mx1 postfix/smtpd[3001]: warning: unknown[192.0.2.200]: SASL PLAIN authentication failed: 
Oct 17 05:00:12 mx1 postfix/smtpd[3001]: warning: unknown[192.0.2.200]: SASL LOGIN authentication failed: UGFzc3dvcmQ6
Oct 17 05:01:00 mx1 postfix/submission/smtpd[3010]: warning: mail.example.net[198.51.100.77]: SASL PLAIN authentication failed: 
Oct 17 05:01:30 mx1 postfix/smtps/smtpd[3020]: warning: unknown[192.0.2.201]: SASL LOGIN authentication failed: UGFzc3dvcmQ6
Oct 17 05:02:00 mx1 postfix/smtpd[3030]: warning: localhost[127.0.0.1]: SASL CRAM-MD5 authentication failed: PDE3ODkzLjE=
Oct 17 05:02:30 mx1 postfix/smtpd[3001]: disconnect from unknown[192.0.2.200] ehlo=1 auth=0/6 commands=1/7
Oct 17 05:40:00 mx1 postfix/smtpd[3040]: warning: unknown[192.0.2.200]: SASL LOGIN authentication failed: UGFzc3dvcmQ6
"""

def write_all():
    for name, text in FILES.items():
        path = os.path.join("data", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="") as f:
            f.write(text)

if __name__ == "__main__":
    write_all()
