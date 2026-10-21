// Benchmark for #832: Flipping an Image -- the ★ arm (two pointers in place).
//
// Mirrors flip_and_invert_image.kara: each row is flipped and inverted in
// one walk from both ends, the middle cell of an odd row only inverted.
// An image is an array of rows, each allocated on its own, as the Kāra
// program's Vec[Vec[i64]] is.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t **rows;
    int64_t n;
} image_t;

static void flip_and_invert_image(image_t *img) {
    int64_t n = img->n;
    for (int64_t r = 0; r < n; r++) {
        int64_t *row = img->rows[r];
        int64_t i = 0, j = n - 1;
        while (i < j) {
            int64_t left = row[i];
            row[i] = 1 - row[j];
            row[j] = 1 - left;
            i++;
            j--;
        }
        if (i == j) row[i] = 1 - row[i];
    }
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 4000000;
    int64_t seed = 832;
    image_t images[64];
    for (int64_t g = 0; g < count; g++) {
        int64_t n = 17 + g % 4;
        images[g].n = n;
        images[g].rows = malloc((size_t)n * sizeof(int64_t *));
        for (int64_t r = 0; r < n; r++) {
            images[g].rows[r] = malloc((size_t)n * sizeof(int64_t));
            for (int64_t c = 0; c < n; c++) images[g].rows[r][c] = next_random(&seed) % 2;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        image_t *img = &images[round % count];
        flip_and_invert_image(img);
        int64_t *row = img->rows[round / count % img->n];
        for (int64_t c = 0; c < img->n; c++) {
            total += row[c];
            checksum = (checksum * 3 + row[c]) % 1000000007;
        }
    }
    printf("%lld rounds of %lld images: %lld ones, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) {
        for (int64_t r = 0; r < images[g].n; r++) free(images[g].rows[r]);
        free(images[g].rows);
    }
    return 0;
}
