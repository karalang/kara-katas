/* Benchmark mirror of parenrepair.kara — LeetCode #301, unique-by-construction
 * repair. Same recursion, same depth-indexed scratch buffer, same sink.
 *
 * `scratch[32][32]` is what the Kara mirror spells as one flat Vec[u8] indexed
 * by depth * 32; keeping the shape identical is what makes the comparison
 * algorithm-for-algorithm rather than allocator-for-allocator. */
#include <stdio.h>

#define NCASES 2000
#define SLEN   24
#define PASSES 64
#define SLOT   32
#define MAXDEPTH 32
#define MOD 1000000007LL

static unsigned char corpus[NCASES * SLEN];
static unsigned char scratch[MAXDEPTH][SLOT];
static long long results;
static long long checksum;

static void repair(int depth, int len, int last_i, int last_j,
                   unsigned char open, unsigned char close) {
    unsigned char *base = scratch[depth];
    unsigned char *child = scratch[depth + 1];

    int count = 0;
    for (int i = last_i; i < len; i++) {
        unsigned char c = base[i];
        if (c == open) count++;
        else if (c == close) count--;
        if (count < 0) {
            for (int j = last_j; j <= i; j++) {
                if (base[j] == close && (j == last_j || base[j - 1] != close)) {
                    int w = 0;
                    for (int k = 0; k < len; k++)
                        if (k != j) child[w++] = base[k];
                    repair(depth + 1, len - 1, i, j, open, close);
                }
            }
            return;
        }
    }

    for (int r = 0; r < len; r++) child[r] = base[len - 1 - r];

    if (open == '(') {
        repair(depth + 1, len, 0, 0, ')', '(');
    } else {
        long long h = 0;
        for (int t = 0; t < len; t++) h = (h * 31 + child[t]) % MOD;
        results++;
        checksum = (checksum + h) % MOD;
    }
}

int main(void) {
    long long state = 12345;
    for (int n = 0; n < NCASES * SLEN; n++) {
        state = (state * 1103515245LL + 12345LL) & 0x7fffffffLL;
        long long r = (state / 65536) % 3;
        corpus[n] = r == 0 ? '(' : (r == 1 ? ')' : 'a');
    }

    for (int p = 0; p < PASSES; p++) {
        for (int ci = 0; ci < NCASES; ci++) {
            const unsigned char *src = corpus + (size_t)ci * SLEN;
            for (int k = 0; k < SLEN; k++) scratch[0][k] = src[k];
            repair(0, SLEN, 0, 0, '(', ')');
        }
    }

    printf("results %lld\n", results);
    printf("checksum %lld\n", checksum);
    return 0;
}
