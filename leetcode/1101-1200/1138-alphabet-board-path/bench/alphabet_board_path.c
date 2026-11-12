// LeetCode #1138: Alphabet Board Path -- the bench, the ★ arm's algorithm:
// coordinates, up and left first, down and right after.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char *p;
    int64_t len, cap;
} Str;

static void push_run(Str *s, char c, int64_t n) {
    if (n <= 0) return;
    while (s->len + n > s->cap) {
        s->cap = s->cap ? s->cap * 2 : 16;
        s->p = realloc(s->p, s->cap);
    }
    for (int64_t i = 0; i < n; i++) s->p[s->len++] = c;
}

static int64_t max0(int64_t x) { return x > 0 ? x : 0; }

static Str alphabet_board_path(const char *target, int64_t n) {
    Str path = {0};
    int64_t row = 0, col = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t k = target[i] - 'a';
        int64_t r = k / 5, k_col = k % 5;
        push_run(&path, 'U', max0(row - r));
        push_run(&path, 'L', max0(col - k_col));
        push_run(&path, 'D', max0(r - row));
        push_run(&path, 'R', max0(k_col - col));
        push_run(&path, '!', 1);
        row = r;
        col = k_col;
    }
    return path;
}

static int64_t seed = 1138;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    static char targets[1000][100];
    for (int j = 0; j < 1000; j++)
        for (int i = 0; i < 100; i++) targets[j][i] = letters[next_random() % 26];
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 100; round++) {
        for (int64_t j = 0; j < 1000; j++) {
            targets[j][(round * 37 + j) % 100] = letters[next_random() % 26];
            Str path = alphabet_board_path(targets[j], 100);
            int64_t mid = (unsigned char)path.p[path.len / 2];
            total += path.len;
            check = (check * 31 + path.len * 128 + mid) % 1000000007;
            free(path.p);
        }
    }
    printf("100 rounds over 1000 targets of 100 letters: lengths total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
