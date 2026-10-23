#!/usr/bin/env python3
"""Writes the inputs under data/: a schema, report definitions, two CSV
files to load and data/jobs.tsv, the script oracle.py and the port replay.

A job is "<kind>\\t<text>": "#" starts a section, "reset" starts a fresh
environment, "let" binds names to a PyPika expression, "show" prints str()
of one, and "program" runs one of the three programs.

Run: python3 -s -P -B mk.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

SCHEMA = """\
# table	column	type	null	default	keys
customers	id	INTEGER	no	-	pk
customers	email	VARCHAR(255)	no	-	unique:email
customers	name	VARCHAR(100)	no	-	-
customers	region	VARCHAR(8)	yes	'EU'	-
customers	vip	BOOLEAN	no	false	-
customers	created_at	TIMESTAMP	no	=now	-
products	sku	VARCHAR(32)	no	-	pk
products	title	VARCHAR(200)	no	-	unique:title_brand
products	brand	VARCHAR(80)	-	-	unique:title_brand
products	price	NUMERIC(10,2)	no	0	-
products	weight	FLOAT	yes	0.25	-
products	active	BOOLEAN	no	true	-
orders	id	INTEGER	no	-	pk
orders	customer_id	INTEGER	no	-	fk:customers.id
orders	status	VARCHAR(16)	no	'new'	-
orders	total	NUMERIC(12,2)	yes	-	-
orders	placed_on	DATE	no	=curdate	-
order_items	order_id	INTEGER	no	-	pk;fk:orders.id
order_items	sku	VARCHAR(32)	no	-	pk;fk:products.sku
order_items	qty	INTEGER	no	1	-
order_items	unit_price	NUMERIC(10,2)	no	-	-
audit_log	id	BIGINT	no	-	pk
audit_log	actor	VARCHAR(64)	no	'system'	-
audit_log	note	TEXT	yes	-	-
"""

# name, from, joins, select, where, groupby, having, orderby, limit, offset
REPORTS = [
    ["paid_orders", "orders:o", "-", "o.id,o.customer_id,o.total",
     "o.status=paid;o.total>=100", "-", "-", "o.total desc,o.id asc", "20", "-"],
    ["revenue_by_region", "orders:o", "inner customers c o.customer_id=c.id",
     "c.region,sum(o.total):revenue,count(*):orders",
     "o.status in paid|shipped", "c.region", "sum(o.total)>1000", "revenue desc", "-", "-"],
    ["top_customers", "customers:c", "left orders o c.id=o.customer_id",
     "c.id,c.name,upper(c.email):email,max(o.total):biggest",
     "c.vip=1 or c.region=US", "c.id,c.name", "count(*)>=3", "biggest desc", "10", "5"],
    ["basket_lines", "order_items:i", "inner orders o i.order_id=o.id;inner products p using sku",
     "o.id,p.title,i.qty,i.unit_price",
     "i.qty between 2 10;p.active=true;p.brand notnull", "-", "-", "o.id asc,p.title asc", "-", "-"],
    ["stale_carts", "orders:o", "-", "o.id,o.placed_on",
     "o.status=new;o.placed_on<2024-01-01;o.total isnull", "-", "-", "o.placed_on asc", "50", "100"],
    ["brand_search", "products:p", "-", "p.sku,lower(p.title):title,p.price",
     "p.title like %lamp% or p.brand like Lux%", "-", "-", "price asc", "-", "-"],
    ["distinct_buyers", "order_items:i", "inner orders o i.order_id=o.id",
     "i.sku,distinct(o.customer_id):buyers,avg(i.unit_price):avg_price,min(i.qty)",
     "-", "i.sku", "count(*)>1", "buyers desc", "3", "-"],
    ["region_check", "customers:c", "full orders o c.id=o.customer_id",
     "c.region,o.status", "c.region!=EU;o.status!=void", "-", "-", "-", "-", "7"],
    ["broken_report", "orders:o", "-", "o.id", "o.total>0", "-", "-", "missing asc", "-", "-"],
]

CUSTOMERS = """\
id,email,name,region,vip
1,ann@example.com,Ann Lee,EU,true
2,bo@example.com,Bo O'Brien,US,false
3,cy@example.com,Cy Ng,,true
4,di@example.com,Di Park,APAC,false
5,ed@example.com,Ed Ruiz,US,true
"""

PRODUCTS = """\
sku,title,brand,price,weight,active
L-100,Desk lamp,Luxo,49.9,1.25,true
L-200,Floor lamp,Luxo,120.0,4.5,true
C-1,Cable,,3.5,0.05,false
M-7,Monitor arm,Ergo,89,2.0,true
"""

J = []


def sec(title):
    J.append(("#", title))


def reset():
    J.append(("reset", ""))


def let(src):
    J.append(("let", src))


def show(src):
    J.append(("show", src))


def program(src):
    J.append(("program", src))


def tutorial():
    sec("The tutorial")
    let("q = Query.from_('customers').select('id', 'fname', 'lname', 'phone')")
    show("q")
    show("q.get_sql()")
    let("customers = Table('customers')")
    show("Query.from_(customers).select(customers.id, customers.fname, customers.lname, customers.phone)")
    let("customers = Table('x_view_customers').as_('customers')")
    show("Query.from_(customers).select(customers.id, customers.phone)")
    let("views = Schema('views')")
    show("Query.from_(views.customers).select(customers.id, customers.phone)")
    let("my_db = Database('my_db')")
    show("Query.from_(my_db.analytics.customers).select(customers.id, customers.phone)")
    show("Query.from_('customers').select('id', 'fname', 'lname', 'phone').orderby('id', order=Order.desc)")
    show("Query.from_('account').select(Field('revenue') - Field('cost'))")
    let("accounts = Table('accounts')")
    show("Query.from_(accounts).select(accounts.revenue - accounts.cost)")
    show("Query.from_(accounts).select((accounts.revenue - accounts.cost).as_('profit'))")
    let("table = Table('table')")
    show("Query.from_(table).select(table.foo + table.bar, table.foo - table.bar, table.foo * table.bar, "
         "table.foo / table.bar, (table.foo + table.bar) / table.fiz)")
    let("customers = Table('customers')")
    let("q = Query.from_(customers).select(customers.id, customers.fname, customers.lname, customers.phone)")
    show("q.where(customers.lname == 'Mustermann')")
    show("q.where(customers.fname == 'Max').where(customers.lname == 'Mustermann')")
    show("Query.from_(customers).select(customers.id, customers.fname).where("
         "customers.age[18:65] & customers.status.isin(['new', 'active']))")
    show("q.where((customers.age >= 18) & (customers.lname == 'Mustermann'))")
    show("q.where((customers.age >= 18) | (customers.lname == 'Mustermann'))")
    show("q.where((customers.age >= 18) ^ customers.is_registered)")
    show("Query.from_(customers).select(customers.id, customers.fname).where(Criterion.all(["
         "customers.is_registered, customers.age >= 18, customers.lname == 'Jones']))")
    show("Query.from_(customers).select(customers.id, customers.fname).where(Criterion.any(["
         "customers.is_registered, customers.age >= 18, customers.lname == 'Jones']))")
    show("Query.from_(customers).where(customers.age >= 18).groupby(customers.id)"
         ".select(customers.id, fn.Sum(customers.revenue))")
    let("payments = Table('payments')")
    show("Query.from_(payments).where(payments.transacted[date(2015, 1, 1):date(2016, 1, 1)])"
         ".groupby(payments.customer_id).having(fn.Sum(payments.total) >= 1000)"
         ".select(payments.customer_id, fn.Sum(payments.total))")
    let("history, customers = Tables('history', 'customers')")
    show("Query.from_(history).join(customers).on(history.customer_id == customers.id)"
         ".select(history.star).where(customers.id == 5)")
    show("Query.from_(history).join(customers).on_field('customer_id', 'group')"
         ".select(history.star).where(customers.group == 'A')")
    show("Query.from_(history).join(customers).using('customer_id').select(history.star)"
         ".where(customers.id == 5)")
    let("last_purchase_at = Query.from_(history).select(history.purchase_at)"
        ".where(history.customer_id == customers.customer_id)"
        ".orderby(history.purchase_at, order=Order.desc).limit(1)")
    show("Query.from_(customers).select(customers.id, last_purchase_at.as_('last_purchase_at'))")
    let("provider_a, provider_b = Tables('provider_a', 'provider_b')")
    let("q = Query.from_(provider_a).select(provider_a.created_time, provider_a.foo, provider_a.bar)")
    let("r = Query.from_(provider_b).select(provider_b.created_time, provider_b.fiz, provider_b.buz)")
    show("q + r")
    show("q * r")
    show("q.intersect(r)")
    show("q.minus(r)")
    show("q - r")
    show("q.except_of(r)")
    let("fruits = Table('fruits')")
    show("Query.from_(fruits).select(fruits.id, fruits.name)"
         ".where(fruits.harvest_date + Interval(months=1) < fn.Now())")
    let("abc = Table('abc')")
    show("Query.from_(abc).select(abc.foo, abc.bar).where(Tuple(abc.foo, abc.bar) == Tuple(1, 2))")
    show("Query.from_(abc).select(abc.foo, abc.bar).where(Tuple(abc.foo, abc.bar) == (1, 2))")
    show("Query.from_(abc).select(abc.foo, abc.bar)"
         ".where(Tuple(abc.foo, abc.bar).isin([(1, 1), (2, 2), (3, 3)]))")
    show("Query.from_(customers).select(customers.id, customers.fname, customers.lname)"
         ".where(customers.lname.like('Mc%'))")
    show("Query.from_(customers).select(customers.id, customers.fname, customers.lname)"
         ".where(customers.lname.regex('^[abc][a-zA-Z]+&'))")
    show("Query.from_(customers).select(customers.id, "
         "fn.Concat(customers.fname, ' ', customers.lname).as_('full_name'))")
    let("DateDiff = CustomFunction('DATE_DIFF', ['interval', 'start_date', 'end_date'])")
    show("Query.from_(customers).select(customers.id, customers.fname, customers.lname, "
         "DateDiff('day', customers.created_date, customers.updated_date))")
    show("Query.from_(customers).select(customers.id, Case()"
         ".when(customers.fname == 'Tom', 'It was Tom')"
         ".when(customers.fname == 'John', 'It was John')"
         ".else_('It was someone else.').as_('who_was_it'))")
    let("sub_query = Query.from_(customers).select('*')")
    show("Query.with_(sub_query, 'an_alias').from_(AliasedQuery('an_alias')).select('*')")
    show("Query.into(customers).insert(1, 'Jane', 'Doe', 'jane@example.com')")
    show("customers.insert(1, 'Jane', 'Doe', 'jane@example.com')")
    show("Query.into(customers).insert(1, 'Jane', 'Doe', 'jane@example.com')"
         ".insert(2, 'John', 'Doe', 'john@example.com')")
    show("Query.into(customers).insert((1, 'Jane', 'Doe', 'jane@example.com'), "
         "(2, 'John', 'Doe', 'john@example.com'))")
    show("MySQLQuery.into(customers).insert(1, 'Jane', 'Doe', 'jane@example.com')"
         ".on_duplicate_key_ignore()")
    show("MySQLQuery.into(customers).insert(1, 'Jane', 'Doe', 'jane@example.com')"
         ".on_duplicate_key_update(customers.email, Values(customers.email))")
    show("PostgreSQLQuery.into(customers).insert(1, 'Jane', 'Doe', 'jane@example.com')"
         ".on_conflict(customers.email).do_nothing()")
    show("PostgreSQLQuery.into(customers).insert(1, 'Jane', 'Doe', 'jane@example.com')"
         ".on_conflict(customers.email).do_update(customers.email, 'bob@example.com')")
    show("Query.into(customers).columns('id', 'fname', 'lname').insert(1, 'Jane', 'Doe')")
    let("customers, customers_backup = Tables('customers', 'customers_backup')")
    show("Query.into(customers_backup).from_(customers).select('*')")
    show("Query.into(customers_backup).columns('id', 'fname', 'lname')"
         ".from_(customers).select(customers.id, customers.fname, customers.lname)")
    let("customers, orders, orders_backup = Tables('customers', 'orders', 'orders_backup')")
    show("Query.into(orders_backup).columns('id', 'address', 'customer_fname', 'customer_lname')"
         ".from_(customers).join(orders).on(orders.customer_id == customers.id)"
         ".select(orders.id, customers.fname, customers.lname)")
    show("Query.update(customers).set(customers.last_login, '2017-01-01 10:00:00')")
    show("Query.update(customers).set(customers.lname, 'smith').where(customers.id == 10)")
    let("customers, profiles = Tables('customers', 'profiles')")
    show("Query.update(customers).join(profiles).on(profiles.customer_id == customers.id)"
         ".set(customers.lname, profiles.lname)")
    show("customers.update().set(customers.lname, 'smith').where(customers.id == 10)")
    show("customers.update().set(customers.lname, 'smith').limit(2)")
    show("Query.into(customers).columns('id', 'fname', 'lname')"
         ".insert(Parameter(':1'), Parameter(':2'), Parameter(':3'))")
    let("t = Table('abc')")
    show("Query.from_(t.for_(SYSTEM_TIME.as_of('2020-01-01'))).select('*')")
    show("Query.from_(t.for_(SYSTEM_TIME.between('2020-01-01', '2020-02-01'))).select('*')")
    show("Query.from_(t.for_(SYSTEM_TIME.from_to('2020-01-01', '2020-02-01'))).select('*')")
    show("Query.from_(t.for_(SYSTEM_TIME.all_())).select('*')")
    show("Query.from_(t.for_(t.valid_period.between('2020-01-01', '2020-02-01'))).select('*')")
    let("t0 = Table('abc').for_(SYSTEM_TIME.as_of('2020-01-01'))")
    let("t1 = Table('efg').for_(SYSTEM_TIME.as_of('2020-01-01'))")
    show("Query.from_(t0).join(t1).on(t0.foo == t1.bar).select('*')")
    show("Query.update(t.for_portion(SYSTEM_TIME.from_to('2020-01-01', '2020-02-01'))).set('foo', 'bar')")
    show("Query.from_(t.for_portion(t.valid_period.from_to('2020-01-01', '2020-02-01'))).delete()")
    show("t.for_(SYSTEM_TIME.all_()).for_(SYSTEM_TIME.all_())")
    show("t.for_portion(SYSTEM_TIME.all_()).for_(SYSTEM_TIME.all_())")
    show("Query.create_table('person').columns("
         "Column('id', 'INT', nullable=False), "
         "Column('first_name', 'VARCHAR(100)', nullable=False), "
         "Column('last_name', 'VARCHAR(100)', nullable=False), "
         "Column('phone_number', 'VARCHAR(20)', nullable=True), "
         "Column('status', 'VARCHAR(20)', nullable=False, default=ValueWrapper('NEW')), "
         "Column('date_of_birth', 'DATETIME'))"
         ".unique('last_name', 'first_name').primary_key('id')")
    show("Query.create_table('names').as_select(Query.from_('person').select('last_name', 'first_name'))")


def values_and_quoting():
    sec("Values, quoting and get_sql options")
    reset()
    let("t = Table('t')")
    let("f = Field('x')")
    for v in ["1", "-7", "2.5", "0.1", "100.0", "'abc'", "\"O'Brien\"", "''", "True", "False", "None",
              "date(2024, 2, 29)", "[1, 2, 3]", "(1, 'a')", "[]", "Order.asc", "DatePart.year"]:
        show("f == %s" % v)
    show("f != 3")
    show("f > 3")
    show("f >= 3")
    show("f < 3")
    show("f <= 3")
    show("3 < f")
    show("3 == f")
    show("'a' != f")
    show("f.eq(1)")
    show("f.ne(1)")
    show("f.gt(1)")
    show("f.gte(1)")
    show("f.lt(1)")
    show("f.lte(1)")
    show("ValueWrapper('x')")
    show("ValueWrapper('x', alias='y')")
    show("ValueWrapper(3.75)")
    show("ValueWrapper(True)")
    show("ValueWrapper(None)")
    show("ValueWrapper(date(1999, 12, 31))")
    show("NullValue()")
    show("NULL")
    show("NULL.as_('nothing')")
    show("t.x")
    show("t.x.as_('y')")
    show("t.x.get_sql()")
    show("t.x.get_sql(with_namespace=True)")
    show("t.x.get_sql(with_namespace=True, quote_char='`')")
    show("t.x.as_('y').get_sql(with_alias=True)")
    show("t.x.as_('y').get_sql(with_alias=True, quote_char='\"')")
    show("t.x.as_('y').get_sql(with_alias=True, alias_quote_char=\"'\", as_keyword=True)")
    show("(t.x == 'it''s').get_sql(quote_char=None, secondary_quote_char='\"')")
    show("(t.x == 'say \"hi\"').get_sql(secondary_quote_char='\"')")
    show("(t.x == 'it''s').get_sql()")
    show("t.as_('u').x")
    show("t.as_('u').x.get_sql(quote_char='\"')")
    show("Table('t', schema='s').x.get_sql(with_namespace=True, quote_char='\"')")
    show("Field('x', table=Table('t', schema='s'))")
    show("Field('x', alias='y', table=t)")
    show("Field('x', alias='y', table=t).get_sql(with_alias=True, with_namespace=True)")
    show("t['select']")
    show("t.field('from')")
    show("t.star")
    show("t.star.get_sql(with_namespace=True, quote_char='\"')")
    show("t.as_('u').star")
    show("t")
    show("t.as_('u')")
    show("Table('t', schema='s')")
    show("Table('t', schema=['db', 'sales'])")
    show("Table('t', schema=('a', 'b', 'c'), alias='z')")
    show("Table('t', schema=Database('db').sales)")
    show("Table('t').get_sql()")
    show("Table('t').as_('u').get_sql(quote_char='`', alias_quote_char=\"'\", as_keyword=True)")
    show("t.alias")
    show("t.as_('u').alias")
    show("t.get_table_name()")
    show("t.as_('u').get_table_name()")
    show("Table('a') == Table('a')")
    show("Table('a') == Table('b')")
    show("Table('a') == Table('a').as_('b')")
    show("Table('a', schema='s') == Table('a', schema='s')")
    show("Table('a', schema='s') == Table('a', schema='r')")
    show("Table('a', schema='s') == Table('a')")
    show("Table('a') != Table('a')")
    show("Query.from_('x') == Query.from_('y')")
    show("Query.from_('x').as_('p') == Query.from_('x')")
    show("Index('idx')")
    show("Values(t.x)")
    show("Values('x')")


def arithmetic():
    sec("Arithmetic")
    reset()
    let("t = Table('t')")
    let("a, b, c = t.a, t.b, t.c")
    for e in ["a + b", "a - b", "a * b", "a / b", "a + b + c", "a - b - c", "a - (b - c)", "a - (b + c)",
              "a + (b - c)", "(a + b) * c", "a * (b + c)", "a * (b - c)", "(a - b) / c", "a / (b * c)",
              "a / b / c", "a / (b / c)", "a * b * c", "a * (b * c)", "(a * b) + c", "a + b * c",
              "-a", "-(a + b)", "+a", "a * -b", "a << 2", "a >> 1", "(a + 1) << 2", "a ** 2", "a % 3",
              "(a + b) ** 2", "1 + a", "10 - a", "2 * (a + 1)", "1.5 / a", "None + a",
              "a + None", "a + 'x'", "a + Interval(days=1)", "a - Interval(hours=2, minutes=5)",
              "a.lshift(1)", "a.rshift(1)", "Bracket(a + b) * c", "(a + b).as_('s')"]:
        show(e)
    show("(a + b).as_('s').get_sql(with_alias=True)")
    show("(a + b).get_sql(with_namespace=True, quote_char='`')")
    show("Query.from_(t).select((a + b).as_('s'), (a * 2).as_('d'), -a)")
    show("2 * 3")
    show("7 - 10")
    show("-(-4)")


def criteria():
    sec("Criteria")
    reset()
    let("t = Table('t')")
    let("x, y, z = t.x, t.y, t.z")
    for e in ["(x == 1) & (y == 2)", "(x == 1) | (y == 2)", "(x == 1) ^ (y == 2)",
              "(x == 1) & (y == 2) & (z == 3)", "((x == 1) | (y == 2)) & (z == 3)",
              "(x == 1) | ((y == 2) & (z == 3))", "((x == 1) & (y == 2)) | ((x == 3) & (y == 4))",
              "((x == 1) | (y == 2)) | (z == 3)", "~(x == 1)", "~((x == 1) & (y == 2))",
              "(x == 1) & ~(y == 2)", "~~(x == 1)", "~x", "x & y", "x | ~y", "(x > 1).negate()",
              "x.isnull()", "x.notnull()", "x.isnotnull()", "~x.isnull()", "x.isnull() & y.notnull()",
              "x.between(1, 10)", "x[1:10]", "x['a':'m']", "x.between(fn.Now(), date(2030, 1, 1))",
              "x.isin([1, 2, 3])", "x.isin((1,))", "x.isin(['a', None])", "x.isin([])",
              "x.notin([1, 2])", "x.isin([1, 2]).negate()", "x.isin(Tuple(1, 2))",
              "x.like('a%')", "x.not_like('a%')", "x.ilike('A%')", "x.not_ilike('A%')",
              "x.rlike('^a')", "x.regex('^a+$')", "x.regexp('b')", "x.glob('*.txt')",
              "x.bin_regex('A')", "x.bitwiseand(4) == 4", "x.bitwiseand(1)", "x.as_of('2020')",
              "x.all_()", "x.from_to(1, 2)", "x[5]", "(x == 1).as_('flag')",
              "Criterion.all([])", "Criterion.any([x == 1])", "Criterion.all([x == 1, y == 2])",
              "Criterion.any([x == 1, y == 2, z == 3])", "Criterion.all([x, y]) | z",
              "EmptyCriterion() & (x == 1)", "EmptyCriterion() | (x == 1)", "(x == 1) & EmptyCriterion()",
              "EmptyCriterion()", "Not(x == 1)", "Not(x)", "x == y", "x != y + 1",
              "(x + 1) & (y == 2)", "x.isin([1]) & x.notin([2])"]:
        show(e)
    show("((x == 1) & (y == 2)).get_sql(subcriterion=True)")
    show("((x == 1) | (y == 2)).get_sql(subcriterion=True, quote_char='`')")
    show("(x == 'a').get_sql(quote_char='`', secondary_quote_char='\"', with_alias=True)")
    show("(x == 1).as_('f').get_sql(with_alias=True)")
    show("(x == 1).as_('f').get_sql(with_alias=True, alias_quote_char='\"')")
    show("x.isnull().as_('n').get_sql(with_alias=True)")
    show("x.isin([1]).as_('i').get_sql(quote_char='\"')")
    show("x.between(1, 2).as_('b')")
    show("Query.from_(t).select(x == 1, (x == 1).as_('f'), ((x == 1) & (y == 2)).as_('g'), x.isnull().as_('n'))")
    show("Query.from_(t).select(x).where((x == 1).as_('f'))")
    show("Query.from_(t).select(x).where(~((x == 1) | (y == 2)))")
    show("Query.from_(t).select(x).where(Not((x == 1) | (y == 2)) & (z == 3))")
    show("Query.from_(t).select(x).where(((x == 1) & (y == 2)) == True)")
    show("Query.from_(t).select(x).where(EmptyCriterion())")
    show("Query.from_(t).select(x).where(Criterion.any([]))")
    show("Query.from_(t).select(x).where(x == 1).where(Criterion.all([]))")
    show("Query.from_(t).select(x).where(x == 1).having(EmptyCriterion())")


def aggregation():
    sec("Aggregates and is_aggregate")
    reset()
    let("t = Table('t')")
    for e in ["fn.Sum(t.x).is_aggregate", "fn.Count('*').is_aggregate", "t.x.is_aggregate",
              "(t.x + 1).is_aggregate", "(fn.Sum(t.x) + 1).is_aggregate", "(fn.Sum(t.x) + t.y).is_aggregate",
              "(fn.Sum(t.x) / fn.Count('*')).is_aggregate", "ValueWrapper(1).is_aggregate",
              "fn.Coalesce(fn.Sum(t.x), 0).is_aggregate", "fn.Coalesce(t.x, 0).is_aggregate",
              "fn.Now().is_aggregate", "(fn.Sum(t.x) > 3).is_aggregate", "(t.x > 3).is_aggregate",
              "((fn.Sum(t.x) > 3) & (fn.Max(t.y) < 9)).is_aggregate", "an.Rank().is_aggregate",
              "an.Sum(t.x).is_aggregate", "Case().when(t.x == 1, fn.Sum(t.y)).is_aggregate",
              "Case().when(fn.Sum(t.x) > 1, 1).else_(t.y).is_aggregate",
              "Case().when(fn.Sum(t.x) > 1, 1).else_(0).is_aggregate",
              "Tuple(fn.Sum(t.x), 1).is_aggregate", "(-fn.Sum(t.x)).is_aggregate",
              "fn.Sum(t.x).isin([1]).is_aggregate", "fn.Sum(t.x)[1:2].is_aggregate",
              "fn.Sum(t.x).isnull().is_aggregate", "Interval(days=1).is_aggregate",
              "NULL.is_aggregate", "Parameter('?').is_aggregate", "(fn.Sum(t.x) + Parameter('?')).is_aggregate",
              "EmptyCriterion().is_aggregate", "Not(fn.Sum(t.x) > 1).is_aggregate",
              "Query.from_(t).select(t.x).is_aggregate"]:
        show(e)


def functions():
    sec("Functions")
    reset()
    let("t = Table('t')")
    for e in ["fn.Count('*')", "fn.Count(t.id)", "fn.Count(t.id).distinct()", "fn.Count('id')",
              "fn.Sum(t.x)", "fn.Sum(t.x).distinct()", "fn.Sum(t.x, alias='total')", "fn.Avg(t.x)",
              "fn.Min(t.x)", "fn.Max(t.x)", "fn.Std(t.x)", "fn.StdDev(t.x)", "fn.Abs(t.x)",
              "fn.First(t.x)", "fn.Last(t.x)", "fn.Sqrt(t.x)", "fn.Floor(t.x)",
              "fn.ApproximatePercentile(t.x, 0.5)", "fn.ApproximatePercentile(t.x, 1)",
              "fn.Cast(t.x, SqlTypes.VARCHAR(255))", "fn.Cast(t.x, SqlTypes.VARCHAR)",
              "fn.Cast(t.x, SqlTypes.INTEGER)", "fn.Cast(t.x, 'numeric(10,2)')",
              "fn.Cast(t.x, SqlTypes.LONG_VARCHAR(10))", "fn.Signed(t.x)", "fn.Unsigned(t.x)",
              "fn.Date(t.d)", "fn.DateDiff('day', t.a, t.b)", "fn.TimeDiff(t.a, t.b)",
              "fn.DateAdd(DatePart.day, 1, t.d)", "fn.DateAdd('week', -2, t.d)",
              "fn.ToDate('2024-01-31', 'YYYY-MM-DD')", "fn.Timestamp(t.d)",
              "fn.TimestampAdd(DatePart.month, 2, t.d)", "fn.TimestampAdd('hour', 1, fn.Now())",
              "fn.Ascii(t.s)", "fn.NullIf(t.a, 0)", "fn.Bin(t.n)", "fn.Concat(t.a, '-', t.b, 7)",
              "fn.Concat()", "fn.Insert(t.s, 1, 2, 'xy')", "fn.Length(t.s)", "fn.Upper(t.s)",
              "fn.Lower(t.s)", "fn.Substring(t.s, 2, 5)", "fn.Reverse(t.s)", "fn.Trim(t.s)",
              "fn.SplitPart(t.s, ',', 2)", "fn.RegexpMatches(t.s, '^a')",
              "fn.RegexpMatches(t.s, '^a', 'i')", "fn.RegexpLike(t.s, 'x+')",
              "fn.Replace(t.s, 'a', 'b')", "fn.Now()", "fn.UtcTimestamp()", "fn.CurTimestamp()",
              "fn.CurDate()", "fn.CurTime()", "fn.Extract(DatePart.year, t.d)",
              "fn.Extract('dow', t.d)", "fn.Extract(DatePart.microsecond, fn.Now())",
              "fn.IsNull(t.x)", "fn.Coalesce(t.x, t.y, 0)", "fn.Coalesce(t.x)",
              "fn.IfNull(t.x, 'none')", "fn.NVL(t.x, 0)", "fn.ToChar(t.d, 'YYYY')",
              "fn.Coalesce(t.x, 0, schema=Schema('util'))",
              "fn.Coalesce(t.x, 0, alias='c', schema=Schema('util', parent=Database('db')))",
              "fn.Upper(fn.Trim(t.s))", "fn.Sum(t.x * t.y)", "fn.Sum(t.x) / fn.Count('*')",
              "fn.Sum(fn.Coalesce(t.x, 0)) + 1", "fn.Count(Query.from_(t).select(t.x))",
              "fn.Max(t.x).as_('m')", "fn.Sum(t.x).filter(t.y > 0)",
              "fn.Sum(t.x).filter(t.y > 0, t.z == 'a')", "fn.Count('*').filter(t.ok)",
              "fn.Count(t.id).distinct().filter(t.ok)", "fn.Avg(t.x).filter()",
              "Rollup(t.a, t.b)", "Rollup()", "fn.Sum(t.x) > fn.Avg(t.x) * 2",
              "fn.Lower(t.s).like('a%')", "fn.Length(t.s)[1:5]", "fn.Count('*') == 0",
              "fn.Sum(t.x).get_sql(quote_char='`', with_alias=True)",
              "fn.Sum(t.x).as_('s').get_sql(quote_char='`', with_alias=True)",
              "fn.Sum(t.x).as_('s').get_sql(quote_char='`', with_alias=True, alias_quote_char='\"', as_keyword=True)",
              "fn.Sum(t.x).get_sql(with_namespace=True)",
              "fn.Concat(t.a, 'it''s').get_sql(secondary_quote_char='\"')",
              "fn.Concat(t.a, 'z').get_sql(quote_char='`')"]:
        show(e)
    let("DateDiff = CustomFunction('DATE_DIFF', ['interval', 'start_date', 'end_date'])")
    show("DateDiff('day', t.a, t.b)")
    show("DateDiff('day', t.a)")
    show("DateDiff('day', t.a, alias='d')")
    show("DateDiff('day', t.a, t.b, alias='d')")
    let("MyNow = CustomFunction('MY_NOW')")
    show("MyNow()")
    show("MyNow(1, 2)")
    show("MyNow(alias='n')")
    show("CustomFunction('F', []) ()")
    show("CustomFunction('F', [])(1)")
    let("s = fn.Sum(t.x)")
    let("s2 = s.filter(t.y > 0)")
    show("s")
    show("s2")
    let("s3 = s.filter(t.z < 0)")
    show("s3")
    show("s2")
    let("d = fn.Count(t.id)")
    let("d2 = d.distinct()")
    show("d")
    show("d2")
    show("d2.filter(t.k == 1)")


def analytics():
    sec("Analytic functions")
    reset()
    let("t = Table('emp')")
    for e in ["an.Rank()", "an.Rank().over(t.dept)", "an.Rank().over(t.dept).orderby(t.salary)",
              "an.Rank().over(t.dept).orderby(t.salary, order=Order.desc)",
              "an.Rank().orderby(t.salary, t.id, order=Order.asc)",
              "an.DenseRank().over(t.dept, t.team).orderby(t.salary)",
              "an.RowNumber().orderby(t.hired)", "an.RowNumber().over()",
              "an.NTile(4).orderby(t.salary)", "an.Median(t.salary).over(t.dept)",
              "an.FirstValue(t.salary).over(t.dept).orderby(t.hired)",
              "an.FirstValue(t.salary).ignore_nulls().over(t.dept).orderby(t.hired)",
              "an.LastValue(t.salary, t.bonus).ignore_nulls()",
              "an.LastValue(t.salary).over(t.dept).orderby(t.hired).rows(an.Preceding(), an.Following())",
              "an.Sum(t.salary).over(t.dept).rows(an.Preceding(2), an.CURRENT_ROW)",
              "an.Sum(t.salary).over(t.dept).orderby(t.hired).rows(an.CURRENT_ROW)",
              "an.Sum(t.salary).over(t.dept).orderby(t.hired).rows(an.Preceding())",
              "an.Avg(t.salary).over(t.dept).range(an.Preceding(7), an.Following(7))",
              "an.Avg(t.salary).orderby(t.hired).range(an.Preceding(0))",
              "an.Count(t.id).over(t.dept)", "an.Max(t.salary).over(t.dept)",
              "an.Min(t.salary).over(t.dept).as_('lowest')", "an.StdDev(t.salary).over(t.dept)",
              "an.StdDevPop(t.salary).over(t.dept)", "an.StdDevSamp(t.salary).over(t.dept)",
              "an.Variance(t.salary).over(t.dept)", "an.VarPop(t.salary).over(t.dept)",
              "an.VarSamp(t.salary).over(t.dept)", "an.Lag(t.salary, 1, 0).over(t.dept).orderby(t.hired)",
              "an.Lead(t.salary).orderby(t.hired)", "an.Lead(t.salary, 2).orderby(t.hired, order=Order.desc)",
              "an.Sum(t.salary).rows(an.Preceding(1), an.CURRENT_ROW)",
              "an.Sum(t.salary).over(t.dept).rows('UNBOUNDED PRECEDING')",
              "an.Sum(t.salary).over(t.dept).rows(an.Preceding(1)).rows(an.Preceding(2))",
              "an.Rank().over('dept')", "an.Rank().orderby('salary')", "an.Rank().over(t.dept).filter(t.ok)",
              "an.Sum(t.salary).over(t.dept).filter(t.ok)", "an.Rank().over(t.dept) > 1",
              "an.Rank().over(t.dept).get_sql(quote_char='`')",
              "an.Rank().over(t.dept).as_('r').get_sql(with_alias=True, quote_char='`')"]:
        show(e)
    let("w = an.Sum(t.salary).over(t.dept)")
    let("w2 = w.over(t.team)")
    show("w")
    show("w2")
    let("w3 = w.orderby(t.hired)")
    show("w")
    show("w3")
    show("Query.from_(t).select(t.name, an.Rank().over(t.dept).orderby(t.salary, order=Order.desc).as_('rk'))")
    show("PostgreSQLQuery.from_(t).select(t.id, an.Sum(t.salary).over(t.dept).orderby(t.hired)"
         ".rows(an.Preceding(3), an.CURRENT_ROW).as_('running'))")


def case_tuple_interval():
    sec("Case, tuples, arrays, parameters and intervals")
    reset()
    let("t = Table('t')")
    for e in ["Case().when(t.x == 1, 'one')", "Case().when(t.x == 1, 'one').else_('many')",
              "Case().when(t.x == 1, 'one').when(t.x == 2, 'two').else_(None)",
              "Case().when(t.x > 0, t.x).else_(-t.x)", "Case().when(t.x > 0, 1).else_(0).as_('pos')",
              "Case(alias='c').when(t.flag, True)", "Case()", "Case().else_(1)",
              "Case().when(t.x == 1, 'a').get_sql(with_alias=True)",
              "Case().when(t.x == 1, 'a').as_('k').get_sql(with_alias=True)",
              "Case().when(t.x == 1, 'a').when(t.y.isnull(), fn.Now())",
              "Case().when((t.x == 1) | (t.y == 2), 'a')",
              "Case().when(t.x == 1, 'a') == 'a'", "Case().when(t.x == 1, 'a').isin(['a', 'b'])",
              "Tuple(1, 2, 'a')", "Tuple(t.a, t.b)", "Tuple()", "Tuple(1)", "Tuple(1, 2).as_('p')",
              "Tuple(t.a, t.b) == Tuple(1, 2)", "Tuple(t.a, t.b).isin([(1, 2), (3, 4)])",
              "Tuple(t.a, (t.b, 1), [2, 3])", "Array(1, 2, 3)", "Array()", "Array('a', t.b)",
              "Array(1, 2).as_('arr')", "Bracket(t.a + t.b)", "Bracket(t.a)", "Bracket(t.a) == 1",
              "(t.a + Bracket(t.b - 1)) * 2", "Parameter(':1')", "Parameter(3)", "QmarkParameter()",
              "NumericParameter(1)", "NamedParameter('name')", "FormatParameter()",
              "PyformatParameter('name')", "t.x == QmarkParameter()", "t.x == NamedParameter('v')",
              "Parameter('$1').as_('p')"]:
        show(e)
    show("Query.from_(t).select(t.a).where(t.x == Parameter('%s')).where(t.y.isin([Parameter('%s'), Parameter('%s')]))")
    show("PostgreSQLQuery.from_(t).select(Array(1, 2), Array(), Tuple(1, 2))")
    show("RedshiftQuery.from_(t).select(Array(t.a, t.b), Array())")
    show("Query.from_(t).select(Array(1, 2), Array())")
    let("c = Case().when(t.x == 1, 'one')")
    let("c2 = c.when(t.x == 2, 'two')")
    show("c")
    show("c2")
    let("c3 = c.else_('other')")
    show("c")
    show("c3")
    for e in ["Interval(days=1)", "Interval(days=3)", "Interval(hours=1, minutes=30)",
              "Interval(years=1, months=2)", "Interval(years=1, seconds=5)", "Interval(days=-3)",
              "Interval(days=-1, hours=6)", "Interval(months=14)", "Interval(weeks=2)",
              "Interval(quarters=1)", "Interval(quarters=1, days=3)", "Interval(weeks=1, days=2)",
              "Interval(microseconds=5)", "Interval(seconds=1, microseconds=500)",
              "Interval(minutes=2, seconds=3)", "Interval(hours=10)", "Interval(seconds=0)",
              "Interval()", "Interval(days=1, hours=2, minutes=3, seconds=4)",
              "Interval(years=2, days=10)", "Interval(months=1, minutes=1)",
              "Interval(days=100, microseconds=1)", "Interval(days=1, dialect=MySQLQuery.from_('x').dialect)",
              "Interval(hours=1, minutes=10, dialect=OracleQuery.from_('x').dialect)",
              "Interval(days=20).get_sql()"]:
        show(e)
    for cls in ["Query", "MySQLQuery", "PostgreSQLQuery", "OracleQuery", "VerticaQuery", "RedshiftQuery",
                "MSSQLQuery"]:
        show("%s.from_(t).select(t.id).where(t.created + Interval(days=2) < fn.Now())" % cls)


def selects_and_stars():
    sec("Select lists and stars")
    reset()
    let("t, u = Tables('t', 'u')")
    for e in ["Query.from_(t).select(t.star)", "Query.from_(t).select('*')",
              "Query.from_(t).select(t.id, t.star)", "Query.from_(t).select(t.star, t.id)",
              "Query.from_(t).select('*').select(t.id)", "Query.from_(t).select(t.id).select('*')",
              "Query.from_(t).select(t.id, 'name', 3, 'x' == t.y)",
              "Query.from_(t).join(u).on(t.id == u.tid).select(t.star, u.star)",
              "Query.from_(t).join(u).on(t.id == u.tid).select(t.star, u.id, t.name)",
              "Query.from_(t).join(u).on(t.id == u.tid).select('*')",
              "Query.from_(t).join(u).on(t.id == u.tid).select(u.id, t.star, u.name)",
              "Query.select(1, 2)", "Query.select(fn.Now(), 'x' + Field('y'))", "Query.select('x')",
              "Query.select(1).orderby('x')", "Query.select(1).groupby('x')",
              "Query.select(t.a)", "Query.select(1, 'a')", "Query.from_(t)", "Query.from_(t).select()",
              "Query.from_(t).select(t.a).distinct()", "Query.from_(t).distinct().select(t.a, t.b)",
              "Query.from_(t).select(t.a.as_('x'), t.b.as_('y'))",
              "Query.from_(t).select(t.a.as_('x')).orderby(t.a.as_('x'))",
              "Query.from_(t).select(t.a.as_('x')).orderby(t.a)",
              "Query.from_(t).select(t.a.as_('x')).groupby(t.a.as_('x'))",
              "Query.from_(t).select(fn.Sum(t.b).as_('total')).orderby(fn.Sum(t.b).as_('total'), order=Order.desc)",
              "Query.from_(t).select(t.a).orderby(t.a, t.b, order=Order.desc)",
              "Query.from_(t).select(t.a).orderby('a').orderby('b', order=Order.asc)",
              "Query.from_(t).select(t.a).orderby(1)", "Query.from_(t).select(t.a).orderby(fn.Length(t.a))",
              "Query.from_(t).select(t.a).where(t.a > 1).where(t.b < 2).where(t.c == 3)",
              "Query.from_(t).select(t.a).where((t.a > 1) | (t.b < 2)).where(t.c == 3)",
              "Query.from_(t).select(t.a).where(t.c == 3).where((t.a > 1) | (t.b < 2))",
              "Query.from_(t).select(t.a).where(u.b == 1)",
              "Query.from_(t).select(t.a).where(t.a.isin(Query.from_(u).select(u.a)))",
              "Query.from_(t).select(t.a).where(t.a.notin(Query.from_(u).select(u.a).where(u.ok == True)))",
              "Query.from_(t).select(t.a).where(t.a > Query.from_(u).select(fn.Max(u.a)))",
              "Query.from_(t).select(t.a, Query.from_(u).select(fn.Count('*')).where(u.tid == t.id).as_('n'))",
              "Query.from_(t).select(t.a, Query.from_(u).select(u.b))",
              "Query.from_(t).select(t.a).limit(10)", "Query.from_(t).select(t.a).limit(0)",
              "Query.from_(t).select(t.a).offset(5)", "Query.from_(t).select(t.a).offset(0)",
              "Query.from_(t).select(t.a).limit(10).offset(20)", "Query.from_(t).select(t.a)[10:30]",
              "Query.from_(t).select(t.a)[:5]", "Query.from_(t).select(t.a)[5:]",
              "Query.from_(t).select(t.a).for_update()", "Query.from_(t).select(t.a).limit(1).for_update()",
              "Query.from_(t).select(t.a).force_index('idx_a')",
              "Query.from_(t).select(t.a).force_index('idx_a', Index('idx_b')).use_index('idx_c')",
              "Query.from_(t).select(t.a).use_index(Index('i1'), 'i2')",
              "Query.from_(t).from_(u).select(t.a, u.b)", "Query.from_(t).from_('v').select('a')",
              "Query.from_(t).select(t.a).prewhere(t.b > 1)",
              "Query.from_(t).select(t.a).prewhere(t.b > 1).prewhere(t.c < 2).where(t.d == 3)",
              "Query.from_(t).select(t.a).groupby(t.a).with_totals()",
              "Query.from_(t).select(t.a)['x']", "Query.from_(t).select(t.a).x",
              "Query.from_(t).select(t.a).as_('sub')",
              "Query.from_(t).select(t.a).as_('sub').get_sql(with_alias=True)",
              "Query.from_(t).select(t.a).get_sql(subquery=True)",
              "Query.from_(t).select(t.a).get_sql(subquery=True, with_alias=True)",
              "Query.from_(t).select(t.a).get_sql(quote_char=None)",
              "Query.from_(t).select(t.a.as_('x')).get_sql(quote_char='`', alias_quote_char=\"'\", as_keyword=True)",
              "Query.from_(t).select(t.a).where(t.b == 'q').get_sql(secondary_quote_char='\"')",
              "Query.from_(t).select(t.a).get_sql(with_namespace=True)",
              "Query.from_(t.as_('x')).select(t.as_('x').a)",
              "Query.from_(t, as_keyword=True).select(t.a.as_('b')).where(t.a > 1)",
              "Query.from_(Table('t').as_('x'), as_keyword=True).select(fn.Count('*').as_('n'))"]:
        show(e)


def groupby_rollup():
    sec("Group by, having and rollup")
    reset()
    let("t = Table('sales')")
    for e in ["Query.from_(t).select(t.region, fn.Sum(t.amount)).groupby(t.region)",
              "Query.from_(t).select('region').groupby('region')",
              "Query.from_(t).select(t.region).groupby(1)",
              "Query.from_(t).select(t.region, t.year).groupby(t.region, 2)",
              "Query.from_(t).select(t.region.as_('r')).groupby(t.region.as_('r'))",
              "Query.from_(t).select(t.region.as_('r')).groupby(t.region.as_('q'))",
              "MSSQLQuery.from_(t).select(t.region.as_('r')).groupby(t.region.as_('r'))",
              "OracleQuery.from_(t).select(t.region.as_('r')).groupby(t.region.as_('r'))",
              "PostgreSQLQuery.from_(t).select(t.region.as_('r')).groupby(t.region.as_('r'))",
              "MySQLQuery.from_(t).select(t.region.as_('r')).groupby(t.region.as_('r'))",
              "Query.from_(t).select(t.region, fn.Sum(t.amount)).groupby(t.region).having(fn.Sum(t.amount) > 100)",
              "Query.from_(t).select(t.region).groupby(t.region).having(fn.Count('*') > 1).having(fn.Max(t.amount) < 9)",
              "Query.from_(t).select(t.region).having(fn.Count('*') > 1)",
              "Query.from_(t).select(t.region, fn.Sum(t.amount).as_('s')).groupby(t.region).orderby(fn.Sum(t.amount).as_('s'))",
              "Query.from_(t).select(t.a, t.b, fn.Sum(t.c)).rollup(t.a, t.b)",
              "Query.from_(t).select(t.a, t.b, fn.Sum(t.c)).rollup([t.a, t.b], t.c)",
              "Query.from_(t).select(t.a, t.b, fn.Sum(t.c)).rollup((t.a, t.b))",
              "Query.from_(t).select(t.a, t.b, fn.Sum(t.c)).groupby(t.a).rollup(t.b)",
              "Query.from_(t).select(t.a, t.b, fn.Sum(t.c)).rollup(t.a).rollup(t.b)",
              "Query.from_(t).select(t.a, t.b, fn.Sum(t.c)).rollup(t.a).groupby(t.b)",
              "Query.from_(t).select(t.a, t.b, fn.Sum(t.c)).rollup()",
              "Query.from_(t).select(t.a, t.b, fn.Sum(t.c)).groupby(t.a, t.b).rollup(vendor='mysql')",
              "MySQLQuery.from_(t).select(t.a, fn.Sum(t.c)).rollup(t.a, vendor='mysql')",
              "MySQLQuery.from_(t).select(t.a, fn.Sum(t.c)).rollup(vendor='mysql')",
              "MySQLQuery.from_(t).select(t.a, fn.Sum(t.c)).rollup(t.a, vendor='mysql').rollup(t.b, vendor='mysql')",
              "MySQLQuery.from_(t).select(t.a, fn.Sum(t.c)).rollup(t.a, vendor='mysql').rollup(t.b)",
              "Query.from_(t).select(t.a, t.b, fn.Sum(t.c)).groupby(t.a, t.b).with_totals()",
              "Query.from_(t).select(t.a, t.b, fn.Sum(t.c)).groupby(Rollup(t.a, t.b))"]:
        show(e)
    let("r1 = Query.from_(t).select(t.a, t.b, fn.Sum(t.c)).rollup(t.a)")
    let("r2 = r1.rollup(t.b)")
    show("r1")
    show("r2")


def joins():
    sec("Joins")
    reset()
    let("a, b, c = Tables('a', 'b', 'c')")
    for how in ["inner_join", "left_join", "left_outer_join", "right_join", "right_outer_join",
                "outer_join", "full_outer_join", "hash_join"]:
        show("Query.from_(a).%s(b).on(a.id == b.aid).select(a.x, b.y)" % how)
    for jt in ["JoinType.inner", "JoinType.left", "JoinType.right", "JoinType.outer", "JoinType.cross"]:
        show("Query.from_(a).join(b, %s).on(a.id == b.aid).select('*')" % jt)
    for e in ["Query.from_(a).cross_join(b).cross().select(a.x, b.y)",
              "Query.from_(a).join(b).cross().select('*')",
              "Query.from_(a).join(b).on(a.id == b.aid).join(c).on(b.id == c.bid).select(a.x, c.z)",
              "Query.from_(a).join(b).on((a.id == b.aid) & (b.kind == 'x')).select(a.x)",
              "Query.from_(a).join(b).on(a.id == b.aid, collate='utf8_general_ci').select(a.x)",
              "Query.from_(a).join(b).on_field('id').select(a.x)",
              "Query.from_(a).join(b).on_field('id', 'region', 'year').select(a.x)",
              "Query.from_(a).join(b).using('id').select(a.x)",
              "Query.from_(a).join(b).using('id', 'region').select(a.x)",
              "Query.from_(a).left_join(b).using('id').where(b.id.isnull()).select(a.star)",
              "Query.from_(a).join(b).on(None)", "Query.from_(a).join(b).on_field()",
              "Query.from_(a).join(b).using()", "Query.from_(a).join(b).on(a.id == c.aid)",
              "Query.from_(a).join(b).on(Field('id') == b.aid)",
              "Query.from_(a).join(b).on(a.id == b.aid).join(c).on(a.id == c.aid).select(a.x)",
              "Query.from_(a).join(b).on(b.id == b.parent).select(b.x)",
              "Query.from_(a).join(5)", "Query.from_(a).join('b')",
              "Query.from_(a).join(b).on(a.id == b.aid).is_joined(b)",
              "Query.from_(a).join(b).on(a.id == b.aid).is_joined(c)",
              "Query.from_(a).join(b).on(a.id == b.aid).is_joined(Table('b'))",
              "Query.from_(a).join(b.as_('bb')).on(a.id == b.as_('bb').aid).select(a.x)",
              "Query.from_(a).select(a.x).join(b).on(a.id == b.aid).select(b.y)",
              "Query.update(a).join(b).on(a.id == b.aid).set(a.x, b.y).where(b.z > 1)",
              "Query.from_(a).join(b).on(a.id == b.aid).where(a.x == 1).delete()",
              "Query.update(a).join(b).on_field('id')",
              "MySQLQuery.from_(a).join(b).on(a.id == b.aid).select(a.x, b.y)",
              "MSSQLQuery.from_(a).join(b).on(a.id == b.aid).select(a.x, b.y)",
              "OracleQuery.from_(a).join(b).on(a.id == b.aid).select(a.x, b.y)"]:
        show(e)
    let("sub = Query.from_(b).select(b.aid, fn.Sum(b.v).as_('total')).groupby(b.aid)")
    show("Query.from_(a).join(sub).on(a.id == sub.aid).select(a.x, sub.total)")
    show("sub.alias")
    show("Query.from_(a).join(sub).on(a.id == sub.aid).select(a.x, sub.total)")
    let("sub2 = Query.from_(c).select(c.aid)")
    show("Query.from_(a).join(sub2).on(a.id == sub2.aid).join(Query.from_(c).select(c.k)).cross().select(a.x)")
    show("sub2.alias")
    let("e = Table('employees')")
    show("Query.from_(e).join(e).on(e.manager_id == e.id).select(e.name)")
    show("e.alias")
    show("Query.from_(e).select(e.name)")
    let("e = Table('employees')")
    let("m = Table('employees').as_('m')")
    show("Query.from_(e).join(m).on(e.manager_id == m.id).select(e.name, m.name.as_('manager'))")
    show("m.alias")
    let("j = Query.from_(a).join(b)")
    let("q1 = j.on(a.id == b.aid)")
    let("q2 = j.on(a.k == b.k)")
    show("q1")
    show("q1 is q2")
    let("base = Query.from_(a).select(a.x)")
    let("q3 = base.join(b).on(a.id == b.aid)")
    show("base")
    show("q3")
    let("aq = AliasedQuery('w')")
    show("Query.with_(Query.from_(b).select(b.aid), 'w').from_(a).join(aq).on(a.id == aq.aid).select(a.x, aq.aid)")


def subqueries_and_sets():
    sec("Subqueries, WITH and set operations")
    reset()
    let("t, u = Tables('t', 'u')")
    let("sub = Query.from_(t).select(t.a, t.b).where(t.c > 1)")
    show("Query.from_(sub).select(sub.a)")
    show("sub.alias")
    show("Query.from_(sub).select(sub.a, sub.star)")
    let("inner = Query.from_(t).select(t.a)")
    let("mid = Query.from_(inner).select(inner.a)")
    show("Query.from_(mid).select(mid.a)")
    show("inner.alias")
    show("mid.alias")
    let("x = Query.from_(t).select(t.a)")
    let("y = Query.from_(u).select(u.a)")
    show("Query.from_(x).from_(y).select(x.a, y.a)")
    show("x.alias")
    show("y.alias")
    show("Query.from_(Query.from_(t).select(t.a).as_('named')).select('*')")
    show("Query.from_(Query.from_(t).select(t.a).as_('named')).select(Field('a'))")
    let("w = Query.from_(t).select(t.a)")
    show("Query.with_(w, 'w1').with_(Query.from_(u).select(u.b), 'w2').from_(AliasedQuery('w1')).select('*')")
    show("Query.with_(w, 'w1').from_(AliasedQuery('w1')).join(AliasedQuery('w2')).on(AliasedQuery('w1').a == AliasedQuery('w2').a).select('*')")
    show("Query.with_(w, 'w1').into(u).from_(AliasedQuery('w1')).select('*')")
    show("Query.with_(w, 'w1').into(u).insert(1)")
    show("Query.with_(w, 'w1').update(u).set(u.a, 1)")
    show("AliasedQuery('w1').get_sql()")
    show("AliasedQuery('w1', Query.from_(t).select(t.a)).get_sql()")
    show("AliasedQuery('w1') == AliasedQuery('w1')")
    show("AliasedQuery('w1') == AliasedQuery('w2')")
    let("q1 = Query.from_(t).select(t.a, t.b)")
    let("q2 = Query.from_(u).select(u.a, u.b)")
    let("q3 = Query.from_(u).select(u.c, u.d)")
    for e in ["q1 + q2", "q1.union(q2)", "q1 * q2", "q1.union_all(q2)", "q1 + q2 + q3", "q1 + q2 * q3",
              "(q1 + q2).union_all(q3)", "q1.union(q2).intersect(q3)", "q1.union(q2).except_of(q3)",
              "(q1 + q2) - q3", "q1.union(q2).minus(q3)", "q1.union(q2).orderby('a')",
              "q1.union(q2).orderby(t.a, order=Order.desc)", "q1.union(q2).orderby(t.b.as_('bb'))",
              "q1.union(q2).limit(5)", "q1.union(q2).limit(5).offset(10)", "q1.union(q2).offset(0)",
              "q1.union(Query.from_(u).select(u.a))",
              "Query.from_(t).select(t.a.as_('k')).union(Query.from_(u).select(u.a)).orderby(t.a.as_('k'))",
              "MySQLQuery.from_(t).select(t.a).union(MySQLQuery.from_(u).select(u.a))",
              "MySQLQuery.from_(t).select(t.a).union(Query.from_(u).select(u.a))",
              "Query.from_(t).select(t.a).union(MySQLQuery.from_(u).select(u.a))",
              "ClickHouseQuery.from_(t).select(t.a).union_all(ClickHouseQuery.from_(u).select(u.a))",
              "(q1 + q2).get_sql(subquery=True)", "(q1 + q2).get_sql(quote_char=None)",
              "(q1 + q2).get_sql(with_alias=True)",
              "(q1 + q2).as_('both').get_sql(with_alias=True)"]:
        show(e)
    let("un = q1 + q2")
    show("Query.from_(un).select('*')")
    show("un.alias")
    show("Query.from_(un).select('*')")
    show("Query.from_(t).select(t.a).where(t.a.isin(q1.union(q2)))")
    let("u2 = q1.union(q2)")
    let("u3 = u2.union(q3)")
    show("u2")
    show("u3")


def inserts_updates_deletes():
    sec("Insert, update and delete")
    reset()
    let("t, u = Tables('t', 'u')")
    for e in ["Query.into(t).insert(1, 'a', None, True, 2.5)", "Query.into('t').insert(1)",
              "Query.into(t).insert([1, 'a'], [2, 'b'])", "Query.into(t).insert((1,), (2,))",
              "Query.into(t).insert((1, 'a'))",
              "Query.into(t).insert(1).insert((2,), (3,))", "Query.into(t).insert()", "Query.into(t)",
              "Query.into(t).insert(fn.Now(), t.x, Parameter('?'), 'x' == t.y)",
              "Query.into(t).insert([1, 2])", "Query.into(t).insert(Tuple(1, 2))",
              "Query.into(t).columns('a', 'b').insert(1, 2)", "Query.into(t).columns(['a', 'b']).insert(1, 2)",
              "Query.into(t).columns(('a', 'b')).insert(1, 2)", "Query.into(t).columns(t.a, u.b).insert(1, 2)",
              "Query.into(t).columns('a').columns('b').insert(1, 2)",
              "Query.into(t).columns('a').insert(1).columns('b')",
              "Query.into(t).replace(1, 'x')", "Query.into(t).insert(1).replace(2)",
              "Query.into(t).replace(1).insert(2)", "Query.into(t).ignore().insert(1)",
              "Query.into(t).ignore().replace(1)", "Query.into(t).into(u)", "Query.from_(t).insert(1)",
              "Query.from_(t).columns('a')", "Query.from_(t).select('a').into(u)",
              "Query.from_(t).select(t.a).into(u).where(t.a > 1)",
              "Query.into(u).from_(t).select(t.a).where(t.a > 1)",
              "Query.into(u).columns('a').from_(t).select(t.a)",
              "Query.into(u).columns('a').insert(1).from_(t).select(t.a)",
              "Query.into(u).columns('a').from_(t).join(t.as_('t2')).on(t.id == t.as_('t2').pid).select(t.a)",
              "Query.update(t).set(t.a, 1)", "Query.update('t').set('a', 1).set('b', 'x')",
              "Query.update(t).set(t.a, None)", "Query.update(t).set(t.a, t.b + 1)",
              "Query.update(t).set(t.a, fn.Now())", "Query.update(t).set(t.a, True).set(t.b, 2.25)",
              "Query.update(t).set(t.a, [1, 2])", "Query.update(t).set(t.a, Order.desc)",
              "Query.update(t).set(t.a, date(2024, 5, 1))", "Query.update(t)",
              "Query.update(t).set(t.a, 1).where(t.id == 5).where(t.b > 2)",
              "Query.update(t).set(t.a, 1).limit(3)", "Query.update(t).set(t.a, 1).offset(3)",
              "Query.update(t).set(t.a, 1).orderby(t.id)",
              "Query.update(t).from_(u).set(t.a, u.b).where(t.id == u.tid)",
              "Query.update(t).set(t.a, u.b).where(t.id == u.tid)",
              "Query.update(t.as_('x')).set(t.as_('x').a, 1)",
              "Query.update(t).update(u)", "Query.from_(t).select(t.a).update(u)",
              "Query.from_(t).delete()", "Query.from_(t).delete().where(t.a == 1)",
              "Query.from_(t).delete().where(t.a == 1).limit(10)",
              "Query.from_(t).where(t.a.isin(Query.from_(u).select(u.a))).delete()",
              "Query.from_(t).delete().delete()", "Query.from_(t).select(t.a).delete()",
              "Query.update(t).set(t.a, 1).delete()", "Query.from_(t).delete().select(t.a)",
              "t.select(t.a, t.b)", "t.select()", "t.update().set(t.a, 1)", "t.insert(1, 2)",
              "MySQLQuery.Table('t').select('a')", "MySQLQuery.Table('t', alias='z').select('a')",
              "MySQLQuery.Table('t').insert(1)", "MySQLQuery.Table('t').update().set('a', 1)",
              "PostgreSQLQuery.Table('t', schema='s').select('a')"]:
        show(e)
    let("p, q = MySQLQuery.Tables('p', ('q', 'qq'))")
    show("p.select(p.a)")
    show("q.select(q.a)")
    let("p, q = Tables('p', ('q', 'qq'), schema='s')")
    show("Query.from_(p).join(q).on(p.id == q.pid).select(p.a, q.b)")


def dialects():
    sec("Dialects")
    reset()
    let("t, u = Tables('users', 'orgs')")
    for cls in ["Query", "MySQLQuery", "PostgreSQLQuery", "MSSQLQuery", "OracleQuery", "SnowflakeQuery",
                "SQLLiteQuery", "ClickHouseQuery", "RedshiftQuery", "VerticaQuery"]:
        show("%s.from_(t).select(t.id, t.name.as_('n'), fn.Count('*').as_('c'))"
             ".where((t.id > 5) & (t.name != \"O'Brien\")).groupby(t.id, t.name.as_('n'))"
             ".orderby(t.name.as_('n')).limit(10).offset(20)" % cls)
        show("%s.from_(t).join(u).on(t.org_id == u.id).select(t.id, u.name).where(t.active == True)" % cls)
        show("%s.from_(Query.from_(t).select(t.id)).select('*')" % cls)
        show("%s.into(t).insert(1, 'a', True, None)" % cls)
        show("%s.update(t).set(t.name, 'b').where(t.id == 1)" % cls)
        show("%s.from_(t).delete().where(t.id == 1)" % cls)
        show("%s.from_(t).select(t.id.as_('i')).get_sql(with_alias=True)" % cls)
        show("%s.from_(t).select(t.id).as_('s').get_sql(with_alias=True)" % cls)
        show("%s.from_(t).select(t.id).limit(5)" % cls)
        show("%s.from_(t).select(t.id).offset(5)" % cls)
        show("%s.from_(t).select(t.id).for_update()" % cls)
        show("%s.from_(t).select(t.id).distinct()" % cls)
    sec("MySQL")
    for e in ["MySQLQuery.into(t).insert(1, 'a').on_duplicate_key_update(t.name, 'b')",
              "MySQLQuery.into(t).insert(1, 'a').on_duplicate_key_update('name', Values('name'))",
              "MySQLQuery.into(t).insert(1, 'a').on_duplicate_key_update(t.name, Values(t.name)).on_duplicate_key_update(t.n, t.n + 1)",
              "MySQLQuery.into(t).insert(1).on_duplicate_key_ignore().on_duplicate_key_update(t.a, 1)",
              "MySQLQuery.into(t).insert(1).on_duplicate_key_update(t.a, 1).on_duplicate_key_ignore()",
              "MySQLQuery.into(t).on_duplicate_key_ignore()", "MySQLQuery.into(t).on_duplicate_key_update(t.a, 1)",
              "MySQLQuery.from_(t).select(t.id).on_duplicate_key_ignore()",
              "MySQLQuery.from_(t).select(t.id).modifier('SQL_CALC_FOUND_ROWS')",
              "MySQLQuery.from_(t).select(t.id).modifier('HIGH_PRIORITY').modifier('SQL_NO_CACHE').distinct()",
              "MySQLQuery.from_(t).select(t.id).for_update(nowait=True)",
              "MySQLQuery.from_(t).select(t.id).for_update(skip_locked=True)",
              "MySQLQuery.from_(t).select(t.id).for_update(nowait=True, skip_locked=True)",
              "MySQLQuery.from_(t).select(t.id).for_update(of=('users',))",
              "MySQLQuery.from_(t).select(t.id).for_update(of=['users'], skip_locked=True)",
              "MySQLQuery.into(t).ignore().insert(1)", "MySQLQuery.into(t).replace(1, 'a')",
              "MySQLQuery.from_(t).select(t.id).where(t.name.rlike('^a')).where(t.n.bitwiseand(2) == 2)",
              "MySQLQuery.from_(t).select(t.id).groupby(t.id).rollup(vendor='mysql')"]:
        show(e)
    let("m1 = MySQLQuery.from_(t).select(t.id)")
    let("m2 = m1.modifier('A')")
    show("m1")
    show("m2")
    sec("PostgreSQL")
    for e in ["PostgreSQLQuery.into(t).insert(1, 'a').returning('id')",
              "PostgreSQLQuery.into(t).insert(1, 'a').returning(t.id, t.name)",
              "PostgreSQLQuery.into(t).insert(1, 'a').returning('*')",
              "PostgreSQLQuery.into(t).insert(1, 'a').returning(t.star)",
              "PostgreSQLQuery.into(t).insert(1, 'a').returning(t.id, '*')",
              "PostgreSQLQuery.into(t).insert(1, 'a').returning('*', t.id)",
              "PostgreSQLQuery.into(t).insert(1, 'a').returning(t.id + 1, fn.Upper(t.name))",
              "PostgreSQLQuery.into(t).insert(1, 'a').returning(fn.Sum(t.id))",
              "PostgreSQLQuery.into(t).insert(1, 'a').returning(u.id)",
              "PostgreSQLQuery.into(t).insert(1, 'a').returning(5)",
              "PostgreSQLQuery.update(t).set(t.name, 'x').where(t.id == 1).returning(t.id)",
              "PostgreSQLQuery.update(t).set(t.name, 'x').returning('id', 'name')",
              "PostgreSQLQuery.from_(t).delete().where(t.id == 1).returning('id')",
              "PostgreSQLQuery.from_(t).select(t.id).returning('id')",
              "PostgreSQLQuery.from_(t).select(t.id).returning(t.id)",
              "PostgreSQLQuery.into(t).insert(1).on_conflict('id').do_nothing()",
              "PostgreSQLQuery.into(t).insert(1).on_conflict().do_nothing()",
              "PostgreSQLQuery.into(t).insert(1).on_conflict('id', 'org').do_update('name')",
              "PostgreSQLQuery.into(t).insert(1).on_conflict(t.id).do_update(t.name, 'z').do_update('n', 2)",
              "PostgreSQLQuery.into(t).insert(1).on_conflict('id').do_update('name').where(t.active == True)",
              "PostgreSQLQuery.into(t).insert(1).on_conflict('id').where(t.active == True).do_nothing()",
              "PostgreSQLQuery.into(t).insert(1).on_conflict('id').where(t.a == 1).where(t.b == 2).do_update('c')",
              "PostgreSQLQuery.into(t).insert(1).on_conflict('id').do_nothing().where(t.a == 1)",
              "PostgreSQLQuery.into(t).insert(1).on_conflict().do_update('name')",
              "PostgreSQLQuery.into(t).insert(1).on_conflict().where(t.a == 1)",
              "PostgreSQLQuery.into(t).insert(1).on_conflict('id')",
              "PostgreSQLQuery.into(t).insert(1).on_conflict('id').do_nothing().do_update('a')",
              "PostgreSQLQuery.into(t).insert(1).on_conflict('id').do_update('a').do_nothing()",
              "PostgreSQLQuery.into(t).insert(1).on_conflict('id').do_update(5)",
              "PostgreSQLQuery.from_(t).select(t.id).on_conflict('id')",
              "PostgreSQLQuery.into(t).insert(1).on_conflict('id').do_update('name').returning('id')",
              "PostgreSQLQuery.into(t).insert(1).on_conflict('id').where(EmptyCriterion()).do_nothing()",
              "PostgreSQLQuery.from_(t).select(t.id, t.name).distinct_on('name')",
              "PostgreSQLQuery.from_(t).select(t.id, t.name).distinct_on('name', t.id).distinct()",
              "PostgreSQLQuery.from_(t).select(t.id).distinct_on(t.name.as_('n'))",
              "PostgreSQLQuery.from_(t).select(t.id).for_update(nowait=True, of=('users',))",
              "PostgreSQLQuery.from_(t).select(t.id).for_update(skip_locked=True)",
              "PostgreSQLQuery.from_(t).using(u).where(t.org_id == u.id).delete()",
              "PostgreSQLQuery.from_(t).using(u).using(Table('v')).where(t.org_id == u.id).delete()",
              "PostgreSQLQuery.from_(t).select(t.id).where(t.tags == ['a', 'b'])",
              "PostgreSQLQuery.from_(t).select(t.id).where(t.name.ilike('a%'))"]:
        show(e)
    let("g1 = PostgreSQLQuery.from_(t).select(t.id, t.name)")
    let("g2 = g1.distinct_on('name')")
    show("g1")
    show("g2")
    let("h1 = PostgreSQLQuery.into(t).insert(1)")
    let("h2 = h1.on_conflict('id')")
    let("h3 = h1.on_conflict('org').do_nothing()")
    show("h3")
    let("d1 = PostgreSQLQuery.from_(t)")
    let("d2 = d1.using(u)")
    show("d1.where(t.id == 1).delete()")
    sec("MSSQL, Oracle, Snowflake, SQLite, ClickHouse and Vertica")
    for e in ["MSSQLQuery.from_(t).select(t.id).top(10)", "MSSQLQuery.from_(t).select(t.id).top('5')",
              "MSSQLQuery.from_(t).select(t.id).top(50, percent=True)",
              "MSSQLQuery.from_(t).select(t.id).top(5, with_ties=True).orderby(t.id)",
              "MSSQLQuery.from_(t).select(t.id).top(5, percent=True, with_ties=True)",
              "MSSQLQuery.from_(t).select(t.id).top('abc')", "MSSQLQuery.from_(t).select(t.id).top(150, percent=True)",
              "MSSQLQuery.from_(t).select(t.id).top(-1, percent=True)",
              "MSSQLQuery.from_(t).select(t.id).top(0)", "MSSQLQuery.from_(t).select(t.id).top(2.9)",
              "MSSQLQuery.from_(t).select(t.id).distinct().top(3)",
              "MSSQLQuery.from_(t).select(t.id).fetch_next(10)",
              "MSSQLQuery.from_(t).select(t.id).orderby(t.id).offset(10).fetch_next(5)",
              "MSSQLQuery.from_(t).select(t.id)[3:9]",
              "MSSQLQuery.update(t).set(t.a, 1).limit(2)",
              "OracleQuery.from_(t).select(t.id).limit(5).offset(1)",
              "OracleQuery.from_(t).select(t.id.as_('i'), fn.Sum(t.n).as_('s')).groupby(t.id.as_('i')).orderby(fn.Sum(t.n).as_('s'))",
              "SnowflakeQuery.from_(t).select(t.id.as_('i')).where(t.id == 1)",
              "SnowflakeQuery.from_(Query.from_(t).select(t.id)).select('*')",
              "SnowflakeQuery.from_(t).join(u).on(t.org_id == u.id).select(t.id.as_('i'), u.name)",
              "SnowflakeQuery.create_table(t).columns('a', ('b', 'INT'))", "SnowflakeQuery.drop_table(t)",
              "SQLLiteQuery.into(t).insert(1, True, False)",
              "SQLLiteQuery.into(t).insert_or_replace(1, 'a')",
              "SQLLiteQuery.into(t).insert_or_replace((1, 'a'), (2, 'b'))",
              "SQLLiteQuery.into(t).replace(1, 'a')",
              "SQLLiteQuery.from_(t).select(t.id, True).where(t.active == True)",
              "SQLLiteQuery.update(t).set(t.active, False)",
              "SQLLiteQuery.from_(t).select(t.id).where(t.flag.isin([True, False, 3]))",
              "ClickHouseQuery.from_(t).select(t.id.as_('i')).where(t.id == 1)",
              "ClickHouseQuery.from_(t.as_('x')).select('*')",
              "ClickHouseQuery.from_(t).delete().where(t.id == 1)",
              "ClickHouseQuery.update(t).set(t.name, 'z').where(t.id == 1)",
              "ClickHouseQuery.from_(t).select(t.id).prewhere(t.day == '2024-01-01').where(t.n > 1)",
              "ClickHouseQuery.from_(t).select(t.id, fn.Count('*').as_('n')).groupby(t.id).with_totals()",
              "VerticaQuery.from_(t).select(t.id).hint('q1')",
              "VerticaQuery.from_(t).select(t.id).hint('q1').hint('q2')",
              "VerticaQuery.into(t).insert(1).hint('ins')", "VerticaQuery.from_(t).hint('empty')",
              "VerticaQuery.update(t).set(t.a, 1).hint('upd')",
              "RedshiftQuery.from_(t).select(t.id).where(t.tags == ['a'])"]:
        show(e)


def ddl():
    sec("Create and drop")
    reset()
    for e in ["Query.create_table('t').columns('a', 'b')",
              "Query.create_table('t').columns(('a', 'INT'), ('b', 'TEXT'))",
              "Query.create_table(Table('t', schema='s')).columns(Column('a', 'INT'))",
              "Query.create_table('t').temporary().columns('a')",
              "Query.create_table('t').unlogged().columns('a')",
              "Query.create_table('t').temporary().unlogged().columns('a')",
              "Query.create_table('t').if_not_exists().columns('a')",
              "Query.create_table('t').columns('a').with_system_versioning()",
              "Query.create_table('t').columns(Column('id', 'INT'), Column('start', 'DATE'), Column('end', 'DATE'))"
              ".period_for('valid', 'start', 'end')",
              "Query.create_table('t').columns('a').period_for('p', Column('s'), Column('e'))",
              "Query.create_table('t').columns('a', 'b').primary_key('a', 'b')",
              "Query.create_table('t').columns('a', 'b').primary_key(Column('a'))",
              "Query.create_table('t').columns('a').primary_key('a').primary_key('a')",
              "Query.create_table('t').columns('a', 'b', 'c').unique('a').unique('b', 'c')",
              "Query.create_table('t').columns('a', 'b').foreign_key(['a'], Table('p'), ['id'])",
              "Query.create_table('t').columns('a', 'b').foreign_key(['a', 'b'], Table('p', schema='s'), ['x', 'y'], "
              "on_delete=ReferenceOption.cascade, on_update=ReferenceOption.set_null)",
              "Query.create_table('t').columns('a').foreign_key(['a'], Table('p'), ['id'], on_update=ReferenceOption.no_action)",
              "Query.create_table('t').columns('a').foreign_key(['a'], Table('p'), ['id'], on_delete=ReferenceOption.restrict)"
              ".foreign_key(['a'], Table('q'), ['id'])",
              "Query.create_table('t').columns('a').foreign_key(['a'], Table('p'), ['id'], on_delete=ReferenceOption.set_default)"
              ".unique('a').primary_key('a')",
              "Query.create_table('t').columns(Column('a', 'INT', nullable=True), Column('b', 'INT', nullable=False))",
              "Query.create_table('t').columns(Column('a', 'INT', default=0), Column('b', 'TEXT', default='x'))",
              "Query.create_table('t').columns(Column('a', 'BOOL', default=True), Column('b', 'TS', default=fn.Now()))",
              "Query.create_table('t').columns(Column('a', 'REAL', default=1.5), Column('b', None, False))",
              "Query.create_table('t').columns(Column('a', default=ValueWrapper(\"it's\")))",
              "Query.create_table('t').columns(Column('a', 'INT', True, 7))",
              "Query.create_table('t').columns(*Columns(('id', 'INT'), 'name', ('z', 'TEXT')))",
              "Query.create_table('t')", "Query.create_table('t').if_not_exists()",
              "Query.create_table('t').as_select(Query.from_('s').select('*'))",
              "Query.create_table('t').temporary().as_select(Query.from_('s').select('a').where(Field('a') > 1))",
              "Query.create_table('t').columns('a').as_select(Query.from_('s').select('*'))",
              "Query.create_table('t').as_select(Query.from_('s').select('*')).columns('a')",
              "Query.create_table('t').as_select('SELECT 1')",
              "Query.create_table('t').create_table('u')",
              "MySQLQuery.create_table('t').columns('a', ('b', 'INT')).primary_key('a')",
              "MySQLQuery.create_table(Table('t', schema='db')).if_not_exists().columns(Column('a', 'INT', default='q'))",
              "PostgreSQLQuery.create_table('t').columns('a')",
              "VerticaQuery.create_table('t').columns('a')",
              "VerticaQuery.create_table('t').temporary().columns('a')",
              "Column('a')", "Column('a', 'INT')", "Column('a', 'INT', nullable=False, default=3)",
              "Column('a', 'VARCHAR(2)', True, 'zz')", "Column('a').get_sql()",
              "Column('a', 'INT').get_sql(quote_char='`')",
              "Query.drop_table('t')", "Query.drop_table(Table('t', schema='s')).if_exists()",
              "Query.drop_table('t').if_exists().if_exists()", "Query.drop_database('db')",
              "Query.drop_database(Database('db')).if_exists()", "Query.drop_user('bob')",
              "Query.drop_view('v').if_exists()", "Query.drop_table('t').drop_table('u')",
              "MySQLQuery.drop_table('t')", "MySQLQuery.drop_user('bob')", "MySQLQuery.drop_database('db')",
              "ClickHouseQuery.drop_table('t')", "ClickHouseQuery.drop_user('bob')",
              "PostgreSQLQuery.drop_view('v')", "SnowflakeQuery.drop_table(Table('t', schema='s'))",
              "Query.drop_table('t').get_sql(quote_char='`')"]:
        show(e)
    let("c1 = Query.create_table('t').columns('a')")
    let("c2 = c1.columns('b')")
    show("c1")
    show("c2")
    let("c3 = c1.unique('a')")
    let("c4 = c1.primary_key('b')")
    show("c3")
    show("c4")


def replace_and_mutability():
    sec("replace_table and immutability")
    reset()
    let("t, u, v = Tables('t', 'u', 'v')")
    let("q = Query.from_(t).join(u).on(t.id == u.tid).select(t.a, u.b, fn.Sum(t.c).as_('s'))"
        ".where(t.a > 1).groupby(t.a, u.b).having(fn.Sum(t.c) > 2).orderby(t.a)")
    show("q")
    show("q.replace_table(t, v)")
    show("q.replace_table(u, v)")
    show("q.replace_table(Table('t'), v)")
    show("q")
    show("Query.into(t).columns(t.a, t.b).insert(t.a + 1, 2).replace_table(t, v)")
    show("Query.update(t).set(t.a, 1).where(t.b == 2).replace_table(t, v)")
    show("Query.from_(t).select(t.star, Case().when(t.a == 1, t.b).else_(t.c), Tuple(t.a, 1))"
         ".where(t.a.isin([1]) & t.b[1:2] & t.c.isnull() & ~(t.d == 1) & (t.e.bitwiseand(1) == 1))"
         ".replace_table(t, v)")
    show("Query.from_(t).select(fn.Coalesce(t.a, 0), t.a + t.b, -t.a).replace_table(t, v)")
    show("Query.from_(t).join(u).using('id').select(u.a).replace_table(u, v)")
    show("Query.from_(t).select(t.star).replace_table(t, v)")
    show("(t.a == u.b).replace_table(t, v)")
    show("fn.Sum(t.a).replace_table(t, v)")
    show("t.a.replace_table(t, v)")
    show("t.a.replace_table(u, v)")
    show("ValueWrapper(1).replace_table(t, v)")
    let("m = Query.from_(t, immutable=False)")
    show("m.select(t.a)")
    show("m")
    show("m.where(t.a > 1)")
    show("m")
    let("m2 = m.limit(3)")
    show("m")
    show("m2 is m")
    let("i = Query.from_(t)")
    let("i2 = i.select(t.a)")
    show("i")
    show("i2 is i")
    let("i3 = i2.as_('z')")
    show("i2.alias")
    show("i3.alias")
    let("ta = t.as_('ta')")
    show("t.alias")
    show("ta.alias")
    let("f = t.x")
    let("g = f.as_('y')")
    show("f.alias")
    show("g.alias")
    show("Query.from_(t).select(t.a).where(Field('b') == 1)")
    show("Query.from_(t).select(t.a).where(t.b == Field('c'))")


def programs():
    sec("Programs")
    reset()
    program("migrate schema.tsv")
    program("report reports.tsv")
    program("load customers.csv customers id 2")
    program("load products.csv products sku 3")


def main():
    tutorial()
    values_and_quoting()
    arithmetic()
    criteria()
    aggregation()
    functions()
    analytics()
    case_tuple_interval()
    selects_and_stars()
    groupby_rollup()
    joins()
    subqueries_and_sets()
    inserts_updates_deletes()
    dialects()
    ddl()
    replace_and_mutability()
    programs()
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "schema.tsv"), "w") as f:
        f.write(SCHEMA)
    with open(os.path.join(DATA, "reports.tsv"), "w") as f:
        f.write("# name\tfrom\tjoins\tselect\twhere\tgroupby\thaving\torderby\tlimit\toffset\n")
        for r in REPORTS:
            assert len(r) == 10, r
            f.write("\t".join(r) + "\n")
    with open(os.path.join(DATA, "customers.csv"), "w") as f:
        f.write(CUSTOMERS)
    with open(os.path.join(DATA, "products.csv"), "w") as f:
        f.write(PRODUCTS)
    with open(os.path.join(DATA, "jobs.tsv"), "w") as f:
        for kind, src in J:
            assert "\t" not in src and "\n" not in src, src
            f.write("%s\t%s\n" % (kind, src))
    print("%d steps" % sum(1 for k, _ in J if k not in ("#", "reset")))


main()
