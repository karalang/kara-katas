// Benchmark for #390: mirror of last_remaining.kara (follow the head).

fn last_remaining(n: i64) -> i64 {
    let mut head = 1;
    let mut step = 1;
    let mut left = n;
    let mut from_left = true;
    while left > 1 {
        if from_left || left % 2 == 1 {
            head += step;
        }
        left /= 2;
        step *= 2;
        from_left = !from_left;
    }
    head
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 390;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..10000000 {
        let hi = next(&mut seed);
        let n = hi * 32768 + next(&mut seed) + 1;
        let r = last_remaining(n);
        total += r;
        checksum = (checksum * 31 + r) % 1000000007;
    }
    println!("10000000 values of n, sum {}, checksum {}", total, checksum);
}
