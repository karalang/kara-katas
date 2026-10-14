# LeetCode #591: Tag Validator -- Python mirror of the ★ arm (one scan
# with a stack of open tags); see tag_validator.kara.


def valid_name(name):
    return 1 <= len(name) <= 9 and all("A" <= c <= "Z" for c in name)


def is_valid(code):
    n = len(code)
    stack = []
    i = 0
    while i < n:
        if i > 0 and not stack:
            return False
        if code.startswith("<![CDATA[", i):
            if not stack:
                return False
            k = code.find("]]>", i + 9)
            if k < 0:
                return False
            i = k + 3
        elif code.startswith("</", i):
            start = i + 2
            k = code.find(">", start)
            if k < 0:
                return False
            name = code[start:k]
            if not stack or stack[-1] != name:
                return False
            stack.pop()
            i = k + 1
        elif code.startswith("<", i):
            start = i + 1
            k = code.find(">", start)
            if k < 0:
                return False
            name = code[start:k]
            if not valid_name(name):
                return False
            stack.append(name)
            i = k + 1
        else:
            if not stack:
                return False
            i += 1
    return not stack


# ---- test harness ---------------------------------------------------------

seed = 0


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def snippet(depth):
    names = ["A", "B", "XY", "ABCDEFGHI", "ABCDEFGHIJ", "b", "", "A1"]
    texts = ["x", " ", ">", "]]>", "<", "!", "[", "y", "/", "..."]
    name = names[step() % len(names) if step() % 3 == 0 else step() % 3]
    out = f"<{name}>"
    parts = step() % 4
    for _ in range(parts):
        roll = step() % 10
        if roll < 3 and depth > 0:
            out += snippet(depth - 1)
        elif roll < 5:
            inside = texts[step() % len(texts)]
            if step() % 8 == 0:
                out += f"<![CDATA[{inside}"
            else:
                out += f"<![CDATA[{inside}]]>"
        else:
            out += texts[step() % len(texts)]
    end = step() % 12
    if end == 0:
        out += "</C>"
    elif end > 1:
        out += f"</{name}>"
    return out


def show(code):
    print(f"{code} -> {str(is_valid(code)).lower()}")


def main():
    global seed
    show("<DIV>This is the first line <![CDATA[<div>]]></DIV>")
    show("<DIV>>>  ![cdata[]] <![CDATA[<div>]>]]>]]>>]</DIV>")
    show("<A>  <B> </A>   </B>")
    show("<DIV>  div tag is not closed  <DIV>")
    show("<DIV>  unmatched <  </DIV>")
    show("<DIV> closed tags with invalid tag name  <b>123</b> </DIV>")
    show("<DIV> unmatched tags with invalid tag name  </1234567890> and <CDATA[[]]>  </DIV>")
    show("<DIV>  unmatched start tag <B>  and unmatched end tag </C>  </DIV>")
    show("<ABCDEFGHI></ABCDEFGHI>")
    show("<ABCDEFGHIJ></ABCDEFGHIJ>")
    show("<></>")
    show("<A></A>x")
    show("x<A></A>")
    show("<![CDATA[x]]><A></A>")
    show("<A></A><B></B>")
    show("<A><![CDATA[</A>]]></A>")
    show("<A><![CDATA[x]]>]]></A>")
    show("<A><![CDATA[x</A>")
    show("<A><B><C></C></B></A>")
    show("<A><B></A></B>")
    show("<A>")
    show("A")
    seed = 591
    valid = 0
    checksum = 0
    for k in range(300):
        code = snippet(3)
        if is_valid(code):
            valid += 1
            checksum = (checksum * 31 + k + len(code)) % 1000000007
    print(f"300 random snippets: {valid} valid, checksum {checksum}")
    deep = "<ABCD>" * 38 + "      " + "</ABCD>" * 38
    print(f"38 deep, {len(deep)} characters: {str(is_valid(deep)).lower()}")
    wide = "<Z>" + "<B><![CDATA[]]></B>" * 25
    while len(wide) < 496:
        wide += " "
    wide += "</Z>"
    print(f"25 side by side, {len(wide)} characters: {str(is_valid(wide)).lower()}")


main()
