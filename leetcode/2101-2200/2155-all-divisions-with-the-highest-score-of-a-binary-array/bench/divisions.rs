// LeetCode #2155: All Divisions With the Highest Score of a Binary Array
// -- the benchmark's Rust mirror of divisions.kara.

fn max_score_indices(nums: &[i64]) -> Vec<i64> {
    let mut right_ones = nums.iter().filter(|&&x| x == 1).count() as i64;
    let mut left_zeros = 0i64;
    let mut top = right_ones;
    let mut found: Vec<i64> = vec![0];
    for (i, &x) in nums.iter().enumerate() {
        if x == 0 {
            left_zeros += 1;
        } else {
            right_ones -= 1;
        }
        let score = left_zeros + right_ones;
        if score > top {
            top = score;
            found.clear();
        }
        if score == top {
            found.push(i as i64 + 1);
        }
    }
    found
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2155i64;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..4 {
        let bits: Vec<i64> = (0..100000).map(|_| next_random(&mut seed) % 2).collect();
        lists.push(bits);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..50i64 {
        for s in 0..4 {
            let at = (next_random(&mut seed) % 100000) as usize;
            lists[s][at] = 1 - lists[s][at];
            let out = max_score_indices(&lists[s]);
            let len = out.len() as i64;
            total += len;
            check = (check * 31 + len + out[0] + out[out.len() - 1] + round) % 1000000007;
        }
    }
    println!("200 solves: {} divisions in all, checksum {}", total, check);
}
