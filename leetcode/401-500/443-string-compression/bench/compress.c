// Benchmark for #443: mirror of compress.kara (reading and writing in
// place) on 1,000 random strings of 2,000 characters, built once, copied
// and compressed 20 times over. Characters are 32-bit, as Kāra's `char`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t compress(uint32_t *chars, int64_t n) {
    int64_t read = 0, write = 0;
    while (read < n) {
        uint32_t c = chars[read];
        int64_t start = read;
        while (read < n && chars[read] == c) {
            read += 1;
        }
        chars[write++] = c;
        int64_t count = read - start;
        if (count > 1) {
            char digits[24];
            int len = snprintf(digits, sizeof digits, "%lld", (long long)count);
            for (int i = 0; i < len; i++) {
                chars[write++] = (uint32_t)digits[i];
            }
        }
    }
    return write;
}

int main(void) {
    const int64_t count = 1000, size = 2000, rounds = 20;
    const int64_t longests[4] = {1, 3, 15, 120};
    int64_t seed = 443;
    // Runs of 1 to 1, 3, 15 or 120 letters from a three-letter alphabet.
    uint32_t **strings = malloc(count * sizeof(uint32_t *));
    for (int64_t s = 0; s < count; s++) {
        int64_t longest = longests[next_random(&seed) % 4];
        uint32_t *chars = malloc(size * sizeof(uint32_t));
        int64_t len = 0;
        while (len < size) {
            uint32_t c = (uint32_t)('a' + next_random(&seed) % 3);
            int64_t run = 1 + next_random(&seed) % longest;
            for (int64_t r = 0; r < run; r++) {
                if (len < size) {
                    chars[len++] = c;
                }
            }
        }
        strings[s] = chars;
    }
    int64_t length = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t s = 0; s < count; s++) {
            uint32_t *chars = malloc(size * sizeof(uint32_t));
            memcpy(chars, strings[s], size * sizeof(uint32_t));
            int64_t n = compress(chars, size);
            length += n;
            checksum = (checksum * 31 + n + chars[n - 1] + round) % 1000000007;
            free(chars);
        }
    }
    printf("%lld rounds on %lld strings of %lld: compressed length %lld, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)size, (long long)length, (long long)checksum);
    for (int64_t s = 0; s < count; s++) {
        free(strings[s]);
    }
    free(strings);
    return 0;
}
