#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* The starts copied into a fresh hash set, open addressing over 256 slots,
   as the Kara arm clones each start into a Set[String]. */
static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ull;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ull;
    return h;
}

static char *dest_city(char *(*paths)[2], int n) {
    char *slots[256] = {0};
    for (int i = 0; i < n; i++) {
        uint64_t at = hash(paths[i][0]) & 255;
        while (slots[at] && strcmp(slots[at], paths[i][0]) != 0) at = (at + 1) & 255;
        if (!slots[at]) slots[at] = strdup(paths[i][0]);
    }
    char *answer = NULL;
    for (int i = 0; i < n && !answer; i++) {
        uint64_t at = hash(paths[i][1]) & 255;
        while (slots[at] && strcmp(slots[at], paths[i][1]) != 0) at = (at + 1) & 255;
        if (!slots[at]) answer = strdup(paths[i][1]);
    }
    for (int i = 0; i < 256; i++) free(slots[i]);
    return answer;
}

int main(void) {
    int64_t seed = 1436;
    static char *trips[1000][100][2];
    for (int t = 0; t < 1000; t++) {
        char *cities[101];
        for (int c = 0; c < 101; c++) {
            char *name = malloc(11);
            for (int k = 0; k < 8; k++) {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                name[k] = (char)('a' + seed / 65536 % 26);
            }
            name[8] = (char)('a' + c / 26);
            name[9] = (char)('a' + c % 26);
            name[10] = 0;
            cities[c] = name;
        }
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int turn = (int)(seed / 65536 % 100);
        for (int i = 0; i < 100; i++) {
            int at = (i + turn) % 100;
            trips[t][i][0] = strdup(cities[at]);
            trips[t][i][1] = strdup(cities[at + 1]);
        }
        for (int c = 0; c < 101; c++) free(cities[c]);
    }
    int64_t check = 0;
    for (int r = 0; r < 100; r++)
        for (int t = 0; t < 1000; t++) {
            char *city = dest_city(trips[t], 100);
            int64_t h = 0;
            for (const char *p = city; *p; p++) h = (h * 31 + (unsigned char)*p) % 1000000007;
            check = (check * 131 + h) % 1000000007;
            free(city);
        }
    printf("10^5 trips of 100 paths: checksum %lld\n", (long long)check);
    return 0;
}
