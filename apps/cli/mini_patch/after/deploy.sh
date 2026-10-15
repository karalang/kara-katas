#!/bin/sh
set -eu
rsync -a --delete ./ shop@prod:/srv/shop/
ssh shop@prod 'sudo systemctl reload nginx && sudo systemctl restart shop'
