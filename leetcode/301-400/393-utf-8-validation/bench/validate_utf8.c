#include <stdio.h>
#include <stdlib.h>

static long lead_len(unsigned char b) {
    if ((b & 0x80) == 0x00) return 1;
    else if ((b & 0xE0) == 0xC0) return 2;
    else if ((b & 0xF0) == 0xE0) return 3;
    else if ((b & 0xF8) == 0xF0) return 4;
    else return 0;
}

static int is_continuation(unsigned char b) {
    return (b & 0xC0) == 0x80;
}

static int validate_window(const unsigned char *data, long base, long w) {
    long end = base + w;
    long i = base;
    while (i < end) {
        long need = lead_len(data[i]);
        if (need == 0) return 0;
        if (i + need > end) return 0;
        for (long k = 1; k < need; k++) {
            if (!is_continuation(data[i + k])) return 0;
        }
        i += need;
    }
    return 1;
}

int main(void) {
    long records = 40000, w = 32, passes = 60;
    long total = records * w;

    unsigned char *data = malloc(total);
    for (long z = 0; z < total; z++) data[z] = 0;

    long state = 12345;
    for (long rec = 0; rec < records; rec++) {
        long base = rec * w;
        long filled = 0;
        while (filled < w) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long r = state >> 16;
            long cat = r % 100;
            long sub = r / 100;
            long rem = w - filled;
            if (cat < 8) {
                data[base + filled] = (unsigned char)(128 + (sub % 64));
                filled += 1;
            } else if (cat < 60 || rem < 2) {
                data[base + filled] = (unsigned char)(sub % 128);
                filled += 1;
            } else if (cat < 80 || rem < 3) {
                data[base + filled]     = (unsigned char)(192 + (sub % 32));
                data[base + filled + 1] = (unsigned char)(128 + (sub % 64));
                filled += 2;
            } else if (cat < 93 || rem < 4) {
                data[base + filled]     = (unsigned char)(224 + (sub % 16));
                data[base + filled + 1] = (unsigned char)(128 + (sub % 64));
                data[base + filled + 2] = (unsigned char)(128 + (sub % 64));
                filled += 3;
            } else {
                data[base + filled]     = (unsigned char)(240 + (sub % 8));
                data[base + filled + 1] = (unsigned char)(128 + (sub % 64));
                data[base + filled + 2] = (unsigned char)(128 + (sub % 64));
                data[base + filled + 3] = (unsigned char)(128 + (sub % 64));
                filled += 4;
            }
        }
    }

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long idx = (p * 40009) % total;
        data[idx] = (unsigned char)(255 - (long)data[idx]);

        long count = 0;
        for (long rec = 0; rec < records; rec++) {
            if (validate_window(data, rec * w, w)) count++;
        }
        sink += count;
    }
    printf("%ld\n", sink);
    free(data);
    return 0;
}
