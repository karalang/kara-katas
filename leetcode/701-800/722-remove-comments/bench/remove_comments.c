/* LeetCode #722 bench harness — C calibration point (clang -O3, single-thread).
 *
 * Byte-indexed segment-slicing — same canonical algorithm as the Kara mirror:
 * scan each line's bytes, classify `/` `*` markers, and memcpy each surviving
 * run into the line buffer as one slice (no per-char copy). Each completed line
 * is heap-allocated into a result array (mirroring the Vec[String] the other
 * mirrors build) before its length is summed and freed. Sink = 30960000.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define REPS 60
#define ITERS 4000
#define TLEN 10

static const char *TEMPLATE[TLEN] = {
    "int main() {            // entry point",
    "  int a = 1; /* inline */ int b = 2;",
    "  /* a multi-line",
    "     block comment that",
    "     spans several lines */ int c = a + b;",
    "  // a full line comment",
    "  int e = c * 3;        /* trailing block */",
    "  int d = a /* x */ + b /* y */ + c;",
    "  return d * 2;//done",
    "}",
};

/* Append line[a..b) to the growable buffer. */
static void flush(char **buffer, int *blen, int *bcap, const char *line, int a, int b) {
    int add = b - a;
    if (add <= 0) {
        return;
    }
    if (*blen + add > *bcap) {
        while (*blen + add > *bcap) {
            *bcap *= 2;
        }
        *buffer = realloc(*buffer, (size_t)*bcap);
    }
    memcpy(*buffer + *blen, line + a, (size_t)add);
    *blen += add;
}

static long pass_len(const char **lines, int nlines) {
    int rcap = 16, rcount = 0;
    char **result = malloc((size_t)rcap * sizeof(char *));
    int bcap = 64, blen = 0;
    char *buffer = malloc((size_t)bcap);
    int in_block = 0;

    for (int li = 0; li < nlines; li++) {
        const char *line = lines[li];
        int n = (int)strlen(line);
        int seg_start = 0;
        int i = 0;
        while (i < n) {
            if (!in_block) {
                if (i + 1 < n && line[i] == '/' && line[i + 1] == '/') {
                    flush(&buffer, &blen, &bcap, line, seg_start, i);
                    seg_start = n;
                    break;
                } else if (i + 1 < n && line[i] == '/' && line[i + 1] == '*') {
                    flush(&buffer, &blen, &bcap, line, seg_start, i);
                    in_block = 1;
                    i += 2;
                } else {
                    i++;
                }
            } else {
                if (i + 1 < n && line[i] == '*' && line[i + 1] == '/') {
                    in_block = 0;
                    i += 2;
                    seg_start = i;
                } else {
                    i++;
                }
            }
        }
        if (!in_block) {
            flush(&buffer, &blen, &bcap, line, seg_start, n);
            if (blen > 0) {
                char *s = malloc((size_t)blen + 1);
                memcpy(s, buffer, (size_t)blen);
                s[blen] = '\0';
                if (rcount >= rcap) {
                    rcap *= 2;
                    result = realloc(result, (size_t)rcap * sizeof(char *));
                }
                result[rcount++] = s;
                blen = 0;
            }
        }
    }

    long total = 0;
    for (int k = 0; k < rcount; k++) {
        total += (long)strlen(result[k]);
        free(result[k]);
    }
    free(result);
    free(buffer);
    return total;
}

int main(void) {
    int nlines = REPS * TLEN;
    const char **lines = malloc((size_t)nlines * sizeof(char *));
    int idx = 0;
    for (int r = 0; r < REPS; r++) {
        for (int t = 0; t < TLEN; t++) {
            lines[idx++] = TEMPLATE[t];
        }
    }
    long sum = 0;
    for (int it = 0; it < ITERS; it++) {
        sum += pass_len(lines, nlines);
    }
    printf("%ld\n", sum);
    free(lines);
    return 0;
}
