"""Write data/: GraphQL documents (one file each), a client app's queries,
schema and JavaScript sources, and data/jobs.txt, the jobs that run them.

The two kitchen-sink documents are graphql-core's own test fixtures
(tests/fixtures/, MIT, the GraphQL Contributors); the rest are written
here.

Run: python3 -s -P -B mk.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
FILES = []
JOBS = []


def put(rel, text):
    path = os.path.join(D, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))
    FILES.append(rel)
    return rel


def case(name, text):
    return put("cases/%s.graphql" % name, text)


def job(line):
    JOBS.append(line)


def section(title):
    JOBS.append("# " + title)


KITCHEN_SINK = '''query queryName($foo: ComplexType, $site: Site = MOBILE) @onQuery {
  whoever123is: node(id: [123, 456]) {
    id ,
    ... on User @onInlineFragment {
      field2 {
        id ,
        alias: field1(first:10, after:$foo,) @include(if: $foo) {
          id,
          ...frag @onFragmentSpread
        }
      }
    }
    ... @skip(unless: $foo) {
      id
    }
    ... {
      id
    }
  }
}

mutation likeStory @onMutation {
  like(story: 123) @onField {
    story {
      id @onField
    }
  }
}

subscription StoryLikeSubscription(
  $input: StoryLikeSubscribeInput @onVariableDefinition
) @onSubscription {
  storyLikeSubscribe(input: $input) {
    story {
      likers {
        count
      }
      likeSentence {
        text
      }
    }
  }
}

fragment frag on Friend @onFragmentDefinition {
  foo(size: $size, bar: $b, obj: {key: "value", block: """

      block string uses \\"""

  """})
}

{
  unnamed(truthy: true, falsy: false, nullish: null),
  query
}

query { __typename }
'''

SCHEMA_KITCHEN_SINK = '''"""This is a description of the schema as a whole."""
schema {
  query: QueryType
  mutation: MutationType
}

"""
This is a description
of the `Foo` type.
"""
type Foo implements Bar & Baz & Two {
  "Description of the `one` field."
  one: Type
  """
  This is a description of the `two` field.
  """
  two(
    """
    This is a description of the `argument` argument.
    """
    argument: InputType!
  ): Type
  """This is a description of the `three` field."""
  three(argument: InputType, other: String): Int
  four(argument: String = "string"): String
  five(argument: [String] = ["string", "string"]): String
  six(argument: InputType = {key: "value"}): Type
  seven(argument: Int = null): Type
}

type AnnotatedObject @onObject(arg: "value") {
  annotatedField(arg: Type = "default" @onArgumentDefinition): Type @onField
}

type UndefinedType

extend type Foo {
  seven(argument: [String]): Type
}

extend type Foo @onType

interface Bar {
  one: Type
  four(argument: String = "string"): String
}

interface AnnotatedInterface @onInterface {
  annotatedField(arg: Type @onArgumentDefinition): Type @onField
}

interface UndefinedInterface

extend interface Bar implements Two {
  two(argument: InputType!): Type
}

extend interface Bar @onInterface

interface Baz implements Bar & Two {
  one: Type
  two(argument: InputType!): Type
  four(argument: String = "string"): String
}

union Feed =
  | Story
  | Article
  | Advert

union AnnotatedUnion @onUnion = A | B

union AnnotatedUnionTwo @onUnion = | A | B

union UndefinedUnion

extend union Feed = Photo | Video

extend union Feed @onUnion

scalar CustomScalar

scalar AnnotatedScalar @onScalar

extend scalar CustomScalar @onScalar

enum Site {
  """
  This is a description of the `DESKTOP` value
  """
  DESKTOP

  """This is a description of the `MOBILE` value"""
  MOBILE

  "This is a description of the `WEB` value"
  WEB
}

enum AnnotatedEnum @onEnum {
  ANNOTATED_VALUE @onEnumValue
  OTHER_VALUE
}

enum UndefinedEnum

extend enum Site {
  VR
}

extend enum Site @onEnum

input InputType {
  key: String!
  answer: Int = 42
}

input AnnotatedInput @onInputObject {
  annotatedField: Type @onInputFieldDefinition
}

