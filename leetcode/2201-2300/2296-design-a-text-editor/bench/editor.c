// LeetCode #2296: Design a Text Editor -- the bench, the ★ arm in C. Two
// stacks of letters: `left` holds the text before the cursor in order,
// `right` the text after it reversed. Adding pushes on `left`, deleting
// pops from it, and a move pops from one stack onto the other.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
    size_t len, cap;
} Stack;

static void push(Stack *s, char c) {
    if (s->len == s->cap) {
        s->cap = s->cap ? s->cap * 2 : 16;
        s->data = realloc(s->data, s->cap);
    }
    s->data[s->len++] = c;
}

typedef struct {
    Stack left, right;
} TextEditor;

static void add_text(TextEditor *e, const char *text) {
    for (const char *p = text; *p; p++) push(&e->left, *p);
}

static int64_t delete_text(TextEditor *e, int64_t k) {
    int64_t n = k < (int64_t)e->left.len ? k : (int64_t)e->left.len;
    e->left.len -= (size_t)n;
    return n;
}

// the last ten letters before the cursor into `out`, NUL-terminated
static void tail(const TextEditor *e, char *out) {
    size_t n = e->left.len < 10 ? e->left.len : 10;
    memcpy(out, e->left.data + e->left.len - n, n);
    out[n] = 0;
}

static void cursor_left(TextEditor *e, int64_t k, char *out) {
    for (int64_t i = 0; i < k && e->left.len > 0; i++) push(&e->right, e->left.data[--e->left.len]);
    tail(e, out);
}

static void cursor_right(TextEditor *e, int64_t k, char *out) {
    for (int64_t i = 0; i < k && e->right.len > 0; i++) push(&e->left, e->right.data[--e->right.len]);
    tail(e, out);
}

typedef struct {
    int64_t kind, k;
    char text[41];
} Call;

static int64_t seed = 2296;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

#define EDITORS 10
#define CALLS 20000

int main(void) {
    static Call editors[EDITORS][CALLS];
    for (int e = 0; e < EDITORS; e++) {
        for (int c = 0; c < CALLS; c++) {
            Call *call = &editors[e][c];
            call->kind = next_random() % 4;
            call->k = next_random() % 40 + 1;
            call->text[0] = 0;
            if (call->kind == 0) {
                for (int64_t i = 0; i < call->k; i++) call->text[i] = (char)('a' + next_random() % 26);
                call->text[call->k] = 0;
            }
        }
    }
    int64_t check = 0;
    char answer[32];
    for (int pass = 0; pass < 10; pass++) {
        for (int e = 0; e < EDITORS; e++) {
            TextEditor ed = {{0}, {0}};
            for (int c = 0; c < CALLS; c++) {
                Call *call = &editors[e][c];
                if (call->kind == 0) {
                    add_text(&ed, call->text);
                    continue;
                } else if (call->kind == 1) {
                    snprintf(answer, sizeof answer, "%lld", (long long)delete_text(&ed, call->k));
                } else if (call->kind == 2) {
                    cursor_left(&ed, call->k, answer);
                } else {
                    cursor_right(&ed, call->k, answer);
                }
                for (const char *p = answer; *p; p++) check = (check * 131 + (unsigned char)*p) % 1000000007;
                check = (check * 131 + 1) % 1000000007;
            }
            free(ed.left.data);
            free(ed.right.data);
        }
    }
    printf("10 passes over 10 editors of 2 * 10^4 calls: checksum %lld\n", (long long)check);
    return 0;
}
