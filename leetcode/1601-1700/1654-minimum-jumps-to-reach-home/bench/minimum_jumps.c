// LeetCode #1654: Minimum Jumps to Reach Home -- the bench's C mirror: the
// ★ arm on 5000 random problems with a, b and x up to 2000 and up to 1000
// forbidden positions, all drawn first.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define PROBLEMS 5000

typedef struct {
    int32_t forbidden[1001];
    int count;
    int32_t a, b, x;
} Problem;

typedef struct {
    int64_t p;
    bool back;
    int32_t jumps;
} State;

static int32_t minimum_jumps(const int32_t *forbidden, int count, int32_t a32, int32_t b32, int32_t x32) {
    int64_t a = a32, b = b32, x = x32;
    int64_t furthest = 0;
    for (int i = 0; i < count; i++)
        if (forbidden[i] > furthest) furthest = forbidden[i];
    int64_t limit = (x > furthest ? x : furthest) + a + b;
    bool *blocked = calloc(limit + 1, sizeof(bool));
    for (int i = 0; i < count; i++) blocked[forbidden[i]] = true;
    bool (*seen)[2] = calloc(limit + 1, sizeof *seen);
    // every state enters the queue at most once
    State *queue = malloc(sizeof(State) * 2 * (limit + 1));
    size_t head = 0, tail = 0;
    queue[tail++] = (State){0, false, 0};
    seen[0][0] = true;
    int32_t answer = -1;
    while (head < tail) {
        State s = queue[head++];
        if (s.p == x) {
            answer = s.jumps;
            break;
        }
        int64_t forward = s.p + a;
        if (forward <= limit && !blocked[forward] && !seen[forward][0]) {
            seen[forward][0] = true;
            queue[tail++] = (State){forward, false, s.jumps + 1};
        }
        int64_t backward = s.p - b;
        if (!s.back && backward >= 0 && !blocked[backward] && !seen[backward][1]) {
            seen[backward][1] = true;
            queue[tail++] = (State){backward, true, s.jumps + 1};
        }
    }
    free(blocked);
    free(seen);
    free(queue);
    return answer;
}

static int64_t seed = 1654;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static Problem problems[PROBLEMS];
    for (int k = 0; k < PROBLEMS; k++) {
        Problem *pr = &problems[k];
        pr->a = (int32_t)(next_random() % 2000 + 1);
        pr->b = (int32_t)(next_random() % 2000 + 1);
        pr->x = (int32_t)(next_random() % 2001);
        int64_t m = next_random() % 1001;
        bool taken[2001] = {false};
        pr->count = 0;
        for (int64_t i = 0; i < m; i++) {
            int32_t f = (int32_t)(next_random() % 2000 + 1);
            if (f != pr->x && !taken[f]) {
                taken[f] = true;
                pr->forbidden[pr->count++] = f;
            }
        }
    }
    int64_t check = 0, total = 0, unreachable = 0;
    for (int k = 0; k < PROBLEMS; k++) {
        Problem *pr = &problems[k];
        int64_t answer = minimum_jumps(pr->forbidden, pr->count, pr->a, pr->b, pr->x);
        if (answer < 0) unreachable += 1;
        total += answer;
        check = (check * 31 + answer + 2) % 1000000007;
    }
    printf("5000 problems up to 2000: jumps sum to %lld, %lld unreachable, checksum %lld\n", (long long)total, (long long)unreachable, (long long)check);
    return 0;
}
