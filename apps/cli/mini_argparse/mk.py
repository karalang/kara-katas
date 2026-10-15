# Writes data/cases.txt: one command line per line, split as a POSIX shell
# splits it.
import os
os.makedirs("data", exist_ok=True)
CASES = r"""
# pkg: the main parser
pkg --help
pkg -V
pkg --version
pkg
pkg install requests
pkg -v install requests flask
pkg -vvv -q i 'flask>=3,<4' "jinja2 == 3.1"
pkg -qv add -U -j8 --target=/opt/lib numpy
pkg --verbose --verbose install --jobs=2 -r base.txt -r dev.txt pandas
pkg -C/srv/app --color never install --no-deps --user six
pkg --directory /srv/app --timeout 2.5 install six
pkg --timeout 1e3 install six
pkg --timeout soon install six
pkg --color=sometimes install six
pkg --col always install six
pkg --in https://mirror.example.org install six
pkg --index https://mirror.example.org/ install six
pkg -C install six
pkg install
pkg install --user --system six
pkg install --system --user six
pkg install -j four six
pkg install -j -3 six
pkg install --up six
pkg install --frobnicate six
pkg --frobnicate install six
pkg install six seven -- --weird-name
pkg install -- -dash-name
pkg frob
pkg install --help
pkg i -h
pkg remove -y left-pad
pkg rm --no-keep-config left-pad is-even
pkg remove --keep-config=yes left-pad
pkg remove
pkg list
pkg list 'django*' --format json --outdated
pkg list --exclude pip setuptools --exclude wheel
pkg list --exclude
pkg list a b
pkg search web framework --limit 5 --sort updated -i
pkg search web --limit 0
pkg search web --limit lots
pkg search --sort size web
pkg search
pkg config
pkg config get index-url
pkg config set index-url https://mirror.example.org --global
pkg config set timeout
pkg config unset a b c
pkg config list
pkg config list extra
pkg config delete key
pkg config --help
pkg config set --help
pkg run test
pkg run test --watch -k slow
pkg -q run lint --fix src/
pkg run
pkg list --help
pkg remove --help
pkg search --help
pkg run --help
# backup: one parser with a required group
backup --help
backup --full /home /mnt/disk
backup --incremental -n -x '*.tmp' -x .cache /home /mnt/disk
backup --since 2024-01-01 --level 19 --dedupe /etc /mnt/disk
backup --since 2024-13-01 /etc /mnt/disk
backup --since yesterday /etc /mnt/disk
backup /home /mnt/disk
backup --full --incremental /home /mnt/disk
backup --full /home
backup --full
backup --full -l 5 /home /mnt/disk
backup --full -l x /home /mnt/disk
backup --full --rate 100 500 /home /mnt/disk
backup --full --rate 100 /home /mnt/disk
backup --full --rate 100 fast /home /mnt/disk
backup --full --notify /home /mnt/disk
backup --full --notify ops@example.org /home /mnt/disk
backup --full --notify=ops@example.org /home /mnt/disk
backup --full --tz-offset -2 /home /mnt/disk
backup --full --tz-offset=-2 /home /mnt/disk
backup --full /home /mnt/disk -5
backup --full --d /home /mnt/disk
backup --full --de /home /mnt/disk
backup --full --keep 3 --keep 4 /home /mnt/disk
backup --full -nx '*.log' /home /mnt/disk
backup --full -nl9 /home /mnt/disk
backup --full -n=yes /home /mnt/disk
backup --full --dry-run=yes /home /mnt/disk
backup --inc /home /mnt/disk extra
"""
open("data/cases.txt", "w").write(CASES.lstrip("\n"))
