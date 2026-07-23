#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long cap = 1024, key_range = 4096, ops = 32000000;

    // Index-pool doubly-linked list: 0 = head sentinel, 1 = tail sentinel,
    // real nodes at 2 .. cap+2. prev/next are pool indices.
    long pool = cap + 2;
    long *nkey  = malloc(pool * sizeof(long));
    long *nval  = malloc(pool * sizeof(long));
    long *nprev = malloc(pool * sizeof(long));
    long *nnext = malloc(pool * sizeof(long));
    for (long i = 0; i < pool; i++) { nkey[i] = -1; nval[i] = 0; nprev[i] = -1; nnext[i] = -1; }
    nnext[0] = 1; nprev[1] = 0;   // empty list: head <-> tail

    // Hand-rolled flat table: key -> pool index (-1 = absent). Bounded key range.
    long *keypos = malloc(key_range * sizeof(long));
    for (long i = 0; i < key_range; i++) keypos[i] = -1;

    long size = 0;
    long sink = 0;
    long state = 12345;
    for (long t = 0; t < ops; t++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long h1 = state >> 16;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long h2 = state >> 16;
        long key = h2 % key_range;

        if (h1 % 2 == 0) {
            // get(key)
            long r;
            long idx = keypos[key];
            if (idx >= 0) {
                // move_front(idx): unlink then push_front
                nnext[nprev[idx]] = nnext[idx];
                nprev[nnext[idx]] = nprev[idx];
                long first = nnext[0];
                nprev[idx] = 0; nnext[idx] = first;
                nprev[first] = idx; nnext[0] = idx;
                r = nval[idx];
            } else {
                r = -1;
            }
            sink += r + 1;
        } else {
            // put(key, v)
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long h3 = state >> 16;
            long v = h3;
            long idx = keypos[key];
            if (idx >= 0) {
                nval[idx] = v;
                nnext[nprev[idx]] = nnext[idx];
                nprev[nnext[idx]] = nprev[idx];
                long first = nnext[0];
                nprev[idx] = 0; nnext[idx] = first;
                nprev[first] = idx; nnext[0] = idx;
            } else {
                if (size < cap) {
                    idx = 2 + size;
                    size += 1;
                } else {
                    long lru = nprev[1];
                    nnext[nprev[lru]] = nnext[lru];
                    nprev[nnext[lru]] = nprev[lru];
                    keypos[nkey[lru]] = -1;
                    idx = lru;
                }
                nkey[idx] = key; nval[idx] = v;
                keypos[key] = idx;
                long first = nnext[0];
                nprev[idx] = 0; nnext[idx] = first;
                nprev[first] = idx; nnext[0] = idx;
            }
        }
    }
    printf("%ld\n", sink);
    free(nkey); free(nval); free(nprev); free(nnext); free(keypos);
    return 0;
}
