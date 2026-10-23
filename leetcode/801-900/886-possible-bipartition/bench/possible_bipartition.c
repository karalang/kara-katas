// LeetCode #886 bench: C mirror of possible_bipartition.kara (the ★ arm,
// two colours by breadth-first search) on the same 4000 groups. The pairs
// are one flat array, the adjacency one array indexed by each person's
// offset into it, and the queue an array, where the others keep a list per
// pair and per person and a growable queue.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int possible_bipartition(int64_t n, const int64_t *pairs, int64_t m) {
    int64_t *start = calloc(n + 2, sizeof *start);
    int64_t *adj = malloc(2 * m * sizeof *adj);
    int64_t *fill = malloc((n + 2) * sizeof *fill);
    int64_t *colour = malloc((n + 1) * sizeof *colour);
    int64_t *queue = malloc((n + 1) * sizeof *queue);
    for (int64_t e = 0; e < m; e++) { start[pairs[2 * e] + 1]++; start[pairs[2 * e + 1] + 1]++; }
    for (int64_t x = 1; x <= n + 1; x++) start[x] += start[x - 1];
    for (int64_t x = 0; x <= n + 1; x++) fill[x] = start[x];
    for (int64_t e = 0; e < m; e++) {
        int64_t a = pairs[2 * e], b = pairs[2 * e + 1];
        adj[fill[a]++] = b;
        adj[fill[b]++] = a;
    }
    for (int64_t x = 0; x <= n; x++) colour[x] = -1;
    int ok = 1;
    for (int64_t s = 1; s <= n && ok; s++) {
        if (colour[s] >= 0) continue;
        colour[s] = 0;
        int64_t head = 0, tail = 0;
        queue[tail++] = s;
        while (head < tail && ok) {
            int64_t u = queue[head++];
            for (int64_t k = start[u]; k < start[u + 1]; k++) {
                int64_t v = adj[k];
                if (colour[v] < 0) { colour[v] = 1 - colour[u]; queue[tail++] = v; }
                else if (colour[v] == colour[u]) { ok = 0; break; }
            }
        }
    }
    free(start); free(adj); free(fill); free(colour); free(queue);
    return ok;
}

static int64_t seed = 886;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t yes = 0, check = 0;
    int64_t *pairs = malloc(2 * 5 * 2000 * sizeof *pairs);
    for (int g = 0; g < 4000; g++) {
        // n people, each disliking the people five distinct offsets on,
        // every offset below n / 2 so that no pair repeats: 5n pairs, up
        // to 10^4; the offsets odd, but one of them even half the time
        int64_t n = 1000 + next_random() % 1001;
        int spoil = next_random() % 2 == 0;
        int64_t offsets[5];
        int count = 0;
        while (count < 5) {
            int64_t d = 1 + next_random() % (n / 2 - 1);
            if (d % 2 == 0 && !(spoil && count == 0)) d -= 1;
            int seen = 0;
            for (int k = 0; k < count; k++) if (offsets[k] == d) seen = 1;
            if (!seen) offsets[count++] = d;
        }
        int64_t m = 0;
        for (int64_t a = 0; a < n; a++) {
            for (int k = 0; k < 5; k++) {
                pairs[2 * m] = a + 1;
                pairs[2 * m + 1] = (a + offsets[k]) % n + 1;
                m++;
            }
        }
        int64_t bit = possible_bipartition(n, pairs, m);
        yes += bit;
        check = (check * 3 + bit + 1) % 1000000007;
    }
    free(pairs);
    printf("4000 groups of up to 2000 people: %lld can be split, checksum %lld\n", (long long)yes, (long long)check);
    return 0;
}
