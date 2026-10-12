// Benchmark for #412: mirror of fizz_buzz.kara (test each case). Every
// entry is its own heap string, as each is a String in the Kāra program.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *copy(const char *s) {
    size_t n = strlen(s);
    char *out = malloc(n + 1);
    memcpy(out, s, n + 1);
    return out;
}

static char **fizz_buzz(int64_t n) {
    char **answer = malloc(n * sizeof *answer);
    char buf[24];
    for (int64_t i = 1; i <= n; i++) {
        if (i % 15 == 0) {
            answer[i - 1] = copy("FizzBuzz");
        } else if (i % 3 == 0) {
            answer[i - 1] = copy("Fizz");
        } else if (i % 5 == 0) {
            answer[i - 1] = copy("Buzz");
        } else {
            snprintf(buf, sizeof buf, "%lld", (long long)i);
            answer[i - 1] = copy(buf);
        }
    }
    return answer;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t calls = argc > 1 ? atoll(argv[1]) : 2000;
    int64_t seed = 412, bytes = 0, checksum = 0;
    for (int64_t c = 0; c < calls; c++) {
        int64_t n = 9000 + step(&seed) % 1001;
        char **answer = fizz_buzz(n);
        int64_t length = 0;
        for (int64_t i = 0; i < n; i++) {
            length += (int64_t)strlen(answer[i]);
            free(answer[i]);
        }
        free(answer);
        bytes += length;
        checksum = (checksum * 31 + length) % 1000000007;
    }
    printf("%lld calls: %lld bytes, checksum %lld\n", (long long)calls, (long long)bytes, (long long)checksum);
    return 0;
}
