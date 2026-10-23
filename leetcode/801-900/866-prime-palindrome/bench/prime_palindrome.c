// LeetCode #866: Prime Palindrome -- C mirror of the bench program (the
// ★ arm, the odd-length palindromes in order).
#include <stdint.h>
#include <stdio.h>

static int64_t odd_palindrome(int64_t root) {
    int64_t y = root;
    int64_t rest = root / 10;
    while (rest > 0) {
        y = y * 10 + rest % 10;
        rest /= 10;
    }
    return y;
}

static int is_prime(int64_t x) {
    if (x < 2) return 0;
    if (x % 2 == 0) return x == 2;
    for (int64_t d = 3; d * d <= x; d += 2) {
        if (x % d == 0) return 0;
    }
    return 1;
}

static int64_t prime_palindrome(int64_t n) {
    if (n >= 8 && n <= 11) return 11;
    for (int64_t root = 1;; root++) {
        int64_t y = odd_palindrome(root);
        if (y >= n && is_prime(y)) return y;
    }
}

static int64_t seed = 866;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t random_n(void) {
    int64_t digits = 1 + next_random() % 8;
    int64_t low = 1;
    for (int64_t i = 1; i < digits; i++) low *= 10;
    int64_t hi = next_random();
    int64_t lo = next_random();
    return low + (hi * 32768 + lo) % (9 * low);
}

int main(void) {
    int64_t queries = 60000;
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t q = 0; q < queries; q++) {
        int64_t n = random_n();
        int64_t p = prime_palindrome(n);
        total += p;
        check = (check * 31 + p) % 1000000007;
    }
    printf("%lld random n of 1 to 8 digits: answers sum to %lld, checksum %lld\n",
           (long long)queries, (long long)total, (long long)check);
    return 0;
}
