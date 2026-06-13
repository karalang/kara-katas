/* LeetCode #722 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR).
 *
 * Same byte-indexed segment-slicing remove_comments as remove_comments.c, but
 * the ITERS reduction is split across a fixed pool of _SC_NPROCESSORS_ONLN
 * pthreads (spawn once, each worker runs a contiguous chunk into a private
 * partial, then join+merge). The ceiling, not a competitor: raw OS threads with
 * zero runtime/work-stealing/GC overhead — how much parallel throughput Kāra's
 * auto-par leaves on the table vs metal, and the most parallel boilerplate of
 * any mirror against Kāra's zero. Same sink (30960000) as every other mirror.
 *
 * Build: clang -O3 remove_comments_par.c -o … -lpthread
 */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

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

typedef struct {
    const char **lines;
    int nlines;
    long start, end;
    long partial;
} Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    long s = 0;
    for (long it = w->start; it < w->end; it++) {
        s += pass_len(w->lines, w->nlines);
    }
    w->partial = s;
    return NULL;
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

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    long chunk = ITERS / nworkers;

    for (long w = 0; w < nworkers; w++) {
        works[w].lines = lines;
        works[w].nlines = nlines;
        works[w].start = w * chunk;
        works[w].end = (w == nworkers - 1) ? ITERS : (w + 1) * chunk;
        works[w].partial = 0;
        pthread_create(&threads[w], NULL, worker, &works[w]);
    }

    long total = 0;
    for (long w = 0; w < nworkers; w++) {
        pthread_join(threads[w], NULL);
        total += works[w].partial;
    }

    printf("%ld\n", total);
    free(threads);
    free(works);
    free(lines);
    return 0;
}
