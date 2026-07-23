#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long pos;
    long chk;
} Reader;

static long read4(const long *src, long m, Reader *rd) {
    long cnt = 0;
    while (cnt < 4 && rd->pos < m) {
        rd->pos++;
        cnt++;
    }
    return cnt;
}

static long read_n(const long *src, long m, Reader *rd, long want) {
    long total = 0;
    long acc = rd->chk;
    int eof = 0;
    while (total < want && !eof) {
        long start = rd->pos;
        long cnt = read4(src, m, rd);
        if (cnt == 0) {
            eof = 1;
        } else {
            long take = (total + cnt <= want) ? cnt : (want - total);
            for (long k = 0; k < take; k++) {
                acc = (acc * 1103515245 + src[start + k] + 1) & 2147483647;
            }
            total += take;
        }
    }
    rd->chk = acc;
    return total;
}

int main(void) {
    long size = 50000;
    long want = 7;
    long passes = 3200;

    long *src = malloc((size_t)size * sizeof(long));
    long state = 12345;
    for (long c = 0; c < size; c++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        src[c] = state % 26;
    }

    Reader rd = {0, 0};
    for (long pass = 0; pass < passes; pass++) {
        long idx = (pass * 131 + 7) % size;
        src[idx] = (src[idx] + 1) % 26;
        rd.pos = 0;
        int cont = 1;
        while (cont) {
            long got = read_n(src, size, &rd, want);
            if (got == 0) {
                cont = 0;
            }
        }
    }
    printf("%ld\n", rd.chk);
    return 0;
}
