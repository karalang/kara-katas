# LeetCode #420: Strong Password Checker -- mirror of strong_password.kara
# (count the runs by length mod 3).


def strong_password_checker(password):
    n = len(password)
    lower = 1 if any("a" <= ch <= "z" for ch in password) else 0
    upper = 1 if any("A" <= ch <= "Z" for ch in password) else 0
    digit = 1 if any("0" <= ch <= "9" for ch in password) else 0
    missing = 3 - lower - upper - digit
    replace = 0
    zero_mod = 0
    one_mod = 0
    i = 0
    while i < n:
        j = i
        while j < n and password[j] == password[i]:
            j += 1
        run = j - i
        if run >= 3:
            replace += run // 3
            if run % 3 == 0:
                zero_mod += 1
            elif run % 3 == 1:
                one_mod += 1
        i = j
    if n < 6:
        return max(missing, 6 - n)
    if n <= 20:
        return max(missing, replace)
    delete = n - 20
    left = delete
    first = min(left, zero_mod)
    replace -= first
    left -= first
    second = min(left, 2 * one_mod)
    replace -= second // 2
    left -= second
    replace -= min(left // 3, replace)
    return delete + max(missing, replace)


seed = 420


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(password):
    print(f'"{password}": {strong_password_checker(password)}')


show("a")
show("aA1")
show("1337C0d3")
show("aaa")
show("aaaaaa")
show("aaa111")
show("ABABABABABABABABABAB1")
show("aaaaaaaaaaaaaaaaaaaaa")
show("bbaaaaaaaaaaaaaaacccccc")
show("1111111111")
show("aaaabbbbccccddeeddeeddeedd")
show("..................!!!")
pool = "aAbB1."
total = 0
checksum = 0
for _ in range(2000):
    n = 1 + step() % 40
    password = ""
    while len(password) < n:
        pick = pool[step() % 6]
        run = 1 + step() % 6
        for _ in range(run):
            if len(password) < n:
                password += pick
    answer = strong_password_checker(password)
    total += answer
    checksum = (checksum * 31 + answer + n) % 1000000007
print(f"2000 random passwords: total {total}, checksum {checksum}")
