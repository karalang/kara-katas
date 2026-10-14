// Benchmark for #551: C mirror of the ★ arm (one pass, two counters);
// see student_attendance_record_i.kara. Records are NUL-terminated
// ASCII strings, read a byte at a time.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int check_record(const char *s) {
    int absences = 0, lates = 0;
    for (; *s; s++) {
        if (*s == 'L') {
            if (++lates == 3) return 0;
        } else {
            lates = 0;
            if (*s == 'A' && ++absences == 2) return 0;
        }
    }
    return 1;
}

static int64_t seed = 551;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int count = 1000, days = 1000;
    char *records = malloc((size_t)count * (days + 1));
    for (int g = 0; g < count; g++) {
        char *s = records + (size_t)g * (days + 1);
        for (int d = 0; d < days; d++) {
            int64_t r = next_random() % 2000;
            s[d] = r < 1 ? 'A' : r < 101 ? 'L' : 'P';
        }
        s[days] = 0;
    }
    int64_t fine = 0, checksum = 0;
    for (int round = 0; round < 300; round++)
        for (int g = 0; g < count; g++) {
            int64_t bit = check_record(records + (size_t)((round * 7 + g) % count) * (days + 1));
            fine += bit;
            checksum = (checksum * 31 + bit + g) % 1000000007;
        }
    printf("%d records, 300 rounds each: %lld fine, checksum %lld\n", count, (long long)fine,
           (long long)checksum);
    free(records);
    return 0;
}
