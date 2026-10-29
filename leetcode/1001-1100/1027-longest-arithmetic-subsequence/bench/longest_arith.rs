// LeetCode #1027: Longest Arithmetic Subsequence -- bench
// Mirrors ./longest_arith.kara; see ../README.md § Benchmarks.

fn longest_arith_seq_length(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut run: Vec<Vec<i64>> = vec![vec![0; 1001]; n];
    let mut best = 2;
    for i in 1..n {
        for j in 0..i {
            let d = (nums[i] - nums[j] + 500) as usize;
            let length = if run[j][d] > 0 { run[j][d] + 1 } else { 2 };
            if length > run[i][d] {
                run[i][d] = length;
            }
            best = best.max(length);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 40;
    let rounds = 3;
    let mut seed = 1027;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let tops: [i64; 4] = [5, 50, 500, 500];
    for k in 0..count {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..1000 {
            nums.push(next_random(&mut seed) % (tops[k % 4] + 1));
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for nums in arrays.iter() {
            let answer = longest_arith_seq_length(nums);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    println!("{count} arrays of 1000 values, {rounds} rounds: sum {total}, checksum {check}");
}
