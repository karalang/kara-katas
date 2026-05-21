# LeetCode #65: Valid Number — Python mirror of valid.kara.
#
# 8-state DFA over the byte stream. Categorize each byte into one of
# {digit, sign, dot, exp, other}, dispatch on (state, category) → next
# state, reject on any unhandled transition. At end-of-input the string
# is valid iff the final state is an accepting state.

DIGIT = 0
SIGN  = 1
DOT   = 2
EXP   = 3
OTHER = 4


def categorize(c: str) -> int:
    if '0' <= c <= '9':
        return DIGIT
    if c == '+' or c == '-':
        return SIGN
    if c == '.':
        return DOT
    if c == 'e' or c == 'E':
        return EXP
    return OTHER


# State legend (accepting states marked *):
#   0: start
#   1: sign seen, awaiting integer-or-dot
#   2: integer digits accumulated                          (*)
#   3: dot with no preceding digit, awaiting fractional
#   4: dot with preceding digit                            (*)
#   5: fractional digits                                   (*)
#   6: 'e'/'E' seen, awaiting optional sign + exponent integer
#   7: sign after 'e', awaiting exponent integer
#   8: exponent digits                                     (*)
def is_number(s: str) -> bool:
    state = 0
    for c in s:
        cat = categorize(c)
        if state == 0:
            if   cat == DIGIT: state = 2
            elif cat == SIGN:  state = 1
            elif cat == DOT:   state = 3
            else: return False
        elif state == 1:
            if   cat == DIGIT: state = 2
            elif cat == DOT:   state = 3
            else: return False
        elif state == 2:
            if   cat == DIGIT: state = 2
            elif cat == DOT:   state = 4
            elif cat == EXP:   state = 6
            else: return False
        elif state == 3:
            if   cat == DIGIT: state = 5
            else: return False
        elif state == 4:
            if   cat == DIGIT: state = 5
            elif cat == EXP:   state = 6
            else: return False
        elif state == 5:
            if   cat == DIGIT: state = 5
            elif cat == EXP:   state = 6
            else: return False
        elif state == 6:
            if   cat == DIGIT: state = 8
            elif cat == SIGN:  state = 7
            else: return False
        elif state == 7:
            if   cat == DIGIT: state = 8
            else: return False
        elif state == 8:
            if   cat == DIGIT: state = 8
            else: return False
        else:
            return False
    return state == 2 or state == 4 or state == 5 or state == 8


def report(s: str) -> None:
    print(f'is_number "{s}": {str(is_number(s)).lower()}')


def main() -> None:
    # Valid cases from the LeetCode spec.
    report("0")
    report("2")
    report("0089")
    report("-0.1")
    report("+3.14")
    report("4.")
    report("-.9")
    report("2e10")
    report("-90E3")
    report("3e+7")
    report("+6e-1")
    report("53.5e93")
    report("-123.456e789")

    # Invalid cases from the LeetCode spec.
    report("abc")
    report("1a")
    report("1e")
    report("e3")
    report("99e2.5")
    report("--6")
    report("-+3")
    report("95a54e53")

    # Edge cases worth exercising — empty fractional with no integer,
    # bare sign / dot, sign-after-sign, exponent without int.
    report(".")
    report(".e1")
    report("+.")
    report("+")
    report("4e+")
    report("6+1")
    report(" 1")
    report("1 ")


if __name__ == "__main__":
    main()