input UndefinedInput

extend input InputType {
  other: Float = 1.23e4 @onInputFieldDefinition
}

extend input InputType @onInputObject

"""
This is a description of the `@skip` directive
"""
directive @skip(
  """This is a description of the `if` argument"""
  if: Boolean! @onArgumentDefinition
) on FIELD | FRAGMENT_SPREAD | INLINE_FRAGMENT

directive @include(if: Boolean!)
  on FIELD
   | FRAGMENT_SPREAD
   | INLINE_FRAGMENT

directive @include2(if: Boolean!) on
  | FIELD
  | FRAGMENT_SPREAD
  | INLINE_FRAGMENT

directive @myRepeatableDir(name: String!) repeatable on
  | OBJECT
  | INTERFACE

extend schema @onSchema

extend schema @onSchema {
  subscription: SubscriptionType
}
'''

# ------------------------------------------------------------ printing

section("the kitchen sinks, parsed and printed back")
job("parse " + case("kitchen_sink", KITCHEN_SINK))
job("parse " + case("schema_kitchen_sink", SCHEMA_KITCHEN_SINK))
job("parse cases/kitchen_sink.graphql no_location")

section("printing: what print_ast keeps and what it drops")
job("parse " + case("shorthand", "{ a, b, ,, c }"))
job("parse " + case("query_keyword", "query { a }"))
job("parse " + case("query_directive", "query @live { a }"))
job("parse " + case("named_no_vars", "query Q { a }"))
job("parse " + case("comments", "# leading comment\n{\n  a # trailing\n  # alone\n  b\n}\n# last"))
job("parse " + case("aliases", "{ me: user(id: 4) { first: name, last: surname } }"))
job("parse " + case("long_args", "{ searchProducts(query: \"wireless noise cancelling headphones\", "
                    "first: 20, after: \"Y3Vyc29yOjQw\", sort: PRICE_ASC, inStock: true) { id name } }"))
# print_ast keeps a field's arguments on one line up to 80 characters
for name, width in [("eighty", 80), ("eighty_one", 81)]:
    line = "f(%s: 1, %s: 2, c: 3)" % ("a" * 34, "b" * (width - 51))
    assert len(line) == width
    job("parse " + case(name, "{ " + line + " }"))
job("parse " + case("variables", "query Q($id: ID!, $first: Int = 10, $tags: [String!]! = [\"a\", \"b\"], "
                    "$f: Filter = {min: 1, max: null} @deprecated) { a }"))
job("parse " + case("values", "{ f(i: -0, j: 123, x: -1.5e-3, y: 0.0, z: 6E+10, s: \"\", e: RED, "
                    "l: [[], [1, [2]]], o: {}, n: {a: {b: {c: $v}}}) }"))
job("parse " + case("fragments", "query { ...A ... on B { b } ... @include(if: $x) { c } ... { d } }\n"
                    "fragment A on T @dir { a }"))
job("parse " + case("crlf", "query Q {\r\n  a\r\n  b\r\n}\r\n"))
job("parse " + case("bom", "﻿query Q { a }"))
job("parse " + case("unicode_names_in_strings", "{ f(s: \"café — 東京 \U0001F680\") }"))

section("printing strings: escapes, unicode and block strings")
job("parse " + case("escapes", r'{ f(s: "quote \" slash \\ \/ \b \f \n \r \t done") }'))
job("parse " + case("unicode_escapes", r'{ f(a: "Aé€", b: "\u{1F600}", c: "😀", '
                    r'd: "\u{0}\u001F\u007F\u0085\u009F ") }'))
job("parse " + case("block_plain", '{ f(s: """\n    first\n      indented\n    last\n  """) }'))
job("parse " + case("block_one_line", '{ f(s: """  leading spaces""", t: """tail quote" """) }'))
job("parse " + case("block_escape", '{ f(s: """has \\""" inside""", t: """a slash \\\n""") }'))
# \\ is not an escape in a block string, so \\""" escapes the quotes
job("parse " + case("block_escape_trap", '{ f(t: """ends with \\\\""") }'))
job("parse " + case("block_long", '{ f(s: """' + "x" * 71 + '""", t: """' + "y" * 70 + '""") }'))
job("parse " + case("block_blank_lines", '{ f(s: """\n\n\n   a\n\n   b\n\n\n""") }'))
job("parse " + case("block_empty", '{ f(s: """""", t: """   """, u: """\n""") }'))
job("parse " + case("block_tabs", '{ f(s: """\n\t\tone\n\t\t\ttwo\n""") }'))
job("parse " + case("block_crlf", '{ f(s: """a\r\n  b\r  c""") }'))
job("parse " + case("block_indented_first", '{ f(s: """  a\n  b""") }'))
job("parse " + case("block_odd_breaks", '{ f(s: """one\x0btwo\x1cthree four""") }'))
job("parse " + case("block_control", '{ f(s: """bell\x07""") }'))

section("descriptions on type system definitions")
job("parse " + case("descriptions", '"""\nA user of the shop.\n"""\ntype User {\n'
                    '  "The primary key."\n  id: ID!\n  """\n  Display name, as entered.\n  """\n'
                    '  name(\n    "Shorten it."\n    short: Boolean = false\n  ): String\n}\n\n'
                    '"Ways to sort." enum Sort { "cheapest first" PRICE_ASC PRICE_DESC }\n'
                    '"""Money, in cents."""\nscalar Cents @specifiedBy(url: "https://example.com/cents")'))

section("legacy fragment variables and the token limit")
legacy = case("legacy_fragment", "fragment F($size: Int = 64) on User { avatar(size: $size) }")
job("parse " + legacy)
job("parse " + legacy + " legacy")
job("parse cases/kitchen_sink.graphql max_tokens=50")
job("parse cases/kitchen_sink.graphql max_tokens=1000")
job("parse " + case("tiny", "{ a }") + " max_tokens=3")
job("parse cases/tiny.graphql max_tokens=2")

# ------------------------------------------------------------ syntax errors

section("syntax errors from the parser")
for name, text in [
    ("eof", "{"),
    ("missing_on", "{ ...MissingOn }\nfragment MissingOn Type"),
    ("field_brace", "{ field: {} }"),
    ("not_an_operation", "notAnOperation Foo { field }"),
    ("spread_only", "..."),
    ("empty_string_name", '{ ""'),
    ("var_in_const", "query Foo($x: Complex = { a: { b: [ $var ] } }) { field }"),
    ("dollar_in_const", "query Foo($x: Int = $) { field }"),
    ("fragment_named_on", "fragment on on on { on }"),
    ("spread_on", "{ ...on }"),
    ("desc_on_query", '"Description" query { a }'),
    ("desc_on_extend", '"Description" extend type T { a: A }'),
    ("enum_true", "enum Test { VALID, true }"),
    ("enum_null", "enum Test { null }"),
    ("extend_schema_bare", "extend schema"),
    ("extend_scalar_bare", "extend scalar Date"),
    ("extend_type_bare", "extend type User"),
    ("extend_unknown", "extend thing Foo"),
    ("bad_location", "directive @foo on FIELD | INCORRECT_LOCATION"),
    ("lowercase_location", "directive @foo on field"),
    ("bad_operation", "subscriptio Foo { a }"),
    ("empty_selection", "{ }"),
    ("empty_args", "{ a() }"),
    ("empty_doc", ""),
    ("only_comment", "# nothing here"),
    ("union_empty_member", "union U = | "),
    ("type_list_unclosed", "query ($a: [Int) { a }"),
    ("double_bang", "query ($a: Int!!) { a }"),
    ("default_missing", "query ($a: Int = ) { a }"),
    ("implements_amp_only", "type T implements & { a: A }"),
    ("schema_no_ops", "schema {}"),
    ("dangling_at", "{ a @ }"),
    ("bad_value", "{ a(b: : ) }"),
    ("object_no_colon", "{ a(b: {c d}) }"),
]:
    job("parse " + case(name, text))

section("syntax errors from the lexer")
for name, text in [
    ("single_quote", "{ ''"),
    ("unterminated", '{ a(s: "no end'),
    ("unterminated_block", '{ a(s: """no end'),
    ("string_newline", '{ a(s: "multi\nline") }'),
    ("bad_escape", r'{ a(s: "bad \z esc") }'),
    ("bad_escape_x", r'{ a(s: "bad \x esc") }'),
    ("bad_unicode_short", r'{ a(s: "bad \u1 esc") }'),
    ("bad_unicode_letters", r'{ a(s: "bad \uXYZW esc") }'),
    ("bad_unicode_big", r'{ a(s: "\u{110000}") }'),
    ("bad_unicode_open", r'{ a(s: "\u{12") }'),
    ("bad_unicode_empty", r'{ a(s: "\u{}") }'),
    ("bad_unicode_long", r'{ a(s: "\u{000000000041}") }'),
    ("lone_surrogate", r'{ a(s: "\uDEAD") }'),
    ("lead_alone", r'{ a(s: "\uD83D x") }'),
    ("lead_then_bad", r'{ a(s: "\uD83DA") }'),
    ("surrogate_braces", r'{ a(s: "\u{D800}") }'),
    ("zero_zero", "{ a(n: 00) }"),
    ("dot_no_digits", "{ a(n: 1.) }"),
    ("dot_e", "{ a(n: 1.e1) }"),
    ("leading_dot", "{ a(n: .123) }"),
    ("exp_no_digits", "{ a(n: 1.0e) }"),
    ("two_dots", "{ a(n: 1.2.3) }"),
    ("hex", "{ a(n: 0xF1) }"),
    ("underscore", "{ a(n: 1_000) }"),
    ("letter_after", "{ a(n: 12abc) }"),
    ("minus_alone", "{ a(n: -) }"),
    ("plus", "{ a(n: +1) }"),
    ("two_dot_spread", "{ ..a }"),
    ("question", "query ($a: Int?) { a }"),
    ("reference_mark", "{ ※ }"),
    ("bell", "{ \x07 }"),
    ("zero_width", "{ a​ }"),
    ("emoji", "{ \U0001F600 }"),
    ("nbsp", "{ a }"),
    # graphql-core reads past the end of the body here and raises
    # IndexError, not GraphQLSyntaxError.
    ("escape_at_end", '{ a(s: "\\'),
    ("unicode_at_end", '{ a(s: "\\u12'),
    ("pair_at_end", '{ a(s: "\\uD83D\\u12'),
]:
    job("parse " + case(name, text))

section("where the error is reported")
job("parse " + case("brace_next_line", "{\n}"))
job("parse " + case("deep_line", "query {\n  user {\n    name(\n  }\n}"))
job("parse " + case("crlf_error", "query {\r\n  a\r\n  b(\r\n}"))
job("parse " + case("cr_error", "query {\r  a\r  b(\r}"))
job("parse " + case("minified", "{" + ",".join("f%d" % i for i in range(30)) + "," + "g(x: 1, y: [1,2,3], z: {w: 1})" +
                    "," + ",".join("h%d" % i for i in range(12)) + ",bad(:1)," + ",".join("k%d" % i for i in range(20)) + "}"))
job("parse " + case("minified_end", "{" + ",".join("field%d" % i for i in range(25)) + ",broken(}"))
job("parse " + case("vtab_comment", "# a\x0bb\n{\n  c(\n}"))
job("parse " + case("line_sep_comment", "# note \n{"))
job("parse " + case("formfeed_last", "{ a }\x0c}"))

# ------------------------------------------------------------ parse_value / parse_type

section("parse_value, parse_const_value and parse_type")
for name, text in [
    ("v_list", '[1, 2.5e3, "s", true, false, null, ENUM, $var, {a: {b: [x]}}]'),
    ("v_block", '"""\n  block\n"""'),
    ("v_empty_object", "{}"),
    ("v_trailing", "1 2"),
    ("v_var_name", "$"),
    ("v_bad", ")"),
    ("v_object_dup", "{a: 1, a: 2}"),
]:
    rel = case(name, text)
    job("value " + rel)
    job("const_value " + rel)
for name, text in [
    ("t_nested", "[[Int!]!]"),
    ("t_named", "  Upload  "),
    ("t_double_bang", "Int!!"),
    ("t_unclosed", "[Int"),
    ("t_empty", ""),
    ("t_list_of_list", "[[[ID]]]!"),
]:
    job("type " + case(name, text))

# ------------------------------------------------------------ tokens

section("the lexer's tokens, with comments, lines and columns")
job("tokens " + case("tok_basic", "query Q($a: Int = -12.5e+3) { f(s: \"x\\ty\", b: \"\") @d # note\n}"))
job("tokens " + case("tok_block", 'type T {\n  """\n  two\n  lines\n  """\n  a: Int\n}\n{ b }'))
job("tokens " + case("tok_block_crlf", '"""a\r\nb\r\n"""\r\nc\r\n  d'))
job("tokens " + case("tok_punct", "! $ & ( ) ... : = @ [ ] { | } , ,,, ﻿ end"))
job("tokens " + case("tok_comments", "#\n# two\r\n#three\rname\n# 日本 é\n"))
job("tokens " + case("tok_unicode", "{ f(s: \"café 東京 \U0001F680\", e: \"\\u00e9\\u{1F680}\") }"))
job("tokens cases/bad_escape.graphql")
job("tokens cases/empty_doc.graphql")

# ------------------------------------------------------------ the app

QUERIES = {
    "app/queries/user.graphql": '''query CurrentUser {
  viewer {
    ...UserFields
    cart { ...CartFields }
  }
}

