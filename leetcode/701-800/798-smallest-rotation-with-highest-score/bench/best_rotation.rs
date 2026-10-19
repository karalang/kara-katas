// LeetCode 798 — Smallest Rotation with Highest Score: the bench, in
// Rust. Mirrors best_rotation.kara: a difference array over the
// rotations.

fn best_rotation(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    let mut change: Vec<i64> = vec![0; n as usize + 1];
    for i in 0..n {
        let first = (i + 1) % n;
        let last = (i - nums[i as usize] + n) % n;
        change[first as usize] += 1;
        change[last as usize + 1] -= 1;
        if first > last {
            change[0] += 1;
            change[n as usize] -= 1;
        }
    }
    let (mut best, mut best_score, mut score) = (0i64, -1i64, 0i64);
    for k in 0..n {
        score += change[k as usize];
        if score > best_score {
            best_score = score;
            best = k;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 100000;
    let mut seed = 798;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..16 {
        let hi = next_random(&mut seed);
        let top = 1 + (hi * 32768 + next_random(&mut seed)) % n;
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            let h = next_random(&mut seed);
            nums.push((h * 32768 + next_random(&mut seed)) % top);
        }
        arrays.push(nums);
    }
    let rounds: i64 = 4000;
    let (mut total, mut check) = (0i64, 0i64);
    for r in 0..rounds {
        let k = best_rotation(&arrays[(r % 16) as usize]);
        total += k;
        check = (check * 131 + k) % 1000000007;
    }
    println!("{rounds} rounds of {n} numbers: rotations adding up to {total}, checksum {check}");
}
