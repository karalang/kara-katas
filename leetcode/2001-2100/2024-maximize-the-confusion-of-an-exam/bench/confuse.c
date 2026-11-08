// LeetCode #2024: Maximize the Confusion of an Exam -- the ★ arm in C, the
// same algorithm and workload as confuse.kara: a sliding window for each
// answer, the longer of the two.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t longest_run(const char *key, int64_t n, char c, int64_t k) {
    int64_t best = 0, left = 0, other = 0;
    for (int64_t right = 0; right < n; right++) {
        if (key[right] != c) other++;
        while (other > k) {
            if (key[left] != c) other--;
            left++;
        }
        if (right - left + 1 > best) best = right - left + 1;
    }
    return best;
}

static int64_t max_consecutive_answers(const char *key, int64_t n, int64_t k) {
    int64_t t = longest_run(key, n, 'T', k);
    int64_t f = longest_run(key, n, 'F', k);
    return t > f ? t : f;
}

static int64_t seed = 2024;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t pcts[5] = {50, 70, 90, 97, 99};
    const int64_t kvals[5] = {1, 10, 100, 1000, 10000};
    char *keys[20];
    int64_t ks[20];
    for (int a = 0; a < 20; a++) {
        int64_t pct = pcts[a % 5];
        keys[a] = malloc(100000);
        for (int i = 0; i < 100000; i++) keys[a][i] = next_random() % 100 < pct ? 'T' : 'F';
        ks[a] = kvals[a / 4];
    }
    int64_t calls = 0, total = 0, check = 0;
    for (int round = 0; round < 5; round++) {
        for (int a = 0; a < 20; a++) {
            int64_t best = max_consecutive_answers(keys[a], 100000, ks[a]);
            calls++;
            total += best;
            check = (check * 31 + best) % 1000000007;
        }
    }
    printf("%lld calls: total %lld, checksum %lld\n", (long long)calls, (long long)total, (long long)check);
    return 0;
}
