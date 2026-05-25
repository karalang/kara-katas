// Benchmark workload — C mirror of simplify.kara, single-threaded.
//
// Same N=8 inputs, K=1_000_000 iters cycled by k % N. Sink is the
// sum of the simplified-output string lengths (i64). Each iteration
// materializes the simplified path into a local buffer (same shape
// of work as the kara/rust/go/py mirrors) and reads the length back
// off the result.
//
// Stack-allocated bounded buffers (MAX_LEN = 64 covers every input)
// — no malloc on the hot path. Hand-rolled scalar baseline, the
// lower-floor reference shape per BENCH.md.

#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define MAX_LEN  64
#define MAX_COMPS 32

static int64_t simplify(const char *s, char *out) {
    int64_t n = (int64_t)strlen(s);

    int64_t starts[MAX_COMPS];
    int64_t ends[MAX_COMPS];
    int64_t top = 0;

    int64_t i = 0;
    while (i < n) {
        while (i < n && s[i] == '/') i++;
        if (i >= n) break;
        int64_t j = i;
        while (j < n && s[j] != '/') j++;
        int64_t len = j - i;

        int is_dot    = (len == 1) && s[i] == '.';
        int is_dotdot = (len == 2) && s[i] == '.' && s[i + 1] == '.';

        if (is_dot) {
            // skip
        } else if (is_dotdot) {
            if (top > 0) top--;
        } else {
            starts[top] = i;
            ends[top] = j;
            top++;
        }
        i = j;
    }

    if (top == 0) {
        out[0] = '/';
        out[1] = '\0';
        return 1;
    }

    int64_t pos = 0;
    for (int64_t k = 0; k < top; k++) {
        out[pos++] = '/';
        int64_t a = starts[k];
        int64_t b = ends[k];
        for (int64_t p = a; p < b; p++) {
            out[pos++] = s[p];
        }
    }
    out[pos] = '\0';
    return pos;
}

int main(void) {
    const char *inputs[8] = {
        "/home/",
        "/home/user/Documents/../Pictures",
        "/.../a/../b/c/../d/./",
        "/a/b/c/../..",
        "/a//b////c/d//././/..",
        "/abc_123",
        "/a/b/../c/../../d",
        "/...hidden",
    };
    int64_t n = 8;
    int64_t k_iters = 1000000;

    char out[MAX_LEN];
    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        sum += simplify(inputs[k % n], out);
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
