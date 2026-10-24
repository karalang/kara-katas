// Benchmark: LeetCode #941 Valid Mountain Array -- the ★ arm, a walk up
// and a walk down, on 100 arrays of 10000 values, LeetCode's longest, in
// 200 rounds. Mirrors valid_mountain_array.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>

static int valid_mountain_array(const int64_t *arr, int64_t n) {
    int64_t i = 0;
    while (i + 1 < n && arr[i] < arr[i + 1]) i++;
    if (i == 0 || i == n - 1) return 0;
    while (i + 1 < n && arr[i] > arr[i + 1]) i++;
    return i == n - 1;
}

static int64_t seed = 941;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t arrays[100][10000];

int main(void) {
    int rounds = 200, count = 100;
    for (int a = 0; a < count; a++) {
        int64_t top = 1 + next_random() % 9998;
        int64_t least = top < 10000 - top ? 0 : 2 * top - 9999;
        for (int64_t i = 0; i < 10000; i++) arrays[a][i] = (i <= top ? i : 2 * top - i) - least;
        if (a % 2 == 1) {
            int64_t hi = next_random();
            int64_t j = (hi * 32768 + next_random()) % 10000;
            arrays[a][j] = next_random() % 10001;
        }
    }
    int64_t mountains = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < count; i++) {
            int c = (r + i) % count;
            if (valid_mountain_array(arrays[c], 10000)) {
                mountains++;
                check = (check * 1000003 + c + 1) % 1000000007;
            }
        }
    }
    printf("%d rounds over %d arrays of 10000 values: %lld mountains, checksum %lld\n", rounds, count,
           (long long)mountains, (long long)check);
    return 0;
}
