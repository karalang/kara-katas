#include <stdio.h>

static long min_i64(long a, long b) { return a < b ? a : b; }
static long max_i64(long a, long b) { return a > b ? a : b; }
static long clamp0(long x) { return x > 0 ? x : 0; }

static long compute_area(long ax1, long ay1, long ax2, long ay2,
                         long bx1, long by1, long bx2, long by2) {
    long area_a = (ax2 - ax1) * (ay2 - ay1);
    long area_b = (bx2 - bx1) * (by2 - by1);
    long overlap_w = clamp0(min_i64(ax2, bx2) - max_i64(ax1, bx1));
    long overlap_h = clamp0(min_i64(ay2, by2) - max_i64(ay1, by1));
    long overlap = overlap_w * overlap_h;
    return area_a + area_b - overlap;
}

int main(void) {
    long pairs = 20000000;
    long mask = 16383;
    long modulus = 1000000007;
    long state = 12345;
    long sink = 0;
    for (long p = 0; p < pairs; p++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long ax1 = state & mask;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long ax2 = ax1 + (state & mask);
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long ay1 = state & mask;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long ay2 = ay1 + (state & mask);
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long bx1 = state & mask;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long bx2 = bx1 + (state & mask);
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long by1 = state & mask;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long by2 = by1 + (state & mask);
        long area = compute_area(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2);
        sink = (sink + area) % modulus;
    }
    printf("%ld\n", sink);
    return 0;
}
