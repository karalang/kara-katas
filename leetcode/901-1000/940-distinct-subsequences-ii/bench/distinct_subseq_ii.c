// Benchmark: LeetCode #940 Distinct Subsequences II -- the ★ arm,
// doubling less the repeats, on 100 words of 2000 letters, LeetCode's
// longest, in 200 rounds. Mirrors distinct_subseq_ii.kara, .rs, .py and
// go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t distinct_subseq_ii(const char *s, int n) {
    const int64_t m = 1000000007;
    int64_t *count = malloc(sizeof(int64_t) * (n + 1));
    int64_t last[26] = {0};
    count[0] = 1;
    for (int i = 0; i < n; i++) {
        int c = s[i] - 'a';
        int64_t next = 2 * count[i] % m;
        if (last[c] > 0) next = (next - count[last[c] - 1] + m) % m;
        count[i + 1] = next;
        last[c] = i + 1;
    }
    int64_t answer = (count[n] - 1 + m) % m;
    free(count);
    return answer;
}

static int64_t seed = 940;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char words[100][2001];

int main(void) {
    int rounds = 200, count = 100;
    for (int w = 0; w < count; w++) {
        int64_t k = 1 + next_random() % 26;
        for (int i = 0; i < 2000; i++) words[w][i] = (char)(next_random() % k + 'a');
        words[w][2000] = 0;
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < count; i++) {
            int64_t a = distinct_subseq_ii(words[(r + i) % count], 2000);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    printf("%d rounds over %d words of 2000 letters: counts adding to %lld, checksum %lld\n", rounds, count,
           (long long)total, (long long)check);
    return 0;
}
