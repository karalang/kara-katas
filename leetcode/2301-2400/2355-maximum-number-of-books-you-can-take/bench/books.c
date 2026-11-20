// LeetCode #2355: Maximum Number of Books You Can Take -- the bench, the ★
// arm in C: the most books from a run ending at each shelf, from the
// nearest shelf to the left that caps the run, found on a monotonic stack.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t best[N];
static int64_t stack[N];

static int64_t maximum_books(const int64_t *books, int64_t n) {
    int64_t top = 0;
    int64_t answer = 0;
    for (int64_t i = 0; i < n; i++) {
        while (top > 0 && books[stack[top - 1]] - stack[top - 1] >= books[i] - i) {
            top--;
        }
        if (top > 0) {
            int64_t j = stack[top - 1];
            int64_t length = i - j;
            best[i] = length * books[i] - length * (length - 1) / 2 + best[j];
        } else {
            int64_t length = i + 1 < books[i] ? i + 1 : books[i];
            best[i] = length * books[i] - length * (length - 1) / 2;
        }
        stack[top++] = i;
        if (best[i] > answer) {
            answer = best[i];
        }
    }
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // array a holds 10^5 shelves: up to 10^5 books every (a + 2)^2-th
    // shelf, up to 100 (a + 1) between
    int64_t seed = 2355;
    int64_t *arrays = malloc(10 * N * sizeof(int64_t));
    for (int64_t a = 0; a < 10; a++) {
        for (int64_t i = 0; i < N; i++) {
            int64_t r = next_random(&seed);
            arrays[a * N + i] = i % ((a + 2) * (a + 2)) == 0 ? r * 3 % 100001 : r % (100 * (a + 1) + 1);
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++) {
        for (int64_t a = 0; a < 10; a++) {
            check = (check * 31 + maximum_books(arrays + a * N, N) % 1000000007 + p) % 1000000007;
        }
    }
    printf("50 passes over 10 arrays of 10^5 shelves: checksum %lld\n", (long long)check);
    free(arrays);
    return 0;
}
