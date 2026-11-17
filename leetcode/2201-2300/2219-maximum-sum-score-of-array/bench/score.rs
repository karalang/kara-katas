// LeetCode #2219: Maximum Sum Score of Array -- bench mirror of
// score.kara: with the total known, one pass keeps the sum before i, and
// the sum from i on is the total less it.

fn maximum_sum_score(nums: &[i64]) -> i64 {
    let mut total: i64 = 0;
    for &x in nums {
        total += x;
    }
    let mut before: i64 = 0;
    // no score is below the smaller of the first number and the total
    let mut best = nums[0].min(total);
    for &x in nums {
        let from_here = total - before;
        before += x;
        best = best.max(before).max(from_here);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// a draw of 30 bits, since one draw stops at 32767
fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2219;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..30 {
        // 10^5 numbers from -10^5 to 10^5
        arrays.push((0..100000).map(|_| wide_random(&mut seed) % 200001 - 100000).collect());
    }
    let mut check: i64 = 0;
    for a in 0..30 {
        for r in 0..10 {
            // punch: one number is drawn again before each answer
            arrays[a][r * 9999] = wide_random(&mut seed) % 200001 - 100000;
            check = (check * 31 + maximum_sum_score(&arrays[a]) + 10000000000) % 1000000007;
        }
    }
    println!("30 arrays of 10^5, 10 punches: checksum {check}");
}
