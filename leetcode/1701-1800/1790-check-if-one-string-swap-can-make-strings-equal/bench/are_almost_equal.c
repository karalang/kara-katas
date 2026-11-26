// LeetCode #1790: Check if One String Swap Can Make Strings Equal -- the
// bench in C, mirroring are_almost_equal.kara: the positions where the
// strings differ.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int are_almost_equal(const char *a, const char *b, int n) {
    int differ[3];
    int count = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] != b[i]) {
            differ[count++] = i;
            if (count > 2) return 0;
        }
    }
    if (count == 0) return 1;
    if (count == 2) return a[differ[0]] == b[differ[1]] && a[differ[1]] == b[differ[0]];
    return 0;
}

static int64_t seed = 1790;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    char *first = malloc(2000 * 101), *second = malloc(2000 * 101);
    for (int k = 0; k < 2000; k++) {
        char *a = first + k * 101, *b = second + k * 101;
        for (int i = 0; i < 100; i++) a[i] = (char)(97 + next_random() % 26);
        a[100] = 0;
        memcpy(b, a, 101);
        for (int r = 0; r < k % 4; r++) {
            int i = (int)(next_random() % 100);
            int j = (int)(next_random() % 100);
            if (k % 4 == 3) {
                b[i] = (char)(97 + (b[i] - 97 + 1) % 26);
            } else {
                char t = b[i]; b[i] = b[j]; b[j] = t;
            }
        }
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 4000000; call++) {
        int k = (int)((check + call) % 2000);
        check = (check * 3 + (are_almost_equal(first + k * 101, second + k * 101, 100) ? 2 : 1)) % 1000000007;
    }
    printf("4000000 calls over 2000 pairs: checksum %lld\n", (long long)check);
    free(first);
    free(second);
    return 0;
}
