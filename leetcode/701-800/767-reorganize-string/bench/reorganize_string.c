// LeetCode 767 — Reorganize String: benchmark, the ★ arm in C.
// Sixty-four random strings of 500 letters, built once; 400,000 rounds
// each reorganize the next of them.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int64_t seed = 767;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// Writes the answer into `out` and returns its length, 0 for none.
static int64_t reorganize_string(const char *s, int64_t n, char *out) {
    int64_t counts[26] = {0};
    for (int64_t i = 0; i < n; i++) counts[s[i] - 'a']++;
    int most = 0;
    for (int k = 1; k < 26; k++)
        if (counts[k] > counts[most]) most = k;
    if (counts[most] > (n + 1) / 2) return 0;
    int64_t place = 0;
    for (int step = 0; step < 27; step++) {
        int k = step == 0 ? most : step - 1;
        if (step > 0 && k == most) continue;
        for (int64_t c = 0; c < counts[k]; c++) {
            if (place >= n) place = 1;
            out[place] = (char)('a' + k);
            place += 2;
        }
    }
    return n;
}

int main(void) {
    int64_t rounds = 400000;
    char pool[64][500];
    for (int p = 0; p < 64; p++) {
        int64_t letters = 1 + next_random() % 26;
        for (int i = 0; i < 500; i++) {
            int64_t k = next_random() % (letters + 1);
            pool[p][i] = (char)('a' + (k == letters ? 0 : k));
        }
    }
    int64_t possible = 0, check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        char *answer = malloc(500);
        int64_t len = reorganize_string(pool[round % 64], 500, answer);
        int64_t letter = 0;
        if (len > 0) {
            possible++;
            letter = answer[round % 500];
        }
        check = (check * 31 + len + letter) % 1000000007;
        free(answer);
    }
    printf("%lld strings of 500 letters: %lld rearranged, checksum %lld\n",
           (long long)rounds, (long long)possible, (long long)check);
    return 0;
}
