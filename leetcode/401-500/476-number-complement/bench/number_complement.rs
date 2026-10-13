// Benchmark for #476: Rust mirror of the ★ arm (a mask of the number's
// own width); see number_complement.kara.

fn find_complement(num: i64) -> i64 {
    let mut mask = 1;
    while mask < num {
        mask = (mask << 1) | 1;
    }
    num ^ mask
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 30000000;
    let mut seed: i64 = 476;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..count {
        let bits = 1 + next_random(&mut seed) % 31;
        let high: i64 = 1 << (bits - 1);
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let num = high | ((a * 32768 + b) % high);
        let got = find_complement(num);
        total += got;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    println!("{} numbers: complements add up to {}, checksum {}", count, total, checksum);
}
