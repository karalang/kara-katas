// LeetCode #636: Exclusive Time of Functions -- benchmark, C.
//
// The ★ arm: one stack of running functions and the time of the last
// event. Each log is split at its two colons in place.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void exclusive_time(int64_t n, char **logs, int64_t count, int64_t *total) {
    int64_t *stack = malloc(count * sizeof(int64_t));
    int64_t depth = 0, prev = 0;
    memset(total, 0, n * sizeof(int64_t));
    for (int64_t i = 0; i < count; i++) {
        char *log = logs[i];
        char *first = strchr(log, ':');
        char *second = strchr(first + 1, ':');
        int64_t id = strtoll(log, NULL, 10);
        int64_t t = strtoll(second + 1, NULL, 10);
        if (second - first - 1 == 5 && strncmp(first + 1, "start", 5) == 0) {
            if (depth > 0) total[stack[depth - 1]] += t - prev;
            stack[depth++] = id;
            prev = t;
        } else {
            int64_t top = stack[--depth];
            total[top] += t - prev + 1;
            prev = t + 1;
        }
    }
    free(stack);
}

static int64_t seed = 636;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

static char **random_logs(int64_t n, int64_t calls, int64_t gap, int64_t *count) {
    char **logs = malloc(2 * calls * sizeof(char *));
    int64_t *stack = malloc(calls * sizeof(int64_t));
    int64_t depth = 0, started = 0, start_at = 0, end_at = 0, k = 0;
    char buf[64];
    while (started < calls || depth > 0) {
        int begin = started < calls && (depth == 0 || next_random() % 2 == 0);
        if (begin) {
            int64_t id = next_random() % n;
            int64_t t = start_at + wide() % gap;
            snprintf(buf, sizeof buf, "%lld:start:%lld", (long long)id, (long long)t);
            stack[depth++] = id;
            started++;
            start_at = t + 1;
            end_at = t;
        } else {
            int64_t id = stack[--depth];
            int64_t t = end_at + wide() % gap;
            snprintf(buf, sizeof buf, "%lld:end:%lld", (long long)id, (long long)t);
            start_at = end_at = t + 1;
        }
        logs[k++] = strdup(buf);
    }
    free(stack);
    *count = k;
    return logs;
}

int main(void) {
    char **inputs[10];
    int64_t counts[10];
    for (int i = 0; i < 10; i++) inputs[i] = random_logs(100, 250, 3800000, &counts[i]);
    int64_t total[100];
    int64_t sum = 0, checksum = 0;
    for (int r = 0; r < 10000; r++) {
        exclusive_time(100, inputs[r % 10], counts[r % 10], total);
        for (int i = 0; i < 100; i++) {
            sum += total[i];
            checksum = (checksum * 31 + total[i]) % 1000000007;
        }
    }
    printf("10 inputs of 500 logs, 10000 rounds: total %lld, checksum %lld\n", (long long)sum,
           (long long)checksum);
    for (int i = 0; i < 10; i++) {
        for (int64_t j = 0; j < counts[i]; j++) free(inputs[i][j]);
        free(inputs[i]);
    }
    return 0;
}
