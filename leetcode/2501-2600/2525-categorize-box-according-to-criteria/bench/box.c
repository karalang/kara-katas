// LeetCode #2525: Categorize Box According to Criteria -- C mirror of the
// benchmark (box.kara): the same boxes, passes, order and checksum.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static const char *categorize_box(int64_t length, int64_t width, int64_t height, int64_t mass) {
    int bulky = length >= 10000 || width >= 10000 || height >= 10000 || length * width * height >= 1000000000;
    int heavy = mass >= 100;
    if (bulky && heavy) return "Both";
    if (bulky) return "Bulky";
    if (heavy) return "Heavy";
    return "Neither";
}

static int64_t seed = 2525;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

static int64_t boxes[100000][4];

int main(void) {
    for (int t = 0; t < 100000; t++) {
        int64_t top = t % 2 == 0 ? 100000 : 2000;
        boxes[t][0] = wide_random() % top + 1;
        boxes[t][1] = wide_random() % top + 1;
        boxes[t][2] = wide_random() % top + 1;
        boxes[t][3] = next_random() % 1000 + 1;
    }
    const int passes = 220;
    int64_t check = 0;
    for (int p = 0; p < passes; p++) {
        int64_t start = check % 100000;
        for (int64_t i = 0; i < 100000; i++) {
            int64_t *b = boxes[(start + i) % 100000];
            const char *name = categorize_box(b[0], b[1], b[2], b[3]);
            int64_t code = strcmp(name, "Both") == 0 ? 1 : strcmp(name, "Bulky") == 0 ? 2 : strcmp(name, "Heavy") == 0 ? 3 : 4;
            check = (check * 31 + code + p) % 1000000007;
        }
    }
    printf("%d passes over 100000 boxes: checksum %lld\n", passes, (long long)check);
    return 0;
}
