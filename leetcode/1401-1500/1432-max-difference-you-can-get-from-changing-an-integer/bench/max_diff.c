#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Each number's text and its two changes in fresh strings, as the Kara arm
   makes a String of each. */
static char *replaced(const char *s, char from, char to) {
    size_t n = strlen(s);
    char *t = malloc(n + 1);
    for (size_t i = 0; i <= n; i++) t[i] = s[i] == from ? to : s[i];
    return t;
}

static int32_t max_diff(int32_t num) {
    char *s = malloc(12);
    snprintf(s, 12, "%d", num);
    char c = 0;
    for (const char *p = s; *p; p++)
        if (*p != '9') { c = *p; break; }
    char *high = c ? replaced(s, c, '9') : replaced(s, 0, 0);
    char *low;
    if (s[0] != '1') {
        low = replaced(s, s[0], '1');
    } else {
        c = 0;
        for (const char *p = s + 1; *p; p++)
            if (*p != '0' && *p != '1') { c = *p; break; }
        low = c ? replaced(s, c, '0') : replaced(s, 0, 0);
    }
    int32_t answer = (int32_t)strtol(high, NULL, 10) - (int32_t)strtol(low, NULL, 10);
    free(s);
    free(high);
    free(low);
    return answer;
}

int main(void) {
    int64_t seed = 1432, check = 0;
    for (int i = 0; i < 3000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t high = seed / 65536;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int32_t num = (int32_t)(1 + (high * 32768 + seed / 65536) % 100000000);
        check = (check * 131 + max_diff(num)) % 1000000007;
    }
    printf("3 * 10^6 numbers: checksum %lld\n", (long long)check);
    return 0;
}
