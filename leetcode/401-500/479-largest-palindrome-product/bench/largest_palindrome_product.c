// Benchmark for #479: C mirror of the ★ arm (palindromes from the top);
// see largest_palindrome_product.kara.
#include <stdio.h>

static long long largest_palindrome(long long n) {
    if (n == 1) {
        return 9;
    }
    long long upper = 1;
    for (long long i = 0; i < n; i++) {
        upper *= 10;
    }
    long long lower = upper / 10;
    upper -= 1;
    for (long long half = upper; half >= lower; half--) {
        long long palindrome = half, rest = half;
        while (rest > 0) {
            palindrome = palindrome * 10 + rest % 10;
            rest /= 10;
        }
        for (long long factor = upper; factor * factor >= palindrome; factor--) {
            if (palindrome % factor == 0 && palindrome / factor >= lower) {
                return palindrome % 1337;
            }
        }
    }
    return -1;
}

int main(void) {
    int rounds = 10;
    long long total = 0, checksum = 0;
    for (int r = 0; r < rounds; r++) {
        for (long long n = 1; n <= 8; n++) {
            long long got = largest_palindrome(n);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    printf("%d rounds of n = 1 to 8: answers add up to %lld, checksum %lld\n", rounds, total, checksum);
    return 0;
}
