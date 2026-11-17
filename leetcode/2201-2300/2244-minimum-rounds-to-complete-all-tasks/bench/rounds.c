// LeetCode #2244: Minimum Rounds to Complete All Tasks -- the
// benchmark's C mirror of rounds.kara: the tasks of each difficulty
// counted in a hash table (open addressing, linear probing, a
// multiplicative hash); a lone task gives -1, any other count c takes
// ceil(c / 3) rounds, summed.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAP (1 << 18)

static int64_t keys[CAP], counts[CAP];
static char used[CAP];

static int64_t minimum_rounds(const int64_t *tasks, int64_t n) {
    memset(used, 0, sizeof used);
    for (int64_t i = 0; i < n; i++) {
        uint64_t h = ((uint64_t)tasks[i] * 0x9E3779B97F4A7C15ULL) >> 46;
        while (used[h] && keys[h] != tasks[i]) h = (h + 1) & (CAP - 1);
        if (!used[h]) {
            used[h] = 1;
            keys[h] = tasks[i];
            counts[h] = 0;
        }
        counts[h]++;
    }
    int64_t rounds = 0;
    for (int64_t h = 0; h < CAP; h++) {
        if (!used[h]) continue;
        if (counts[h] == 1) return -1;
        rounds += (counts[h] + 2) / 3;
    }
    return rounds;
}

static int64_t seed = 2244;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    static int64_t kinds[30000], tasks[100000];
    int64_t check = 0;
    for (int l = 0; l < 40; l++) {
        for (int i = 0; i < 30000; i++) kinds[i] = wide_random() % 1000000000 + 1;
        for (int i = 0; i < 100000; i += 2) tasks[i] = tasks[i + 1] = kinds[wide_random() % 30000];
        check = (check * 31 + minimum_rounds(tasks, 100000) + 1) % 1000000007;
    }
    printf("40 lists of 100000 tasks: checksum %lld\n", (long long)check);
    return 0;
}
