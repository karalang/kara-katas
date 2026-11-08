// LeetCode #2018: Check if Word Can Be Placed In Crossword -- the ★ arm's
// benchmark, a mirror of crossword.kara: the lines built and each run
// collected into its own growable array per call.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
    size_t len, cap;
} Vec;

static void push(Vec *v, char c) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap);
    }
    v->data[v->len++] = c;
}

static bool fits(const Vec *segment, const char *word, size_t k) {
    if (segment->len != k) return false;
    bool forward = true, backward = true;
    for (size_t i = 0; i < k && forward; i++)
        forward = segment->data[i] == ' ' || segment->data[i] == word[i];
    for (size_t i = 0; i < k && backward; i++)
        backward = segment->data[i] == ' ' || segment->data[i] == word[k - 1 - i];
    return forward || backward;
}

static bool place_word_in_crossword(char **board, size_t m, size_t n, const char *word) {
    size_t k = strlen(word);
    size_t count = m + n;
    Vec *lines = calloc(count, sizeof(Vec));
    for (size_t r = 0; r < m; r++)
        for (size_t c = 0; c < n; c++) push(&lines[r], board[r][c]);
    for (size_t c = 0; c < n; c++)
        for (size_t r = 0; r < m; r++) push(&lines[m + c], board[r][c]);
    bool found = false;
    for (size_t l = 0; l < count && !found; l++) {
        Vec *line = &lines[l];
        Vec segment = {0};
        for (size_t i = 0; i < line->len + 1; i++) {
            if (i == line->len || line->data[i] == '#') {
                if (fits(&segment, word, k)) {
                    found = true;
                    break;
                }
                segment.len = 0;
            } else {
                push(&segment, line->data[i]);
            }
        }
        free(segment.data);
    }
    for (size_t l = 0; l < count; l++) free(lines[l].data);
    free(lines);
    return found;
}

static int64_t seed = 2018;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { BOARDS = 120, SIDE = 200 };
    static char *boards[BOARDS][SIDE];
    static char words[BOARDS][32];
    for (int b = 0; b < BOARDS; b++) {
        int64_t walls = b % 2 + 1;
        for (int r = 0; r < SIDE; r++) {
            boards[b][r] = malloc(SIDE);
            for (int c = 0; c < SIDE; c++) {
                if (next_random() % 10 < walls)
                    boards[b][r][c] = '#';
                else if (next_random() % 10 < 4)
                    boards[b][r][c] = (char)('a' + next_random() % 3);
                else
                    boards[b][r][c] = ' ';
            }
        }
        int len = b % 10 + 10;
        for (int i = 0; i < len; i++) words[b][i] = (char)('a' + next_random() % 3);
        words[b][len] = '\0';
    }
    int64_t calls = 0, placed = 0, check = 0;
    for (int round = 0; round < 40; round++) {
        for (int b = 0; b < BOARDS; b++) {
            bool answer = place_word_in_crossword(boards[b], SIDE, SIDE, words[b]);
            calls++;
            if (answer) placed++;
            check = (check * 2 + (answer ? 1 : 0)) % 1000000007;
        }
    }
    printf("%lld calls: %lld placed, checksum %lld\n", (long long)calls, (long long)placed, (long long)check);
    return 0;
}
