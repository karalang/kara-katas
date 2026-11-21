// LeetCode #2526: Find Consecutive Integers from a Data Stream -- C mirror
// of the benchmark (stream.kara): the same numbers and passes, each a
// fresh stream fed every number.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef struct {
    int64_t value, k, run;
} DataStream;

static DataStream data_stream_new(int64_t value, int64_t k) {
    DataStream s = {value, k, 0};
    return s;
}

static bool consec(DataStream *s, int64_t num) {
    s->run = num == s->value ? s->run + 1 : 0;
    return s->run >= s->k;
}

static int64_t seed = 2526;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t nums[100000];

int main(void) {
    for (int i = 0; i < 100000; i++) nums[i] = next_random() % 3 + 1;
    const int passes = 1250;
    int64_t check = 0;
    for (int p = 0; p < passes; p++) {
        DataStream s = data_stream_new(check % 3 + 1, check % 8 + 1);
        int64_t trues = 0;
        for (int i = 0; i < 100000; i++)
            if (consec(&s, nums[i])) trues++;
        check = (check * 31 + trues + p) % 1000000007;
    }
    printf("%d passes over 10^5 numbers: checksum %lld\n", passes, (long long)check);
    return 0;
}
