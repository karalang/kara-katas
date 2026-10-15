import json
import logging
import os

log = logging.getLogger("shop")

DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100


def load_config(path):
    with open(path) as f:
        return json.load(f)


def page_size(params):
    size = int(params.get("size", DEFAULT_PAGE_SIZE))
    if size > MAX_PAGE_SIZE:
        size = MAX_PAGE_SIZE
    return size


def list_orders(db, params):
    size = page_size(params)
    offset = int(params.get("offset", 0))
    rows = db.query("SELECT * FROM orders LIMIT ? OFFSET ?", size, offset)
    return [dict(r) for r in rows]


def health(db):
    return db.ping()


def cancel_order(db, order_id):
    order = db.get("orders", order_id)
    if order is None:
        return False
    db.update("orders", order_id, status="canceled")
    log.info("cancelled %s", order_id)
    return True


def main():
    config = load_config(os.environ.get("SHOP_CONFIG", "shop.json"))
    log.setLevel(config.get("log_level", "INFO"))
    print("shop starting")


if __name__ == "__main__":
    main()
