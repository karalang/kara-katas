#!/usr/bin/env python3
"""Writes data/: the HTML a small static-site generator renders through
SmartyPants (data/posts/), and data/jobs.tsv, the script oracle.py and
mini_smartypants.kara both replay.

Each line of jobs.tsv is one step, its fields separated by tabs:

    job      <title>
    sp       <text> <attr>       smartypants(text, attr); attr "-" is None
    fn       <name> <text> [<mode>]   one of the module's functions
    default  <attr>              Attr.default = attr
    skip     <tag,tag,...>       smartypants.tags_to_skip = the list ("-":
                                 the library's own list)
    file     <post> <attr>       smartypants() over data/posts/<post>
    cli      <arg> ...           the smartypants command, run in data/

In text fields a backslash escapes itself, a tab (\\t) and a newline
(\\n); anything else is literal.

Run: python3 -s -P -B mk.py"""
import os

os.makedirs("data/posts", exist_ok=True)

Q, B, b, d, D, i, e, w = 1, 6, 2, 8, 24, 40, 64, 128
u, h, s = 256, 512, 768
SET0, SET1, SET2, SET3 = 0, Q | b | d | e, Q | b | D | e, Q | b | i | e

POSTS = {
    "week-notes.html": """<h1>Week notes: "shipping" the '26 redesign</h1>
<p>It's been a long week -- the kind where "done" means 'mostly done'...
We finally shipped the new navigation; the team's reaction was, well, "fine."</p>
<p>Some numbers: 3 deploys, 2 rollbacks, 1 very patient on-call engineer.
Load times dropped from 2.4s to 1.1s -- that's a 54% cut. Not bad for the '90s-era
backend we're still running.</p>
<p>Quote of the week: "Don't ship on Fridays," said nobody who's ever met a deadline.</p>
<p>Next week . . . more of the same?</p>
""",
    "release-notes.html": """<h2>Release 4.2 -- "Larkspur"</h2>
<p>Use the new <code>--dry-run</code> flag to preview changes. Press <kbd>Ctrl-"</kbd> to open the palette.</p>
<pre><code>$ deploy --env "staging" --tag 'v4.2'
echo "it's done" -- really
</code></pre>
<p>Upgrading from 3.x? Read the "Breaking changes" section first -- it's short.</p>
<pre>
  config['retries'] = 3   # "three" tries
</pre>
<p>Thanks to everyone who filed bugs in the '25 beta... you know who you are.</p>
""",
    "recipe.html": """<h1>Grandma's "naïve" café crème</h1>
<p>Serves 4--6. You'll need a 9" pan (about 23 cm) and a friend who's 5'10" to reach the top shelf.</p>
<p>Whisk 'em together until it's "just right" -- rock 'n' roll style.</p>
<p>Le chef a dit : « C'est l'heure ! » and she said "Ça va?" -- yes, ça va.</p>
<p>Bake at 180°C for 25--30 minutes...</p>
""",
    "dreamweaver.html": """<p>He said &quot;Let's write some code.&quot; &mdash; and we did.</p>
<p>&quot;Quoted&quot; text&nbsp;'here' and&nbsp;"there" &ndash; plus &#8220;already curly&#8221;.</p>
<p>Prices: &pound;5 -- &euro;6 ... &quot;cheap&quot;</p>
""",
    "script-page.html": """<html><head>
<style>
  q:before { content: "\\201C"; }  /* "quotes" -- in CSS */
</style>
<script type="text/javascript">
<!--
var msg = "it's a test -- ignore";
document.write('<a href="' + msg + '">' + "link" + "</a>");
//-->
</script>
</head><body>
<!-- a "comment" with no double dash -->
<!-- a comment -- with a double dash -->
<p>After the "comments" -- text.</p>
<math><mi>x</mi><mo>"</mo></math>
<p>Done -- 'really'.</p>
</body></html>
""",
    "escapes.html": """<p>Use \\"dumb quotes\\" when you mean them, and \\'single\\' ones.</p>
<p>A literal \\-\\- stays two dashes, \\.\\.\\. stays three dots, a backslash is \\\\.</p>
<p>``Backtick quotes'' and `single backticks' too.</p>
<p>A \\`backtick\\` escaped.</p>
""",
    "broken.html": """<p>An <b>unclosed "tag <i>here</i> and "quotes" -- still.</p>
<PRE>Upper "case" pre -- kept</PRE>
<prefix>"prefix" is not pre -- or is it?</prefix>
</code> a stray close "tag" -- then text.
<sample>"sample" starts with samp</sample> "after"
<code>"open" code <pre>"nested" pre</pre> "still" inside</code> "outside"
<p>Ends without a newline -- "here"</p>""",
    "plain.txt": """Plain text with no tags at all.
"Quotes", 'apostrophes', it's, '70s, 1970's -- and ellipses...
Line three -- with --- triple and ---- quadruple dashes.
""",
    "empty.html": "",
}
for name, body in POSTS.items():
    with open(os.path.join("data/posts", name), "w", encoding="utf-8") as f:
        f.write(body)

