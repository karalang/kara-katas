# Writes the inputs of mini_ini into data/: real-world INI files and the
# jobs that read them.
import os, shutil

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data/conf.d")

def put(name, text):
    with open("data/" + name, "w", newline="") as f:
        f.write(text)

put("app.ini", """# Settings for the orders service.
[DEFAULT]
home = /srv/orders
log_dir = %(home)s/logs
debug = no

[server]
host = 0.0.0.0
port = 8080
workers: 4
Debug = Yes
url = http://%(host)s:%(port)s/
pid_file = %(home)s/run/orders.pid

[database]
; the replica is read-only
url = postgresql://orders@db.internal:5432/orders
pool size = 10
timeout = 30s
log_file = %(log_dir)s/db.log

[paths]
static = %(home)s/static
media = %(static)s/../media
progress = 100%%
broken = %(nowhere)s/x
loop = %(loop)s
bad = 50% done
""")

put("setup.cfg", """[metadata]
name = orders
version = 2.3.1
description = Order service
long_description = file: README.md
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License

[options]
packages = find:
python_requires = >=3.10
install_requires =
    requests>=2.31
    sqlalchemy>=2.0

    # optional below
    redis>=5.0
zip_safe = False

[options.entry_points]
console_scripts =
    orders = orders.cli:main

[flake8]
max-line-length = 100
exclude = .git,__pycache__,build
""")

put("my.cnf", """# MySQL server configuration
[client]
port = 3306
socket = /var/run/mysqld/mysqld.sock

[mysqld]
user = mysql
skip-external-locking
skip-name-resolve
bind-address = 127.0.0.1
key_buffer_size = 16M
max_allowed_packet = 64M   # raised for imports
sql_mode = STRICT_TRANS_TABLES;NO_ENGINE_SUBSTITUTION

[mysqldump]
quick
quote-names
max_allowed_packet = 16M
""")

put("php.ini", """[PHP]
engine = On
short_open_tag = Off ; deprecated
precision = 14
memory_limit = 128M ;per script
error_reporting = E_ALL & ~E_DEPRECATED
display_errors = Off
date.timezone = "UTC"
include_path = ".:/usr/share/php"

[Session]
session.save_path = "/var/lib/php/sessions"
session.name = PHPSESSID;not a comment here
""")

put("buildout.cfg", """[buildout]
directory = /home/dev/project
parts = app test
eggs-directory = ${directory}/eggs
bin-directory = ${buildout:directory}/bin

[app]
recipe = zc.recipe.egg
eggs = ${buildout:parts} requests
interpreter = ${buildout:bin-directory}/py
price = $$5

[test]
recipe = zc.recipe.testrunner
defaults = ['--auto-color']
missing = ${app:nope}
nosection = ${other:thing}
colons = ${a:b:c}
syntax = ${unclosed
""")

put("git.ini", """[core]
\trepositoryformatversion = 0
\tbare = false
[remote "origin"]
\turl = git@example.org:orders.git
\tfetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
\tremote = origin
\tmerge = refs/heads/main
""")

put("unit.service", """[Unit]
Description=Orders worker
After=network.target
After=postgresql.service

[Service]
ExecStart=/srv/orders/bin/worker --queue=orders
Environment=QUEUE=orders
Environment=CONCURRENCY=4
Restart=on-failure
""")

put("defaults.ini", """[server]
host = 127.0.0.1
port = 8000
timeout = 30

[features]
search = on
beta = off
""")
put("conf.d/local.ini", """[server]
port = 9000

[features]
beta = true
export = 1
""")
put("conf.d/broken.ini", """[server]
port = 9100
this line has no delimiter
=no name
[features]
    indented = fine
another bad line
""")
put("noheader.ini", "key = value\n[later]\nx = 1\n")
put("dupsection.ini", "[a]\nx = 1\n\n[b]\ny = 2\n\n[a]\nz = 3\n")
put("dupoption.ini", "[a]\nx = 1\ny = 2\nX = 3\n")
put("valueless.ini", "[a]\nflag\n    continued\n")
put("tabs.ini", "[weird]\nkey with spaces = value with spaces  \n  leading = indented key\n\tmulti = first\n\t\tsecond\n\n\t\tthird after blank\nempty =\ncolon: yes : no\n[ spaced name ]\n[x] trailing text\nk=v\n")

put("jobs.txt", """# Each job starts with `parser`, followed by its options.
parser interpolation=basic
read data/app.ini data/missing.ini
sections
dump
get server url
getint server port
getint database timeout
getboolean server debug
getboolean DEFAULT debug
get server nothing
get cache dir
items database
set paths static /var/www/static
get paths media
set paths fine 10%%
set paths wrong 10% off
set nowhere a b
write

parser interpolation=none
read data/setup.cfg
dump
get options install_requires
get metadata classifiers
write

parser interpolation=none empty_lines=0
read data/setup.cfg
get options install_requires

parser interpolation=none no_value=1 inline=#
read data/my.cnf
dump
has mysqld skip-name-resolve
has mysqld skip-networking
get mysqld skip-external-locking
write

parser interpolation=none no_value=0
read data/my.cnf

parser interpolation=none inline=;
read data/php.ini
dump

parser interpolation=extended
read data/buildout.cfg
dump
get app interpreter

parser interpolation=none
read data/git.ini
sections
get remote "origin" fetch
write

parser interpolation=none
read data/unit.service

parser interpolation=none strict=0 delimiters==
read data/unit.service
dump

parser interpolation=basic
read data/defaults.ini data/conf.d/local.ini
dump
getboolean features search
getboolean features beta
getboolean features export
add features
add DEFAULT
add logging
set logging level INFO
remove-option server timeout
remove-option server timeout
remove-section features
remove-section features
write

parser interpolation=basic
read data/defaults.ini data/conf.d/broken.ini data/conf.d/local.ini
dump

parser interpolation=basic
read data/noheader.ini

parser interpolation=basic
read data/dupsection.ini
dump

parser interpolation=basic strict=0
read data/dupsection.ini data/dupoption.ini
dump

parser interpolation=basic
read data/dupoption.ini
dump

parser interpolation=basic no_value=1
read data/valueless.ini
dump

parser interpolation=none
read data/tabs.ini
dump
write

parser interpolation=none default=general comments=#
read data/app.ini
sections
dump
""")