query UserById($id: ID!, $withOrders: Boolean = false) {
  user(id: $id) {
    ...UserFields
    orders(first: 5) @include(if: $withOrders) {
      edges { node { id total { ...MoneyFields } } }
    }
  }
}
''',
    "app/queries/fragments.graphql": '''fragment UserFields on User {
  id
  name
  avatar(size: 64)
}

fragment MoneyFields on Money { amount currency }

fragment CartFields on Cart {
  id
  lines { quantity product { ...ProductCard } }
  subtotal { ...MoneyFields }
}

fragment ProductCard on Product {
  id
  title
  price { ...MoneyFields }
  images(first: 1) { url altText }
}
''',
    "app/queries/catalog.graphql": '''# The product listing page and its search box.
query Products($first:Int=24,$after:String,$sort:ProductSort=RELEVANCE,$filter:ProductFilter={inStock:true}){products(first:$first,after:$after,sort:$sort,filter:$filter){pageInfo{hasNextPage endCursor}edges{cursor node{...ProductCard}}}}

query Search($q: String!) {
  search(query: $q, types: [PRODUCT, COLLECTION]) {
    __typename
    ... on Product { ...ProductCard }
    ... on Collection { id title productsCount }
  }
}
''',
    "app/queries/checkout.graphql": '''mutation AddToCart($productId: ID!, $quantity: Int = 1) {
  cartLinesAdd(lines: [{productId: $productId, quantity: $quantity}]) {
    cart { ...CartFields }
    userErrors { field message }
  }
}

