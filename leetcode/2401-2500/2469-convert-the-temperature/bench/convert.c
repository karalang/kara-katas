// LeetCode #2469: Convert the Temperature -- the bench, the ★ arm in C:
// the two formulas as given, written into a caller's array of two.
#include <math.h>
#include <stdint.h>
#include <stdio.h>

static void convert_temperature(double celsius, double out[2]) {
    out[0] = celsius + 273.15;
    out[1] = celsius * 1.80 + 32.00;
}

int main(void) {
    // 230 passes over every temperature from 0 to 1000 in hundredths,
    // each pass starting at a hundredth chosen from the checksum so far;
    // every answer's kelvin in hundredths and Fahrenheit in thousandths,
    // rounded, folded into the checksum
    int64_t check = 0;
    for (int64_t p = 0; p < 230; p++) {
        int64_t start = check % 100001;
        for (int64_t i = 0; i < 100001; i++) {
            int64_t h = (start + i) % 100001;
            double got[2];
            convert_temperature((double)h / 100.0, got);
            int64_t kelvin = (int64_t)round(got[0] * 100.0);
            int64_t fahrenheit = (int64_t)round(got[1] * 1000.0);
            check = (check * 31 + kelvin + fahrenheit + p) % 1000000007;
        }
    }
    printf("230 passes over every hundredth from 0 to 1000: checksum %lld\n", (long long)check);
    return 0;
}
