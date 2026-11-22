// LeetCode #2826: Sorting Three Groups -- the bench's Rust mirror of the
// ★ arm: a three-state table of the most numbers kept so far ending at a
// value at most v.

fn minimum_operations(nums: &[i64]) -> i64 {
    let mut best = [0i64; 3];
    for &x in nums {
        let v = (x - 1) as usize;
        best[v] += 1;
        for w in v + 1..3 {
            best[w] = best[w].max(best[v]);
        }
    }
    nums.len() as i64 - best[2]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 200000;
    let rounds = 5;
    let mut seed = 2826;
    let cases: Vec<Vec<i64>> = (0..count).map(|_| (0..100).map(|_| next_random(&mut seed) % 3 + 1).collect()).collect();
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in &cases {
            let a = minimum_operations(nums);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{} arrays of 100, {} rounds: {} removals, checksum {}", count, rounds, total, check);
}
