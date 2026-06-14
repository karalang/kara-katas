/* LeetCode #405 bench harness — C calibration point (clang -O3, single-thread).
 *
 * Bitwise mask-and-shift hex render — same canonical algorithm as the Kara
 * mirror. Sequential string-building bench: concatenate TOTAL hex renderings
 * into one growing buffer, then byte-checksum it. Persisting the output defeats
 * render elision. Sink = byte-sum of the concatenated output.
 */
#include <stdio.h>
#include <stdlib.h>

#define TOTAL 4000000L

static const char HEX[16] = {'0','1','2','3','4','5','6','7',
                             '8','9','a','b','c','d','e','f'};

/* Append the hex rendering of num to the growable buffer at *blen. */
static void append_hex(char **buf, long *blen, long *bcap, long num) {
    unsigned long n = (unsigned long)(num & 0xffffffffL);
    char tmp[8];
    int len = 0;
    if (n == 0) {
        tmp[len++] = '0';
    } else {
        while (n > 0) {
            tmp[len++] = HEX[n & 0xf];
            n >>= 4;
        }
    }
    if (*blen + len > *bcap) {
        while (*blen + len > *bcap) {
            *bcap *= 2;
        }
        *buf = realloc(*buf, (size_t)*bcap);
    }
    for (int i = 0; i < len; i++) {
        (*buf)[*blen + i] = tmp[len - 1 - i];
    }
    *blen += len;
}

int main(void) {
    long bcap = 64, blen = 0;
    char *buf = malloc((size_t)bcap);
    for (long k = 0; k < TOTAL; k++) {
        long v = (k * 2654435761L) & 0xffffffffL;
        append_hex(&buf, &blen, &bcap, v);
    }
    long sum = 0;
    for (long i = 0; i < blen; i++) {
        sum += (long)(unsigned char)buf[i];
    }
    printf("%ld\n", sum);
    free(buf);
    return 0;
}
