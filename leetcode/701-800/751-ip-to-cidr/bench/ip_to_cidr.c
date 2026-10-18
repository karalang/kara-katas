// LeetCode 751 — IP to CIDR, bench: the ★ arm (greedy by the lowest
// set bit) on half a million ranges from a pool of 1000 addresses.
// Mirrors ip_to_cidr.kara.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t address(const char *ip) {
    int64_t x = 0, part = 0;
    for (const char *p = ip; ; p++) {
        if (*p == '.' || *p == 0) {
            x = x * 256 + part;
            part = 0;
            if (*p == 0) break;
        } else {
            part = part * 10 + (*p - '0');
        }
    }
    return x;
}

// Writes the blocks into out, one string each, and returns how many.
static int64_t ip_to_cidr(const char *ip, int64_t n, char out[][20]) {
    int64_t x = address(ip), left = n, count = 0;
    while (left > 0) {
        int64_t size = x == 0 ? 4294967296LL : (x & -x);
        while (size > left) size /= 2;
        int64_t bits = 0;
        while ((1LL << bits) < size) bits++;
        snprintf(out[count++], 20, "%lld.%lld.%lld.%lld/%lld", (long long)(x / 16777216 % 256),
                 (long long)(x / 65536 % 256), (long long)(x / 256 % 256), (long long)(x % 256),
                 (long long)(32 - bits));
        x += size;
        left -= size;
    }
    return count;
}

static int64_t seed = 751;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t queries = 500000;
    static char pool[1000][16];
    for (int i = 0; i < 1000; i++) {
        int64_t a = next_random() % 255, b = next_random() % 256;
        int64_t c = next_random() % 256, d = next_random() % 256;
        snprintf(pool[i], 16, "%lld.%lld.%lld.%lld", (long long)a, (long long)b, (long long)c, (long long)d);
    }
    static char found[64][20];
    int64_t blocks = 0, check = 0;
    for (int64_t q = 0; q < queries; q++) {
        int64_t n = 1 + next_random() % 1000;
        int64_t k = ip_to_cidr(pool[q % 1000], n, found);
        blocks += k;
        for (int64_t i = 0; i < k; i++) check = (check * 31 + (int64_t)strlen(found[i])) % 1000000007;
    }
    printf("%lld ranges: %lld blocks in all, checksum %lld\n", (long long)queries, (long long)blocks, (long long)check);
    return 0;
}
