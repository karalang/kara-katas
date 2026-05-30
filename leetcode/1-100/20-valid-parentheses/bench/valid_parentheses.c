/*
 * Benchmark workload — Valid Parentheses (LeetCode #20).
 * C mirror of bench/valid_parentheses.kara. A small grown-from-empty
 * dynamic byte buffer (doubling realloc) mirrors Kāra's `Vec.new()`
 * push traffic; the validator's stack is the same dynamic-array shape.
 * Same depth/K, type rotation, 1/7 corruption, and count-valid sink.
 * Built with `clang -O3` — the LLVM-backend floor for the seq lane.
 * See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

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

int main(void) {
    const int64_t depth = 1000;
    const int64_t k_iters = 500000;

    int64_t count = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        int64_t kind = k % 3;
        int corrupt = (k % 7) == 0;
        Buf buf = build_brackets(depth, kind, corrupt);
        if (is_valid_bytes(buf.data, buf.len)) {
            count++;
        }
        free(buf.data);
    }
    printf("%lld\n", (long long)count);
    return 0;
}
