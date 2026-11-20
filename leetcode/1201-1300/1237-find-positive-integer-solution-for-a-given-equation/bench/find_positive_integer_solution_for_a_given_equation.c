// LeetCode #1237 bench: the ★ arm in C, over the same 9 functions, z from 1
// to 100 and 30 passes as the Kāra bench.
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int id;
} CustomFunction;

static int f(const CustomFunction *c, int x, int y) {
    switch (c->id) {
    case 1: return x + y;
    case 2: return x * y;
    case 3: return x * x + y;
    case 4: return x + y * y;
    case 5: return x * x + y * y;
    case 6: return (x + y) * (x + y);
    case 7: return x * x * x + y * y * y;
    case 8: return x * x * y;
    default: return x * y * y;
    }
}

// The pairs, two ints each, into `out`; returns how many.
static int find_solution(const CustomFunction *c, int z, int *out) {
    int n = 0, x = 1, y = 1000;
    while (x <= 1000 && y >= 1) {
        int v = f(c, x, y);
        if (v < z) {
            x++;
        } else if (v > z) {
            y--;
        } else {
            out[2 * n] = x;
            out[2 * n + 1] = y;
            n++;
            x++;
            y--;
        }
    }
    return n;
}

int main(void) {
    int *pairs = malloc(2 * 1000 * sizeof(int));
    long check = 0;
    for (int pass = 0; pass < 30; pass++)
        for (int id = 1; id <= 9; id++)
            for (int z = 1; z <= 100; z++) {
                CustomFunction c = {id};
                int n = find_solution(&c, z, pairs);
                for (int i = 0; i < n; i++)
                    check = (check * 131 + (long)pairs[2 * i] * 1001 + pairs[2 * i + 1]) % 1000000007;
            }
    printf("9 functions, z from 1 to 100, 30 passes: checksum %ld\n", check);
    free(pairs);
    return 0;
}
