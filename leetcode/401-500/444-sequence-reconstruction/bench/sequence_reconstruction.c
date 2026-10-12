// Benchmark for #444: mirror of sequence_reconstruction.kara (positions
// and neighbouring pairs) on 50 random cases of n = 5,000, built once
// and answered 30 times over. A case's sequences are stored flat, with
// each one's start in an offsets array.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

typedef struct {
    int64_t *values;   // every sequence's values, one after another
    int64_t *offsets;  // sequence i is values[offsets[i] .. offsets[i + 1]]
    int64_t count;     // number of sequences
} Sequences;

static bool sequence_reconstruction(const int64_t *nums, int64_t n, const Sequences *sequences) {
    int64_t *position = calloc(n + 1, sizeof(int64_t));
    bool *covered = calloc(n, sizeof(bool));
    bool answer = true;
    for (int64_t i = 0; i < n; i++) {
        position[nums[i]] = i;
    }
    for (int64_t s = 0; s < sequences->count && answer; s++) {
        const int64_t *v = sequences->values + sequences->offsets[s];
        int64_t len = sequences->offsets[s + 1] - sequences->offsets[s];
        for (int64_t j = 1; j < len; j++) {
            int64_t a = position[v[j - 1]];
            int64_t b = position[v[j]];
            if (a >= b) {
                answer = false;
                break;
            }
            if (b == a + 1) {
                covered[a] = true;
            }
        }
    }
    for (int64_t i = 0; i < n - 1 && answer; i++) {
        if (!covered[i]) {
            answer = false;
        }
    }
    free(position);
    free(covered);
    return answer;
}

int main(void) {
    const int64_t count = 50, n = 5000, rounds = 30;
    int64_t seed = 444;
    int64_t **cases_nums = malloc(count * sizeof(int64_t *));
    Sequences *cases_sequences = malloc(count * sizeof(Sequences));
    int64_t values = 0;
    for (int64_t c = 0; c < count; c++) {
        int64_t *nums = malloc(n * sizeof(int64_t));
        for (int64_t v = 1; v <= n; v++) {
            nums[v - 1] = v;
        }
        for (int64_t i = n - 1; i > 0; i--) {
            int64_t j = next_random(&seed) % (i + 1);
            int64_t t = nums[i];
            nums[i] = nums[j];
            nums[j] = t;
        }
        int64_t windows = 1 + next_random(&seed) % (n * 2 + 2);
        Sequences *sq = &cases_sequences[c];
        sq->values = malloc((windows * 12 + n) * sizeof(int64_t));
        sq->offsets = malloc((windows + 2) * sizeof(int64_t));
        sq->count = 0;
        int64_t used = 0;
        for (int64_t w = 0; w < windows; w++) {
            int64_t start = next_random(&seed) % n;
            int64_t length = 1 + next_random(&seed) % 12;
            int64_t end = start + length < n ? start + length : n;
            sq->offsets[sq->count] = used;
            int64_t first = used;
            for (int64_t k = start; k < end; k++) {
                if (used == first || next_random(&seed) % 10 != 0) {
                    sq->values[used++] = nums[k];
                }
            }
            values += used - first;
            sq->count++;
        }
        if (c % 2 == 0) {
            sq->offsets[sq->count] = used;
            memcpy(sq->values + used, nums, n * sizeof(int64_t));
            used += n;
            values += n;
            sq->count++;
        }
        sq->offsets[sq->count] = used;
        cases_nums[c] = nums;
    }
    int64_t true_count = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t c = 0; c < count; c++) {
            bool answer = sequence_reconstruction(cases_nums[c], n, &cases_sequences[c]);
            if (answer) {
                true_count++;
            }
            checksum = (checksum * 31 + c * 2 + (answer ? 1 : 0) + round) % 1000000007;
        }
    }
    printf("%lld rounds on %lld cases of n = %lld (%lld values in sequences): %lld true, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)values, (long long)true_count,
           (long long)checksum);
    for (int64_t c = 0; c < count; c++) {
        free(cases_nums[c]);
        free(cases_sequences[c].values);
        free(cases_sequences[c].offsets);
    }
    free(cases_nums);
    free(cases_sequences);
    return 0;
}
