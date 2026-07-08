/*
 * Benchmark workload — Text Justification (LeetCode #68).
 * C mirror of bench/text_justification.kara. Runs the ★'s greedy-pack +
 * even-spread logic but streams the emitted bytes (word chars + gap spaces) into
 * a rolling polynomial hash instead of building line strings — no per-call
 * allocation, so it measures the packing/spacing codegen, not the allocator.
 * Fixed 40-word list, justified K=300_000 times at a swept width. See
 * ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <string.h>

static const char *WORDS[] = {
    "the","quick","brown","fox","jumps","over","a","lazy","dog","while","gentle",
    "breeze","carries","autumn","leaves","across","quiet","meadow","near","old",
    "stone","bridge","where","children","often","gather","to","watch","river","flow",
    "beneath","ancient","willow","trees","and","listen","as","the","wind","hums"};
static const int NW = 40;
static const int64_t MOD = 1000000007;

static int64_t justify_hash(int64_t max_width, int64_t h) {
    int i = 0;
    while (i < NW) {
        int j = i, line_chars = 0, count = 0;
        while (j < NW) {
            int wl = (int)strlen(WORDS[j]);
            if (line_chars + wl + count <= max_width) { line_chars += wl; count++; j++; }
            else break;
        }
        int gaps = count - 1;
        int64_t total = max_width - line_chars;
        int is_last = (j == NW);

        if (is_last || count == 1) {
            int64_t used = 0;
            for (int g = 0; g < count; g++) {
                for (const char *p = WORDS[i + g]; *p; p++) { h = (h * 131 + (unsigned char)*p) % MOD; used++; }
                if (g < count - 1) { h = (h * 131 + 32) % MOD; used++; }
            }
            while (used < max_width) { h = (h * 131 + 32) % MOD; used++; }
        } else {
            int64_t base = total / gaps, extra = total % gaps;
            for (int g = 0; g < count; g++) {
                for (const char *p = WORDS[i + g]; *p; p++) h = (h * 131 + (unsigned char)*p) % MOD;
                if (g < gaps) {
                    int64_t sp = base + (g < extra ? 1 : 0);
                    for (int64_t s = 0; s < sp; s++) h = (h * 131 + 32) % MOD;
                }
            }
        }
        i = j;
    }
    return h;
}

int main(void) {
    const int64_t total = 300000;
    const int64_t span = 40;

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t width = 10 + (k % span);
        acc = justify_hash(width, acc);
    }
    printf("%lld\n", (long long)acc);
    return 0;
}