mutation Checkout($input: CheckoutInput!) @retry(times: 2) {
  checkoutComplete(input: $input) {
    order { id number total { ...MoneyFields } }
    userErrors { field message code }
  }
}

subscription OrderStatus($orderId: ID!) {
  orderStatusChanged(id: $orderId) { status updatedAt }
}
''',
    "app/queries/admin.graphql": '''query AdminDashboard {
  stats(range: LAST_7_DAYS) {
    revenue { ...MoneyFields }
    orders
    topProducts(first: 3) { ...ProductCard ...MissingFragment }
  }
}
''',
    "app/queries/broken.graphql": '''query Broken {
  user(id: "1") {
    name
    orders(first: ) { id }
  }
}
''',
    "app/queries/formatted.graphql": '''query Ping {
  ping
}
''',
}

SCHEMA = {
    "app/schema/schema.graphql": '''"""The shop's public API."""
schema {
  query: Query
  mutation: Mutation
}

scalar DateTime @specifiedBy(url: "https://scalars.graphql.org/andimarek/date-time")

interface Node { id: ID! }

type Query {
  viewer: User
  user(id: ID!): User
  products(first: Int = 24, after: String, sort: ProductSort, filter: ProductFilter): ProductConnection!
  search(query: String!, types: [SearchType!]): [SearchResult!]!
  stats(range: Range!): Stats @auth(requires: ADMIN)
}

