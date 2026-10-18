// LeetCode 748 — Shortest Completing Word, bench: the ★ arm (letter
// counts) on a list of 1000 words that keeps changing, against a new
// plate each round. Mirrors shortest_completing_word.kara.
#include <stdint.h>
#include <stdio.h>

#define N 1000

static char words[N][16];
static int64_t lens[N];

static int64_t shortest_completing_word(const char *plate, int64_t plen) {
    int64_t need[26] = {0};
    for (int64_t k = 0; k < plen; k++) {
        char c = plate[k];
        if (c >= 'a' && c <= 'z') need[c - 'a']++;
        else if (c >= 'A' && c <= 'Z') need[c - 'A']++;
    }
    int64_t best = -1;
    for (int64_t i = 0; i < N; i++) {
        if (best != -1 && lens[i] >= lens[best]) continue;
        int64_t have[26] = {0};
        for (int64_t k = 0; k < lens[i]; k++) have[words[i][k] - 'a']++;
        int complete = 1;
        for (int c = 0; c < 26; c++)
            if (have[c] < need[c]) complete = 0;
        if (complete) best = i;
    }
    return best;
}

static int64_t seed = 748;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void random_word(int64_t i) {
    int64_t n = 1 + next_random() % 15;
    for (int64_t k = 0; k < n; k++) words[i][k] = (char)(97 + next_random() % 6);
    lens[i] = n;
}

static int64_t random_plate(char *s) {
    int64_t n = 1 + next_random() % 7;
    for (int64_t k = 0; k < n; k++) {
        int64_t kind = next_random() % 6, code;
        if (kind < 2) code = 97 + next_random() % 6;
        else if (kind < 4) code = 65 + next_random() % 6;
        else if (kind == 4) code = 48 + next_random() % 10;
        else code = 32;
        s[k] = (char)code;
    }
    return n;
}

int main(void) {
    const int64_t rounds = 100000;
    for (int64_t i = 0; i < N; i++) random_word(i);
    int64_t letters = 0, check = 0;
    char plate[8];
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < 5; c++) random_word(next_random() % (N - 1));
        int64_t plen = random_plate(plate);
        int64_t m = 0;
        for (int64_t k = 0; k < plen; k++) {
            char c = plate[k];
            if (c >= 'a' && c <= 'z') words[N - 1][m++] = c;
            else if (c >= 'A' && c <= 'Z') words[N - 1][m++] = (char)(c + 32);
        }
        if (m == 0) words[N - 1][m++] = 'a';
        lens[N - 1] = m;
        int64_t got = shortest_completing_word(plate, plen);
        letters += lens[got];
        for (int64_t k = 0; k < lens[got]; k++) check = (check * 31 + (unsigned char)words[got][k]) % 1000000007;
    }
    printf("%lld plates against 1000 words: answers %lld letters long in all, checksum %lld\n", (long long)rounds, (long long)letters, (long long)check);
    return 0;
}
