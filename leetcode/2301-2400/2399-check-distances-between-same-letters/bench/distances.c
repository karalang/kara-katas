// LeetCode #2399: Check Distances Between Same Letters -- the bench, the
// ★ arm in C: the first index of each letter, checked at its second.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2399;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int check_distances(const char *s, int64_t n, const int64_t *distance) {
    int64_t first[26];
    for (int c = 0; c < 26; c++) first[c] = -1;
    for (int64_t i = 0; i < n; i++) {
        int64_t c = s[i] - 'a';
        if (first[c] < 0) {
            first[c] = i;
        } else if (i - first[c] - 1 != distance[c]) {
            return 0;
        }
    }
    return 1;
}

// All 26 letters, each twice, shuffled, and the distances true of it;
// when `off`, one letter's distance is one away from its true one.
static void make_case(char *b, int64_t *distance, int off) {
    for (int64_t i = 0; i < 52; i++) b[i] = (char)('a' + i / 2);
    for (int64_t i = 1; i < 52; i++) {
        int64_t j = next_random() % (i + 1);
        char x = b[i];
        b[i] = b[j];
        b[j] = x;
    }
    int64_t first[26];
    for (int c = 0; c < 26; c++) {
        first[c] = -1;
        distance[c] = 0;
    }
    for (int64_t i = 0; i < 52; i++) {
        int64_t c = b[i] - 'a';
        if (first[c] < 0) first[c] = i;
        else distance[c] = i - first[c] - 1;
    }
    if (off) {
        int64_t letter = next_random() % 26;
        distance[letter] += distance[letter] == 0 ? 1 : -1;
    }
}

int main(void) {
    static char strings[1000][52];
    static int64_t distances[1000][26];
    for (int i = 0; i < 1000; i++) make_case(strings[i], distances[i], i % 2 == 1);
    int64_t check = 0, yes = 0;
    for (int64_t p = 0; p < 2000; p++) {
        for (int i = 0; i < 1000; i++) {
            int answer = check_distances(strings[i], 52, distances[i]);
            if (answer) yes++;
            check = (check * 31 + (answer ? 2 : 1) + p) % 1000000007;
        }
    }
    printf("2000 passes over 1000 strings of 52 letters: checksum %lld, %lld yes\n", (long long)check, (long long)yes);
    return 0;
}
