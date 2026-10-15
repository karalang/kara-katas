// Benchmark for #679: the ★ arm, pairs combined in floating point.
#include <math.h>
#include <stdint.h>
#include <stdio.h>

static int reach(const double *values, int n) {
    if (n == 1) return fabs(values[0] - 24.0) < 0.000001;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            double a = values[i], b = values[j];
            double next[4];
            int m = 0;
            for (int k = 0; k < n; k++)
                if (k != i && k != j) next[m++] = values[k];
            double results[6] = {a + b, a - b, b - a, a * b};
            int r = 4;
            if (b != 0.0) results[r++] = a / b;
            if (a != 0.0) results[r++] = b / a;
            for (int t = 0; t < r; t++) {
                next[m] = results[t];
                if (reach(next, m + 1)) return 1;
            }
        }
    }
    return 0;
}

static int judge_point24(const int64_t *cards) {
    double values[4];
    for (int i = 0; i < 4; i++) values[i] = (double)cards[i];
    return reach(values, 4);
}

int main(void) {
    int64_t solvable = 0, sum = 0;
    for (int64_t a = 1; a < 14; a++)
        for (int64_t b = 1; b < 14; b++)
            for (int64_t c = 1; c < 14; c++)
                for (int64_t d = 1; d < 14; d++) {
                    int64_t cards[4] = {a, b, c, d};
                    int64_t code = a * 1000 + b * 100 + c * 10 + d;
                    if (judge_point24(cards)) {
                        solvable += 1;
                        sum = (sum * 31 + code) % 1000000007;
                    } else {
                        sum = (sum * 31 + 7) % 1000000007;
                    }
                }
    printf("28561 hands: %lld solvable, checksum %lld\n", (long long)solvable, (long long)sum);
    return 0;
}
