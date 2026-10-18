# The inputs of mini_nginx: nginx.conf with mime.types, three broken
# configs, the document roots, and the requests. Run as a script, it
# writes them into data/; the oracle and gen_kara.py import FILES.
import os

FILES = {}

FILES["nginx.conf"] = r"""# web1: two sites, an API, per-user pages and a catch-all.
worker_processes 2;

events {
    worker_connections 1024;
}

http {
    include mime.types;
    default_type application/octet-stream;

    upstream api_backend {
        server 10.0.0.11:8080;
        server 10.0.0.12:8080;
        server 10.0.0.13:8080;
    }

    # Requests for a name no server claims are dropped.
    server {
        listen 80 default_server;
        server_name _;
        return 444;
    }

    server {
        listen 80;
        server_name example.com www.example.com;
        root data/www/example;
        index index.html index.htm;

        rewrite "^/blog/(\d{4})/(\d{2})/([a-z0-9-]+)$" /posts/$1-$2-$3.html last;
        rewrite ^/old-about$ /about/ permanent;
        rewrite ^/search$ /find?engine=local;

        location = /healthz {
            return 200 "ok\n";
        }

        location / {
            try_files $uri $uri/ =404;
        }

        location ^~ /static/ {
            root data/www/assets;
            add_header Cache-Control "max-age=86400";
        }

        location ~* \.(png|jpe?g|gif|ico)$ {
            root data/www/assets;
            add_header Cache-Control "max-age=3600";
        }

        location ~ ^/posts/ {
            try_files $uri /posts/missing.html;
        }

        location /api/ {
            proxy_pass http://api_backend;
        }

        location ~ /\. {
            return 403;
        }

        location /downloads/ {
            alias data/www/files/;
        }

        location /go/ {
            rewrite ^/go/(.*)$ https://$1 redirect;
            return 404;
        }

        location /find {
            return 200 "search: $args\n";
        }

        location /loop {
            rewrite ^ /loop2 last;
        }

        location /loop2 {
            rewrite ^ /loop last;
        }

        location /app/ {
            try_files $uri /app/index.html;
        }

        location /admin {
            return 301 https://$host$request_uri;
        }

        location /legacy/ {
            rewrite ^/legacy/(.*)$ /static/$1 break;
            root data/www/assets;
        }
    }

    server {
        listen 80;
        server_name *.example.org;
        return 302 https://example.com$request_uri;
    }

    server {
        listen 80;
        server_name mail.*;
        return 200 "webmail is down for maintenance\n";
    }

    server {
        listen 8080;
        server_name ~^(?<user>[a-z0-9]+)\.users\.example\.net$;
        root data/www/users/$user;

        location / {
            try_files $uri $uri/index.html =404;
        }
    }
}
"""

FILES["mime.types"] = """types {
    text/html                html htm;
    text/css                 css;
    text/plain               txt;
    application/javascript   js;
    application/json         json;
    application/pdf          pdf;
    image/png                png;
    image/jpeg               jpeg jpg;
    image/x-icon             ico;
}
"""

FILES["broken1.conf"] = """http {
    server {
        listen 80;
        server_name broken.example.com
    }
}
"""

FILES["broken2.conf"] = """http {
    server {
        lisen 80;
    }
}
"""

FILES["broken3.conf"] = """http {
    server {
        listen 80;
        location / {
            root data/www;
"""

FILES["requests.txt"] = """# method port host target
GET 80 example.com /
GET 80 www.example.com /about
GET 80 example.com /about/
GET 80 example.com /old-about?x=1
GET 80 example.com /blog/2026/10/hello-world?ref=feed
GET 80 example.com /blog/2026/11/not-written
GET 80 example.com /healthz
GET 80 example.com /static/site.css
GET 80 example.com /static/logo.png
GET 80 example.com /img/cat.jpg
GET 80 example.com /img/dog.gif
GET 80 example.com /api/orders?page=2
GET 80 example.com /api/users/7
GET 80 example.com /api/
GET 80 example.com /.env
GET 80 example.com /static/../.git/config
GET 80 example.com /../../etc/passwd
GET 80 example.com //app//main.js
GET 80 example.com /app/settings/profile
GET 80 example.com /downloads/report.pdf
GET 80 example.com /downloads/notes%20v2.txt
GET 80 example.com /downloads/
GET 80 example.com /docs
GET 80 example.com /docs/
GET 80 example.com /go/docs.example.com/start?lang=en
GET 80 example.com /search?q=nginx
GET 80 example.com /loop
GET 80 example.com /admin/users?sort=name
GET 80 example.com /legacy/site.css
GET 80 EXAMPLE.COM:80 /HEALTHZ
GET 80 shop.example.org /cart?id=5
GET 80 deep.shop.example.org /
GET 80 mail.example.net /inbox
GET 80 unknown.test /
GET 8080 alice.users.example.net /
GET 8080 alice.users.example.net /notes.txt
GET 8080 bob.users.example.net /
GET 8080 nobody.example.net /
"""

FILES["www/example/index.html"] = "<h1>Example</h1>\n"
FILES["www/example/about/index.html"] = "<h1>About us</h1>\n<p>Since 2009.</p>\n"
FILES["www/example/posts/2026-10-hello-world.html"] = "<article>Hello, world.</article>\n"
FILES["www/example/posts/missing.html"] = "<p>That post is gone.</p>\n"
FILES["www/example/app/index.html"] = "<div id=\"app\"></div><script src=\"/app/main.js\"></script>\n"
FILES["www/example/app/main.js"] = "console.log('app');\n"
FILES["www/example/.env"] = "DB_PASSWORD=hunter2\n"
FILES["www/example/.git/config"] = "[core]\n\tbare = false\n"
FILES["www/example/docs/guide.txt"] = "Read the guide.\n"
FILES["www/assets/static/site.css"] = "body { margin: 0; }\n"
FILES["www/assets/static/logo.png"] = "PNG-BYTES-0123456789\n"
FILES["www/assets/img/cat.jpg"] = "JPEG-CAT\n"
FILES["www/files/report.pdf"] = "%PDF-1.7 quarterly report\n"
FILES["www/files/notes v2.txt"] = "second draft\n"
FILES["www/users/alice/index.html"] = "<h1>Alice's page</h1>\n"
FILES["www/users/alice/notes.txt"] = "buy milk\n"
FILES["www/users/bob/photo.jpg"] = "JPEG-BOB\n"


def write_all():
    for name, text in FILES.items():
        path = os.path.join("data", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="") as f:
            f.write(text)


if __name__ == "__main__":
    write_all()
