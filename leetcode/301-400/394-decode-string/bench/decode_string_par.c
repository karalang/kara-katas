/* LeetCode #394 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR).
 *
 * Same iterative-stack decode as decode_string.c, but the ITERS reduction is
 * split across a fixed pool of _SC_NPROCESSORS_ONLN pthreads (spawn once, each
 * worker decodes a contiguous chunk into a private partial, then a join+merge).
 * This is the ceiling, not a competitor: raw OS threads with zero runtime /
 * work-stealing / GC overhead — how much parallel throughput Kāra's auto-par
 * leaves on the table. It is also the MOST parallel boilerplate of any mirror
 * (manual pthread_create/join + chunk + merge), against Kāra's zero. Same sink
 * (41600000) as every other mirror.
 *
 * Build: clang -O3 decode_string_par.c -o … -lpthread
 */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ENCODED "3[ab2[cd]ef]5[gh]2[ij3[kl]m]"
#define ITERS 800000

static int is_letter(char b) {
    return b != '[' && b != ']' && !(b >= '0' && b <= '9');
}

typedef struct {
    char *data;
    long len, cap;
} Str;

static void str_init(Str *s) {
    s->cap = 16;
    s->len = 0;
    s->data = malloc((size_t)s->cap);
}

static void str_append(Str *s, const char *p, long n) {
    if (s->len + n > s->cap) {
        while (s->len + n > s->cap) {
            s->cap *= 2;
        }
        s->data = realloc(s->data, (size_t)s->cap);
    }
    memcpy(s->data + s->len, p, (size_t)n);
    s->len += n;
}

static long decode_len(const char *s) {
    long n = (long)strlen(s);
    int scap = 16, scount = 0;
    char **str_stack = malloc((size_t)scap * sizeof(char *));
    long *str_len_stack = malloc((size_t)scap * sizeof(long));
    long *num_stack = malloc((size_t)scap * sizeof(long));
    Str cur;
    str_init(&cur);
    long k = 0;
    long i = 0;
    while (i < n) {
        char b = s[i];
        if (b >= '0' && b <= '9') {
            k = k * 10 + (b - '0');
            i++;
        } else if (b == '[') {
            if (scount >= scap) {
                scap *= 2;
                str_stack = realloc(str_stack, (size_t)scap * sizeof(char *));
                str_len_stack = realloc(str_len_stack, (size_t)scap * sizeof(long));
                num_stack = realloc(num_stack, (size_t)scap * sizeof(long));
            }
            str_stack[scount] = cur.data;
            str_len_stack[scount] = cur.len;
            num_stack[scount] = k;
            scount++;
            str_init(&cur);
            k = 0;
            i++;
        } else if (b == ']') {
            scount--;
            long count = num_stack[scount];
            char *prev = str_stack[scount];
            long prevlen = str_len_stack[scount];
            long newlen = prevlen + cur.len * count;
            char *buf = malloc((size_t)(newlen > 0 ? newlen : 1));
            memcpy(buf, prev, (size_t)prevlen);
            long off = prevlen;
            for (long r = 0; r < count; r++) {
                memcpy(buf + off, cur.data, (size_t)cur.len);
                off += cur.len;
            }
            free(prev);
            free(cur.data);
            cur.data = buf;
            cur.len = newlen;
            cur.cap = newlen > 0 ? newlen : 1;
            i++;
        } else {
            long j = i;
            while (j < n && is_letter(s[j])) {
                j++;
            }
            str_append(&cur, s + i, j - i);
            i = j;
        }
    }
    long result = cur.len;
    free(cur.data);
    free(str_stack);
    free(str_len_stack);
    free(num_stack);
    return result;
}

typedef struct {
    long start, end;
    long partial;
} Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    long s = 0;
    for (long it = w->start; it < w->end; it++) {
        s += decode_len(ENCODED);
    }
    w->partial = s;
    return NULL;
}

int main(void) {
    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    long chunk = ITERS / nworkers;

    for (long w = 0; w < nworkers; w++) {
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
    return 0;
}
