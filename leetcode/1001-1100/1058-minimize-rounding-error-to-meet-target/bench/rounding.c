// LeetCode #1058: Minimize Rounding Error to Meet Target -- the benchmark,
// the same algorithm as rounding.kara.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef long long i64;

static i64 thousandths(const char *p) {
    i64 value = 0;
    for (; *p; p++) {
        if (*p != '.') {
            value = value * 10 + (*p - '0');
        }
    }
    return value;
}

static int descending(const void *a, const void *b) {
    i64 x = *(const i64 *)a, y = *(const i64 *)b;
    return (x < y) - (x > y);
}

// Writes the answer into `out`.
static void minimize_error(char **prices, int n, i64 target, char *out) {
    i64 floor_sum = 0;
    i64 *fractions = malloc(sizeof(i64) * (size_t)n);
    int count = 0;
    for (int i = 0; i < n; i++) {
        i64 t = thousandths(prices[i]);
        floor_sum += t / 1000;
        if (t % 1000 != 0) {
            fractions[count++] = t % 1000;
        }
    }
    i64 up = target - floor_sum;
    if (up < 0 || up > count) {
        strcpy(out, "-1");
        free(fractions);
        return;
    }
    qsort(fractions, (size_t)count, sizeof(i64), descending);
    i64 error = 0;
    for (int k = 0; k < count; k++) {
        error += k < up ? 1000 - fractions[k] : fractions[k];
    }
    sprintf(out, "%lld.%03lld", error / 1000, error % 1000);
    free(fractions);
}

static i64 next_random(i64 *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static char *random_price(i64 *seed) {
    i64 whole = next_random(seed) % 1000;
    i64 part = next_random(seed) % 4 == 0 ? 0 : next_random(seed) % 999 + 1;
    char *s = malloc(16);
    sprintf(s, "%lld.%03lld", whole, part);
    return s;
}

int main(void) {
    i64 seed = 1058;
    char *lists[40][500];
    for (int l = 0; l < 40; l++) {
        for (int i = 0; i < 500; i++) {
            lists[l][i] = random_price(&seed);
        }
    }
    i64 calls = 0, check = 0;
    char answer[32];
    for (int round = 0; round < 8; round++) {
        for (int l = 0; l < 40; l++) {
            i64 floor_sum = 0, with_fraction = 0;
            for (int i = 0; i < 500; i++) {
                i64 t = thousandths(lists[l][i]);
                floor_sum += t / 1000;
                if (t % 1000 != 0) {
                    with_fraction++;
                }
            }
            for (i64 target = floor_sum - 1; target < floor_sum + with_fraction + 2; target++) {
                minimize_error(lists[l], 500, target, answer);
                for (char *c = answer; *c; c++) {
                    check = (check * 131 + *c) % 1000000007;
                }
                calls++;
            }
        }
    }
    printf("%lld calls: checksum %lld\n", calls, check);
    for (int l = 0; l < 40; l++) {
        for (int i = 0; i < 500; i++) {
            free(lists[l][i]);
        }
    }
    return 0;
}