type Mutation {
  cartLinesAdd(lines: [CartLineInput!]!): CartPayload
  checkoutComplete(input: CheckoutInput!): CheckoutPayload
}

type User implements Node {
  id: ID!
  name: String!
  avatar(size: Int = 32): Url
  cart: Cart
  orders(first: Int, after: String): OrderConnection
}

type Product implements Node {
  id: ID!
  title: String!
  price: Money!
  images(first: Int): [Image!]!
}

type Money { amount: Decimal! currency: Currency! }

enum Currency { USD EUR GBP INR JPY }

enum ProductSort { RELEVANCE PRICE_ASC PRICE_DESC NEWEST }

input ProductFilter { inStock: Boolean, minPrice: Int, maxPrice: Int }

union SearchResult = Product | Collection

directive @auth(requires: Role = USER) on FIELD_DEFINITION | OBJECT
''',
    "app/schema/orders.graphql": '''type Cart implements Node {
  id: ID!
  lines: [CartLine!]!
  subtotal: Money!
}

type CartLine { quantity: Int! product: Product! }

type Order implements Node & Timestamped {
  id: ID!
  number: Int!
  total: Money!
  status: OrderStatus!
}

enum OrderStatus { PENDING PAID SHIPPED DELIVERED }

input CartLineInput { productId: ID!, quantity: Int = 1 }

