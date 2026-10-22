// Benchmark for #845: Longest Mountain in Array -- C twin of the Kāra ★ arm
// (one pass with two counters).
#include <stdio.h>
#include <stdint.h>

#define N 10000

static int64_t longest_mountain(const int64_t *arr, int64_t n) {
    int64_t best = 0, up = 0, down = 0;
    for (int64_t i = 1; i < n; i++) {
        if ((down > 0 && arr[i - 1] < arr[i]) || arr[i - 1] == arr[i]) {
            up = 0;
            down = 0;
        }
        if (arr[i - 1] < arr[i]) up++;
        else if (arr[i - 1] > arr[i]) down++;
        if (up > 0 && down > 0 && up + down + 1 > best) best = up + down + 1;
    }
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 20000;
    int64_t seed = 845;
    static int64_t arrays[64][N];
    for (int64_t g = 0; g < count; g++) {
        int64_t *arr = arrays[g];
        int64_t len = 0;
        if (g % 3 == 0) {
            for (int64_t i = 0; i < N; i++) arr[len++] = next_random(&seed) % 10001;
        } else if (g % 3 == 1) {
            int64_t v = 5000;
            for (int64_t i = 0; i < N; i++) {
                arr[len++] = v;
                v += next_random(&seed) % 3 - 1;
            }
        } else {
            while (len < N) {
                int64_t up = next_random(&seed) % 40;
                int64_t down = next_random(&seed) % 40;
                int64_t base = next_random(&seed) % 100;
                for (int64_t k = 0; k < up + 1; k++)
                    if (len < N) arr[len++] = base + k;
                for (int64_t k = 0; k < down; k++)
                    if (len < N) arr[len++] = base + up - k - 1;
            }
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t m = longest_mountain(arrays[round % count], N);
        total += m;
        checksum = (checksum * 31 + m) % 1000000007;
    }
    printf("%lld rounds of %lld arrays: lengths sum to %lld, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    return 0;
}
