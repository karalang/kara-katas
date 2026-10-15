# Writes the input YAML files into data/.
import os
os.makedirs("data", exist_ok=True)
def w(name, text):
    open("data/" + name, "w").write(text)

w("deploy.yaml", """\
# shop API: deployment, service and config
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shop-api
  namespace: shop
  labels: &labels
    app: shop-api
    tier: backend
spec:
  replicas: 3
  selector:
    matchLabels: *labels
  template:
    metadata:
      labels: *labels
    spec:
      containers:
        - name: api
          image: registry.example.com/shop/api:1.9.0
          args: ["--port=8000", "--workers", "4"]
          ports:
            - containerPort: 8000
              protocol: TCP
          env:
            - name: DEBUG
              value: "false"
            - name: CACHE_TTL
              value: '300'
          resources:
            requests: {cpu: 250m, memory: 256Mi}
            limits:
              cpu: "1"
              memory: 512Mi
        - name: log-shipper
          image: registry.example.com/infra/vector:0.41
---
apiVersion: v1
kind: Service
metadata:
  name: shop-api
  namespace: shop
spec:
  type: ClusterIP
  selector:
    app: shop-api
  ports:
  - port: 80
    targetPort: 8000
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: shop-api-config
data:
  app.ini: |
    [server]
    port = 8000

    [cache]
    ttl = 300
  motd: >
    Welcome to the shop API.
    Deploys happen on Tuesdays.

    Ask in #shop-ops.
  empty.txt: ""
""")

w("compose.yaml", """\
version: "3.8"

x-common: &common
  restart: unless-stopped
  logging:
    driver: json-file
    options: {max-size: 10m, max-file: "3"}

services:
  web:
    <<: *common
    image: nginx:1.27
    ports:
      - "8080:80"
      - 443:443
    depends_on: [api]
  api:
    <<: *common
    build: ./api
    restart: always
    environment:
      - DATABASE_URL=postgres://shop@db/shop
      - WORKERS=4
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/healthz"]
      interval: 30s
      retries: 3
  db:
    image: postgres:16
    ports:
      - 5432:5432
    volumes:
      - db-data:/var/lib/postgresql/data
  ssh:
    image: linuxserver/openssh-server
    ports:
      - 22:22

volumes:
  db-data:
""")

w("ci.yml", """\
name: CI
on:
  push:
    branches: [main]
  pull_request:
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-24.04, macos-14]
        python: ["3.11", "3.12", 3.10]
    steps:
      - uses: actions/checkout@v4
      - name: Install
        run: |
          python -m pip install -U pip
          pip install -e ".[test]"
      - name: Test
        run: pytest -q --maxfail=1
        env:
          CI: true
          PYTHONHASHSEED: 0
      - name: Summary
        if: ${{ always() }}
        run: >-
          echo "tests finished for
          ${{ matrix.os }}" >> $GITHUB_STEP_SUMMARY
""")

w("site.yml", """\
- hosts: web
  become: yes
  vars:
    http_port: 80
    max_clients: 200
  tasks:
    - name: install nginx
      apt: name=nginx state=present update_cache=yes
    - name: write config
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        mode: 0644
      notify: restart nginx
    - name: config dir
      file: {path: /etc/nginx/conf.d, state: directory, mode: "0755"}
    - name: open firewall
      ufw: rule=allow port={{ http_port }}
      when: ansible_os_family == "Debian" and firewall_enabled
  handlers:
    - name: restart nginx
      service: name=nginx state=restarted
""")

w("edge.yaml", """\
# scalars the way YAML 1.1 (and PyYAML) read them
country: NO
answer: yes
switch: off
nothing: ~
empty:
octal: 0755
hex: 0x1F
binary: 0b1010
million: 1_000_000
sexagesimal: 190:20:30
negative: -42
float: 3.0
half: .5
exponent: 6.02e+23
not_a_float: 1e3
infinity: -.inf
version: 1.10
date: 2026-10-14
stamp: 2026-10-14T09:12:01Z
local: 2026-10-14 09:12:01.5
quoted: "tab\\there, \\u00e9, \\"quotes\\", \\\\"
single: 'it''s ''quoted'''
unicode: café
url: http://example.com/a#b
hash: not # a comment
folded plain: this plain scalar
  goes on over
  three lines
key with spaces: "value with: colon"
spaced value:   padded   
nested: {a: 1, b: [x, y, {c: d}], "e f": null}
list of lists:
- [1, 2]
- - 3
  - 4
-   five
keep: |+
  kept

strip: |-
  stripped
indented: |2
    two extra
duplicate: first
duplicate: second
1: one
true: yes
null: z
3.5: f
""")

w("multi.yaml", """\
--- # first document
a: 1
...
---
- b
- c
--- plain document
---
""")

w("tab.yaml", """\
server:
\tport: 8000
""")

w("quote.yaml", """\
name: shop
motd: "Welcome,
  please
""")

w("indent.yaml", """\
services:
  web:
    image: nginx
   ports: [80]
""")

w("alias.yaml", """\
base: &base {a: 1}
derived:
  <<: *bse
""")

w("flow.yaml", """\
ports: [80, 443
env: prod
""")

w("dash.yaml", """\
steps:
  - run: make
  run: test
""")
