# LeetCode #2469: Convert the Temperature -- the bench, the ★ arm in
# Python: the two formulas as given.


def convert_temperature(celsius):
    return [celsius + 273.15, celsius * 1.80 + 32.00]


def main():
    # 230 passes over every temperature from 0 to 1000 in hundredths,
    # each pass starting at a hundredth chosen from the checksum so far;
    # every answer's kelvin in hundredths and Fahrenheit in thousandths,
    # rounded, folded into the checksum
    check = 0
    for p in range(230):
        start = check % 100001
        for i in range(100001):
            h = (start + i) % 100001
            got = convert_temperature(h / 100.0)
            kelvin = round(got[0] * 100.0)
            fahrenheit = round(got[1] * 1000.0)
            check = (check * 31 + kelvin + fahrenheit + p) % 1000000007
    print(f"230 passes over every hundredth from 0 to 1000: checksum {check}")


main()
