// Benchmark lane for LeetCode 315 — Rust mirror of bench/count_smaller.kara.
// Generate N values once, then PASSES Fenwick-tree passes (sort+dedup for the
// ranks, then per element a binary search, a prefix query and a point update,
// right to left), each after swapping two elements chosen from the checksum.

const N: i64 = 200000;
const PASSES: i64 = 24;
const MASK: i64 = 1073741823;

fn lcg(s: i64) -> i64 {
    (s * 1103515245 + 12345) & 0x7fffffff
}

fn lower_bound(sorted: &[i64], x: i64) -> usize {
    let mut lo = 0usize;
    let mut hi = sorted.len();
    while lo < hi {
        let mid = (lo + hi) / 2;
        if sorted[mid] < x {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo
}

fn count_smaller(nums: &[i64]) -> Vec<i64> {
    let n = nums.len();
    let mut distinct = nums.to_vec();
    distinct.sort();
    distinct.dedup();
    let m = distinct.len();
    let mut tree = vec![0i64; m + 1];
    let mut counts = vec![0i64; n];
    for i in (0..n).rev() {
        let r = lower_bound(&distinct, nums[i]);
        let mut total = 0i64;
        let mut x = r as i64;
        while x > 0 {
            total += tree[x as usize];
            x -= x & -x;
        }
        counts[i] = total;
        x = r as i64 + 1;
        while x <= m as i64 {
            tree[x as usize] += 1;
            x += x & -x;
        }
    }
    counts
}

fn main() {
    let mut seed: i64 = 315;
    let mut nums: Vec<i64> = Vec::with_capacity(N as usize);
    for _ in 0..N {
        seed = lcg(seed);
        nums.push(seed % 200001 - 100000);
    }
    let mut checksum: i64 = 0;
    for _ in 0..PASSES {
        let i = (checksum % N) as usize;
        let j = ((checksum * 7 + 13) % N) as usize;
        nums.swap(i, j);
        let counts = count_smaller(&nums);
        let total: i64 = counts.iter().sum();
        checksum = (checksum * 31 + total) & MASK;
        nums.swap(i, j);
    }
    println!("checksum {}", checksum);
}
