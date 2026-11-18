// LeetCode #1603: Design Parking System -- the bench in C, mirroring
// parking.kara: the spaces left of each size in an array.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int32_t left[3];
} ParkingSystem;

static bool add_car(ParkingSystem *p, int32_t car_type) {
    int32_t slot = car_type - 1;
    if (p->left[slot] == 0) return false;
    p->left[slot] -= 1;
    return true;
}

static int64_t seed = 1603;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int32_t lots[1000][3];
    for (int k = 0; k < 1000; k++)
        for (int s = 0; s < 3; s++) lots[k][s] = (int32_t)(next_random() % 3001);
    int32_t *cars = malloc(10000000 * sizeof(int32_t));
    for (int64_t i = 0; i < 10000000; i++) cars[i] = (int32_t)(next_random() % 3 + 1);
    int64_t check = 0, parked = 0;
    for (int64_t round = 0; round < 20; round++) {
        for (int k = 0; k < 1000; k++) {
            ParkingSystem lot = {{lots[k][0], lots[k][1], lots[k][2]}};
            int64_t count = 0;
            for (int64_t i = (int64_t)k * 10000; i < (int64_t)(k + 1) * 10000; i++)
                if (add_car(&lot, cars[i])) count++;
            parked += count;
            check = (check * 31 + count + round + 1) % 1000000007;
        }
    }
    printf("20 rounds of 1000 lots of up to 3000 spaces a size, 10000 cars each: %lld parked, checksum %lld\n",
           (long long)parked, (long long)check);
    free(cars);
    return 0;
}
