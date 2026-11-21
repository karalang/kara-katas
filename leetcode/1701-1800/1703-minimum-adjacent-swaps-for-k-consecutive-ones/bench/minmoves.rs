// LeetCode #1703: Minimum Adjacent Swaps for K Consecutive Ones -- the
// bench's Rust mirror: the ★ arm on 50 random arrays of 100000 values,
// each with a random k, all drawn first, each answered 40 times.

// each window of k ones about its median, q[j] = p[j] - j, by prefix sums
fn min_moves(nums: &[i32], k: i32) -> i32 {
    let mut q: Vec<i64> = Vec::new();
    for (i, &v) in nums.iter().enumerate() {
        if v == 1 {
            q.push(i as i64 - q.len() as i64);
        }
    }
    let mut prefix: Vec<i64> = vec![0];
    for &x in q.iter() {
        prefix.push(prefix[prefix.len() - 1] + x);
    }
    let k = k as i64;
    let mut best = i64::MAX;
    for i in 0..=(q.len() as i64 - k) {
        let end = i + k;
        let m = i + k / 2;
        let qm = q[m as usize];
        let left = qm * (m - i) - (prefix[m as usize] - prefix[i as usize]);
        let right = (prefix[end as usize] - prefix[m as usize + 1]) - qm * (end - m - 1);
        best = best.min(left + right);
    }
    best as i32
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let rounds = 40;
    let n = 100000;
    let mut seed = 1703;
    let mut arrays: Vec<(Vec<i32>, i32)> = Vec::new();
    for _ in 0..count {
        // each value a 1 with a chance of its array's own, 1 to 10 in 10
        let lean = next_random(&mut seed) % 10 + 1;
        let mut nums: Vec<i32> = Vec::new();
        for _ in 0..n {
            nums.push(if next_random(&mut seed) % 10 < lean { 1 } else { 0 });
        }
        let ones = nums.iter().filter(|&&v| v == 1).count() as i64;
        let k = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % ones + 1) as i32;
        arrays.push((nums, k));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, k) in arrays.iter() {
            let answer = min_moves(nums, *k) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n} values, {rounds} rounds: answers sum to {sum}, checksum {check}");
}
