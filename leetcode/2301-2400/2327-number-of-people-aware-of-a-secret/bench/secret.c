// LeetCode #2327: Number of People Aware of a Secret -- the bench, the ★
// arm in C. A running count of the people sharing gains those who
// learned the secret `delay` days back and loses those who learned it
// `forget` days back, and that many learn it each day. O(n).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int64_t people_aware_of_secret(int64_t n, int64_t delay, int64_t forget) {
    int64_t *learned = calloc((size_t)(n + 1), sizeof(int64_t));
    learned[1] = 1;
    int64_t sharing = 0;
    for (int64_t day = 2; day <= n; day++) {
        if (day - delay >= 1) sharing = (sharing + learned[day - delay]) % MOD;
        if (day - forget >= 1) sharing = (sharing - learned[day - forget] + MOD) % MOD;
        learned[day] = sharing;
    }
    int64_t aware = 0;
    for (int64_t day = n - forget + 1; day <= n; day++) aware = (aware + learned[day]) % MOD;
    free(learned);
    return aware;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2327;
    int64_t delays[3000], forgets[3000];
    for (int k = 0; k < 3000; k++) {
        forgets[k] = next_random(&seed) % 989 + 2;
        delays[k] = next_random(&seed) % (forgets[k] - 1) + 1;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++) {
        for (int64_t k = 0; k < 3000; k++) {
            int64_t n = 990 + (k + p) % 11;
            check = (check * 31 + people_aware_of_secret(n, delays[k], forgets[k])) % 1000000007LL;
        }
    }
    printf("10 passes over 3000 cases of up to 1000 days: checksum %lld\n", (long long)check);
    return 0;
}
