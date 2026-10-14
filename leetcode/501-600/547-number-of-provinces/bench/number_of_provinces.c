// Benchmark for #547: C mirror of the ★ arm (depth-first search); see
// number_of_provinces.kara. The matrix is one flat array of n * n.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static void visit(const int64_t *m, int n, int city, char *seen) {
    seen[city] = 1;
    for (int other = 0; other < n; other++)
        if (m[city * n + other] == 1 && !seen[other]) visit(m, n, other, seen);
}

static int64_t find_circle_num(const int64_t *m, int n) {
    char *seen = calloc(n, 1);
    int64_t provinces = 0;
    for (int city = 0; city < n; city++)
        if (!seen[city]) {
            provinces++;
            visit(m, n, city, seen);
        }
    free(seen);
    return provinces;
}

static int64_t seed = 547;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int count = 30, n = 200;
    int64_t *all[30];
    for (int g = 0; g < count; g++) {
        int64_t *m = calloc((size_t)n * n, sizeof(int64_t));
        for (int i = 0; i < n; i++) m[i * n + i] = 1;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                if (next_random() % 1000 < 1 + g % 10) m[i * n + j] = m[j * n + i] = 1;
        all[g] = m;
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < 200; round++)
        for (int g = 0; g < count; g++) {
            int a = (round * 13 + g) % n, b = (round * 29 + g * 3 + 1) % n;
            if (a != b) {
                int64_t flip = 1 - all[g][a * n + b];
                all[g][a * n + b] = all[g][b * n + a] = flip;
            }
            int64_t p = find_circle_num(all[g], n);
            total += p;
            checksum = (checksum * 31 + p) % 1000000007;
        }
    printf("%d matrices, 200 rounds each: %lld provinces, checksum %lld\n", count,
           (long long)total, (long long)checksum);
    for (int g = 0; g < count; g++) free(all[g]);
    return 0;
}
