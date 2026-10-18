// LeetCode 754 — Reach a Number, bench: the ★ arm (step by step),
// mirrored from reach_number.kara.

fn reach_number(target: i64) -> i64 {
    let t = target.abs();
    let mut k = 0;
    let mut sum = 0;
    while sum < t || (sum - t) % 2 != 0 {
        k += 1;
        sum += k;
    }
    k
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 30000;
    let mut seed: i64 = 754;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let mut target = (a * 32768 + b) % 1000000000 + 1;
        if next_random(&mut seed) % 2 == 0 {
            target = -target;
        }
        let moves = reach_number(target);
        total += moves;
        check = (check * 31 + moves) % 1000000007;
    }
    println!("{} targets: {} moves in all, checksum {}", rounds, total, check);
}
