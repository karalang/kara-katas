// LeetCode #1410 bench, C: the same walk, at each `&` the name up to the
// next `;` within seven characters looked up, workload and checksum as
// entity_parser.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *NAMES[] = {"&quot;", "&apos;", "&amp;", "&gt;", "&lt;", "&frasl;"};
static const char SYMBOLS[] = {'"', '\'', '&', '>', '<', '/'};

static size_t entity_parser(const char *text, size_t n, char *out) {
    size_t len = 0, i = 0;
    while (i < n) {
        if (text[i] == '&') {
            size_t w = i + 7 < n ? 7 : n - i;
            const char *semi = memchr(text + i, ';', w);
            if (semi) {
                size_t end = (size_t)(semi - (text + i));
                int hit = -1;
                for (int e = 0; e < 6; e++) {
                    if (strlen(NAMES[e]) == end + 1 && memcmp(NAMES[e], text + i, end + 1) == 0) {
                        hit = e;
                        break;
                    }
                }
                if (hit >= 0) {
                    out[len++] = SYMBOLS[hit];
                    i += end + 1;
                    continue;
                }
            }
        }
        out[len++] = text[i];
        i += 1;
    }
    return len;
}

int main(void) {
    static const char *pieces[] = {"a", "b", " ", "&", ";", "&quot;", "&apos;", "&amp;", "&gt;", "&lt;", "&frasl;",
                                   "&amp", "&gt", "&quot", "&ambassador;", "&lt;;", "&&", "amp;", "&frasl"};
    const int64_t np = sizeof(pieces) / sizeof(pieces[0]);
    int64_t seed = 1410, check = 0;
    char *pool = malloc(300100);
    size_t plen = 0;
    while (plen < 300000) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        const char *p = pieces[seed / 65536 % np];
        size_t l = strlen(p);
        memcpy(pool + plen, p, l);
        plen += l;
    }
    char *out = malloc(100000);
    for (int r = 0; r < 300; r++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        size_t start = (size_t)(seed / 65536 % ((int64_t)plen - 100000));
        size_t len = entity_parser(pool + start, 100000, out);
        int64_t sum = 0;
        for (size_t k = 0; k < len; k++) {
            sum += (unsigned char)out[k];
        }
        check = (check * 131 + (int64_t)len + sum) % 1000000007;
    }
    printf("300 windows of 10^5 characters: checksum %lld\n", (long long)check);
    free(pool);
    free(out);
    return 0;
}
