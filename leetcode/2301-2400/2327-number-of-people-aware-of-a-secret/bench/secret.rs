// LeetCode #2327: Number of People Aware of a Secret -- the bench, the ★
// arm in Rust. A running count of the people sharing gains those who
// learned the secret `delay` days back and loses those who learned it
// `forget` days back, and that many learn it each day. O(n).

const MOD: i64 = 1000000007;

fn people_aware_of_secret(n: i64, delay: i64, forget: i64) -> i64 {
    let mut learned = vec![0i64; (n + 1) as usize];
    learned[1] = 1;
    let mut sharing = 0i64;
    for day in 2..=n {
        if day - delay >= 1 {
            sharing = (sharing + learned[(day - delay) as usize]) % MOD;
        }
        if day - forget >= 1 {
            sharing = (sharing - learned[(day - forget) as usize] + MOD) % MOD;
        }
        learned[day as usize] = sharing;
    }
    let mut aware = 0i64;
    for day in (n - forget + 1)..=n {
        aware = (aware + learned[day as usize]) % MOD;
    }
    aware
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 2327;
    let mut cases: Vec<(i64, i64)> = Vec::new();
    for _ in 0..3000 {
        let forget = next_random(&mut seed) % 989 + 2;
        let delay = next_random(&mut seed) % (forget - 1) + 1;
        cases.push((delay, forget));
    }
    let mut check: i64 = 0;
    for p in 0..10i64 {
        for k in 0..3000usize {
            let (delay, forget) = cases[k];
            let n = 990 + (k as i64 + p) % 11;
            check = (check * 31 + people_aware_of_secret(n, delay, forget)) % 1000000007;
        }
    }
    println!("10 passes over 3000 cases of up to 1000 days: checksum {}", check);
}
