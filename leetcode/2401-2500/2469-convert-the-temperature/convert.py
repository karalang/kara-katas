def convert_temperature(celsius):
    return [celsius + 273.15, celsius * 1.80 + 32.00]


# ---- test harness ---------------------------------------------------------

seed = 2469


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(values):
    return f"[{values[0]:.5f}, {values[1]:.5f}]"


def main():
    for celsius in (36.50, 122.11, 0.00, 1000.00, 0.01, 40.00, 999.99):
        print(f"{celsius:.2f} -> {show(convert_temperature(celsius))}")
    kelvin_sum = 0
    fahrenheit_sum = 0
    for hundredths in range(100001):
        got = convert_temperature(hundredths / 100.0)
        kelvin_sum += round(got[0] * 100000.0)
        fahrenheit_sum += round(got[1] * 100000.0)
    print(f"every hundredth: kelvin {kelvin_sum}, fahrenheit {fahrenheit_sum}")
    check = 0
    for _ in range(3000):
        a = next_random()
        hundredths = (a * 32768 + next_random()) % 100001
        got = convert_temperature(hundredths / 100.0)
        for v in got:
            check = (check * 31 + round(v * 100000.0)) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
