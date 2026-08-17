/* LeetCode 279 bench mirror — C. Same DP, same checksum. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 300000
int main(void) {
    int64_t *least = malloc((size_t)(N + 1) * sizeof(int64_t));
    least[0] = 0;
    for (int64_t i = 1; i <= N; i++) {
        int64_t best = i;
        for (int64_t j = 1; j * j <= i; j++) {
            int64_t cand = least[i - j * j] + 1;
            if (cand < best) best = cand;
        }
        least[i] = best;
    }
    int64_t sum = 0;
    for (int64_t k = 0; k <= N; k++) sum = (sum * 31 + least[k]) % 1000000007LL;
    printf("%lld\n", (long long)((sum * 10 + least[N]) % 1000000007LL));
    return 0;
}
