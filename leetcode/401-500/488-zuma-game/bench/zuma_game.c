// Benchmark for #488: C mirror of the ★ arm (breadth first); see
// zuma_game.kara. C has no hash set, so the seen states are an
// open-addressing table written out here, keyed by the state string.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define KEY 32 // a board of at most 21 balls, '|', a hand of at most 5

typedef struct {
    char *keys; // capacity * KEY bytes; an empty slot starts with 0
    long long capacity, size;
} Seen;

static unsigned long long hash(const char *s) {
    unsigned long long h = 1469598103934665603ULL;
    for (; *s; s++) {
        h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    }
    return h;
}

static void seen_init(Seen *t, long long capacity) {
    t->capacity = capacity;
    t->size = 0;
    t->keys = calloc(capacity, KEY);
}

// Adds the key; returns 1 when it was not there before.
static int seen_insert(Seen *t, const char *key) {
    if (2 * (t->size + 1) > t->capacity) {
        Seen bigger;
        seen_init(&bigger, t->capacity * 2);
        for (long long k = 0; k < t->capacity; k++) {
            if (t->keys[k * KEY]) {
                seen_insert(&bigger, t->keys + k * KEY);
            }
        }
        free(t->keys);
        *t = bigger;
    }
    long long mask = t->capacity - 1, at = hash(key) & mask;
    while (t->keys[at * KEY]) {
        if (strcmp(t->keys + at * KEY, key) == 0) {
            return 0;
        }
        at = (at + 1) & mask;
    }
    strcpy(t->keys + at * KEY, key);
    t->size++;
    return 1;
}

// Removes every run of three or more, again and again; returns the length.
static int shrink(char *b, int n) {
    for (;;) {
        char kept[KEY];
        int m = 0, removed = 0, i = 0;
        while (i < n) {
            int j = i;
            while (j < n && b[j] == b[i]) {
                j++;
            }
            if (j - i >= 3) {
                removed = 1;
            } else {
                for (int k = i; k < j; k++) {
                    kept[m++] = b[k];
                }
            }
            i = j;
        }
        memcpy(b, kept, m);
        n = m;
        if (!removed) {
            return n;
        }
    }
}

typedef struct {
    char board[KEY], hand[8];
    int n, h;
} State;

static int cmp_char(const void *a, const void *b) {
    return *(const char *)a - *(const char *)b;
}

static long long find_min_step(const char *board, const char *hand) {
    long long cap = 1024, count = 0;
    State *level = malloc(sizeof(State) * cap);
    State first;
    first.n = strlen(board);
    memcpy(first.board, board, first.n);
    first.h = strlen(hand);
    memcpy(first.hand, hand, first.h);
    qsort(first.hand, first.h, 1, cmp_char);
    level[count++] = first;
    Seen seen;
    seen_init(&seen, 1024);
    long long steps = 0, result = -1;
    while (count > 0 && result < 0) {
        steps++;
        long long next_cap = 1024, next_count = 0;
        State *next = malloc(sizeof(State) * next_cap);
        for (long long s = 0; s < count && result < 0; s++) {
            State *st = &level[s];
            for (int t = 0; t < st->h && result < 0; t++) {
                char c = st->hand[t];
                if (t > 0 && st->hand[t - 1] == c) {
                    continue;
                }
                for (int i = 0; i <= st->n; i++) {
                    char *b = st->board;
                    int starts_run = i < st->n && b[i] == c && (i == 0 || b[i - 1] != c);
                    int splits_pair = i > 0 && i < st->n && b[i - 1] == b[i] && b[i] != c;
                    if (!starts_run && !splits_pair) {
                        continue;
                    }
                    State after;
                    memcpy(after.board, b, i);
                    after.board[i] = c;
                    memcpy(after.board + i + 1, b + i, st->n - i);
                    after.n = shrink(after.board, st->n + 1);
                    if (after.n == 0) {
                        result = steps;
                        break;
                    }
                    after.h = 0;
                    for (int k = 0; k < st->h; k++) {
                        if (k != t) {
                            after.hand[after.h++] = st->hand[k];
                        }
                    }
                    char key[KEY];
                    memcpy(key, after.board, after.n);
                    key[after.n] = '|';
                    memcpy(key + after.n + 1, after.hand, after.h);
                    key[after.n + 1 + after.h] = 0;
                    if (seen_insert(&seen, key)) {
                        if (next_count == next_cap) {
                            next_cap *= 2;
                            next = realloc(next, sizeof(State) * next_cap);
                        }
                        next[next_count++] = after;
                    }
                }
            }
        }
        free(level);
        level = next;
        count = next_count;
    }
    free(level);
    free(seen.keys);
    return result;
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const char colours[] = "RYBGW";
    char boards[60][17], hands[60][6];
    long long seed = 488;
    for (int c = 0; c < 60; c++) {
        long long palette = 2 + c % 3;
        int n = 0;
        while (n < 16) {
            char ball = colours[next_random(&seed) % palette];
            if (n >= 2 && boards[c][n - 1] == ball && boards[c][n - 2] == ball) {
                continue;
            }
            boards[c][n++] = ball;
        }
        boards[c][16] = 0;
        for (int k = 0; k < 5; k++) {
            hands[c][k] = colours[next_random(&seed) % palette];
        }
        hands[c][5] = 0;
    }
    long long cleared = 0, total = 0, checksum = 0;
    for (int c = 0; c < 60; c++) {
        long long steps = find_min_step(boards[c], hands[c]);
        if (steps >= 0) {
            cleared++;
            total += steps;
        }
        checksum = (checksum * 31 + steps + 2) % 1000000007;
    }
    printf("60 cases of 16 balls and a hand of 5: %lld cleared with %lld balls, checksum %lld\n", cleared, total, checksum);
    return 0;
}
