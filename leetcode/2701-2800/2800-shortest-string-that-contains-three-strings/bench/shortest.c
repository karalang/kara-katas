// LeetCode #2800: Shortest String That Contains Three Strings -- the
// bench in C: the ★ arm over 2000 triples of up to 100 letters from a and
// b, all drawn first, then each answered 200 times.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define COUNT 2000

static int64_t seed = 2800;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void word(char *w, int64_t m) {
    for (int64_t i = 0; i < m; i++) w[i] = "ab"[next_random() % 2];
    w[m] = 0;
}

// s merged with t into out (out may not alias either)
static void merge(const char *s, const char *t, char *out) {
    size_t n = strlen(s), m = strlen(t);
    memcpy(out, s, n + 1);
    if (strstr(s, t)) return;
    size_t k = m < n ? m : n;
    for (; k > 0; k--) {
        if (memcmp(s + n - k, t, k) == 0) break;
    }
    memcpy(out + n, t + k, m - k + 1);
}

static void minimum_string(const char *a, const char *b, const char *c, char *best) {
    const char *words[3] = {a, b, c};
    static const int orders[6][3] = {{0, 1, 2}, {0, 2, 1}, {1, 0, 2}, {1, 2, 0}, {2, 0, 1}, {2, 1, 0}};
    char mid[208], s[312];
    best[0] = 0;
    size_t bl = 0;
    for (int o = 0; o < 6; o++) {
        merge(words[orders[o][0]], words[orders[o][1]], mid);
        merge(mid, words[orders[o][2]], s);
        size_t sl = strlen(s);
        if (bl == 0 || sl < bl || (sl == bl && strcmp(s, best) < 0)) {
            memcpy(best, s, sl + 1);
            bl = sl;
        }
    }
}

static int64_t digest(const char *s) {
    int64_t h = 0;
    for (; *s; s++) h = (h * 131 + (unsigned char)*s) % 1000000007;
    return h;
}

static char words_[COUNT][3][104];

int main(void) {
    int rounds = 200;
    for (int c = 0; c < COUNT; c++)
        for (int i = 0; i < 3; i++) word(words_[c][i], next_random() % 100 + 1);
    char best[312];
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            minimum_string(words_[c][0], words_[c][1], words_[c][2], best);
            total += strlen(best);
            check = (check * 31 + digest(best) + r) % 1000000007;
        }
    }
    printf("%d triples of up to 100, %d rounds: lengths sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
