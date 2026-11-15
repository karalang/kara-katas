// benchmark's Rust mirror of distant.kara (LeetCode #2200, the ★ arm): the
// key's windows, a `next` index.

fn find_k_distant_indices(nums: &[i64], key: i64, k: i64) -> Vec<i64> {
    let n = nums.len() as i64;
    let mut out: Vec<i64> = Vec::new();
    let mut next = 0;
    for j in 0..n {
        if nums[j as usize] != key {
            continue;
        }
        let from = if j - k > next { j - k } else { next };
        let to = if j + k < n - 1 { j + k } else { n - 1 };
        for i in from..=to {
            out.push(i);
        }
        next = to + 1;
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2200;
    let mut cases: Vec<(Vec<i64>, i64, i64)> = Vec::new();
    for c in 0..1000 {
        let top = [50, 200, 1000][c % 3];
        let nums: Vec<i64> = (0..1000).map(|_| next_random(&mut seed) % top + 1).collect();
        let key = nums[(next_random(&mut seed) % 1000) as usize];
        let k = next_random(&mut seed) % 20 + 1;
        cases.push((nums, key, k));
    }
    let mut check: i64 = 0;
    for _ in 0..600 {
        for (nums, key, k) in &cases {
            let out = find_k_distant_indices(nums, *key, *k);
            check = (check * 31 + out.len() as i64) % 1000000007;
            if !out.is_empty() {
                check = (check * 31 + out[out.len() / 2]) % 1000000007;
            }
        }
    }
    println!("600 passes over 1000 arrays: checksum {}", check);
}
