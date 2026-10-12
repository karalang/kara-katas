// Benchmark for #379: mirror of phone_directory.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t size;
    int64_t *free;
} PhoneDirectory;

static PhoneDirectory dir_new(int64_t max_numbers) {
    int64_t size = 1;
    while (size < max_numbers) size *= 2;
    int64_t *free = calloc((size_t)(2 * size), sizeof *free);
    for (int64_t n = 0; n < max_numbers; n++) free[size + n] = 1;
    for (int64_t i = size - 1; i >= 1; i--) free[i] = free[2 * i] + free[2 * i + 1];
    return (PhoneDirectory){size, free};
}

static void dir_set(PhoneDirectory *d, int64_t number, int64_t value) {
    int64_t i = d->size + number;
    d->free[i] = value;
    i /= 2;
    while (i >= 1) {
        d->free[i] = d->free[2 * i] + d->free[2 * i + 1];
        i /= 2;
    }
}

static int64_t dir_get(PhoneDirectory *d) {
    if (d->free[1] == 0) return -1;
    int64_t i = 1;
    while (i < d->size) i = d->free[2 * i] > 0 ? 2 * i : 2 * i + 1;
    int64_t number = i - d->size;
    dir_set(d, number, 0);
    return number;
}

static int dir_check(const PhoneDirectory *d, int64_t number) { return d->free[d->size + number] == 1; }

static void dir_release(PhoneDirectory *d, int64_t number) { dir_set(d, number, 1); }

int main(void) {
    const int64_t m = 10000;
    PhoneDirectory d = dir_new(m);
    int64_t seed = 379, checksum = 0;
    for (int64_t q = 0; q < 20000000; q++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t op = (seed / 65536) % 4;
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t x = (seed / 65536) % m;
        int64_t v;
        if (op == 0)
            v = dir_get(&d) + 1;
        else if (op == 1)
            v = dir_check(&d, x) ? 1 : 0;
        else {
            dir_release(&d, x);
            v = 0;
        }
        checksum = (checksum * 31 + v) % 1000000007;
    }
    free(d.free);
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
