// LeetCode #2502: Design Memory Allocator -- C mirror of the benchmark
// (alloc.kara): the same sessions, calls and checksum; every unit's owner
// in a calloc'd array.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2502;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t allocate(int64_t *memory, int64_t n, int64_t size, int64_t m_id) {
    int64_t run = 0;
    for (int64_t i = 0; i < n; i++) {
        if (memory[i] == 0) {
            run++;
            if (run == size) {
                int64_t start = i + 1 - size;
                for (int64_t j = start; j <= i; j++) memory[j] = m_id;
                return start;
            }
        } else {
            run = 0;
        }
    }
    return -1;
}

static int64_t free_memory(int64_t *memory, int64_t n, int64_t m_id) {
    int64_t freed = 0;
    for (int64_t i = 0; i < n; i++) {
        if (memory[i] == m_id) {
            memory[i] = 0;
            freed++;
        }
    }
    return freed;
}

int main(void) {
    const int64_t sessions = 400, n = 1000;
    int64_t check = 0;
    for (int64_t s = 0; s < sessions; s++) {
        int64_t *memory = calloc(n, sizeof(int64_t));
        for (int k = 0; k < 1000; k++) {
            int64_t r;
            if ((next_random() + check) % 3 < 2) {
                int64_t size = next_random() % 20 + 1;
                r = allocate(memory, n, size, next_random() % 50 + 1);
            } else {
                r = free_memory(memory, n, next_random() % 50 + 1);
            }
            check = (check * 31 + r + 1 + s) % 1000000007;
        }
        free(memory);
    }
    printf("%lld sessions of 1000 calls on 1000 units: checksum %lld\n", (long long)sessions, (long long)check);
    return 0;
}
