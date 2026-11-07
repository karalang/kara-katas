"""Writes data/ for mini_alembic: the migration scripts of a small shop's
database (users, products, orders, a billing branch merged back in, an
experiment that fails half way), a handful of broken scripts, and the
script of commands run against them.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs(os.path.join("data", "versions"), exist_ok=True)


def put(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def mig(name, text):
    put(os.path.join("versions", name), text)


mig("1f0a3c_create_users.mig", """\
# The first table: who can sign in.
revision: 1f0a3c
down: none
message: create users

upgrade:
    create_table users id:int:pk email:text:notnull name:text
    create_index ix_users_email users email unique
downgrade:
    drop_index ix_users_email
    drop_table users
""")

mig("2b7d91_create_products.mig", """\
revision: 2b7d91
down: 1f0a3c
message: create products

upgrade:
    create_table products id:int:pk sku:text:notnull title:text price:real:notnull:default=0
    create_index ix_products_sku products sku unique
downgrade:
    drop_index ix_products_sku
    drop_table products
""")

mig("3c4e02_create_orders.mig", """\
revision: 3c4e02
down: 2b7d91
message: create orders

upgrade:
    create_table orders id:int:pk user_id:int:notnull placed:date:notnull status:text:notnull:default=new
    create_table order_items order_id:int:pk product_id:int:pk qty:int:notnull:default=1
    create_index ix_orders_user orders user_id
downgrade:
    drop_index ix_orders_user
    drop_table order_items
    drop_table orders
""")

mig("4a9b17_add_user_phone.mig", """\
revision: 4a9b17
down: 3c4e02
message: add phone to users

upgrade:
    add_column users phone:text
downgrade:
    drop_column users phone
""")

mig("5d21c8_billing_accounts.mig", """\
# Billing grows on a branch of its own until it is merged back.
revision: 5d21c8
down: 4a9b17
label: billing
message: billing accounts

upgrade:
    create_table accounts id:int:pk user_id:int:notnull balance:real:notnull:default=0
    create_index ix_accounts_user accounts user_id unique
downgrade:
    drop_index ix_accounts_user
    drop_table accounts
""")

mig("6e3f40_invoices.mig", """\
revision: 6e3f40
down: 5d21c8
message: invoices

upgrade:
    create_table invoices id:int:pk account_id:int:notnull total:real:notnull issued:date
    execute INSERT INTO invoices (id, account_id, total) SELECT 0, 0, 0 WHERE 1 = 0
downgrade:
    drop_table invoices
""")

mig("7b08d2_order_state.mig", """\
revision: 7b08d2
down: 4a9b17
message: order status becomes state

upgrade:
    rename_column orders status state
    alter_column orders state type=text notnull
downgrade:
    rename_column orders state status
""")

mig("8c5a63_merge_billing.mig", """\
revision: 8c5a63
down: 6e3f40, 7b08d2
message: merge billing into main

upgrade:
downgrade:
""")

mig("9d71e5_drop_phone.mig", """\
# Fails at its second step: the index it just made still uses the column.
revision: 9d71e5
down: 8c5a63
label: experiments
message: index phones then drop them

upgrade:
    create_index ix_users_phone users phone
    drop_column users phone
downgrade:
    add_column users phone:text
    drop_index ix_users_phone
""")

mig("a0b1c2_order_notes.mig", """\
revision: a0b1c2
down: 8c5a63
message: order notes

upgrade:
    add_column orders note:text
    rename_table order_items order_lines
downgrade:
    rename_table order_lines order_items
    drop_column orders note
""")

mig("b3c4d5_backfill_notes.mig", """\
revision: b3c4d5
down: a0b1c2
message: backfill notes

upgrade:
    execute UPDATE orders SET note = 'none' WHERE note IS NULL;
    alter_column orders note notnull
downgrade:
    alter_column orders note null
""")

mig("b3c911_index_order_state.mig", """\
revision: b3c911
down: b3c4d5
message: index order state

upgrade:
    create_index ix_orders_state orders state,placed
downgrade:
    drop_index ix_orders_state
""")

# Broken scripts. Each is reported and skipped.

mig("ab12ab_loop_a.mig", """\
revision: ab12ab
down: ab34ab
message: one half of a loop

upgrade:
downgrade:
""")

mig("ab34ab_loop_b.mig", """\
revision: ab34ab
down: ab12ab
message: the other half

upgrade:
downgrade:
""")

mig("2b7d91_products_again.mig", """\
revision: 2b7d91
down: 1f0a3c
message: products, a second time

upgrade:
    create_table products id:int:pk
downgrade:
    drop_table products
""")

mig("bb0001_no_down.mig", """\
revision: bb0001
down: 3c4e02
message: forgot the way back

