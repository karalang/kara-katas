// Benchmark: LeetCode #962 Maximum Width Ramp -- the ★ arm, decreasing
// stack, on 50000 numbers, LeetCode's largest, falling overall with
// noise. Each call first sets one number to a new random value. Mirrors
// max_width_ramp.kara, .c, .py and go-seq/.

fn max_width_ramp(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut stack: Vec<usize> = Vec::new();
    for i in 0..n {
        if stack.is_empty() || nums[i] < nums[stack[stack.len() - 1]] {
            stack.push(i);
        }
    }
    let mut best = 0;
    let mut j = n as i64 - 1;
    while j >= 0 && !stack.is_empty() {
        while !stack.is_empty() && nums[stack[stack.len() - 1]] <= nums[j as usize] {
            best = best.max(j - stack[stack.len() - 1] as i64);
            stack.pop();
        }
        j -= 1;
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn falling(seed: &mut i64, n: i64, step: i64, noise: i64) -> Vec<i64> {
    (0..n)
        .map(|p| 50000 - noise - p / step + next_random(seed) % (noise + 1))
        .collect()
}

fn main() {
    let rounds = 40;
    let mut seed = 962;
    let mut cases: Vec<Vec<i64>> = (0..50)
        .map(|i| falling(&mut seed, 50000, 1 + i % 5, 10 * (i / 5)))
        .collect();
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..50 {
            let c = (r + i) % 50;
            let p = (next_random(&mut seed) % 50000) as usize;
            cases[c][p] = next_random(&mut seed) % 50001;
            let w = max_width_ramp(&cases[c]);
            total += w;
            check = (check * 31 + w + i as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds over 50 cases of 50000 numbers: the ramps sum to {total}, checksum {check}");
}
