/* C mirror of the utf8-codepoints decode bench — same algorithm, same sink. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MODULUS 1000000007LL
#define REPEAT 9523LL
#define ITERS 400LL

static long utf8_byte_len(unsigned char lead) {
    if (lead < 0x80) return 1;
    else if (lead >= 0xC0 && lead <= 0xDF) return 2;
    else if (lead >= 0xE0 && lead <= 0xEF) return 3;
    else if (lead >= 0xF0 && lead <= 0xF7) return 4;
    else return 1;
}

/* Encode one Unicode scalar to UTF-8, append to buf at *pos. */
static void enc(unsigned char *buf, long *pos, unsigned int cp) {
    if (cp < 0x80) {
        buf[(*pos)++] = (unsigned char)cp;
    } else if (cp < 0x800) {
        buf[(*pos)++] = (unsigned char)(0xC0 | (cp >> 6));
        buf[(*pos)++] = (unsigned char)(0x80 | (cp & 0x3F));
    } else if (cp < 0x10000) {
        buf[(*pos)++] = (unsigned char)(0xE0 | (cp >> 12));
        buf[(*pos)++] = (unsigned char)(0x80 | ((cp >> 6) & 0x3F));
        buf[(*pos)++] = (unsigned char)(0x80 | (cp & 0x3F));
    } else {
        buf[(*pos)++] = (unsigned char)(0xF0 | (cp >> 18));
        buf[(*pos)++] = (unsigned char)(0x80 | ((cp >> 12) & 0x3F));
        buf[(*pos)++] = (unsigned char)(0x80 | ((cp >> 6) & 0x3F));
        buf[(*pos)++] = (unsigned char)(0x80 | (cp & 0x3F));
    }
}

int main(void) {
    unsigned int cps[] = {
        0x61,0x62,0x63,0x20,0x31,0x32,0x33,0x20,
        0xe9,0xf1,0x3b1,0x3b2,0x434,0x436,
        0x65e5,0x672c,0x1d11e,0x1f980,0x20
    };
    int ncp = sizeof(cps)/sizeof(cps[0]);
    /* base byte length, then full buffer. */
    long base_bytes = 0;
    for (int j = 0; j < ncp; j++) {
        unsigned int c = cps[j];
        base_bytes += (c < 0x80) ? 1 : (c < 0x800) ? 2 : (c < 0x10000) ? 3 : 4;
    }
    long n = base_bytes * REPEAT;
    unsigned char *buf = (unsigned char*)malloc(n + 4);
    long pos = 0;
    for (long r = 0; r < REPEAT; r++)
        for (int j = 0; j < ncp; j++) enc(buf, &pos, cps[j]);

    long long sink = 0, count = 0;
    for (long t = 0; t < ITERS; t++) {
        long i = 0;
        while (i < n) {
            unsigned char lead = buf[i];
            long len = utf8_byte_len(lead);
            long long cp = (len == 1) ? lead
                : (len == 2) ? (lead & 0x1F)
                : (len == 3) ? (lead & 0x0F)
                : (lead & 0x07);
            long k = 1;
            while (k < len && i + k < n) {
                cp = (cp << 6) | (buf[i + k] & 0x3F);
                k++;
            }
            sink = (sink + cp) % MODULUS;
            count++;
            i += len;
        }
    }
    printf("%lld %lld\n", count, sink);
    free(buf);
    return 0;
}
