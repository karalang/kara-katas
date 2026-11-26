#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t min_number_of_frogs(const char *s, int64_t n) {
    int32_t heard[5] = {0, 0, 0, 0, 0};
    int32_t most = 0;
    for (int64_t j = 0; j < n; j++) {
        int i;
        switch (s[j]) {
            case 'c': i = 0; break;
            case 'r': i = 1; break;
            case 'o': i = 2; break;
            case 'a': i = 3; break;
            case 'k': i = 4; break;
            default: return -1;
        }
        heard[i]++;
        if (i > 0 && heard[i] > heard[i - 1]) return -1;
        if (heard[0] - heard[4] > most) most = heard[0] - heard[4];
    }
    return heard[0] == heard[4] ? most : -1;
}

int main(void) {
    int64_t seed = 1419;
    const char *word = "croak";
    char *pool = malloc(1000 * 500);
    int64_t len = 0;
    int64_t croaking[100];
    for (int b = 0; b < 1000; b++) {
        int64_t active = 0, started = 0;
        while (started < 100 || active > 0) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t r = seed / 65536;
            if (started < 100 && (active == 0 || r % 3 == 0)) {
                pool[len++] = 'c';
                croaking[active++] = 1;
                started++;
            } else {
                int64_t i = r / 3 % active;
                pool[len++] = word[croaking[i]];
                croaking[i]++;
                if (croaking[i] == 5) croaking[i] = croaking[--active];
            }
        }
    }
    int64_t check = 0;
    for (int w = 0; w < 500; w++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t start = 500 * (seed / 65536 % 801);
        check = (check * 131 + min_number_of_frogs(pool + start, 100000) + 1) % 1000000007;
    }
    printf("500 windows of 10^5 letters: checksum %lld\n", (long long)check);
    return 0;
}
