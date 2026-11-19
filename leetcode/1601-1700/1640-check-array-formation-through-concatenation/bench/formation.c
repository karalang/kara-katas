// LeetCode #1640: Check Array Formation Through Concatenation -- the
// bench's C mirror: the ★ arm on 50000 random cases of the values 1 to 100
// in a random order, cut into pieces of 1 to 3 and shuffled, every third
// one with two values swapped, all drawn first, with an open-addressing
// hash map written out for each piece's first value.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { CASES = 50000, N = 100, CAP = 256 };

typedef struct {
    int32_t *values;
    size_t len;
} Piece;

typedef struct {
    int32_t arr[N];
    Piece pieces[N];
    size_t count;
} Case;

typedef struct {
    int32_t keys[CAP];
    int64_t values[CAP];
    char used[CAP];
} Map;

static size_t slot(const Map *m, int32_t key) {
    uint64_t h = (uint64_t)(int64_t)key * 0x9E3779B97F4A7C15ull;
    size_t i = (size_t)(h >> 32) & (CAP - 1);
    while (m->used[i] && m->keys[i] != key) i = (i + 1) & (CAP - 1);
    return i;
}

static int can_form_array(const int32_t *arr, size_t n, const Piece *pieces, size_t count) {
    Map *starting = calloc(1, sizeof(Map));
    for (size_t k = 0; k < count; k++) {
        size_t s = slot(starting, pieces[k].values[0]);
        starting->used[s] = 1;
        starting->keys[s] = pieces[k].values[0];
        starting->values[s] = (int64_t)k;
    }
    size_t i = 0;
    int formed = 1;
    while (i < n && formed) {
        size_t s = slot(starting, arr[i]);
        if (!starting->used[s]) {
            formed = 0;
            break;
        }
        const Piece *p = &pieces[starting->values[s]];
        for (size_t v = 0; v < p->len; v++) {
            if (i >= n || arr[i] != p->values[v]) {
                formed = 0;
                break;
            }
            i++;
        }
    }
    free(starting);
    return formed;
}

static int64_t seed = 1640;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    Case *cases = malloc(sizeof(Case) * CASES);
    for (int c = 0; c < CASES; c++) {
        Case *tc = &cases[c];
        for (int i = 0; i < N; i++) tc->arr[i] = i + 1;
        for (int k = N - 1; k >= 1; k--) {
            int64_t j = next_random() % (k + 1);
            int32_t t = tc->arr[k];
            tc->arr[k] = tc->arr[j];
            tc->arr[j] = t;
        }
        tc->count = 0;
        size_t start = 0;
        while (start < N) {
            size_t end = start + (size_t)(next_random() % 3 + 1);
            if (end > N) end = N;
            Piece p = {malloc(sizeof(int32_t) * (end - start)), end - start};
            memcpy(p.values, tc->arr + start, sizeof(int32_t) * (end - start));
            tc->pieces[tc->count++] = p;
            start = end;
        }
        for (size_t k = tc->count - 1; k >= 1; k--) {
            int64_t j = next_random() % (int64_t)(k + 1);
            Piece t = tc->pieces[k];
            tc->pieces[k] = tc->pieces[j];
            tc->pieces[j] = t;
        }
        if (c % 3 == 2) {
            int64_t a = next_random() % 100, b = next_random() % 100;
            int32_t t = tc->arr[a];
            tc->arr[a] = tc->arr[b];
            tc->arr[b] = t;
        }
    }
    int64_t check = 0;
    int trues = 0;
    for (int c = 0; c < CASES; c++) {
        int formed = can_form_array(cases[c].arr, N, cases[c].pieces, cases[c].count);
        if (formed) trues++;
        check = (check * 31 + (formed ? 2 : 1)) % 1000000007;
    }
    for (int c = 0; c < CASES; c++)
        for (size_t k = 0; k < cases[c].count; k++) free(cases[c].pieces[k].values);
    free(cases);
    printf("50000 cases of 100 values: %d can be formed, checksum %lld\n", trues, (long long)check);
    return 0;
}
