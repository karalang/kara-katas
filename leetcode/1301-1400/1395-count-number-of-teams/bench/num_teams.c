// LeetCode #1395 bench, C mirror of the ★ arm.
#include <stdint.h>
#include <stdio.h>

static int32_t num_teams(const int32_t *rating, int n) {
    int32_t teams = 0;
    for (int j = 0; j < n; j++) {
        int32_t less_left = 0, greater_left = 0, less_right = 0, greater_right = 0;
        for (int i = 0; i < j; i++) {
            if (rating[i] < rating[j]) less_left += 1;
            else greater_left += 1;
        }
        for (int k = j + 1; k < n; k++) {
            if (rating[k] < rating[j]) less_right += 1;
            else greater_right += 1;
        }
        teams += less_left * greater_right + greater_left * less_right;
    }
    return teams;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    enum { N = 1000 };
    int32_t rating[N];
    int64_t seed = 1395;
    for (int v = 1; v <= N; v++) rating[v - 1] = v * 97;
    for (int64_t i = N - 1; i >= 1; i--) {
        int64_t j = next_random(&seed) % (i + 1);
        int32_t t = rating[i];
        rating[i] = rating[j];
        rating[j] = t;
    }
    int64_t check = 0;
    for (int round = 0; round < 300; round++) {
        seed = (seed + check) % 2147483648LL;
        int64_t a = next_random(&seed) % N;
        int64_t b = next_random(&seed) % N;
        int32_t t = rating[a];
        rating[a] = rating[b];
        rating[b] = t;
        check = (check * 131 + num_teams(rating, N)) % 1000000007;
    }
    printf("300 rounds over 1000 soldiers: checksum %lld\n", (long long)check);
    return 0;
}
