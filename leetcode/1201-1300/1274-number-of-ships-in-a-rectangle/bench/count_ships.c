// LeetCode #1274 bench, in C: the ★ arm (divide and conquer by
// quarters through the sea's interface) on 500 random seas of 10 ships in
// the whole 1001-by-1001 square and 10 more in a corner, drawn once, 30
// rounds; every count, and the number of questions asked, folded into a
// checksum.
// The sea is a struct and `has_ships` a plain function on it, as in
// LeetCode's C interface.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef struct {
    int64_t xs[20], ys[20];
    int n;
    int64_t calls;
} Sea;

static bool has_ships(Sea *sea, const int64_t *top_right, const int64_t *bottom_left) {
    sea->calls++;
    for (int i = 0; i < sea->n; i++)
        if (bottom_left[0] <= sea->xs[i] && sea->xs[i] <= top_right[0] && bottom_left[1] <= sea->ys[i] &&
            sea->ys[i] <= top_right[1])
            return true;
    return false;
}

static int64_t count_ships(Sea *sea, const int64_t *top_right, const int64_t *bottom_left) {
    if (bottom_left[0] > top_right[0] || bottom_left[1] > top_right[1]) return 0;
    if (!has_ships(sea, top_right, bottom_left)) return 0;
    if (top_right[0] == bottom_left[0] && top_right[1] == bottom_left[1]) return 1;
    int64_t mx = (top_right[0] + bottom_left[0]) / 2;
    int64_t my = (top_right[1] + bottom_left[1]) / 2;
    int64_t a[2] = {mx, my}, b[2] = {top_right[0], my}, c[2] = {mx + 1, bottom_left[1]};
    int64_t d[2] = {mx, top_right[1]}, e[2] = {bottom_left[0], my + 1}, f[2] = {mx + 1, my + 1};
    return count_ships(sea, a, bottom_left) + count_ships(sea, b, c) + count_ships(sea, d, e) +
           count_ships(sea, top_right, f);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1274;
    static Sea seas[500];
    for (int s = 0; s < 500; s++) {
        seas[s].n = 0;
        for (int i = 0; i < 20; i++) {
            int64_t span = i < 10 ? 1001 : 30;
            int64_t x = next_random(&seed) % span;
            int64_t y = next_random(&seed) % span;
            bool seen = false;
            for (int j = 0; j < seas[s].n; j++)
                if (seas[s].xs[j] == x && seas[s].ys[j] == y) seen = true;
            if (!seen) {
                seas[s].xs[seas[s].n] = x;
                seas[s].ys[seas[s].n] = y;
                seas[s].n++;
            }
        }
    }
    const int64_t top_right[2] = {1000, 1000}, bottom_left[2] = {0, 0};
    int64_t check = 0;
    for (int64_t round = 0; round < 30; round++)
        for (int s = 0; s < 500; s++) {
            seas[s].calls = 0;
            int64_t n = count_ships(&seas[s], top_right, bottom_left);
            check = (check * 131 + n + round) % 1000000007;
            check = (check * 131 + seas[s].calls) % 1000000007;
        }
    printf("30 rounds of 500 seas: checksum %lld\n", (long long)check);
    return 0;
}
