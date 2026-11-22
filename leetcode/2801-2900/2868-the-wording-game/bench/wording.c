// LeetCode #2868: The Wording Game -- the bench, as wording.kara: 20
// deals of 10^5 words, each played 20 times by the table arm. Words are
// NUL-terminated strings compared by strcmp, and the tables are built
// on each call.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char **words;
    int64_t len;
} hand;

static void table(hand h, int64_t *top) {
    for (int i = 0; i < 26; i++) top[i] = -1;
    for (int64_t i = 0; i < h.len; i++) top[h.words[i][0] - 'a'] = i;
}

static bool can_alice_win(hand a, hand b) {
    const char *last = a.words[0];
    int64_t tops[2][26];
    table(a, tops[0]);
    table(b, tops[1]);
    hand hands[2] = {a, b};
    int turn = 1;
    for (;;) {
        int c = last[0] - 'a';
        int64_t same = tops[turn][c];
        if (same >= 0 && strcmp(hands[turn].words[same], last) > 0) {
            last = hands[turn].words[same];
        } else if (c < 25 && tops[turn][c + 1] >= 0) {
            last = hands[turn].words[tops[turn][c + 1]];
        } else {
            return turn == 1;
        }
        turn = 1 - turn;
    }
}

static int64_t seed = 2868;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int by_text(const void *x, const void *y) { return strcmp(*(char *const *)x, *(char *const *)y); }

static void deal(int64_t n, int64_t letters, int64_t longest, hand *a, hand *b) {
    char **words = malloc(n * sizeof *words);
    for (int64_t i = 0; i < n; i++) {
        int64_t len = next_random() % longest + 1;
        words[i] = malloc(len + 1);
        for (int64_t k = 0; k < len; k++) words[i][k] = 'a' + next_random() % letters;
        words[i][len] = 0;
    }
    qsort(words, n, sizeof *words, by_text);
    int64_t m = 0;
    for (int64_t i = 0; i < n; i++) {
        if (m > 0 && strcmp(words[m - 1], words[i]) == 0) {
            free(words[i]);
        } else {
            words[m++] = words[i];
        }
    }
    a->words = malloc(m * sizeof *words);
    b->words = malloc(m * sizeof *words);
    a->len = b->len = 0;
    int64_t first = next_random() % m;
    for (int64_t i = 0; i < m; i++) {
        if (i == first || (next_random() % 2 == 0 && i != (first + 1) % m)) {
            a->words[a->len++] = words[i];
        } else {
            b->words[b->len++] = words[i];
        }
    }
    free(words);
}

int main(void) {
    const int64_t count = 20, rounds = 20, n = 100000;
    hand as[20], bs[20];
    for (int64_t c = 0; c < count; c++) deal(n, c % 2 == 0 ? 26 : 5, 8, &as[c], &bs[c]);
    int64_t wins = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            bool win = can_alice_win(as[c], bs[c]);
            wins += win;
            check = (check * 2 + r + (win ? 1 : 0)) % 1000000007;
        }
    }
    printf("%lld deals of %lld words, %lld rounds: Alice wins %lld, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)wins, (long long)check);
    return 0;
}
