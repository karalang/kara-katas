// LeetCode #1791: Find Center of Star Graph -- the bench in C, mirroring
// find_center.kara: the node the first two edges share.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t find_center(int32_t (*edges)[2]) {
    int32_t a = edges[0][0], b = edges[0][1];
    return (a == edges[1][0] || a == edges[1][1]) ? a : b;
}

static int64_t seed = 1791;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int32_t (*stars)[99][2] = malloc(sizeof(int32_t) * 2000 * 99 * 2);
    for (int s = 0; s < 2000; s++) {
        int64_t center = 1 + next_random() % 100;
        int m = 0;
        for (int64_t leaf = 1; leaf <= 100; leaf++) {
            if (leaf == center) continue;
            if (next_random() % 2 == 0) {
                stars[s][m][0] = (int32_t)center; stars[s][m][1] = (int32_t)leaf;
            } else {
                stars[s][m][0] = (int32_t)leaf; stars[s][m][1] = (int32_t)center;
            }
            m++;
        }
        for (int i = m - 1; i >= 1; i--) {
            int j = (int)(next_random() % (i + 1));
            int32_t t0 = stars[s][i][0], t1 = stars[s][i][1];
            stars[s][i][0] = stars[s][j][0]; stars[s][i][1] = stars[s][j][1];
            stars[s][j][0] = t0; stars[s][j][1] = t1;
        }
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 20000000; call++) {
        check = (check * 41 + find_center(stars[(check + call) % 2000])) % 1000000007;
    }
    printf("20000000 calls over 2000 stars: checksum %lld\n", (long long)check);
    free(stars);
    return 0;
}
