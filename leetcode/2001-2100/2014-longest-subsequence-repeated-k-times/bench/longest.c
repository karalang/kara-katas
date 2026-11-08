// LeetCode #2014: Longest Subsequence Repeated k Times -- the ★ arm's
// benchmark, a mirror of longest.kara. Each candidate is its own heap
// string, as a `String` is; the queue grows by doubling.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int repeats(const char *s, int n, const char *t, int len, int64_t k) {
    int i = 0;
    int64_t found = 0;
    for (int j = 0; j < n; j++) {
        if (s[j] == t[i]) {
            i++;
            if (i == len) {
                found++;
                if (found == k) return 1;
                i = 0;
            }
        }
    }
    return 0;
}

// returns a heap string; the caller frees it
static char *longest_subsequence_repeated_k(const char *s, int n, int64_t k) {
    int64_t counts[26] = {0};
    for (int i = 0; i < n; i++) counts[s[i] - 'a']++;
    char letters[26];
    int nl = 0;
    for (int i = 0; i < 26; i++)
        if (counts[i] >= k) letters[nl++] = (char)('a' + i);
    size_t cap = 16, head = 0, tail = 0;
    char **queue = malloc(cap * sizeof(char *));
    queue[tail++] = calloc(1, 1);
    char *best = calloc(1, 1);
    while (head < tail) {
        char *t = queue[head++];
        int len = (int)strlen(t);
        for (int c = 0; c < nl; c++) {
            char *next = malloc(len + 2);
            memcpy(next, t, len);
            next[len] = letters[c];
            next[len + 1] = 0;
            if (repeats(s, n, next, len + 1, k)) {
                free(best);
                best = strdup(next);
                if (tail == cap) {
                    cap *= 2;
                    queue = realloc(queue, cap * sizeof(char *));
                }
                queue[tail++] = next;
            } else {
                free(next);
            }
        }
        free(t);
    }
    free(queue);
    return best;
}

static int64_t seed = 2014;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *random_text(int n, int64_t letters) {
    char pattern[8];
    int width = (int)(next_random() % 7 + 1);
    for (int i = 0; i < width; i++) pattern[i] = (char)('a' + next_random() % letters);
    char *text = malloc(n + 1);
    int len = 0, at = 0;
    while (len < n) {
        if (next_random() % 10 < 9) text[len++] = pattern[at];
        if (len < n && next_random() % 10 < 1) text[len++] = (char)('a' + next_random() % letters);
        at = (at + 1) % width;
    }
    text[len] = 0;
    return text;
}

int main(void) {
    char *texts[200];
    int64_t ks[200];
    for (int c = 0; c < 200; c++) {
        ks[c] = 251 + next_random() % 50;
        texts[c] = random_text(2000, c % 8 + 2);
    }
    int64_t calls = 0, total = 0, check = 0;
    for (int r = 0; r < 5; r++) {
        for (int c = 0; c < 200; c++) {
            char *answer = longest_subsequence_repeated_k(texts[c], 2000, ks[c]);
            int64_t len = (int64_t)strlen(answer);
            calls++;
            total += len;
            for (int i = 0; i < len; i++) check = (check * 31 + answer[i]) % 1000000007;
            check = (check * 31 + len) % 1000000007;
            free(answer);
        }
    }
    for (int c = 0; c < 200; c++) free(texts[c]);
    printf("%lld calls: total length %lld, checksum %lld\n", (long long)calls, (long long)total, (long long)check);
    return 0;
}
