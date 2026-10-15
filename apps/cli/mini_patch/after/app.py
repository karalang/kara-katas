import json
import logging
import os
import time

log = logging.getLogger("shop")

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def load_config(path):
    with open(path) as f:
        return json.load(f)


def page_size(params):
    size = int(params.get("size", DEFAULT_PAGE_SIZE))
    if size < 1:
        size = 1
    if size > MAX_PAGE_SIZE:
        size = MAX_PAGE_SIZE
    return size


def list_orders(db, params):
    size = page_size(params)
    offset = int(params.get("offset", 0))
    rows = db.query("SELECT * FROM orders LIMIT ? OFFSET ?", size, offset)
    return [dict(r) for r in rows]


def cancel_order(db, order_id):
    order = db.get("orders", order_id)
    if order is None or order["status"] == "shipped":
        return False
    db.update("orders", order_id, status="cancelled", at=time.time())
    log.info("cancelled %s", order_id)
    return True


def main():
    config = load_config(os.environ.get("SHOP_CONFIG", "shop.json"))
    log.setLevel(config.get("log_level", "INFO"))
    log.info("shop starting on %s", config.get("port", 8000))


if __name__ == "__main__":
    main()
