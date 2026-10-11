// Benchmark for #370 -- mirror of range_addition.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t start, end, inc; } Update;

static int64_t *get_modified_array(int64_t length, const Update *updates, int64_t k) {
    int64_t *diff = calloc(length + 1, sizeof *diff);
    for (int64_t j = 0; j < k; j++) {
        diff[updates[j].start] += updates[j].inc;
        diff[updates[j].end + 1] -= updates[j].inc;
    }
    int64_t *out = malloc(length * sizeof *out);
    int64_t running = 0;
    for (int64_t i = 0; i < length; i++) {
        running += diff[i];
        out[i] = running;
    }
    free(diff);
    return out;
}

int main(void) {
    int64_t seed = 370, checksum = 0;
    Update *updates = malloc(10000 * sizeof *updates);
    for (int r = 0; r < 50; r++) {
        for (int j = 0; j < 10000; j++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t high = seed / 65536;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t a = (high * 32768 + seed / 65536) % 100000;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t high2 = seed / 65536;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t b = (high2 * 32768 + seed / 65536) % 100000;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t inc = (seed / 65536) % 2001 - 1000;
            updates[j] = (Update){a < b ? a : b, a < b ? b : a, inc};
        }
        int64_t *out = get_modified_array(100000, updates, 10000);
        for (int64_t i = 0; i < 100000; i++) checksum = (checksum * 31 + out[i] + 100000000) % 1000000007;
        free(out);
    }
    free(updates);
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
