# LeetCode #125: Valid Palindrome — reference oracle.
#
# A string is a valid palindrome if, after lowercasing letters and dropping
# every non-alphanumeric byte, it reads the same forwards and backwards.
#
# Two pointers walk inward from both ends; each skips bytes that fail the
# `isalnum` predicate, then the surviving bytes are compared case-folded:
#   alnum filter  -> is_ascii_alphanumeric
#   case fold     -> 'A'..'Z' + 32
# The closest corpus analog to the lexer's identifier/keyword scan: the same
# `is_alpha` / `is_ascii_digit` byte predicates and ASCII case-fold.


def is_palindrome(s):
    i, j = 0, len(s) - 1
    while i < j:
        while i < j and not s[i].isalnum():
            i += 1
        while i < j and not s[j].isalnum():
            j -= 1
        if i < j:
            if s[i].lower() != s[j].lower():
                return False
            i += 1
            j -= 1
    return True


def report(s):
    print(f'"{s}" -> {"true" if is_palindrome(s) else "false"}')


def main():
    # LeetCode canonical examples.
    report("A man, a plan, a canal: Panama")  # true
    report("race a car")                       # false
    report(" ")                                # true  (empty after filtering)

    # Case folding.
    report("Able was I ere I saw elBA")        # true
    report("No lemon, no melon")               # true

    # Digits participate.
    report("0P")                               # false (0 vs p)
    report("a1b2b1a")                          # true
    report("1a2")                              # false

    # Punctuation-only / single char / empty.
    report(".,")                               # true
    report("a")                                # true
    report("")                                 # true
    report("aa")                               # true
    report("ab")                               # false

    # Mixed punctuation between alnum.
    report("Madam, I'm Adam")                  # true
    report("Was it a car or a cat I saw?")     # true
    report("Mr. Owl ate my metal worm")        # true


if __name__ == "__main__":
    main()
