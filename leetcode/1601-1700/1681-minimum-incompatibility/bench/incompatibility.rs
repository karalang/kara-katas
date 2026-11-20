// LeetCode #1681: Minimum Incompatibility -- the bench's Rust mirror: the ★
// arm on 300 arrays of 16 values from 1 to 16, each with a random k that
// divides 16, all drawn first, each answered 4 times.

fn minimum_incompatibility(nums: &[i32], k: i32) -> i32 {
    let n = nums.len();
    let size = n / k as usize;
    let full: usize = (1 << n) - 1;
    let mut cost = vec![-1i32; 1 << n];
    for s in 0..=full {
        if s.count_ones() as usize != size {
            continue;
        }
        let mut seen: i64 = 0;
        let mut lo = i32::MAX;
        let mut hi = i32::MIN;
        let mut ok = true;
        for i in 0..n {
            if s >> i & 1 == 1 {
                let bit = 1i64 << nums[i];
                if seen & bit != 0 {
                    ok = false;
                    break;
                }
                seen |= bit;
                lo = lo.min(nums[i]);
                hi = hi.max(nums[i]);
            }
        }
        if ok {
            cost[s] = hi - lo;
        }
    }
    let unreached = i32::MAX;
    let mut best = vec![unreached; 1 << n];
    best[0] = 0;
    for m in 0..full {
        if best[m] == unreached || m.count_ones() as usize % size != 0 {
            continue;
        }
        let free = full ^ m;
        let lowest = free & free.wrapping_neg();
        let mut s = free;
        while s > 0 {
            if s & lowest != 0 && cost[s] >= 0 {
                best[m | s] = best[m | s].min(best[m] + cost[s]);
            }
            s = (s - 1) & free;
        }
    }
    if best[full] == unreached { -1 } else { best[full] }
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let arrays = 300;
    let n: i64 = 16;
    let rounds: i64 = 4;
    let ks = [1, 2, 4, 8, 16];
    let mut seed: i64 = 1681;
    let mut cases: Vec<(Vec<i32>, i32)> = Vec::new();
    for _ in 0..arrays {
        let nums: Vec<i32> = (0..n).map(|_| (next_random(&mut seed) % n + 1) as i32).collect();
        let k = ks[(next_random(&mut seed) % 5) as usize];
        cases.push((nums, k));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, k) in &cases {
            let answer = minimum_incompatibility(nums, *k) as i64;
            total += answer;
            check = (check * 31 + answer + 1 + r) % 1000000007;
        }
    }
    println!("{} arrays of {} values, {} rounds: answers sum to {}, checksum {}", arrays, n, rounds, total, check);
}