TEXTS = [
    '"foo" -- bar',
    '"Isn\'t this fun?"',
    "'Isn't this fun?'",
    "1440-80's", "1440-'80s", "1440--'80s", "1960s", "1960's", "one two '60s", "'60s",
    "the '80s and the 90's",
    "21st century", "3rd",
    'You should use ";" here',
    'Take a look at the "<a>Essay on quoting</a>" paper.',
    'Take a look at "<a>Essay on quoting</a>".',
    "<p>He said &quot;Let's write some code.&quot; This code here <code>if True:\n\tprint &quot;Okay&quot;</code> is python code.</p>",
    "--", "-->", "-- \t  >",
    '<!-- "foo" --> blah--blah <!-- "bar" -->',
    '<p>foo -- "bar"<!-- foo-bar\n<p>blah "this"</p>\n-->\n</p>',
    "<!-- comment -->", "<!-- <li>Fee-fi-of-fum</li> -->", '<!-- "foo" --> <!-- "bar" -->',
    "<!-- -- -->", "<!-- -- -- \t >", "<!---->", "<!-- --->", "<!-- x -- >",
    '"quote here"', '"quote&ndash;here"',
    "Nothing endures but change. -- Heraclitus",
    "Life itself is the proper binge. --- Julia Child (1912--2004)",
    "Dare to be naïve. -- Buckminster Fuller (1895---1983)",
    "Huh...?", "Wait. . . what?", "Four.... dots", "Spaced . . . . out",
    "``Isn't this fun?''", "`Isn't this fun?'", "``double'' and `single'",
    r'"smarty" \"pants\"', r"\\", r"a \- b \. c \` d \' e \" f \\ g",
    "'", '"', "x'", "'x", 'x"', '"x', "' '", '" "',
    "He said, \"'Quoted' words in a larger quote.\"",
    "'\"Nested\" inside'",
    "\"'Double then single'\"",
    "\"...\" and '...'",
    "\"?\" she asked", "'!' he said", "\"!\" -- '?'",
    "Rock 'n' roll", "'Tis the season", "the dog's bone, the dogs' bones",
    "&nbsp;'tis &nbsp;\"so\"", "&mdash;'word' &ndash;\"word\"",
    "&#8211;'dash' &#8212;\"dash\" &#x2013;'hex' &#x2014;\"hex\"",
    "(\"paren\") ['bracket'] {\"brace\"} -'dash'-",
    "\"5'10\" tall\"", "a 9\" pan, 12' board",
    "'quoted'\n'next line'", "\"tab\"\t'tab'",
    "Ça va? \"Très bien\" -- 'merci'", "«Bonjour» \"monde\"",
    "数字 \"引用\" 'テスト'", "emoji 🎉 \"party\" 'time'",
    "'_underscore_' \"_also_\"",
    "<b>\"bold\"</b> <i>'italic'</i>",
    "<a href=\"x\">\"link\"</a>",
    "<code>\"code\"</code> \"after\"",
    "<pre>\"pre\" -- </pre> -- \"after\"",
    "<PRE>\"upper\"</PRE> \"after\"",
    "<pre><code>\"a\"</pre> \"b\"</code> \"c\"",
    "<code><pre>\"a\"</code></pre> \"b\"",
    "</pre> \"stray close\"",
    "<pre/> \"self closing\"",
    "<prefix>\"not pre\"</prefix>",
    "<script>if (a--) { x = \"y\"; }</script> -- \"z\"",
    "<style>a { b: \"c\" }</style> \"d\"",
    "a < b and \"c\" > d",
    "<p \"unterminated tag", "text <", "> \"gt\" first",
    "", "plain", "...", "---", "----", "-----",
    "&quot;", "&quot;quot&quot;", "&amp;quot; \"x\"",
    "\\\"escaped\\\"",
    "it's 'single' and \"double\"",
    "'''", '"""', "''", '""', "\"'\"", "'\"'",
    "x 'y z' w", "x \"y z\" w",
    "1'2\"3", "'1' '2s' '3 '",
    "the '80s's music", "'00s", "'12s",
    "'s", "s'", "'s'", "dogs's",
    "-'x'", "--'x'", "—'x'", "–\"x\"",
]

ATTRS = ["-", 0, SET1, SET2, SET3, Q, b, B, d, D, i, e, w, Q | w, w | B,
         SET1 | u, SET1 | h, SET1 | s, SET2 | h, SET3 | s, SET2 | u,
         b | B, D | i, d | D, u | h, Q | B, B | e | d, 1023, 4096]

L = []


def esc(t):
    return t.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")


def step(*fields):
    L.append("\t".join(str(f) for f in fields))


