// LeetCode #2383: Minimum Hours of Training to Win a Competition -- the
// bench, the ★ arm in C: the energy trained to one above the opponents'
// sum, the experience walked through the opponents.

#include <stdint.h>
#include <stdio.h>

static int64_t min_number_of_hours(int64_t initial_energy, int64_t initial_experience, const int64_t *energy,
                                   const int64_t *experience, int64_t n) {
    int64_t needed = 1;
    for (int64_t i = 0; i < n; i++) {
        needed += energy[i];
    }
    int64_t hours = 0;
    if (initial_energy < needed) {
        hours = needed - initial_energy;
    }
    int64_t have = initial_experience;
    for (int64_t i = 0; i < n; i++) {
        int64_t e = experience[i];
        if (have <= e) {
            hours += e + 1 - have;
            have = e + 1;
        }
        have += e;
    }
    return hours;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t energies[1000][100];
static int64_t experiences[1000][100];
static int64_t starts[1000][2];

int main(void) {
    // 1000 contests of 100 opponents, contest c's from 1 to 1 + c % 100;
    // pass p starts contest c with (p + c) % 50 more energy and
    // (3 p + c) % 50 more experience than its own start
    int64_t seed = 2383;
    for (int64_t c = 0; c < 1000; c++) {
        int64_t top = 1 + c % 100;
        starts[c][0] = 1 + next_random(&seed) % 100;
        starts[c][1] = 1 + next_random(&seed) % 100;
        for (int i = 0; i < 100; i++) {
            energies[c][i] = 1 + next_random(&seed) % top;
        }
        for (int i = 0; i < 100; i++) {
            experiences[c][i] = 1 + next_random(&seed) % top;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 5000; p++) {
        for (int64_t c = 0; c < 1000; c++) {
            int64_t hours = min_number_of_hours(starts[c][0] + (p + c) % 50, starts[c][1] + (3 * p + c) % 50,
                                                energies[c], experiences[c], 100);
            check = (check * 31 + hours + p) % 1000000007;
        }
    }
    printf("5000 passes over 1000 contests of 100 opponents: checksum %lld\n", (long long)check);
    return 0;
}
