// LeetCode #2030: Smallest K-Length Subsequence With Occurrences of a
// Letter -- the ★ arm in C, the same algorithm and workload as subseq.kara:
// a fresh stack per call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static unsigned char *smallest_subsequence(const unsigned char *s, int64_t n, int64_t k, unsigned char want,
                                           int64_t repetition, int64_t *len) {
    int64_t remain = 0;
    for (int64_t i = 0; i < n; i++) remain += s[i] == want;
    unsigned char *stack = malloc(n + 1);
    int64_t top = 0, have = 0;
    for (int64_t i = 0; i < n; i++) {
        unsigned char c = s[i];
        while (top > 0 && stack[top - 1] > c && top - 1 + n - i >= k &&
               (stack[top - 1] != want || have - 1 + remain >= repetition)) {
            if (stack[--top] == want) have--;
        }
        if (top < k) {
            if (c == want) {
                stack[top++] = c;
                have++;
            } else if (k - top > repetition - have) {
                stack[top++] = c;
            }
        }
        if (c == want) remain--;
    }
    *len = top;
    return stack;
}

static int64_t seed = 2030;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static unsigned char texts[10][50000];
    for (int64_t a = 0; a < 10; a++) {
        int64_t span = 2 + 3 * a, c = 0;
        for (int i = 0; i < 50000; i++) {
            int64_t r = next_random() % 10;
            if (r < 4) c = (c + 1) % span;
            else if (r < 7) c = next_random() % span;
            texts[a][i] = (unsigned char)(97 + c);
        }
    }
    int64_t calls = 0, kept = 0, check = 0;
    for (int64_t round = 0; round < 20; round++) {
        for (int64_t a = 0; a < 10; a++) {
            int64_t k = (round * 2477 + a * 911) % 50000 + 1;
            unsigned char letter = (unsigned char)(97 + (round + a) % (2 + 3 * a));
            int64_t copies = 0;
            for (int i = 0; i < 50000; i++) copies += texts[a][i] == letter;
            int64_t m = k < copies ? k : copies;
            int64_t repetition = (round * 131 + a * 17) % m + 1;
            int64_t len;
            unsigned char *got = smallest_subsequence(texts[a], 50000, k, letter, repetition, &len);
            calls++;
            kept += len;
            check = (check * 31 + len) % 1000000007;
            check = (check * 31 + got[0] + got[len / 2] + got[len - 1]) % 1000000007;
            free(got);
        }
    }
    printf("%lld calls: %lld letters kept, checksum %lld\n", (long long)calls, (long long)kept, (long long)check);
    return 0;
}
