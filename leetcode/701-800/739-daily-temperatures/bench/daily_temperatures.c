// LeetCode #739: Daily Temperatures -- a stack of colder days.
// Benchmark mirror of the Kara star arm: walk the days keeping a stack
// of the days still waiting; a day warmer than the top answers it, and
// every day under it that it is warmer than, and then waits itself.
// The answer and the stack are growable arrays, as in the Kara arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *data;
    int64_t len, cap;
} Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap * sizeof(int64_t));
    }
    v->data[v->len++] = x;
}

static Vec daily_temperatures(const int64_t *temperatures, int64_t n) {
    Vec answer = {0, 0, 0};
    for (int64_t i = 0; i < n; i++) push(&answer, 0);
    Vec waiting = {0, 0, 0};
    for (int64_t i = 0; i < n; i++) {
        while (waiting.len > 0 && temperatures[waiting.data[waiting.len - 1]] < temperatures[i]) {
            int64_t j = waiting.data[--waiting.len];
            answer.data[j] = i - j;
        }
        push(&waiting, i);
    }
    free(waiting.data);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 739, n = 100000, total = 0;
    int64_t *t = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) t[i] = 30 + next_random(&seed) % 71;
    for (int r = 0; r < 300; r++) {
        for (int k = 0; k < 100; k++) {
            int64_t a = next_random(&seed);
            int64_t b = next_random(&seed);
            int64_t j = (a * 32768 + b) % n;
            t[j] = 30 + next_random(&seed) % 71;
        }
        Vec answer = daily_temperatures(t, n);
        for (int64_t i = 0; i < answer.len; i++) total += answer.data[i];
        free(answer.data);
    }
    printf("300 rounds of 100000 days: %lld days waited in all\n", (long long)total);
    free(t);
    return 0;
}