step("job", "the library's examples and tests")
for t in TEXTS[:40]:
    step("sp", esc(t), "-")
for t, a in [('"foo" -- bar', d), ("<p>He said &quot;Let's write some code.&quot;</p>", w),
             ("<p>He said &quot;Let's write some code.&quot;</p>", Q | w),
             ('"quote here"', SET1 | u), ('"quote&ndash;here"', SET1 | u),
             ('"quote here"', SET1 | h), ('"quote here"', SET1 | s)]:
    step("sp", esc(t), a)

step("job", "every text with every attribute")
for t in TEXTS:
    for a in ATTRS:
        step("sp", esc(t), a)

step("job", "the converters one at a time")
for name in ["convert_quotes", "convert_backticks", "convert_single_backticks",
             "convert_dashes", "convert_dashes_oldschool",
             "convert_dashes_oldschool_inverted", "convert_ellipses", "process_escapes"]:
    for t in TEXTS:
        step("fn", name, esc(t))
ENT = ["&#8216;", "&#8216;SmartyPants&#8217;", "&#8220;Hello &#8212; world.&#8221;",
       "&#8211;&#8212;&#8216;&#8217;&#8220;&#8221;&#8230;", "&#8230;&#8230; &#8213; &#821;",
       "&#38;#8220;", "plain"]
for t in ENT:
    for mode in [0, 1, 2]:
        step("fn", "convert_entities", esc(t), mode)
for t in TEXTS + ["<a><b>", "<<a>>", "a<!--b-->c", "<!-- a -- b --> <!-- c --  >",
                  "<!--\n-- \n-->", "<!-- x --\t\n >", "<!-- unterminated", "x<y",
                  "<a href=\"<MTFoo>\">", "<!---->", "<!-- -- ->", "<>", "<!>"]:
    step("fn", "_tokenize", esc(t))
for tags in ["-", "pre", "pre,code", "a|b", "", "x,,y"]:
    step("fn", "_tags_to_skip_regex", tags)

step("job", "changing the default")
for a in [Q, Q | d, SET2 | h, 0, SET1]:
    step("default", a)
    for t in ['"foo" -- bar', "'tis... the '80s --- \"really\""]:
        step("sp", esc(t), "-")
        step("sp", esc(t), SET3)

step("job", "skipping other elements")
for tags in ["pre,code", "p", "h1,h2", "blockquote", "", "PRE", "b,i", "-"]:
    step("skip", tags)
    for t in ["<p>\"para\" -- 'x'</p> \"out\"", "<pre>\"pre\"</pre> <code>\"code\"</code> \"out\"",
              "<h1>\"head\"</h1><h2>'sub'</h2> -- \"body\"",
              "<b>\"bold\"</b> <i>'it'</i> \"plain\"", "<blockquote>\"q\"</blockquote> \"after\""]:
        step("sp", esc(t), "-")

step("job", "rendering the posts")
for post in sorted(POSTS):
    for a in ["-", SET2 | u, SET3 | h, SET1 | s, Q | w, 0]:
        step("file", post, a)
step("skip", "pre,samp,code,tt,kbd,script,style,math,h1")
step("file", "week-notes.html", "-")
step("file", "recipe.html", SET1 | u)
step("skip", "-")

step("job", "the command line")
CLI = [
    ["posts/week-notes.html"],
    ["-a", "2", "posts/recipe.html"],
    ["-a", "qbdew", "posts/dreamweaver.html"],
    ["--attr", "qw", "posts/dreamweaver.html"],
    ["--attr=1u", "posts/recipe.html", "posts/plain.txt"],
    ["-a1h", "posts/escapes.html"],
    ["-a", "3s", "posts/week-notes.html"],
    ["-a", "0", "posts/broken.html"],
    ["-a", "Bq", "posts/escapes.html"],
    ["-a", "Dei", "posts/plain.txt"],
    ["-a", "", "posts/plain.txt"],
    ["-a", "qz", "posts/plain.txt"],
    ["-a", "zyz", "posts/plain.txt"],
    ["-a", "x1", "posts/plain.txt"],
    ["-a", "4", "posts/plain.txt"],
    ["-a", "set1", "posts/plain.txt"],
    ["-s", "pre,code,h1", "posts/week-notes.html"],
    ["-s", "p", "posts/release-notes.html"],
    ["--skip=", "posts/broken.html"],
    ["-s", "script", "posts/script-page.html"],
    ["posts/empty.html", "posts/plain.txt", "posts/empty.html"],
    ["posts/missing.html"],
    ["posts/plain.txt", "posts/missing.html"],
    ["-v"],
    ["--version", "posts/plain.txt"],
    ["-x", "posts/plain.txt"],
    ["-a"],
    ["posts/plain.txt", "-a", "q"],
    ["--", "-a"],
]
for args in CLI:
    step("cli", *[x if x else "''" for x in args])

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
