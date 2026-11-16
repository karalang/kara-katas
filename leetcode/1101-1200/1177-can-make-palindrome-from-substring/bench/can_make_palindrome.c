// LeetCode #1177: Can Make Palindrome from Substring -- the ★ arm's bench
// in C: the parity masks of every prefix in a malloc'd array, each query's
// odd letters counted with __builtin_popcountll on two masks XORed, the
// answers in a malloc'd array of bools. The same string, the same queries
// (each its own malloc'd three values) and the same 200 calls.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool *can_make_pali_queries(const char *s, int64_t n, int64_t **queries, int64_t q) {
    int64_t *masks = malloc(sizeof(int64_t) * (n + 1));
    masks[0] = 0;
    for (int64_t i = 0; i < n; i++) masks[i + 1] = masks[i] ^ (1LL << (s[i] - 'a'));
    bool *answer = malloc(q);
    for (int64_t i = 0; i < q; i++) {
        int64_t *t = queries[i];
        answer[i] = __builtin_popcountll(masks[t[1] + 1] ^ masks[t[0]]) / 2 <= t[2];
    }
    free(masks);
    return answer;
}

static int64_t seed = 1177;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t n = 100000, q = 100000;
    char *s = malloc(n + 1);
    for (int64_t i = 0; i < n; i++) s[i] = (char)('a' + next_random() % 26);
    s[n] = 0;
    int64_t **queries = malloc(sizeof(int64_t *) * q);
    for (int64_t i = 0; i < q; i++) {
        int64_t a = next_random() % 100000;
        int64_t b = next_random() % 100000;
        queries[i] = malloc(sizeof(int64_t) * 3);
        queries[i][0] = a < b ? a : b;
        queries[i][1] = a < b ? b : a;
        queries[i][2] = next_random() % 14;
    }
    int calls = 200;
    int64_t check = 0;
    for (int c = 0; c < calls; c++) {
        bool *answer = can_make_pali_queries(s, n, queries, q);
        for (int64_t i = 0; i < q; i++) check = (check * 3 + (answer[i] ? 2 : 1)) % 1000000007;
        free(answer);
    }
    printf("%d calls: checksum %lld\n", calls, (long long)check);
    for (int64_t i = 0; i < q; i++) free(queries[i]);
    free(queries);
    free(s);
    return 0;
}
