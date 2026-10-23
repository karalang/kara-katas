// LeetCode #917: Reverse Only Letters -- bench: C mirror of the two
// pointers swapping letters in reverse_only_letters.kara. The bytes are
// copied, swapped, and copied once more into a new string, as the Kara
// version builds a new String.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int is_letter(unsigned char b) { return (b >= 'a' && b <= 'z') || (b >= 'A' && b <= 'Z'); }

static char *reverse_only_letters(const char *s) {
    size_t n = strlen(s);
    unsigned char *bytes = malloc(n);
    memcpy(bytes, s, n);
    size_t i = 0, j = n;
    while (i < j) {
        if (!is_letter(bytes[i])) {
            i++;
        } else if (!is_letter(bytes[j - 1])) {
            j--;
        } else {
            unsigned char keep = bytes[i];
            bytes[i] = bytes[j - 1];
            bytes[j - 1] = keep;
            i++;
            j--;
        }
    }
    char *out = malloc(n + 1);
    for (size_t k = 0; k < n; k++)
        out[k] = (char)bytes[k];
    out[n] = 0;
    free(bytes);
    return out;
}

static int64_t seed = 917;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char *random_string(int64_t letters) {
    char *s = malloc(101);
    for (int k = 0; k < 100; k++) {
        if (next_random() % 100 < letters) {
            int64_t c = next_random() % 52;
            s[k] = (char)(c < 26 ? 97 + c : 65 + c - 26);
        } else {
            int64_t b = 34;
            while (b == 34 || b == 92)
                b = 33 + next_random() % 90;
            s[k] = (char)b;
        }
    }
    s[100] = 0;
    return s;
}

int main(void) {
    int64_t rounds = 1000;
    int64_t n = 1000;
    char **pool = malloc(sizeof(char *) * n);
    for (int64_t c = 0; c < n; c++)
        pool[c] = random_string(c % 101);
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < n; c++) {
            char *out = reverse_only_letters(pool[c]);
            size_t len = strlen(out);
            check = (check * 1000003 + (unsigned char)out[0] * 256 + (unsigned char)out[len - 1]) % 1000000007;
            free(out);
        }
    }
    printf("%lld rounds over %lld strings of 100: checksum %lld\n", (long long)rounds, (long long)n, (long long)check);
    for (int64_t c = 0; c < n; c++)
        free(pool[c]);
    free(pool);
    return 0;
}
