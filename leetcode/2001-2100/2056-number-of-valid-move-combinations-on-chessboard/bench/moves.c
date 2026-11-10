// LeetCode #2056: Number of Valid Move Combinations On Chessboard -- C
// mirror of the ★ arm's benchmark (moves.kara): the same 200 boards of 4
// pieces, the same moves and backtracking, each new move walked against the
// moves already chosen.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    int64_t dr, dc, steps;
} Move;

static int64_t seed = 2056;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int moves_of(int kind, int64_t r, int64_t c, Move *moves) {
    static const int64_t dirs[8][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}, {1, 1}, {1, -1}, {-1, 1}, {-1, -1}};
    int from = kind == 2 ? 4 : 0, to = kind == 0 ? 4 : 8;  // 0 rook, 1 queen, 2 bishop
    int n = 0;
    moves[n++] = (Move){0, 0, 0};
    for (int d = from; d < to; d++) {
        int64_t dr = dirs[d][0], dc = dirs[d][1];
        for (int64_t steps = 1; r + dr * steps >= 1 && r + dr * steps <= 8 && c + dc * steps >= 1 && c + dc * steps <= 8;
             steps++)
            moves[n++] = (Move){dr, dc, steps};
    }
    return n;
}

static int collide(const int64_t *a, Move ma, const int64_t *b, Move mb) {
    int64_t last = ma.steps > mb.steps ? ma.steps : mb.steps;
    for (int64_t t = 1; t <= last; t++) {
        int64_t ta = t < ma.steps ? t : ma.steps, tb = t < mb.steps ? t : mb.steps;
        if (a[0] + ma.dr * ta == b[0] + mb.dr * tb && a[1] + ma.dc * ta == b[1] + mb.dc * tb) return 1;
    }
    return 0;
}

static int64_t at[4][2];
static Move options[4][32];
static int counts[4];
static Move chosen[4];
static int pieces;

static int64_t count_from(int i) {
    if (i == pieces) return 1;
    int64_t total = 0;
    for (int k = 0; k < counts[i]; k++) {
        Move m = options[i][k];
        int ok = 1;
        for (int j = 0; j < i && ok; j++)
            if (collide(at[j], chosen[j], at[i], m)) ok = 0;
        if (ok) {
            chosen[i] = m;
            total += count_from(i + 1);
        }
    }
    return total;
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int b = 0; b < 200; b++) {
        pieces = 0;
        int kinds[4];
        while (pieces < 4) {
            int64_t r = next_random() % 8 + 1;
            int64_t c = next_random() % 8 + 1;
            int kind = (int)(next_random() % 3);
            int seen = 0;
            for (int j = 0; j < pieces; j++)
                if (at[j][0] == r && at[j][1] == c) seen = 1;
            if (!seen) {
                at[pieces][0] = r;
                at[pieces][1] = c;
                kinds[pieces] = kind;
                pieces++;
            }
        }
        // the kinds drawn in the order "rook", "queen", "bishop"
        for (int i = 0; i < 4; i++) counts[i] = moves_of(kinds[i], at[i][0], at[i][1], options[i]);
        int64_t count = count_from(0);
        total += count;
        check = (check * 31 + count) % 1000000007;
    }
    printf("200 boards: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
