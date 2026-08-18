/* LeetCode 282 bench mirror — C. Same backtracking search, same string
 * building along the branches, same count+hash sink.
 *
 * EACH BRANCH HEAP-ALLOCATES ITS EXPRESSION, deliberately. A stack buffer is the
 * natural C move here and it measured 4.6x faster than the other three lanes —
 * but Kara, Rust and Go all allocate a fresh string per branch, so a stack-buffer
 * C lane is not running the same algorithm and the comparison would be
 * dishonest. malloc/free per branch is what parity costs. */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#define INPUTS 220
#define NDIG 9
static char num[NDIG + 1];
static int64_t target, found, hash_;

static void search(int pos, char *expr, int elen, int64_t cur, int64_t last) {
    if (pos == NDIG) {
        if (cur == target) { found++; hash_ = (hash_ * 31 + elen) % 1000000007LL; }
        return;
    }
    for (int end = pos + 1; end <= NDIG; end++) {
        if (end > pos + 1 && num[pos] == '0') return;
        int64_t n = 0;
        for (int k = pos; k < end; k++) n = n * 10 + (num[k] - '0');
        int plen = end - pos;
        if (pos == 0) {
            char *buf = malloc((size_t)plen + 1);
            memcpy(buf, num + pos, (size_t)plen); buf[plen] = 0;
            search(end, buf, plen, n, n);
            free(buf);
        } else {
            const char ops[3] = {'+', '-', '*'};
            for (int o = 0; o < 3; o++) {
                int nl = elen + 1 + plen;
                char *buf = malloc((size_t)nl + 1);
                memcpy(buf, expr, (size_t)elen);
                buf[elen] = ops[o];
                memcpy(buf + elen + 1, num + pos, (size_t)plen);
                buf[nl] = 0;
                if (o == 0)      search(end, buf, nl, cur + n, n);
                else if (o == 1) search(end, buf, nl, cur - n, -n);
                else             search(end, buf, nl, cur - last + last * n, last * n);
                free(buf);
            }
        }
    }
}

int main(void) {
    int64_t seed = 20260820;
    int64_t total = 0;
    for (int t = 0; t < INPUTS; t++) {
        for (int d = 0; d < NDIG; d++) {
            seed = (seed*1103515245LL+12345LL)%2147483648LL;
            num[d] = (char)('0' + 1 + (seed/19) % 6);
        }
        num[NDIG] = 0;
        seed = (seed*1103515245LL+12345LL)%2147483648LL;
        target = (seed/23) % 40;
        found = 0;
        char *empty = malloc(1); empty[0] = 0;
        search(0, empty, 0, 0, 0);
        free(empty);
        total += found;
    }
    printf("%lld %lld\n", (long long)total, (long long)hash_);
    return 0;
}
