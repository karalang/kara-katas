// LeetCode #621: Task Scheduler -- C mirror of the Kāra bench.
//
// The ★ arm's frame count over the same lists and rounds; a task is a
// `char`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t least_interval(const char *tasks, int64_t len, int64_t n) {
    int64_t counts[26] = {0};
    for (int64_t i = 0; i < len; i++) {
        counts[tasks[i] - 'A'] += 1;
    }
    int64_t most = 0;
    for (int c = 0; c < 26; c++) {
        if (counts[c] > most) {
            most = counts[c];
        }
    }
    int64_t tied = 0;
    for (int c = 0; c < 26; c++) {
        if (counts[c] == most) {
            tied += 1;
        }
    }
    int64_t frame = (most - 1) * (n + 1) + tied;
    return frame > len ? frame : len;
}

static int64_t seed = 621;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char *random_tasks(int64_t size, int64_t kinds, int skew) {
    char *tasks = malloc(size);
    int64_t weight = skew ? kinds * (kinds + 1) / 2 : kinds;
    for (int64_t i = 0; i < size; i++) {
        int64_t r = next_random() % weight;
        int64_t k = 0;
        if (skew) {
            while (r > k) {
                r -= k + 1;
                k += 1;
            }
        } else {
            k = r;
        }
        tasks[i] = (char)(65 + k);
    }
    return tasks;
}

int main(void) {
    enum { LISTS = 100, ROUNDS = 30000, SIZE = 10000 };
    char *all[LISTS];
    for (int i = 0; i < LISTS; i++) {
        int64_t kinds = 1 + next_random() % 26;
        all[i] = random_tasks(SIZE, kinds, i % 2 == 0);
    }
    int64_t sum = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        int64_t answer = least_interval(all[(r * 7) % LISTS], SIZE, r % 101);
        sum += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    printf("%d lists, %d rounds: total %lld, checksum %lld\n", LISTS, ROUNDS, (long long)sum, (long long)checksum);
    for (int i = 0; i < LISTS; i++) {
        free(all[i]);
    }
    return 0;
}
