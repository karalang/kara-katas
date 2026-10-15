divert(-1)
ifdef(`WORKERS', , `define(`WORKERS', `2')')
ifdef(`ENV', , `define(`ENV', `dev')')
define(`CONNECTIONS', `ifelse(ENV, `prod', `4096', `256')')
define(`SERVER', `    server {
        listen $1;
        server_name $2;
ifelse(ENV, `prod', `        ssl_certificate /etc/ssl/$2.pem;
')dnl
        root /srv/$2;
$3dnl
    }')
divert`'dnl
