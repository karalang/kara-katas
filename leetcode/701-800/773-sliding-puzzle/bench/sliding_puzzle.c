// LeetCode 773 — Sliding Puzzle: benchmark, the ★ arm in C.
// All 720 boards, in dictionary order, built once; ROUNDS rounds each
// solve the next of them. A state is six digit characters; the seen set
// is an open-addressing hash set of them with FNV-1a, and the queue an
// array, since at most 720 states are ever queued.
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define ROUNDS 20000
#define SLOTS 2048

static const int neighbours[6][3] = {{1, 3, -1}, {0, 2, 4}, {1, 5, -1}, {0, 4, -1}, {1, 3, 5}, {2, 4, -1}};

typedef struct {
    char keys[SLOTS][7];
    uint8_t used[SLOTS];
} Set;

static uint32_t hash(const char *s) {
    uint32_t h = 2166136261u;
    for (int i = 0; i < 6; i++) h = (h ^ (unsigned char)s[i]) * 16777619u;
    return h;
}

// Adds s; returns 0 if it was already there.
static int set_add(Set *set, const char *s) {
    uint32_t i = hash(s) & (SLOTS - 1);
    while (set->used[i]) {
        if (memcmp(set->keys[i], s, 6) == 0) return 0;
        i = (i + 1) & (SLOTS - 1);
    }
    set->used[i] = 1;
    memcpy(set->keys[i], s, 7);
    return 1;
}

static Set seen;
static char queue[720][7];
static int64_t steps_of[720];

static int64_t sliding_puzzle(const int64_t board[2][3]) {
    char start[7];
    for (int r = 0; r < 2; r++)
        for (int c = 0; c < 3; c++) start[r * 3 + c] = (char)('0' + board[r][c]);
    start[6] = 0;
    memset(seen.used, 0, sizeof seen.used);
    set_add(&seen, start);
    int head = 0, tail = 0;
    memcpy(queue[tail], start, 7);
    steps_of[tail++] = 0;
    while (head < tail) {
        const char *state = queue[head];
        int64_t steps = steps_of[head++];
        if (memcmp(state, "123450", 6) == 0) return steps;
        int zero = 0;
        while (state[zero] != '0') zero++;
        for (int k = 0; k < 3 && neighbours[zero][k] >= 0; k++) {
            char moved[7];
            memcpy(moved, state, 7);
            moved[zero] = moved[neighbours[zero][k]];
            moved[neighbours[zero][k]] = '0';
            if (set_add(&seen, moved)) {
                memcpy(queue[tail], moved, 7);
                steps_of[tail++] = steps + 1;
            }
        }
    }
    return -1;
}

static int next_order(int64_t *cells, int n) {
    int i = n - 2;
    while (i >= 0 && cells[i] >= cells[i + 1]) i--;
    if (i < 0) return 0;
    int j = n - 1;
    while (cells[j] <= cells[i]) j--;
    int64_t t = cells[i];
    cells[i] = cells[j];
    cells[j] = t;
    for (int lo = i + 1, hi = n - 1; lo < hi; lo++, hi--) {
        t = cells[lo];
        cells[lo] = cells[hi];
        cells[hi] = t;
    }
    return 1;
}

static int64_t boards[720][2][3];

int main(void) {
    int64_t cells[6] = {0, 1, 2, 3, 4, 5};
    int count = 0;
    do {
        for (int k = 0; k < 6; k++) boards[count][k / 3][k % 3] = cells[k];
        count++;
    } while (next_order(cells, 6));
    int64_t solved = 0, check = 0;
    for (int64_t round = 0; round < ROUNDS; round++) {
        int64_t answer = sliding_puzzle((const int64_t(*)[3])boards[round % 720]);
        if (answer >= 0) solved++;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("%d boards: %lld solvable, checksum %lld\n", ROUNDS, (long long)solved, (long long)check);
    return 0;
}
