// Benchmark for #422: mirror of valid_word_square.kara (every cell
// against its mirror). A flip rebuilds the row, as the Kāra program does.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int valid_word_square(char **words, const int64_t *lens, int64_t n) {
    for (int64_t i = 0; i < n; i++) {
        const char *row = words[i];
        for (int64_t j = 0; j < lens[i]; j++) {
            if (j >= n) return 0;
            if (i >= lens[j] || words[j][i] != row[j]) return 0;
        }
    }
    return 1;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static void flip(char **words, const int64_t *lens, int64_t i, int64_t j) {
    char *word = malloc(lens[i]);
    for (int64_t k = 0; k < lens[i]; k++) {
        word[k] = k == j ? (char)(195 - words[i][k]) : words[i][k];
    }
    free(words[i]);
    words[i] = word;
}

int main(int argc, char **argv) {
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 6000;
    int64_t n = 500, seed = 422;
    int64_t *grid = malloc(n * n * sizeof *grid);
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = i; j < n; j++) {
            int64_t c = step(&seed) % 2;
            grid[i * n + j] = c;
            grid[j * n + i] = c;
        }
    }
    int64_t *lengths = malloc(n * sizeof *lengths);
    lengths[0] = n;
    for (int64_t i = 1; i < n; i++) {
        int64_t drop = step(&seed) % 4 == 0 ? 1 : 0;
        int64_t l = lengths[i - 1] - drop;
        lengths[i] = l > 1 ? l : 1;
    }
    char **words = malloc(n * sizeof *words);
    int64_t *lens = malloc(n * sizeof *lens);
    int64_t cells = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t height = 0;
        while (height < n && lengths[height] > i) height++;
        lens[i] = lengths[i] < height ? lengths[i] : height;
        words[i] = malloc(lens[i]);
        for (int64_t j = 0; j < lens[i]; j++) words[i][j] = (char)(97 + grid[i * n + j]);
        cells += lens[i];
    }
    int64_t valid = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t i = step(&seed) % n;
        int64_t j = step(&seed) % lens[i];
        flip(words, lens, i, j);
        if (r % 3 != 0) flip(words, lens, j, i);
        int answer = valid_word_square(words, lens, n);
        if (answer) valid++;
        checksum = (checksum * 31 + (answer ? r + 1 : 0)) % 1000000007;
        if (r % 3 == 0) flip(words, lens, i, j);
    }
    printf("%lld rounds on %lld words, %lld letters: %lld valid, checksum %lld\n", (long long)rounds, (long long)n, (long long)cells, (long long)valid, (long long)checksum);
    return 0;
}
