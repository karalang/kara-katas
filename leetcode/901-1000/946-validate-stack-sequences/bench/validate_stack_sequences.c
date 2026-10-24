// Benchmark: LeetCode #946 Validate Stack Sequences -- the ★ arm, the
// stack replayed, on sequences of 1000 values, LeetCode's longest.
// Mirrors validate_stack_sequences.kara, .rs, .py and go-seq/.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 1000
#define COUNT 20

// the stack in an array allocated for each call, as the other languages'
// growable arrays are
static bool validate_stack_sequences(const int64_t *pushed, const int64_t *popped, int64_t n) {
    int64_t *stack = malloc(sizeof(int64_t) * (size_t)n);
    int64_t top = 0, j = 0;
    for (int64_t i = 0; i < n; i++) {
        stack[top++] = pushed[i];
        while (top > 0 && stack[top - 1] == popped[j]) {
            top--;
            j++;
        }
    }
    free(stack);
    return j == n;
}

static int64_t seed = 946;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t pushes[COUNT][N];
static int64_t pops[COUNT][N];

int main(void) {
    const int64_t rounds = 2500, count = COUNT, n = N;
    // the values 0 to 1000 in a random order, the first 1000 pushed, and
    // the pops of a random run of pushes and pops, every second one with
    // two neighbouring pops swapped
    for (int64_t c = 0; c < count; c++) {
        int64_t all[1001];
        for (int64_t v = 0; v < 1001; v++) all[v] = v;
        for (int64_t i = 0; i < n; i++) {
            int64_t j = i + next_random() % (1001 - i);
            int64_t t = all[i];
            all[i] = all[j];
            all[j] = t;
        }
        for (int64_t i = 0; i < n; i++) pushes[c][i] = all[i];
        int64_t stack[N];
        int64_t top = 0, len = 0, i = 0;
        while (len < n) {
            if (i < n && (top == 0 || next_random() % 2 == 0)) {
                stack[top++] = pushes[c][i++];
            } else {
                pops[c][len++] = stack[--top];
            }
        }
        if (c % 2 == 1) {
            int64_t k = next_random() % (n - 1);
            int64_t t = pops[c][k];
            pops[c][k] = pops[c][k + 1];
            pops[c][k + 1] = t;
        }
    }
    int64_t fits = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t k = (r + i) % count;
            bool ok = validate_stack_sequences(pushes[k], pops[k], n);
            if (ok) fits++;
            check = (check * 31 + (ok ? 1 : 2)) % 1000000007;
        }
    }
    printf("%lld rounds over %lld pairs of sequences of %lld values: %lld fit, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)fits, (long long)check);
    return 0;
}
