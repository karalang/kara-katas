// LeetCode #2430: Maximum Deletions on a String -- the bench, the ★ arm:
// the longest common prefix of the suffixes at `i` and `k` kept in two
// rows, each row from the one after it, and `best[i]` the most
// operations that clear the suffix from `i`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t delete_string(const unsigned char *b, int64_t n) {
    int64_t *next_row = calloc(n + 1, sizeof(int64_t));
    int64_t *row = calloc(n + 1, sizeof(int64_t));
    int64_t *best = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = n - 1; i >= 0; i--) {
        for (int64_t k = i + 1; k < n; k++)
            row[k] = b[i] == b[k] ? next_row[k + 1] + 1 : 0;
        best[i] = 1;
        for (int64_t j = 1; j < (n - i) / 2 + 1; j++)
            if (row[i + j] >= j && best[i + j] + 1 > best[i])
                best[i] = best[i + j] + 1;
        int64_t *done = next_row;
        next_row = row;
        row = done;
    }
    int64_t answer = best[0];
    free(next_row);
    free(row);
    free(best);
    return answer;
}

static int64_t seed = 2430;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 4000;
    unsigned char *words[8];
    for (int w = 0; w < 8; w++) {
        words[w] = malloc(n);
        for (int64_t i = 0; i < n; i++) {
            int64_t back = 1 + next_random() % 3;
            if (i >= back && next_random() % 2 == 0)
                words[w][i] = words[w][i - back];
            else
                words[w][i] = 'a' + next_random() % 2;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 6; p++)
        for (int64_t w = 0; w < 8; w++) {
            words[w][(p * 997 + w * 131) % n] = 'a' + p % 2;
            check = (check * 31 + delete_string(words[w], n) + p) % 1000000007;
        }
    printf("6 passes over 8 words of 4000 letters: checksum %lld\n", (long long)check);
    for (int w = 0; w < 8; w++) free(words[w]);
    return 0;
}
