//! Benchmark workload — bit-shift long division, LeetCode #29.
//!
//! Algorithmic mirror of bench/bit_shift.kara and bench/bit_shift.py. See
//! ../README.md § Benchmarks for the choice of N and the LCG input.

fn divide(dividend: i64, divisor: i64) -> i64 {
    const INT_MAX: i64 = 2147483647;
    const INT_MIN: i64 = -2147483648;
    if dividend == INT_MIN && divisor == -1 {
        return INT_MAX;
    }
    let negative = (dividend < 0) != (divisor < 0);
    let mut a = dividend.abs();
    let b = divisor.abs();
    let mut result = 0i64;
    while a >= b {
        let mut temp = b;
        let mut multiple = 1i64;
        while a >= (temp << 1) {
            temp <<= 1;
            multiple <<= 1;
        }
        a -= temp;
        result += multiple;
    }
    if negative { -result } else { result }
}

fn main() {
    const N: i64 = 5_000_000;
    let mut state: i64 = 1;
    let mut sum: i64 = 0;
    for _ in 0..N {
        state = (state * 1103515245 + 12345) % 2147483648;
        let dividend = state - 1073741824;
        state = (state * 1103515245 + 12345) % 2147483648;
        let mut divisor = (state % 2000) - 1000;
        if divisor == 0 {
            divisor = 1;
        }
        sum += divide(dividend, divisor);
    }
    println!("{}", sum);
}
