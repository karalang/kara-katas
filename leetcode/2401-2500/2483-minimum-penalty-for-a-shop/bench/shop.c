// LeetCode #2483: Minimum Penalty for a Shop -- bench, C mirror of
// shop.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t best_closing_time(const char *customers) {
    int64_t balance = 0, best = 0, best_hour = 0, hour = 0;
    for (const char *c = customers; *c; c++) {
        if (*c == 'Y')
            balance += 1;
        else
            balance -= 1;
        hour += 1;
        if (balance > best) {
            best = balance;
            best_hour = hour;
        }
    }
    return best_hour;
}

static int64_t seed = 2483;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char logs[20][10000];
    for (int g = 0; g < 20; g++)
        for (int i = 0; i < 10000; i++) logs[g][i] = next_random() % 2 == 0 ? 'Y' : 'N';
    int64_t check = 0;
    char *log = malloc(10001);
    for (int64_t p = 0; p < 600; p++) {
        for (int g = 0; g < 20; g++) {
            int64_t at = check % 10000;
            logs[g][at] = logs[g][at] == 'Y' ? 'N' : 'Y';
            memcpy(log, logs[g], 10000);
            log[10000] = 0;
            check = (check * 31 + best_closing_time(log) + p) % 1000000007;
        }
    }
    free(log);
    printf("600 passes over 20 logs of 10^4 hours: checksum %lld\n", (long long)check);
    return 0;
}
