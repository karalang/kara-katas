# LeetCode #394: Decode String — reference oracle.
#
# Decode `k[encoded]` runs, nested: `3[a2[c]]` -> "accaccacc". One stack-based
# left-to-right scan:
#   digit   -> k = k*10 + d         (multi-digit repeat counts)
#   '['     -> push (out_so_far, k), reset out="" and k=0
#   ']'     -> pop (prev, count); out = prev + out*count
#   letter  -> out += letter
#
# The closest corpus analog to the self-hosted lexer's escape / repeat
# machinery: digit-run -> integer accumulation, a bracket-nesting stack, and a
# push/concat output storm.


def decode_string(s):
    str_stack = []
    num_stack = []
    cur = ""
    k = 0
    for ch in s:
        if ch.isdigit():
            k = k * 10 + (ord(ch) - ord("0"))
        elif ch == "[":
            str_stack.append(cur)
            num_stack.append(k)
            cur = ""
            k = 0
        elif ch == "]":
            count = num_stack.pop()
            prev = str_stack.pop()
            cur = prev + cur * count
        else:
            cur += ch
    return cur


def report(s):
    print(f'"{s}" -> "{decode_string(s)}"')


def main():
    # LeetCode canonical examples.
    report("3[a]2[bc]")        # aaabcbc
    report("3[a2[c]]")         # accaccacc
    report("2[abc]3[cd]ef")    # abcabccdcdcdef
    report("abc3[cd]xyz")      # abccdcdcdxyz

    # Single repeat / multi-digit counts.
    report("1[a]")             # a
    report("10[a]")            # aaaaaaaaaa
    report("12[ab]")           # ababababababababababababab

    # Deep nesting.
    report("2[2[2[a]]]")       # aaaaaaaa
    report("3[z3[y]]")         # zyyyzyyyzyyy
    report("2[a3[b]c]")        # abbbcabbbc

    # No brackets / mixed prefix+suffix literals.
    report("abcdef")           # abcdef
    report("2[a]bc3[d]")       # aabcddd
    report("x2[y]z")           # xyyz

    # Adjacent groups and letters between nests.
    report("2[ab3[cd]]ef")     # abcdcdcdabcdcdcdef


if __name__ == "__main__":
    main()
