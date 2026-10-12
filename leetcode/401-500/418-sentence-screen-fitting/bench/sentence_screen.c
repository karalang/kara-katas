// LeetCode #418: Sentence Screen Fitting -- C mirror of
// sentence_screen.kara (one pointer into the text). Each call joins the
// sentence into a fresh buffer, as the Kāra program does.
// Usage: ./sentence_screen [calls]
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t words_typing(char **sentence, int64_t n, int64_t rows, int64_t cols) {
    int64_t length = 0;
    for (int64_t i = 0; i < n; i++) {
        length += (int64_t)strlen(sentence[i]) + 1;
    }
    char *text = malloc(length);
    int64_t k = 0;
    for (int64_t i = 0; i < n; i++) {
        size_t w = strlen(sentence[i]);
        memcpy(text + k, sentence[i], w);
        k += w;
        text[k++] = ' ';
    }
    int64_t at = 0;
    for (int64_t r = 0; r < rows; r++) {
        at += cols;
        if (text[at % length] == ' ') {
            at += 1;
        } else {
            while (at > 0 && text[(at - 1) % length] != ' ') {
                at -= 1;
            }
        }
    }
    free(text);
    return at / length;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t calls = argc > 1 ? atoll(argv[1]) : 10000;
    int64_t seed = 418;
    char *pool[200];
    for (int i = 0; i < 200; i++) {
        int64_t length = 1 + step(&seed) % 10;
        pool[i] = malloc(length + 1);
        for (int64_t j = 0; j < length; j++) {
            pool[i][j] = (char)(97 + step(&seed) % 26);
        }
        pool[i][length] = '\0';
    }
    int64_t total = 0, checksum = 0;
    char *sentence[100];
    for (int64_t c = 0; c < calls; c++) {
        int64_t n = 1 + step(&seed) % 100;
        for (int64_t i = 0; i < n; i++) {
            sentence[i] = strdup(pool[step(&seed) % 200]);
        }
        int64_t rows = 1 + step(&seed) % 20000;
        int64_t cols = 10 + step(&seed) % 19991;
        int64_t answer = words_typing(sentence, n, rows, cols);
        for (int64_t i = 0; i < n; i++) {
            free(sentence[i]);
        }
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    printf("%lld calls: total %lld, checksum %lld\n", (long long)calls, (long long)total, (long long)checksum);
    for (int i = 0; i < 200; i++) {
        free(pool[i]);
    }
    return 0;
}
