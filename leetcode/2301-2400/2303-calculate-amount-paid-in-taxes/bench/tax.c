// LeetCode #2303: Calculate Amount Paid in Taxes -- the bench, the ★ arm
// in C. Walk the brackets in order, taxing the part of the income inside
// each at its percent, summed in hundredths and divided once at the end.
#include <math.h>
#include <stdint.h>
#include <stdio.h>

enum { LISTS = 20, BANDS = 100 };

static double calculate_tax(const int64_t (*brackets)[2], int64_t n, int64_t income) {
    int64_t hundredths = 0, below = 0;
    for (int64_t i = 0; i < n; i++) {
        if (below >= income) break;
        int64_t upper = brackets[i][0];
        hundredths += ((upper < income ? upper : income) - below) * brackets[i][1];
        below = upper;
    }
    return (double)hundredths / 100.0;
}

static int64_t seed = 2303;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t lists[LISTS][BANDS][2];
    for (int a = 0; a < LISTS; a++)
        for (int64_t i = 0; i < BANDS; i++) {
            int64_t less = i == BANDS - 1 ? 0 : next_random() % 5;
            lists[a][i][0] = 10 * (i + 1) - less;
            lists[a][i][1] = next_random() % 101;
        }
    int64_t check = 0;
    for (int p = 0; p < 100; p++)
        for (int a = 0; a < LISTS; a++)
            for (int64_t income = 0; income <= 1000; income++) {
                int64_t tax = (int64_t)round(calculate_tax(lists[a], BANDS, income) * 100.0);
                check = (check * 31 + tax) % 1000000007;
            }
    printf("100 passes over 20 lists of 100 brackets and 1001 incomes: checksum %lld\n", (long long)check);
    return 0;
}
