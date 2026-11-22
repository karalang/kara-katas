// LeetCode #2735: Collecting Chocolates -- the bench (chocolates.kara in
// Rust): each type's cheapest price within k turns, narrowed one turn at a
// time, and the least of k x plus their sum.

fn min_cost(nums: &[i64], x: i64) -> i64 {
    let n = nums.len();
    let mut cheapest = nums.to_vec();
    let mut best: i64 = nums.iter().sum();
    for k in 1..n {
        for t in 0..n {
            cheapest[t] = cheapest[t].min(nums[(t + n - k) % n]);
        }
        let total: i64 = cheapest.iter().sum();
        best = best.min(k as i64 * x + total);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let cases = 100;
    let n = 1000;
    let rounds = 3;
    let mut seed: i64 = 2735;
    let mut problems: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..cases {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            let hi = next_random(&mut seed);
            nums.push((hi * 32768 + next_random(&mut seed)) % 1000000000 + 1);
        }
        let hi = next_random(&mut seed);
        let x = (hi * 32768 + next_random(&mut seed)) % 10000000 + 1;
        problems.push((nums, x));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, x) in problems.iter() {
            let cost = min_cost(nums, *x);
            sum += cost;
            check = (check * 31 + cost + r) % 1000000007;
        }
    }
    println!("{} cases of {} chocolates, {} rounds: costs sum to {}, checksum {}", cases, n, rounds, sum, check);
}
