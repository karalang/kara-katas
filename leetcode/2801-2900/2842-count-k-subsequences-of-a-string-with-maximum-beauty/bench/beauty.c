// LeetCode #2842: Count K-Subsequences of a String With Maximum Beauty
// -- the bench, mirrored from beauty.kara: the counts sorted, most
// first, the letters above the k-th all taken and the rest chosen
// among those tied with it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int64_t power(int64_t base, int64_t exp) {
    int64_t result = 1, b = base % MOD, e = exp;
    while (e > 0) {
        if (e % 2 == 1) result = result * b % MOD;
        b = b * b % MOD;
        e /= 2;
    }
    return result;
}

static int64_t choose(int64_t n, int64_t r) {
    int64_t top = 1, bottom = 1;
    for (int64_t i = 0; i < r; i++) {
        top = top * (n - i) % MOD;
        bottom = bottom * (i + 1) % MOD;
    }
    return top * power(bottom, MOD - 2) % MOD;
}

static int desc(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x < y) - (x > y);
}

static int64_t count_k_subsequences_with_max_beauty(const char *s, long n, int64_t k) {
    int64_t count[26] = {0}, freq[26];
    for (long i = 0; i < n; i++) count[s[i] - 'a']++;
    int64_t m = 0;
    for (int c = 0; c < 26; c++)
        if (count[c] > 0) freq[m++] = count[c];
    if (k > m) return 0;
    qsort(freq, m, sizeof(int64_t), desc);
    int64_t last = freq[k - 1], above = 0, tied = 0;
    for (int64_t i = 0; i < m; i++) {
        if (freq[i] > last) above++;
        if (freq[i] == last) tied++;
    }
    int64_t ways = choose(tied, k - above) * power(last, k - above) % MOD;
    for (int64_t i = 0; i < above; i++) ways = ways * freq[i] % MOD;
    return ways;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const long count = 100, n = 200000, rounds = 40;
    int64_t seed = 2842;
    char *texts = malloc(count * n);
    int64_t ks[100];
    for (long c = 0; c < count; c++) {
        int64_t kinds = next_random(&seed) % 24 + 3;
        for (long i = 0; i < n; i++) texts[c * n + i] = (char)(97 + next_random(&seed) % kinds);
        ks[c] = next_random(&seed) % 26 + 1;
    }
    int64_t zero = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (long c = 0; c < count; c++) {
            int64_t ways = count_k_subsequences_with_max_beauty(texts + c * n, n, ks[c]);
            if (ways == 0) zero++;
            check = (check * 31 + ways + r) % 1000000007;
        }
    }
    printf("%ld strings of %ld, %ld rounds: %lld with none, checksum %lld\n", count, n, rounds, (long long)zero, (long long)check);
    free(texts);
    return 0;
}
