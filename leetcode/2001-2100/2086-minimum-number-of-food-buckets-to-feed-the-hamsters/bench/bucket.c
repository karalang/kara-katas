// LeetCode #2086: Minimum Number of Food Buckets to Feed the Hamsters -- C
// mirror of the ★ arm's benchmark (bucket.kara): the same street and 3000
// windows, each a pointer and a length into the street, served by the same
// greedy with a `calloc`'d array of buckets.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 2086;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t minimum_buckets(const char *cells, int64_t n) {
    bool *bucket = calloc(n > 0 ? n : 1, sizeof(bool));
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        if (cells[i] != 'H') continue;
        if (i > 0 && bucket[i - 1]) continue;
        if (i + 1 < n && cells[i + 1] == '.') {
            bucket[i + 1] = true;
            count++;
        } else if (i > 0 && cells[i - 1] == '.') {
            bucket[i - 1] = true;
            count++;
        } else {
            free(bucket);
            return -1;
        }
    }
    free(bucket);
    return count;
}

int main(void) {
    const char *pieces[] = {".", "H.", ".H", "H.H", ".H.H.", "..H"};
    char *street = malloc(1000000 + 8);
    int64_t len = 0;
    while (len < 1000000) {
        const char *p = pieces[next_random() % 6];
        size_t k = strlen(p);
        memcpy(street + len, p, k);
        len += k;
    }
    int64_t total = 0, impossible = 0, check = 0;
    for (int k = 0; k < 3000; k++) {
        int64_t hi = next_random();
        int64_t from = (hi * 32768 + next_random()) % 900000;
        int64_t a = minimum_buckets(street + from, 100000);
        if (a < 0) impossible++;
        else total += a;
        check = (check * 31 + a + 1) % 1000000007;
    }
    printf("3000 windows: sum %lld, %lld impossible, checksum %lld\n", (long long)total, (long long)impossible, (long long)check);
    free(street);
    return 0;
}
