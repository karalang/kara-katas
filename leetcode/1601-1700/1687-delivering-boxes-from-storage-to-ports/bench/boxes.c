// LeetCode #1687: Delivering Boxes from Storage to Ports -- the bench's C
// mirror: the ★ arm on 50 random problems of 100000 boxes, all drawn first,
// each answered 20 times. The deque is an array with a head and a tail,
// since each start goes in once; the tables are malloc'd per answer, as
// the other languages build new vectors.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 50
#define SIZE 100000
#define ROUNDS 20

static int32_t deliver(const int32_t (*boxes)[2], int64_t n, int32_t max_boxes, int32_t max_weight) {
    int32_t *changes = calloc((size_t)n, sizeof *changes);
    int64_t *weight = calloc((size_t)n + 1, sizeof *weight);
    for (int64_t k = 0; k < n; k++) {
        weight[k + 1] = weight[k] + boxes[k][1];
        if (k > 0) changes[k] = changes[k - 1] + (boxes[k][0] != boxes[k - 1][0] ? 1 : 0);
    }
    int32_t *trips = calloc((size_t)n + 1, sizeof *trips);
    int64_t *starts = malloc((size_t)n * sizeof *starts);
    int64_t head = 0, tail = 0;
    for (int64_t i = 1; i <= n; i++) {
        int64_t j = i - 1;
        int32_t cost = trips[j] - changes[j];
        while (tail > head && trips[starts[tail - 1]] - changes[starts[tail - 1]] >= cost) tail--;
        starts[tail++] = j;
        while (tail > head && (i - starts[head] > max_boxes || weight[i] - weight[starts[head]] > max_weight)) head++;
        int64_t front = starts[head];
        trips[i] = trips[front] - changes[front] + changes[i - 1] + 2;
    }
    int32_t answer = trips[n];
    free(changes);
    free(weight);
    free(trips);
    free(starts);
    return answer;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1687;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    static int32_t boxes[COUNT][SIZE][2];
    static int32_t max_boxes[COUNT], max_weight[COUNT];
    for (int c = 0; c < COUNT; c++) {
        int64_t ports_count = next_random() % 100 + 1;
        max_boxes[c] = (int32_t)(next_random() % 1000 + 1);
        max_weight[c] = (int32_t)(wide() % 99001 + 1000);
        for (int i = 0; i < SIZE; i++) {
            boxes[c][i][0] = (int32_t)(next_random() % ports_count + 1);
            boxes[c][i][1] = (int32_t)(next_random() % 1000 + 1);
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int32_t answer = deliver((const int32_t(*)[2])boxes[c], SIZE, max_boxes[c], max_weight[c]);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d problems of %d boxes, %d rounds: %lld trips, checksum %lld\n", COUNT, SIZE, ROUNDS, (long long)total, (long long)check);
    return 0;
}