extend type Query {
  order(id: ID!): Order
}

extend type User @key(fields: "id")

extend enum Currency { CAD AUD }

extend union SearchResult = Order

extend schema { subscription: Subscription }

type Subscription { orderStatusChanged(id: ID!): Order }
''',
}

JS = {
    "app/src/UserCard.jsx": '''import { gql, useQuery } from "@apollo/client";

const USER_CARD = gql`
  query UserCard($id: ID!) {
    user(id: $id) { id name avatar(size: 48) }
  }
`;

export function UserCard({ id }) {
  const { data } = useQuery(USER_CARD, { variables: { id } });
  return <div className="card">{data?.user.name}</div>;
}

const BROKEN = gql`
  query Broken($id: ID!) {
    user(id: $id) {
      name
      friends(first: 10 {
        name
      }
    }
  }
`;
''',
    "app/src/api.ts": '''import gql from "graphql-tag";

export const PRODUCT_FIELDS = gql`fragment ProductFields on Product { id title }`;

export const SEARCH = gql`query Search($q: String!) { search(query: $q) { ... on Product { ...ProductFields } } }`;

export function byId(id: string) {
  return gql`query ById { node(id: "${id}") { id } }`;
}

  const TYPO = gql`query Typo { product(id: 1) { title, price { amount } }`;
''',
}

for rel, text in QUERIES.items():
    put(rel, text)
for rel, text in SCHEMA.items():
    put(rel, text)
for rel, text in JS.items():
    put(rel, text)

section("a client app: format check, persisted-query manifest, schema check, gql`` extraction")
job("!format " + " ".join(sorted(QUERIES)))
job("!manifest " + " ".join(sorted(QUERIES)))
job("!schema " + " ".join(SCHEMA))
job("!schema cases/schema_kitchen_sink.graphql")
job("!extract " + " ".join(JS))

# The tokens jobs print values with repr(); keep what they lex to printable
# characters outside ASCII, so repr shows them as they are.
for line in JOBS:
    if line.startswith("tokens "):
        with open(os.path.join(D, line.split()[1]), encoding="utf-8") as f:
            for c in f.read():
                assert ord(c) < 0x80 or c.isprintable() or c == "\ufeff", (line, c)

with open(os.path.join(D, "jobs.txt"), "w", encoding="utf-8") as f:
    for line in JOBS:
        f.write(line + "\n")
with open(os.path.join(D, "files.txt"), "w", encoding="utf-8") as f:
    for rel in FILES:
        f.write(rel + "\n")
print(len(FILES), "files,", sum(1 for j in JOBS if not j.startswith("#")), "jobs")
