// Benchmark for #400: mirror of nth_digit.kara (skip whole blocks).

fn find_nth_digit(n: i64) -> i64 {
    let mut rest = n;
    let mut digits = 1;
    let mut count = 9;
    let mut start = 1;
    while rest > digits * count {
        rest -= digits * count;
        digits += 1;
        count *= 10;
        start *= 10;
    }
    let number = start + (rest - 1) / digits;
    let mut shift = digits - 1 - (rest - 1) % digits;
    let mut x = number;
    while shift > 0 {
        x = x / 10;
        shift -= 1;
    }
    x % 10
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let calls = 10000000;
    let mut seed: i64 = 4001;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..calls {
        let hi = step(&mut seed);
        let n = 1 + (hi * 32768 + step(&mut seed)) % 2147483647;
        let d = find_nth_digit(n);
        total += d;
        checksum = (checksum * 31 + d) % 1000000007;
    }
    println!("{} calls: total {}, checksum {}", calls, total, checksum);
}
