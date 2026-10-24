// Benchmark: LeetCode #961 N-Repeated Element in Size 2N Array -- the ★
// arm, near neighbours, on 10000 numbers, LeetCode's largest, with the
// repeated value at every other place. Each call swaps two of the other
// values first. Mirrors repeated_n_times.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>

#define N 5000
#define LEN (2 * N)
#define COUNT 50

static int64_t seed = 961;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t repeated_n_times(const int64_t *nums, int64_t len) {
    for (int64_t k = 1; k < 4; k++) {
        for (int64_t i = 0; i < len - k; i++) {
            if (nums[i] == nums[i + k]) return nums[i];
        }
    }
    return -1;
}

static void alternating(int64_t *out, int first) {
    char used[10001] = {0};
    int64_t r = next_random() % 10001;
    used[r] = 1;
    int64_t len = 0;
    while (len < LEN) {
        int64_t v = next_random() % 10001;
        if (!used[v]) {
            used[v] = 1;
            out[len++] = first ? r : v;
            out[len++] = first ? v : r;
        }
    }
}

static int64_t cases[COUNT][LEN];

int main(void) {
    int rounds = 1000;
    for (int i = 0; i < COUNT; i++) alternating(cases[i], i % 2 == 0);
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < COUNT; i++) {
            int c = (r + i) % COUNT;
            int64_t p = 2 * (next_random() % 4999) + 1 - c % 2;
            int64_t t = cases[c][p];
            cases[c][p] = cases[c][p + 2];
            cases[c][p + 2] = t;
            int64_t a = repeated_n_times(cases[c], LEN);
            total += a;
            check = (check * 31 + a + i) % 1000000007;
        }
    }
    printf("%d rounds over 50 cases of 10000 numbers: the repeated ones sum to %lld, checksum %lld\n",
           rounds, (long long)total, (long long)check);
    return 0;
}
