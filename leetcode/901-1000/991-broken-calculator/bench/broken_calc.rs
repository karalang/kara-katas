// LeetCode #991: Broken Calculator -- bench, the ★ arm (greedy from the
// target back), the same algorithm and workload as broken_calc.kara.

fn broken_calc(start_value: i64, target: i64) -> i64 {
    let mut ops = 0;
    let mut t = target;
    while t > start_value {
        if t % 2 == 1 {
            t += 1;
        } else {
            t /= 2;
        }
        ops += 1;
    }
    ops + start_value - t
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 5000;
    let mut seed = 991;
    let mut starts = Vec::new();
    let mut targets = Vec::new();
    for _ in 0..1000 {
        let a = next_random(&mut seed);
        starts.push(1 + (a * 32768 + next_random(&mut seed)) % 1000);
        let b = next_random(&mut seed);
        targets.push(1 + (b * 32768 + next_random(&mut seed)) % 1000000000);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..1000 {
            let got = broken_calc(starts[(r + i) % 1000], targets[i]);
            total += got;
            check = (check * 31 + got + 1) % 1000000007;
        }
    }
    println!("{} rounds over 1000 pairs: {} operations, checksum {}", rounds, total, check);
}
