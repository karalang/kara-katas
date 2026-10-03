// Benchmark workload for LeetCode #334 — Rust mirror of increasing_triplet.kara.

const VALUES: i64 = 1000000;
const PUNCHES: i64 = 100;
const MODULUS: i64 = 1073741789;

fn increasing_triplet(nums: &[i64]) -> bool {
    let mut first: Option<i64> = None;
    let mut second: Option<i64> = None;
    for &x in nums {
        match second {
            Some(s) if x > s => return true,
            _ => {}
        }
        match first {
            Some(f) if x > f => second = Some(x),
            _ => first = Some(x),
        }
    }
    false
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = next(seed);
    hi * 32768 + next(seed)
}

fn main() {
    let mut nums: Vec<i64> = Vec::new();
    let mut top = 2 * VALUES;
    for _ in 0..(VALUES / 2) {
        nums.push(top - 1);
        nums.push(top);
        top -= 2;
    }
    let mut seed = 334i64;
    let mut sink = 0i64;
    for p in 0..PUNCHES {
        let at = (2 + 2 * (wide(&mut seed) % (VALUES / 2 - 1))) as usize;
        let old = nums[at];
        if p % 2 == 0 {
            nums[at] = nums[at - 1] + 1;
        }
        let answer = if increasing_triplet(&nums) { 1 } else { 0 };
        nums[at] = old;
        sink = (sink * 1000003 + answer * 2000003 + at as i64) % MODULUS;
    }
    println!("{sink}");
}
