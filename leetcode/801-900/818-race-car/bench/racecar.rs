// Benchmark for #818: Race Car -- the ★ arm (the best run to each distance).
//
// Mirrors racecar.kara: one table of the best run to every distance up to
// the target, each entry the better of overshooting and stopping short.

fn racecar(target: i64) -> i64 {
    let mut best = vec![0i64; (target + 1) as usize];
    for t in 1..=target {
        let mut n: i64 = 0;
        while (1i64 << n) <= t {
            n += 1;
        }
        let full = (1i64 << n) - 1;
        if t == full {
            best[t as usize] = n;
            continue;
        }
        let mut shortest = n + 1 + best[(full - t) as usize];
        let short = (1i64 << (n - 1)) - 1;
        for m in 0..n - 1 {
            let back = (1i64 << m) - 1;
            let steps = (n - 1) + 1 + m + 1 + best[(t - short + back) as usize];
            if steps < shortest {
                shortest = steps;
            }
        }
        best[t as usize] = shortest;
    }
    best[target as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds: i64 = 40000;
    let mut seed: i64 = 818;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let t = 1 + next_random(&mut seed) % 10000;
        let answer = racecar(t);
        total += answer;
        checksum = (checksum * 131 + answer) % 1000000007;
    }
    println!("{} rounds of targets up to 10000: total {}, checksum {}", rounds, total, checksum);
}
