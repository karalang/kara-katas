// Benchmark for #423: mirror of original_digits.kara (unique letters).
// The answer is built in a fresh buffer on every call, as the Kāra
// program builds a fresh String.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *original_digits(const char *s, int64_t n, int64_t *out_len) {
    int64_t letters[26] = {0};
    for (int64_t i = 0; i < n; i++) letters[s[i] - 'a']++;
    int64_t count[10];
    count[0] = letters['z' - 'a'];
    count[2] = letters['w' - 'a'];
    count[4] = letters['u' - 'a'];
    count[6] = letters['x' - 'a'];
    count[8] = letters['g' - 'a'];
    count[3] = letters['h' - 'a'] - count[8];
    count[5] = letters['f' - 'a'] - count[4];
    count[7] = letters['s' - 'a'] - count[6];
    count[1] = letters['o' - 'a'] - count[0] - count[2] - count[4];
    count[9] = letters['i' - 'a'] - count[5] - count[6] - count[8];
    int64_t total = 0;
    for (int d = 0; d < 10; d++) total += count[d];
    char *out = malloc(total + 1);
    int64_t k = 0;
    for (int d = 0; d < 10; d++) {
        for (int64_t t = 0; t < count[d]; t++) out[k++] = (char)('0' + d);
    }
    *out_len = k;
    return out;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t calls = argc > 1 ? atoll(argv[1]) : 100000;
    int64_t blocks = 20000, seed = 423;
    const char *names[10] = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
    char *text = malloc(blocks * 8 * 5 + 1);
    int64_t len = 0;
    int64_t *ends = malloc((blocks + 1) * sizeof *ends);
    ends[0] = 0;
    char pool[64];
    for (int64_t b = 0; b < blocks; b++) {
        int64_t count = 1 + step(&seed) % 8, size = 0;
        for (int64_t c = 0; c < count; c++) {
            const char *w = names[step(&seed) % 10];
            for (size_t k = 0; w[k]; k++) pool[size++] = w[k];
        }
        for (int64_t i = 0; i < size; i++) {
            int64_t j = i + step(&seed) % (size - i);
            char keep = pool[i];
            pool[i] = pool[j];
            pool[j] = keep;
        }
        memcpy(text + len, pool, size);
        len += size;
        ends[b + 1] = len;
    }
    int64_t digits = 0, checksum = 0;
    for (int64_t c = 0; c < calls; c++) {
        int64_t length = 50 + step(&seed) % 200;
        int64_t first = step(&seed) % (blocks - length);
        int64_t out_len;
        char *answer = original_digits(text + ends[first], ends[first + length] - ends[first], &out_len);
        digits += out_len;
        for (int64_t k = 0; k < out_len; k++) checksum = (checksum * 31 + (answer[k] - 47)) % 1000000007;
        free(answer);
    }
    printf("%lld calls on %lld letters: %lld digits, checksum %lld\n", (long long)calls, (long long)len, (long long)digits, (long long)checksum);
    return 0;
}
