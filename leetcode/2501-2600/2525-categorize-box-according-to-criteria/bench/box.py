# LeetCode #2525: Categorize Box According to Criteria -- benchmark mirror
# of the ★ arm (box.kara): 100000 boxes built once, then the passes, each
# naming every box from an offset the checksum picks.


def categorize_box(length, width, height, mass):
    bulky = length >= 10000 or width >= 10000 or height >= 10000 or length * width * height >= 1000000000
    heavy = mass >= 100
    match (bulky, heavy):
        case (True, True):
            return "Both"
        case (True, False):
            return "Bulky"
        case (False, True):
            return "Heavy"
        case _:
            return "Neither"


seed = 2525


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    return next_random() * 32768 + next_random()


def main():
    boxes = []
    for t in range(100000):
        top = 100000 if t % 2 == 0 else 2000
        length = wide_random() % top + 1
        width = wide_random() % top + 1
        height = wide_random() % top + 1
        boxes.append((length, width, height, next_random() % 1000 + 1))
    passes = 220
    check = 0
    for p in range(passes):
        start = check % 100000
        for i in range(100000):
            length, width, height, mass = boxes[(start + i) % 100000]
            name = categorize_box(length, width, height, mass)
            code = 1 if name == "Both" else 2 if name == "Bulky" else 3 if name == "Heavy" else 4
            check = (check * 31 + code + p) % 1000000007
    print(f"{passes} passes over 100000 boxes: checksum {check}")


main()
