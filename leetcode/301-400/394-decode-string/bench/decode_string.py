# LeetCode #394 bench harness — Python mirror (ergonomic foil).
#
# Decode a fixed nested-encoded string ITERS times, reducing each pass to its
# decoded length. The template decodes to only 52 chars but nests three repeat
# levels, so each of the 800k passes does the full scan + stack + small-repeat +
# allocation churn the kata stresses (per-decode overhead dominates, not raw
# memcpy bandwidth). Sink = ITERS * decoded_len, one i64 every comparator matches.

ENCODED = "3[ab2[cd]ef]5[gh]2[ij3[kl]m]"
ITERS = 800000


def decode_string(s):
    str_stack = []
    num_stack = []
    cur = ""
    k = 0
    for ch in s:
        if "0" <= ch <= "9":
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


def main():
    total = 0
    for _ in range(ITERS):
        total += len(decode_string(ENCODED))
    print(total)


if __name__ == "__main__":
    main()
