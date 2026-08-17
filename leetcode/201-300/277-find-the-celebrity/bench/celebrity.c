/* LeetCode 277 bench mirror — C. Same formula-based `knows`, same instance
 * split, sequential. */
#include <stdio.h>
#include <stdint.h>

#define N 2500000
#define INSTANCES 64

static int knows(int64_t star, int64_t a, int64_t b) {
    if (b == star) return 1;
    if (a == star) return 0;
    int64_t h = (a * 1103515245LL + b * 12345LL) % 2147483647LL;
    return h % 2 == 0;
}

static int64_t find_celebrity(int64_t n, int64_t star) {
    int64_t cand = 0;
    for (int64_t i = 1; i < n; i++)
        if (knows(star, cand, i)) cand = i;
    for (int64_t j = 0; j < n; j++)
        if (j != cand) {
            if (knows(star, cand, j)) return -1;
            if (!knows(star, j, cand)) return -1;
        }
    return cand;
}

int main(void) {
    int64_t sink = 0;
    for (int64_t i = 0; i < INSTANCES; i++) {
        int64_t star = (i * 7919LL) % N;
        sink = (sink + (i * 1000003LL + find_celebrity(N, star)) % 1000000007LL) % 1000000007LL;
    }
    printf("%lld\n", (long long)sink);
    return 0;
}
