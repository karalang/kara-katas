/* LeetCode 278 bench mirror — C. Build one dictionary, solve it 48 times. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define WORDS 250000
#define ALPHA 6
#define WIDTH 8
#define INSTANCES 48

static char *dict;               /* WORDS * (WIDTH+1) */
static inline const char *W(int i) { return dict + (size_t)i * (WIDTH + 1); }

static int solve_len(void) {
    int present[26] = {0}, indeg[26] = {0};
    static unsigned char adj[676];
    memset(adj, 0, sizeof adj);
    for (int i = 0; i < WORDS; i++)
        for (const char *p = W(i); *p; p++) present[*p - 'a'] = 1;
    for (int p = 0; p + 1 < WORDS; p++) {
        const char *a = W(p), *c = W(p + 1);
        int found = 0;
        int shorter = (int)strlen(a) < (int)strlen(c) ? (int)strlen(a) : (int)strlen(c);
        for (int k = 0; k < shorter; k++)
            if (a[k] != c[k]) {
                int u = a[k] - 'a', v = c[k] - 'a';
                if (!adj[u * 26 + v]) { adj[u * 26 + v] = 1; indeg[v]++; }
                found = 1;
                break;
            }
        if (!found && strlen(a) > strlen(c)) return 0;
    }
    int done[26] = {0}, remaining = 0, out = 0;
    for (int r = 0; r < 26; r++) if (present[r]) remaining++;
    while (remaining > 0) {
        int pick = -1;
        for (int s = 0; s < 26; s++)
            if (present[s] && !done[s] && indeg[s] == 0) { pick = s; break; }
        if (pick < 0) return 0;
        done[pick] = 1;
        out++;
        for (int t = 0; t < 26; t++) if (adj[pick * 26 + t]) indeg[t]--;
        remaining--;
    }
    return out;
}

int main(void) {
    dict = malloc((size_t)WORDS * (WIDTH + 1));
    for (int n = 0; n < WORDS; n++) {
        char *w = dict + (size_t)n * (WIDTH + 1);
        int rem = n;
        int digits[WIDTH];
        for (int pos = 0; pos < WIDTH; pos++) { digits[pos] = rem % ALPHA; rem /= ALPHA; }
        for (int q = WIDTH - 1, o = 0; q >= 0; q--, o++)
            w[o] = (char)('a' + (ALPHA - 1 - digits[q]));
        w[WIDTH] = 0;
    }
    int64_t sink = 0;
    for (int64_t i = 0; i < INSTANCES; i++)
        sink = (sink + ((int64_t)i * 1000003LL + solve_len()) % 1000000007LL) % 1000000007LL;
    printf("%lld\n", (long long)sink);
    return 0;
}
