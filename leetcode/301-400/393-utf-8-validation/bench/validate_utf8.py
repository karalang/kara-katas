"""Benchmark workload for LeetCode #393 — UTF-8 Validation (Python; scale lane)."""


def lead_len(b):
    if b & 0x80 == 0x00:
        return 1
    elif b & 0xE0 == 0xC0:
        return 2
    elif b & 0xF0 == 0xE0:
        return 3
    elif b & 0xF8 == 0xF0:
        return 4
    return 0


def is_continuation(b):
    return b & 0xC0 == 0x80


def validate_window(data, base, w):
    end = base + w
    i = base
    while i < end:
        need = lead_len(data[i])
        if need == 0:
            return False
        if i + need > end:
            return False
        k = 1
        while k < need:
            if not is_continuation(data[i + k]):
                return False
            k += 1
        i += need
    return True


def main():
    records = 40000
    w = 32
    passes = 60
    total = records * w

    data = bytearray(total)

    state = 12345
    for rec in range(records):
        base = rec * w
        filled = 0
        while filled < w:
            state = (state * 1103515245 + 12345) & 2147483647
            r = state >> 16
            cat = r % 100
            sub = r // 100
            rem = w - filled
            if cat < 8:
                data[base + filled] = (128 + (sub % 64)) & 0xFF
                filled += 1
            elif cat < 60 or rem < 2:
                data[base + filled] = (sub % 128) & 0xFF
                filled += 1
            elif cat < 80 or rem < 3:
                data[base + filled] = (192 + (sub % 32)) & 0xFF
                data[base + filled + 1] = (128 + (sub % 64)) & 0xFF
                filled += 2
            elif cat < 93 or rem < 4:
                data[base + filled] = (224 + (sub % 16)) & 0xFF
                data[base + filled + 1] = (128 + (sub % 64)) & 0xFF
                data[base + filled + 2] = (128 + (sub % 64)) & 0xFF
                filled += 3
            else:
                data[base + filled] = (240 + (sub % 8)) & 0xFF
                data[base + filled + 1] = (128 + (sub % 64)) & 0xFF
                data[base + filled + 2] = (128 + (sub % 64)) & 0xFF
                data[base + filled + 3] = (128 + (sub % 64)) & 0xFF
                filled += 4

    sink = 0
    for p in range(passes):
        idx = (p * 40009) % total
        data[idx] = (255 - data[idx]) & 0xFF

        count = 0
        for rec in range(records):
            if validate_window(data, rec * w, w):
                count += 1
        sink += count

    print(sink)


main()
