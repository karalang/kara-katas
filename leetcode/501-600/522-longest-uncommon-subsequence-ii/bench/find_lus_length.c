// Benchmark for #522: C mirror of the ★ arm (longest first); see
// find_lus_length.kara. As the ★ arm collects the shorter word's letters
// into a fresh vector on every test, so does this; the order of the
// words is a fresh array sorted stably by length, longest first.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *text;
    int64_t len;
} Word;

static bool is_subsequence(const Word *small, const Word *big) {
    char *s = malloc((size_t)small->len + 1);
    memcpy(s, small->text, (size_t)small->len);
    int64_t i = 0;
    for (int64_t k = 0; k < big->len; k++)
        if (i < small->len && s[i] == big->text[k]) i++;
    free(s);
    return i == small->len;
}

static int64_t find_lus_length(const Word *strs, int64_t n) {
    int64_t *order = malloc(n * sizeof(int64_t));
    // A stable insertion sort, longest first.
    for (int64_t k = 0; k < n; k++) {
        int64_t at = k;
        while (at > 0 && strs[order[at - 1]].len < strs[k].len) {
            order[at] = order[at - 1];
            at--;
        }
        order[at] = k;
    }
    int64_t answer = -1;
    for (int64_t x = 0; x < n && answer < 0; x++) {
        int64_t i = order[x];
        bool uncommon = true;
        for (int64_t j = 0; j < n; j++)
            if (j != i && is_subsequence(&strs[i], &strs[j])) {
                uncommon = false;
                break;
            }
        if (uncommon) answer = strs[i].len;
    }
    free(order);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 2,000 random lists of 50 words of 1 to 10 letters from 1 to 3
    // letters, one word in three a copy of an earlier one, made once;
    // then every list solved in each of 100 rounds.
    int64_t seed = 522, n_lists = 2000;
    Word *lists = malloc(n_lists * 50 * sizeof(Word));
    for (int64_t l = 0; l < n_lists; l++) {
        Word *strs = &lists[l * 50];
        int64_t letters = 1 + next_random(&seed) % 3;
        for (int64_t k = 0; k < 50; k++) {
            if (k > 0 && next_random(&seed) % 3 == 0) {
                int64_t from = next_random(&seed) % k;
                strs[k] = (Word){malloc(16), strs[from].len};
                memcpy(strs[k].text, strs[from].text, (size_t)strs[from].len);
            } else {
                int64_t len = 1 + next_random(&seed) % 10;
                strs[k] = (Word){malloc(16), len};
                for (int64_t i = 0; i < len; i++) strs[k].text[i] = (char)(97 + next_random(&seed) % letters);
            }
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < 100; round++)
        for (int64_t l = 0; l < n_lists; l++) {
            int64_t answer = find_lus_length(&lists[l * 50], 50);
            total += answer;
            checksum = (checksum + (round + 1) * (l + 1) * (answer + 2)) % 1000000007;
        }
    printf("2000 lists of 50 words, 100 rounds: total %lld, checksum %lld\n", (long long)total, (long long)checksum);
    for (int64_t i = 0; i < n_lists * 50; i++) free(lists[i].text);
    free(lists);
    return 0;
}
