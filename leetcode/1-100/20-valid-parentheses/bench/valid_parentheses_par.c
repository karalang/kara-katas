/* LeetCode #20 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR,
 * valid_parentheses). Same grown-from-empty byte-buffer build + dynamic-
 * array stack validate; the K=500k count-reduction split across a fixed
 * pool of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge).
 * Raw OS threads, no runtime — the ceiling auto-par is measured against.
 * Sink matches the kara/rust/c/go mirrors.
 * Build: clang -O3 valid_parentheses_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

typedef struct {
    uint8_t *data;
    int64_t len;
    int64_t cap;
} Buf;

static void buf_push(Buf *b, uint8_t v) {
    if (b->len == b->cap) {
        b->cap = b->cap ? b->cap * 2 : 8;
        b->data = (uint8_t *)realloc(b->data, (size_t)b->cap);
    }
    b->data[b->len++] = v;
}

static int is_valid_bytes(const uint8_t *bytes, int64_t n) {
    Buf stack = {NULL, 0, 0};
    int valid = 1;
    for (int64_t i = 0; i < n; i++) {
        uint8_t b = bytes[i];
        if (b == '(' || b == '[' || b == '{') {
            uint8_t closer = b == '(' ? ')' : (b == '[' ? ']' : '}');
            buf_push(&stack, closer);
        } else {
            if (stack.len == 0) {
                valid = 0;
                break;
            }
            uint8_t top = stack.data[--stack.len];
            if (top != b) {
                valid = 0;
                break;
            }
        }
    }
    if (valid && stack.len != 0) {
        valid = 0;
    }
    free(stack.data);
    return valid;
}

static Buf build_brackets(int64_t depth, int64_t kind, int corrupt) {
    uint8_t op = '(', cl = ')', wrong = ']';
    if (kind == 1) {
        op = '[';
        cl = ']';
        wrong = ')';
    } else if (kind == 2) {
        op = '{';
        cl = '}';
        wrong = ')';
    }
    Buf buf = {NULL, 0, 0};
    for (int64_t i = 0; i < depth; i++) buf_push(&buf, op);
    for (int64_t i = 0; i < depth - 1; i++) buf_push(&buf, cl);
    buf_push(&buf, corrupt ? wrong : cl);
    return buf;
}

#define DEPTH 1000LL
#define K_ITERS 500000LL

typedef struct {
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t kind = k % 3;
        int corrupt = (k % 7) == 0;
        Buf buf = build_brackets(DEPTH, kind, corrupt);
        if (is_valid_bytes(buf.data, buf.len)) {
            s++;
        }
        free(buf.data);
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = K_ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].start = (int64_t)w * chunk;
        works[w].end = (w == nworkers - 1) ? K_ITERS : ((int64_t)w + 1) * chunk;
        works[w].partial = 0;
        pthread_create(&threads[w], NULL, worker, &works[w]);
    }
    int64_t total = 0;
    for (long w = 0; w < nworkers; w++) {
        pthread_join(threads[w], NULL);
        total += works[w].partial;
    }
    printf("%lld\n", (long long)total);
    free(threads);
    free(works);
    return 0;
}
