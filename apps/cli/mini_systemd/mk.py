# The inputs of mini_systemd: vendor and admin unit files, drop-ins,
# a template, and the systemctl jobs to run. Run as a script, it writes
# them into data/; the mirror and gen_kara.py import FILES.
import os

FILES = {}
V = "usr/lib/systemd/system/"
A = "etc/systemd/system/"

FILES[V + "basic.target"] = """[Unit]
Description=Basic System
Requires=sysinit.target
After=sysinit.target
"""

FILES[V + "sysinit.target"] = """[Unit]
Description=System Initialization
Wants=systemd-journald.service local-fs.target
After=local-fs.target
"""

FILES[V + "local-fs.target"] = """[Unit]
Description=Local File Systems
"""

FILES[V + "network.target"] = """[Unit]
Description=Network
After=network-pre.target
"""

FILES[V + "network-online.target"] = """[Unit]
Description=Network is Online
Requires=network.target
After=network.target
"""

FILES[V + "multi-user.target"] = """[Unit]
Description=Multi-User System
Requires=basic.target
Conflicts=rescue.target
After=basic.target rescue.target
"""

FILES[V + "rescue.target"] = """[Unit]
Description=Rescue Mode
Requires=sysinit.target
After=sysinit.target
"""

FILES[V + "systemd-journald.service"] = """[Unit]
Description=Journal Service

[Service]
Type=notify
ExecStart=/usr/lib/systemd/systemd-journald
"""

FILES[V + "postgresql.service"] = """[Unit]
Description=PostgreSQL database server
After=network.target

[Service]
Type=notify
User=postgres
ExecStart=/usr/bin/postgres -D /var/lib/postgres/data

[Install]
WantedBy=multi-user.target
"""

FILES[V + "redis.service"] = """[Unit]
Description=Redis in-memory data store
After=network.target

[Service]
ExecStart=/usr/bin/redis-server /etc/redis/redis.conf

[Install]
WantedBy=multi-user.target
"""

FILES[V + "nginx.service"] = """[Unit]
Description=A high performance web server and a reverse proxy server
After=network.target

[Service]
Type=forking
ExecStart=/usr/sbin/nginx -g 'daemon on; master_process on;'

[Install]
WantedBy=multi-user.target
"""

FILES[A + "webapp.service"] = """# The shop's API, run by the admin.
[Unit]
Description=Shop API (%n)
Requires=postgresql.service
Wants=redis.service metrics-agent.service
After=postgresql.service redis.service network-online.target
Wants=network-online.target

[Service]
User=shop
ExecStart=/srv/shop/bin/api --port 8080

[Install]
WantedBy=multi-user.target
"""

FILES[A + "webapp.service.d/10-env.conf"] = """[Service]
Environment=RUST_LOG=info
"""

FILES[A + "webapp.service.d/20-limits.conf"] = """[Unit]
# Drop the soft dependency on redis; the cache is optional now.
Wants=
Wants=metrics-agent.service network-online.target
"""

FILES[A + "metrics-agent.service"] = """[Unit]
Description=Metrics agent
# The agent reports on the API, so it starts after it ...
After=webapp.service

[Service]
ExecStart=/usr/bin/metrics-agent --fail
"""

FILES[A + "metrics-agent.service.d/override.conf"] = """[Unit]
# ... and the admin also put it before it, which makes a cycle.
Before=webapp.service
"""

FILES[V + "getty@.service"] = """[Unit]
Description=Getty on %i
After=systemd-user-sessions.service

[Service]
ExecStart=-/sbin/agetty -o '-p -- \\\\u' --noclear %i $TERM

[Install]
WantedBy=getty.target
DefaultInstance=tty1
"""

FILES[V + "getty.target"] = """[Unit]
Description=Login Prompts
"""

FILES[A + "backup.service"] = """[Unit]
Description=Nightly backup
Requires=postgresql.service broken-mount.service
After=postgresql.service broken-mount.service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup
"""

FILES[A + "broken-mount.service"] = """[Unit]
Description=Mount the backup disk

[Service]
Type=oneshot
ExecStart=/usr/bin/mount-backup --fail
"""

FILES[A + "loop-a.service"] = """[Unit]
Description=Loop A
Requires=loop-b.service
After=loop-b.service
"""

FILES[A + "loop-b.service"] = """[Unit]
Description=Loop B
Requires=loop-a.service
After=loop-a.service
"""

FILES["jobs.txt"] = """# systemctl commands, one per line
cat webapp.service
show webapp.service
show getty@tty2.service
show missing.service
enable postgresql.service
enable redis.service
enable webapp.service
enable nginx.service
enable getty@tty3.service
enable getty@.service
enable metrics-agent.service
disable nginx.service
list-dependencies multi-user.target
start multi-user.target
list-units
start backup.service
start loop-a.service
start rescue.target
list-units
stop postgresql.service
list-units
"""


def write_all():
    for name, text in FILES.items():
        path = os.path.join("data", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="") as f:
            f.write(text)


if __name__ == "__main__":
    write_all()
