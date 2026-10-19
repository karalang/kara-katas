// LeetCode 796 — Rotate String: the bench, in C. Mirrors
// rotate_string.kara: goal is a rotation when it is as long as s and in
// s written twice, made fresh for each call and searched with strstr.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int rotate_string(const char *s, const char *goal) {
    size_t n = strlen(s);
    if (strlen(goal) != n) return 0;
    char *twice = malloc(2 * n + 1);
    memcpy(twice, s, n);
    memcpy(twice + n, s, n);
    twice[2 * n] = 0;
    int found = strstr(twice, goal) != NULL;
    free(twice);
    return found;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 796;
    static char ss[4096][101], goals[4096][101];
    for (int p = 0; p < 4096; p++) {
        int64_t letters = 1 + next_random(&seed) % 4;
        for (int i = 0; i < 100; i++) ss[p][i] = (char)(97 + next_random(&seed) % letters);
        ss[p][100] = 0;
        int64_t kind = next_random(&seed) % 3;
        if (kind == 2) {
            for (int i = 0; i < 100; i++) goals[p][i] = (char)(97 + next_random(&seed) % letters);
        } else {
            int64_t k = next_random(&seed) % 100;
            int64_t change = kind == 1 ? next_random(&seed) % 100 : -1;
            for (int j = 0; j < 100; j++) {
                char c = ss[p][(j + k) % 100];
                goals[p][j] = j == change ? (char)(97 + (c - 97 + 1) % letters) : c;
            }
        }
        goals[p][100] = 0;
    }
    int64_t rounds = 1500000, rotations = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        if (rotate_string(ss[r % 4096], goals[r % 4096])) {
            rotations++;
            check = (check * 131 + r % 4096) % 1000000007;
        }
    }
    printf("%lld pairs: %lld rotations, checksum %lld\n", (long long)rounds, (long long)rotations, (long long)check);
    return 0;
}
