// Benchmark for #397: mirror of integer_replacement.kara (greedy on the last two bits).

fn integer_replacement(n: i64) -> i64 {
    let mut v = n;
    let mut ops = 0;
    while v != 1 {
        if v % 2 == 0 {
            v = v / 2;
        } else if v == 3 || v % 4 == 1 {
            v -= 1;
        } else {
            v += 1;
        }
        ops += 1;
    }
    ops
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let calls = 5000000;
    let mut seed: i64 = 397;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..calls {
        let hi = step(&mut seed);
        let n = 1 + (hi * 32768 + step(&mut seed)) % 2147483647;
        let r = integer_replacement(n);
        total += r;
        checksum = (checksum * 31 + r) % 1000000007;
    }
    println!("{} calls: total {}, checksum {}", calls, total, checksum);
}
