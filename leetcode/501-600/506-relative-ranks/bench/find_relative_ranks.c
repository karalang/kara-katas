// Benchmark for #506 in C: the ★ arm (the athletes sorted by score); see
// ../find_relative_ranks.kara. qsort on the indices, highest score first
// (the scores are all different, so qsort's instability changes
// nothing), and a malloc'd string for every rank.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const int64_t *key_score;

static int by_score_desc(const void *a, const void *b) {
    int64_t x = key_score[*(const int64_t *)a], y = key_score[*(const int64_t *)b];
    return (x < y) - (x > y);
}

static char **find_relative_ranks(const int64_t *score, int64_t n) {
    int64_t *order = malloc((size_t)n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) order[i] = i;
    key_score = score;
    qsort(order, (size_t)n, sizeof(int64_t), by_score_desc);
    char **answer = malloc((size_t)n * sizeof(char *));
    static const char *medals[3] = {"Gold Medal", "Silver Medal", "Bronze Medal"};
    for (int64_t place = 0; place < n; place++) {
        char buf[24];
        if (place < 3) {
            strcpy(buf, medals[place]);
        } else {
            snprintf(buf, sizeof buf, "%lld", (long long)(place + 1));
        }
        answer[order[place]] = strdup(buf);
    }
    free(order);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 500 lists of 10,000 athletes (the problem's most), all different
    // scores from 0 to 10^6 (the j-th is j * 100 plus less than 100,
    // shuffled), built once. Then each list is ranked once, the length
    // of every rank folded into a checksum.
    const int64_t lists = 500, n = 10000;
    int64_t seed = 506;
    int64_t *all = malloc((size_t)(lists * n) * sizeof(int64_t));
    for (int64_t c = 0; c < lists; c++) {
        int64_t *score = all + c * n;
        for (int64_t j = 0; j < n; j++) score[j] = j * 100 + next_random(&seed) % 100;
        for (int64_t k = n - 1; k > 0; k--) {
            int64_t other = next_random(&seed) % (k + 1);
            int64_t t = score[k];
            score[k] = score[other];
            score[other] = t;
        }
    }
    int64_t letters = 0, checksum = 0;
    for (int64_t c = 0; c < lists; c++) {
        char **ranks = find_relative_ranks(all + c * n, n);
        for (int64_t i = 0; i < n; i++) {
            int64_t len = (int64_t)strlen(ranks[i]);
            letters += len;
            checksum = (checksum * 31 + len) % 1000000007;
            free(ranks[i]);
        }
        free(ranks);
    }
    printf("%lld lists of %lld athletes: %lld characters, checksum %lld\n", (long long)lists,
           (long long)n, (long long)letters, (long long)checksum);
    free(all);
    return 0;
}
