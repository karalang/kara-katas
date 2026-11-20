// LeetCode #1710: Maximum Units on a Truck -- the C mirror of the bench
// (units.kara): the box types sorted by units, most first, and boxes
// taken from the front until the truck is full, on 1000 random problems
// of 1000 box types, each answered 10 times.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int boxes;
    int units;
} BoxType;

static int by_units_down(const void *a, const void *b) {
    int x = ((const BoxType *)a)->units;
    int y = ((const BoxType *)b)->units;
    return (y > x) - (y < x);
}

// sorts a copy, as the other languages do
static int maximum_units(const BoxType *box_types, int n, int truck_size) {
    BoxType *order = malloc(sizeof(BoxType) * n);
    memcpy(order, box_types, sizeof(BoxType) * n);
    qsort(order, n, sizeof(BoxType), by_units_down);
    int room = truck_size;
    int total = 0;
    for (int i = 0; i < n; i++) {
        int take = order[i].boxes < room ? order[i].boxes : room;
        total += take * order[i].units;
        room -= take;
        if (room == 0) {
            break;
        }
    }
    free(order);
    return total;
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int count = 1000;
    const long long rounds = 10;
    const int n = 1000;
    long long seed = 1710;
    BoxType *problems = malloc(sizeof(BoxType) * count * n);
    int *sizes = malloc(sizeof(int) * count);
    for (int p = 0; p < count; p++) {
        for (int i = 0; i < n; i++) {
            problems[p * n + i].boxes = (int)(next_random(&seed) % 1000 + 1);
            problems[p * n + i].units = (int)(next_random(&seed) % 1000 + 1);
        }
        long long a = next_random(&seed);
        sizes[p] = (int)((a * 32768 + next_random(&seed)) % 1000000 + 1);
    }
    long long sum = 0;
    long long check = 0;
    for (long long r = 0; r < rounds; r++) {
        for (int p = 0; p < count; p++) {
            long long answer = maximum_units(problems + p * n, n, sizes[p]);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d problems of %d box types, %lld rounds: answers sum to %lld, checksum %lld\n", count, n, rounds, sum, check);
    free(problems);
    free(sizes);
    return 0;
}
