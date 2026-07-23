#include <stdio.h>
#include <stdlib.h>

static int is_upper(int b) { return b >= 'A' && b <= 'Z'; }
static int is_lower(int b) { return b >= 'a' && b <= 'z'; }
static int is_digit(int b) { return b >= '0' && b <= '9'; }

static long draw_hi(long *state) {
    *state = (*state * 1103515245L + 12345L) & 2147483647L;
    return *state >> 16;
}

int main(void) {
    long num_chunks = 20000, passes = 400, id_range = 24;

    long capbuf = num_chunks * 16 + 16;
    unsigned char *buf = malloc(capbuf);
    long *dpos = malloc(capbuf * sizeof(long));
    long blen = 0, ndig = 0;
    long state = 12345;

    for (long ch = 0; ch < num_chunks; ch++) {
        long tt = draw_hi(&state) % 5;
        // element / mult emitters (inline)
        #define ELEM() do { \
            long du = draw_hi(&state); \
            buf[blen++] = (unsigned char)('A' + du % 6); \
            if ((du / 6) % 2 == 0) { long dl = draw_hi(&state); buf[blen++] = (unsigned char)('a' + dl % 3); } \
            long dc = draw_hi(&state); buf[blen++] = (unsigned char)('1' + dc % 9); dpos[ndig++] = blen - 1; \
        } while (0)
        #define MULT() do { long dm = draw_hi(&state); buf[blen++] = (unsigned char)('0' + 2 + dm % 8); dpos[ndig++] = blen - 1; } while (0)
        if (tt == 0) { ELEM(); }
        else if (tt == 1) { ELEM(); ELEM(); }
        else if (tt == 2) { buf[blen++] = '('; ELEM(); ELEM(); buf[blen++] = ')'; MULT(); }
        else if (tt == 3) { buf[blen++] = '('; ELEM(); buf[blen++] = '('; ELEM(); ELEM(); buf[blen++] = ')'; MULT(); buf[blen++] = ')'; MULT(); }
        else { buf[blen++] = '('; ELEM(); ELEM(); ELEM(); buf[blen++] = ')'; MULT(); }
    }

    long n = blen, ndg = ndig;
    long max_emit = 3 * num_chunks + 16;
    long *nid = malloc(max_emit * sizeof(long));
    long *cnt = malloc(max_emit * sizeof(long));
    long *pst = malloc(max_emit * sizeof(long));
    long *mapc = malloc(id_range * sizeof(long));

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long pos = dpos[p % ndg];
        buf[pos] = (unsigned char)('1' + (((long)buf[pos] - '1' + 1) % 9));

        long ne = 0, ps = 0, i = 0;
        while (i < n) {
            unsigned char b = buf[i];
            if (b == '(') {
                pst[ps++] = ne;
                i++;
            } else if (b == ')') {
                i++;
                long mult = 0; int have = 0;
                while (i < n && is_digit(buf[i])) { mult = mult * 10 + (buf[i] - '0'); have = 1; i++; }
                if (!have) mult = 1;
                long start = pst[--ps];
                for (long k = start; k < ne; k++) cnt[k] *= mult;
            } else if (is_upper(b)) {
                long up = b - 'A';
                i++;
                long low = 0;
                if (i < n && is_lower(buf[i])) { low = (buf[i] - 'a') + 1; i++; }
                long id = up * 4 + low;
                long c = 0; int have = 0;
                while (i < n && is_digit(buf[i])) { c = c * 10 + (buf[i] - '0'); have = 1; i++; }
                if (!have) c = 1;
                nid[ne] = id; cnt[ne] = c; ne++;
            } else {
                i++;
            }
        }

        for (long z = 0; z < id_range; z++) mapc[z] = 0;
        for (long e = 0; e < ne; e++) mapc[nid[e]] += cnt[e];
        long checksum = 0;
        for (long z = 0; z < id_range; z++) checksum += z * mapc[z];
        sink += checksum;
    }
    printf("%ld\n", sink);
    free(buf); free(dpos); free(nid); free(cnt); free(pst); free(mapc);
    return 0;
}
