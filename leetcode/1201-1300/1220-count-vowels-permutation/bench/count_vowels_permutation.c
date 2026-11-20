// LeetCode #1220 bench, C mirror of the Kāra ★ arm: five running counts,
// the strings of the length so far that end in each vowel, for every n from
// 1 to 8000; checksum of the answers.
#include <stdio.h>
#include <stdint.h>

static int64_t count_vowel_permutation(int64_t n) {
    const int64_t modulus = 1000000007;
    int64_t a = 1, e = 1, i = 1, o = 1, u = 1;
    for (int64_t k = 1; k < n; k++) {
        int64_t na = (e + i + u) % modulus, ne = (a + i) % modulus, ni = (e + o) % modulus, no = i, nu = (i + o) % modulus;
        a = na; e = ne; i = ni; o = no; u = nu;
    }
    return (a + e + i + o + u) % modulus;
}

int main(void) {
    int64_t check = 0;
    for (int64_t n = 1; n <= 8000; n++) {
        check = (check * 131 + count_vowel_permutation(n)) % 1000000007;
    }
    printf("every n from 1 to 8000: checksum %lld\n", (long long)check);
    return 0;
}
