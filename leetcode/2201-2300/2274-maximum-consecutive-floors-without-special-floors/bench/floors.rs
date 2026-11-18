// LeetCode #2274: Maximum Consecutive Floors Without Special Floors --
// the bench, the ★ arm.

fn max_consecutive(bottom: i64, top: i64, special: &[i64]) -> i64 {
    let mut floors = special.to_vec();
    floors.sort();
    let mut best = (floors[0] - bottom).max(top - floors[floors.len() - 1]);
    for i in 1..floors.len() {
        best = best.max(floors[i] - floors[i - 1] - 1);
    }
    best
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2274;
    let mut check = 0;
    for _ in 0..50 {
        let mut special: Vec<i64> = Vec::new();
        let mut f = 1 + next_random(&mut seed) % 20000;
        while f <= 1000000000 && special.len() < 100000 {
            special.push(f);
            f += 1 + next_random(&mut seed) % 20000;
        }
        for j in (1..special.len()).rev() {
            let r = (next_random(&mut seed) % (j as i64 + 1)) as usize;
            special.swap(j, r);
        }
        check = (check * 31 + max_consecutive(1, 1000000000, &special)) % 1000000007;
    }
    println!("50 buildings of 10^5: checksum {check}");
}
