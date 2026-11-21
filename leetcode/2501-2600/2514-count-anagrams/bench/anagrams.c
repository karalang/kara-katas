// LeetCode #2514: Count Anagrams -- C mirror of the benchmark
// (anagrams.kara): the same sentences, passes, order and checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int64_t power(int64_t base, int64_t exponent) {
    int64_t result = 1, b = base % MOD, e = exponent;
    while (e > 0) {
        if (e % 2 == 1) result = result * b % MOD;
        b = b * b % MOD;
        e /= 2;
    }
    return result;
}

static int64_t count_anagrams(const char *s, int64_t n) {
    int64_t *factorial = malloc((n + 1) * sizeof(int64_t));
    factorial[0] = 1;
    for (int64_t i = 1; i <= n; i++) factorial[i] = factorial[i - 1] * i % MOD;
    int64_t answer = 1;
    int64_t i = 0;
    for (;;) {
        int64_t counts[26] = {0};
        int64_t begin = i;
        while (i < n && s[i] != ' ') counts[s[i++] - 'a']++;
        answer = answer * factorial[i - begin] % MOD;
        for (int c = 0; c < 26; c++) answer = answer * power(factorial[counts[c]], MOD - 2) % MOD;
        if (i == n) break;
        i++;
    }
    free(factorial);
    return answer;
}

static int64_t seed = 2514;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    char *sentences[20];
    int64_t lengths[20];
    for (int t = 0; t < 20; t++) {
        char *text = malloc(100001);
        int64_t size = 0;
        for (;;) {
            int64_t length = next_random() % 200 + 1;
            if (size + 1 + length > 100000) break;
            if (size > 0) text[size++] = ' ';
            for (int64_t k = 0; k < length; k++) text[size++] = (char)('a' + next_random() % 26);
        }
        sentences[t] = text;
        lengths[t] = size;
    }
    const int64_t passes = 4;
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        int64_t start = check % 20;
        for (int64_t k = 0; k < 20; k++) {
            int64_t j = (start + k) % 20;
            check = (check * 31 + count_anagrams(sentences[j], lengths[j]) + p) % 1000000007;
        }
    }
    printf("%lld passes over 20 sentences of 10^5: checksum %lld\n", (long long)passes, (long long)check);
    for (int t = 0; t < 20; t++) free(sentences[t]);
    return 0;
}
