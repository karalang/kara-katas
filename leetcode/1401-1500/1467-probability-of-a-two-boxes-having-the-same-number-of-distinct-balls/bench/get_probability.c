// LeetCode #1467 bench in C: the ★ arm (a depth-first search over how many
// of each colour go into the first box) on the same 100 sets of 8 colours
// and 2 passes. A probability is never negative, so the cast that
// truncates it rounds as the others' floor does.
#include <stdint.h>
#include <stdio.h>

static int64_t choose(int64_t n, int64_t k) {
    int64_t c = 1;
    for (int64_t i = 0; i < k; i++) c = c * (n - i) / (i + 1);
    return c;
}

static int64_t ways(const int *balls, int len, int i, int64_t first, int64_t a, int64_t b) {
    if (i == len) return first == 0 && a == b ? 1 : 0;
    int64_t n = balls[i];
    int64_t top = n < first ? n : first;
    int64_t total = 0;
    for (int64_t j = 0; j <= top; j++) {
        int64_t a2 = j > 0 ? a + 1 : a;
        int64_t b2 = j < n ? b + 1 : b;
        total += choose(n, j) * ways(balls, len, i + 1, first - j, a2, b2);
    }
    return total;
}

static double get_probability(const int *balls, int len) {
    int64_t total = 0;
    for (int i = 0; i < len; i++) total += balls[i];
    int64_t good = ways(balls, len, 0, total / 2, 0, 0);
    return (double)good / (double)choose(total, total / 2);
}

static int64_t seed = 1467;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int sets[100][8];
    int count = 0;
    while (count < 100) {
        int sum = 0;
        for (int i = 0; i < 8; i++) {
            sets[count][i] = (int)(1 + next_random() % 6);
            sum += sets[count][i];
        }
        if (sum % 2 == 0) count++;
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 2; pass++) {
        for (int s = 0; s < 100; s++) {
            int k = (int)(check % 8);
            sets[s][k] = sets[s][k] <= 4 ? sets[s][k] + 2 : sets[s][k] - 2;
            double p = get_probability(sets[s], 8);
            check = (check * 31 + (int64_t)(p * 1000000000.0 + 0.5) + pass) % 1000000007;
        }
    }
    printf("2 passes over 100 sets of 8 colours: checksum %lld\n", (long long)check);
    return 0;
}
