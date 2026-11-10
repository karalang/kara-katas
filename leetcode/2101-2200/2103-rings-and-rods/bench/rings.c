// LeetCode #2103: Rings and Rods -- bench, C mirror of rings.kara.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t count_points(const char *rings, size_t len) {
    int64_t masks[10] = {0};
    for (size_t i = 0; i < len; i += 2) {
        int64_t bit = rings[i] == 'R' ? 1 : rings[i] == 'G' ? 2 : 4;
        masks[rings[i + 1] - '0'] |= bit;
    }
    int64_t full = 0;
    for (int d = 0; d < 10; d++)
        if (masks[d] == 7) full++;
    return full;
}

static int64_t seed = 2103;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char strings[4096][201];

int main(void) {
    for (int s = 0; s < 4096; s++) {
        int64_t rods = s % 2 == 0 ? 10 : 3;
        for (int r = 0; r < 100; r++) {
            strings[s][2 * r] = "RGB"[next_random() % 3];
            strings[s][2 * r + 1] = (char)('0' + next_random() % rods);
        }
        strings[s][200] = 0;
    }
    int64_t total = 0, check = 0;
    for (int64_t k = 0; k < 300000; k++) {
        const char *x = strings[k * 7919 % 4096];
        int64_t got = count_points(x, strlen(x));
        total += got;
        check = (check * 31 + got) % 1000000007;
    }
    printf("300000 counts: %lld rods with all three, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
