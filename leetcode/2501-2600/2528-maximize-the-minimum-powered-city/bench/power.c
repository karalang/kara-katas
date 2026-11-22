// LeetCode #2528: Maximize the Minimum Powered City -- C mirror of the
// benchmark (power.kara): the same cities, passes, order and checksum.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define N 100000

static int64_t stations[N], prefix[N + 1], power[N], ends[N + 1];

static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }
static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static int reachable(int64_t n, int64_t r, int64_t k, int64_t target) {
    memset(ends, 0, sizeof(int64_t) * (n + 1));
    int64_t running = 0, used = 0;
    for (int64_t i = 0; i < n; i++) {
        running += ends[i];
        int64_t have = power[i] + running;
        if (have < target) {
            int64_t need = target - have;
            used += need;
            if (used > k) return 0;
            running += need;
            ends[min64(i + 2 * r + 1, n)] -= need;
        }
    }
    return 1;
}

static int64_t max_power(int64_t n, int64_t r, int64_t k) {
    prefix[0] = 0;
    for (int64_t i = 0; i < n; i++) prefix[i + 1] = prefix[i] + stations[i];
    int64_t lo = -1;
    for (int64_t i = 0; i < n; i++) {
        power[i] = prefix[min64(i + r + 1, n)] - prefix[max64(i - r, 0)];
        if (lo == -1 || power[i] < lo) lo = power[i];
    }
    int64_t hi = lo + k;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo + 1) / 2;
        if (reachable(n, r, k, mid)) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}

static int64_t seed = 2528;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    for (int i = 0; i < N; i++) stations[i] = next_random() % 100001;
    const int passes = 20;
    int64_t check = 0;
    for (int p = 0; p < passes; p++) {
        int64_t r = check % 100;
        int64_t k = 1000000000 - check % 1000;
        check = (check * 31 + max_power(N, r, k) + p) % 1000000007;
    }
    printf("%d passes over 100000 cities: checksum %lld\n", passes, (long long)check);
    return 0;
}
