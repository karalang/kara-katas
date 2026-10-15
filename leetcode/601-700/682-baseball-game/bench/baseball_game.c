// LeetCode #682: Baseball Game -- a stack of the valid scores. Bench.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 200
#define LEN 5000
#define ROUNDS 30

static int64_t seed = 682;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t abs64(int64_t x) { return x < 0 ? -x : x; }

static int64_t cal_points(char **ops, int64_t n, int64_t *record) {
    int64_t top = 0;
    for (int64_t k = 0; k < n; k++) {
        const char *op = ops[k];
        if (strcmp(op, "+") == 0) {
            record[top] = record[top - 1] + record[top - 2];
            top++;
        } else if (strcmp(op, "D") == 0) {
            record[top] = record[top - 1] * 2;
            top++;
        } else if (strcmp(op, "C") == 0) {
            top--;
        } else {
            record[top++] = strtoll(op, NULL, 10);
        }
    }
    int64_t total = 0;
    for (int64_t k = 0; k < top; k++) total += record[k];
    return total;
}

static void random_ops(char **out, int64_t n) {
    const int64_t limit = 1073741824;
    int64_t *record = malloc(sizeof(int64_t) * n);
    int64_t k = 0, len = 0;
    char buf[16];
    while (len < n) {
        int64_t pick = next_random() % 10;
        if (pick == 0 && k >= 1) {
            k--;
            out[len++] = strdup("C");
        } else if (pick == 1 && k >= 1 && abs64(record[k - 1]) < limit / 2) {
            record[k] = record[k - 1] * 2;
            k++;
            out[len++] = strdup("D");
        } else if (pick == 2 && k >= 2 && abs64(record[k - 1] + record[k - 2]) < limit) {
            record[k] = record[k - 1] + record[k - 2];
            k++;
            out[len++] = strdup("+");
        } else if (pick >= 3) {
            int64_t x = next_random() % 60001 - 30000;
            record[k++] = x;
            snprintf(buf, sizeof buf, "%lld", (long long)x);
            out[len++] = strdup(buf);
        }
    }
    free(record);
}

int main(void) {
    static char *lists[COUNT][LEN];
    for (int64_t k = 0; k < COUNT; k++) random_ops(lists[k], LEN);
    int64_t *record = malloc(sizeof(int64_t) * LEN);
    int64_t sum = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int64_t k = 0; k < COUNT; k++) {
            int64_t at = (k * 7 + r) % COUNT;
            int64_t points = cal_points(lists[at], LEN, record);
            sum = (sum * 31 + points % 1000000007 + 1000000007) % 1000000007;
        }
    }
    printf("%d games scored, checksum %lld\n", COUNT * ROUNDS, (long long)sum);
    return 0;
}
