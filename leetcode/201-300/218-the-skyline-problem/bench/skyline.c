#include <stdio.h>
#include <stdlib.h>

/* Benchmark workload for LeetCode #218 — The Skyline Problem.
 *
 * The kata computes a skyline by divide & conquer, mirroring merge sort: split
 * the buildings, recurse, then merge the two contours with a max-height sweep and
 * a "emit only on change" dedup. The bench builds ONE big PRNG building set, then
 * PASSES times punches a single building's height and re-runs the full skyline,
 * accumulating the contour's key points. It is deliberately allocation-heavy —
 * every merge node allocates a fresh contour — so it measures allocator + memory
 * throughput as much as compute. Sink = sum of (x + h) over every key point of
 * every pass. */

#define N        24000L    /* number of buildings                    */
#define PASSES   100L      /* skyline re-runs (build-once + punch)    */
#define XR       200000L   /* left-edge range                        */
#define WR       120L      /* max width                              */
#define HR       1000L     /* max height                             */

typedef struct { long left, right, height; } Building;
typedef struct { long x, h; } Point;

static Building bs[N];

/* Merge two contours (each sorted by x, ending at h = 0) into a fresh array.
 * Writes the result length through *outn. */
static Point *merge(const Point *L, long nl, const Point *R, long nr, long *outn) {
    Point *res = malloc((nl + nr) * sizeof(Point));
    long ri = 0;
    long i = 0, j = 0, h1 = 0, h2 = 0;
    while (i < nl && j < nr) {
        long x, maxh;
        if (L[i].x < R[j].x) {
            x = L[i].x; h1 = L[i].h; i++;
        } else if (L[i].x > R[j].x) {
            x = R[j].x; h2 = R[j].h; j++;
        } else {
            x = L[i].x; h1 = L[i].h; h2 = R[j].h; i++; j++;
        }
        maxh = h1 > h2 ? h1 : h2;
        if (ri == 0 || res[ri - 1].h != maxh) {
            res[ri].x = x; res[ri].h = maxh; ri++;
        }
    }
    while (i < nl) { res[ri++] = L[i++]; }
    while (j < nr) { res[ri++] = R[j++]; }
    *outn = ri;
    return res;
}

static Point *skyline(long lo, long hi, long *outn) {
    if (hi - lo == 1) {
        Point *r = malloc(2 * sizeof(Point));
        r[0].x = bs[lo].left;  r[0].h = bs[lo].height;
        r[1].x = bs[lo].right; r[1].h = 0;
        *outn = 2;
        return r;
    }
    long mid = lo + (hi - lo) / 2;
    long nl, nr;
    Point *L = skyline(lo, mid, &nl);
    Point *R = skyline(mid, hi, &nr);
    Point *m = merge(L, nl, R, nr, outn);
    free(L); free(R);
    return m;
}

int main(void) {
    long state = 12345;
    for (long i = 0; i < N; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long left = state % XR;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long width = 1 + state % WR;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long height = 1 + state % HR;
        bs[i].left = left; bs[i].right = left + width; bs[i].height = height;
    }

    long sink = 0;
    for (long p = 0; p < PASSES; p++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long idx = p % N;
        bs[idx].height = 1 + state % HR;      /* punch one building */
        long n;
        Point *sky = skyline(0, N, &n);
        for (long k = 0; k < n; k++) sink += sky[k].x + sky[k].h;
        free(sky);
    }
    printf("%ld\n", sink);
    return 0;
}