upgrade:
    add_column users age:int
""")

mig("c0ffee_bad_type.mig", """\
revision: c0ffee
down: b3c911
message: carts

upgrade:
    create_table carts id:integer:pk user_id:int
downgrade:
    drop_table carts
""")

mig("cc0002_label_clash.mig", """\
revision: cc0002
down: 3c4e02
label: billing
message: a second billing

upgrade:
downgrade:
""")

mig("d00d1e_typo.mig", """\
revison: d00d1e
down: 1f0a3c
message: typo in a key

upgrade:
downgrade:
""")

mig("dd0003_outside.mig", """\
revision: dd0003
down: 1f0a3c
message: an operation before its section
add_column users age:int

upgrade:
downgrade:
""")

mig("e1e1e1_orphan.mig", """\
revision: e1e1e1
down: 777777
message: parent never written

upgrade:
downgrade:
""")

mig("e2e2e2_child_of_bad.mig", """\
revision: e2e2e2
down: c0ffee
message: child of a broken script

upgrade:
downgrade:
""")

mig("ee0004_bad_ops.mig", """\
revision: ee0004
down: 1f0a3c
message: every way to misspell an operation

upgrade:
    create_table Users id:int
downgrade:
    drop_table users
""")

mig("ee0005_bad_column.mig", """\
revision: ee0005
down: 1f0a3c
message: a column with no type

upgrade:
    add_column users nickname
downgrade:
""")

mig("ee0006_bad_flag.mig", """\
revision: ee0006
down: 1f0a3c
message: unknown flag

upgrade:
    add_column users nickname:text:unique
downgrade:
""")

mig("ee0007_unknown_op.mig", """\
revision: ee0007
down: 1f0a3c
message: unknown operation

upgrade:
    truncate users
downgrade:
""")

mig("ee0008_usage.mig", """\
revision: ee0008
down: 1f0a3c
message: wrong number of words

upgrade:
    rename_table users
downgrade:
""")

mig("ee0009_bad_index.mig", """\
revision: ee0009
down: 1f0a3c
message: index options

upgrade:
    create_index ix_x users email clustered
downgrade:
""")

mig("ee000a_dup_key.mig", """\
revision: ee000a
down: 1f0a3c
down: 2b7d91
message: two downs

upgrade:
downgrade:
""")

mig("ee000b_bad_id.mig", """\
revision: ee000b
down: 1F0A3C
message: upper case parent

upgrade:
downgrade:
""")

mig("ee000c_no_message.mig", """\
revision: ee000c
down: 1f0a3c

upgrade:
downgrade:
""")

mig("ee000d_dup_column.mig", """\
revision: ee000d
down: 1f0a3c
message: same column twice

upgrade:
    create_table tags id:int:pk name:text name:text
downgrade:
    drop_table tags
""")

mig("fa11ed_wrong_name.mig", """\
revision: fa11ee
down: 1f0a3c
message: the file name and the id disagree

upgrade:
downgrade:
""")

mig("ff0010_twice_section.mig", """\
revision: ff0010
down: 1f0a3c
message: two upgrade sections

upgrade:
    add_column users a:int
upgrade:
    add_column users b:int
downgrade:
""")

mig("ff0011_no_colon.mig", """\
revision: ff0011
down: 1f0a3c
message keeps going without a colon

upgrade:
downgrade:
""")

mig("README.txt", """\
Not a migration: only *.mig files are read.
""")

put("script.txt", """\
# A morning with the shop's migrations. `#` starts a comment.

current
heads
history

upgrade 1f0a
current
upgrade +2
schema

# Two heads now, so `head` is ambiguous.
upgrade head
upgrade billing@head
upgrade billing
current
upgrade 6e3
upgrade 7b0
current
downgrade -1
sql 8c5a63
upgrade 8c5a63
current

# The experiment fails at its second step and is rolled back.
upgrade experiments@head
current
schema
upgrade a0b1c2
upgrade +1
upgrade b3c
upgrade +2
upgrade +1
current
schema

# Stamping moves the version without touching the schema.
stamp 9d71e5
check
stamp a0b1c2
check
stamp heads
stamp b3c911
check

revision - b3c911 add carts table
revision wishlist 3c4e02 wishlists
heads
merge join experiments and carts
merge
heads
show 1f0a3c
show 8c5
show experiments
history
upgrade heads

restart
current
downgrade 4a9b17
current
schema
downgrade -2
current
sql heads
downgrade base
current
schema
check
downgrade -1
upgrade +99
upgrade zz
upgrade 1
upgrade e1e1e1
downgrade b3c911
stamp
frobnicate now
upgrade 1f0a3c 2b7d91
""")
