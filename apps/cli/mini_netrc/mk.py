"""Writes data/ for mini_netrc: the .netrc files a deploy tool reads its
credentials from (all of them fake), each exercising the lexer's quoting,
comments, macros and mistakes, and the script that queries them.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)

FILES = {
    # A typical file: machines, the `user` synonym, an account, a default
    # and a macro; a machine named twice keeps its first place.
    "deploy.netrc": (
        "machine ftp.example.org login anonymous password guest@example.org\n"
        "machine build.example.org\n"
        "\tlogin ci-bot\n"
        "\tpassword not-a-real-token\n"
        "\taccount ops\n"
        "\n"
        "machine mirror.example.org user mirror password fake-pass-1\n"
        "macdef init\n"
        "cd /pub\n"
        "binary\n"
        "\n"
        "machine build.example.org login ci-bot-2 password rotated-fake\n"
        "default login anonymous password anon@example.org\n"
    ),
    # Quoting: a quoted token may hold spaces and a `\"`; a backslash
    # outside quotes takes the next character; a `#` inside a value is part
    # of it; a value may be the empty string.
    "quoting.netrc": (
        'machine git.example.org login "Ada Lovelace" password "two words"\n'
        'machine q.example.org login say\\ hi password "a \\"quoted\\" one"\n'
        "machine hash.example.org login h password pass#word\n"
        "machine lead.example.org login l password #leading\n"
        'machine empty.example.org login "" password ""\n'
        "machine tab.example.org\tlogin\tt\tpassword\tp\n"
        "machine back.example.org login b password c:\\\\dir\\\\\n"
        "machine utf.example.org login u password p\u00e4ssw\u00f6rd\n"
    ),
    # Comments: a lone `#` skips the rest of its line, but only when no
    # newline came between the previous token and it; a `#word` is a token.
    "comments.netrc": (
        "# deploy credentials\n"
        "machine a.example.org login a password pa # trailing note\n"
        "# a whole-line comment right after\n"
        "machine b.example.org login b password pb\n"
        "#tight-comment\n"
        "machine c.example.org login c password pc\n"
    ),
    # After a blank line the comment's words are read as tokens.
    "gap_comment.netrc": (
        "machine a.example.org login a password pa\n"
        "\n"
        "# note after a gap\n"
        "machine b.example.org login b password pb\n"
    ),
    # Windows line endings read as newlines; a macro ends at an empty line.
    "crlf.netrc": (
        "machine w.example.org\r\n"
        "  login win\r\n"
        "  password fake-win\r\n"
        "macdef upload\r\n"
        "put build.zip\r\n"
        "bye\r\n"
        "\r\n"
        "machine x.example.org login x password px\r\n"
    ),
    # A macro's name may share its line with the first body line; the
    # body's lines do not count toward the line number.
    "macros.netrc": (
        "macdef first put a.txt\n"
        "put b.txt\n"
        "\n"
        "macdef second\n"
        "ls\n"
        "\n"
        "macdef first\n"
        "get c.txt\n"
        "\n"
        "machine m.example.org login m password pm\n"
    ),
    # The same, then a mistake: its line number leaves out the macros'.
    "after_macro.netrc": (
        "macdef first put a.txt\n"
        "put b.txt\n"
        "\n"
        "machine m.example.org login m password pm frobnicate\n"
    ),
    "empty.netrc": "",
    "only_comments.netrc": "# nothing here\n   \n\t# indented\n",
    "bad_toplevel.netrc": "port 21\nmachine a login a password pa\n",
    # After an entry, `login` is still one of its followers.
    "late_login.netrc": "machine a login a password pa\nlogin b\n",
    "bad_follower.netrc": "machine a login a\n\tpasswd pa\n",
    "missing_name.netrc": "machine a login a password pa\nmachine\n",
    "empty_name.netrc": 'machine "" login a password pa\n',
    "open_macro.netrc": "macdef deploy\nput x\nput y\n",
    "open_quote.netrc": 'machine a login a password "never closed\n',
    "dangling.netrc": "machine a login a password\n",
    "lone_hash_entry.netrc": "machine a login a #\npassword pa\n",
}

SCRIPT = r"""# Queries against the .netrc files under data/.
parse deploy
dump deploy
auth deploy ftp.example.org
auth deploy build.example.org
auth deploy mirror.example.org
auth deploy unknown.example.org
macro deploy init
macro deploy nosuch

parse quoting
dump quoting
auth quoting git.example.org
auth quoting q.example.org
auth quoting hash.example.org
auth quoting lead.example.org
auth quoting empty.example.org
auth quoting tab.example.org
auth quoting back.example.org
auth quoting utf.example.org
auth quoting nosuch.example.org

parse comments
dump comments
parse gap_comment
parse crlf
dump crlf
macro crlf upload
parse macros
dump macros
macro macros first
macro macros second
parse after_macro
parse empty
dump empty
auth empty anywhere
parse only_comments

parse bad_toplevel
parse late_login
auth late_login a
parse bad_follower
parse missing_name
parse empty_name
parse open_macro
parse open_quote
dump open_quote
parse dangling
dump dangling
parse lone_hash_entry
dump lone_hash_entry

# Mistakes.
parse nosuch
dump nosuch
auth deploy
auth nosuch ftp.example.org
macro deploy
parse
parse a b
login deploy
"""

for name, body in FILES.items():
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(body)
with open(os.path.join("data", "script.txt"), "w", encoding="utf-8", newline="") as fh:
    fh.write(SCRIPT)
