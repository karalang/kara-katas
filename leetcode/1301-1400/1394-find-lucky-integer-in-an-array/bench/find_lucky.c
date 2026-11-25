// LeetCode #1394 bench, C mirror of the ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t find_lucky(const int32_t *arr, int n) {
    int32_t *count = calloc(501, sizeof(int32_t));
    for (int k = 0; k < n; k++) count[arr[k]] += 1;
    int32_t answer = -1;
    for (int32_t x = 500; x >= 1; x--) {
        if (count[x] == x) {
            answer = x;
            break;
        }
    }
    free(count);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    enum { N = 500 };
    int32_t arr[N];
    int64_t seed = 1394;
    for (int k = 0; k < N; k++) arr[k] = (int32_t)(1 + next_random(&seed) % 40);
    int64_t check = 0;
    for (int round = 0; round < 600000; round++) {
        seed = (seed + check) % 2147483648LL;
        int64_t i = next_random(&seed) % N;
        arr[i] = (int32_t)(1 + next_random(&seed) % 40);
        check = (check * 131 + find_lucky(arr, N) + 1) % 1000000007;
    }
    printf("600000 rounds over 500 values: checksum %lld\n", (long long)check);
    return 0;
}
