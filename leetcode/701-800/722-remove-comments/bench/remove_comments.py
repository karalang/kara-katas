# LeetCode #722 bench harness — Python mirror (ergonomic foil).
#
# Byte-indexed segment-slicing — same canonical algorithm as the Kāra mirror:
# scan each line, classify `/` `*` markers, append each surviving run as one
# slice (no per-char push). Sink = ITERS * (surviving chars per pass) = 30960000.

REPS = 60
ITERS = 4000

TEMPLATE = [
    "int main() {            // entry point",
    "  int a = 1; /* inline */ int b = 2;",
    "  /* a multi-line",
    "     block comment that",
    "     spans several lines */ int c = a + b;",
    "  // a full line comment",
    "  int e = c * 3;        /* trailing block */",
    "  int d = a /* x */ + b /* y */ + c;",
    "  return d * 2;//done",
    "}",
]


def remove_comments(source):
    result = []
    buffer = []
    in_block = False
    for line in source:
        n = len(line)
        seg_start = 0
        i = 0
        while i < n:
            if not in_block:
                if i + 1 < n and line[i] == "/" and line[i + 1] == "/":
                    buffer.append(line[seg_start:i])
                    seg_start = n
                    break
                elif i + 1 < n and line[i] == "/" and line[i + 1] == "*":
                    buffer.append(line[seg_start:i])
                    in_block = True
                    i += 2
                else:
                    i += 1
            else:
                if i + 1 < n and line[i] == "*" and line[i + 1] == "/":
                    in_block = False
                    i += 2
                    seg_start = i
                else:
                    i += 1
        if not in_block:
            buffer.append(line[seg_start:n])
            joined = "".join(buffer)
            if joined:
                result.append(joined)
            buffer = []
    return result


def pass_len(source):
    return sum(len(s) for s in remove_comments(source))


def build_lines(reps):
    lines = []
    for _ in range(reps):
        lines.extend(TEMPLATE)
    return lines


def main():
    lines = build_lines(REPS)
    total = 0
    for _ in range(ITERS):
        total += pass_len(lines)
    print(total)


if __name__ == "__main__":
    main()
