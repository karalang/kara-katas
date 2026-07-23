use std::collections::HashMap;

fn abs_i64(x: i64) -> i64 {
    if x < 0 { -x } else { x }
}

fn bucket_of(x: i64, w: i64) -> i64 {
    if x >= 0 { x / w } else { (x + 1) / w - 1 }
}

fn near_value(m: &HashMap<i64, i64>, b: i64, x: i64, t: i64) -> bool {
    if let Some(&v) = m.get(&b) {
        if abs_i64(x - v) <= t {
            return true;
        }
    }
    false
}

fn contains(nums: &[i64], n: i64, k: i64, t: i64) -> bool {
    if k <= 0 {
        return false;
    }
    let w = t + 1;
    let mut buckets: HashMap<i64, i64> = HashMap::new();
    let mut i = 0i64;
    while i < n {
        let x = nums[i as usize];
        let b = bucket_of(x, w);
        if near_value(&buckets, b, x, t) {
            return true;
        }
        if near_value(&buckets, b - 1, x, t) {
            return true;
        }
        if near_value(&buckets, b + 1, x, t) {
            return true;
        }
        buckets.insert(b, x);
        if i >= k {
            let old = nums[(i - k) as usize];
            buckets.remove(&bucket_of(old, w));
        }
        i += 1;
    }
    false
}

fn main() {
    let n: i64 = 20000;
    let pairs: i64 = 800;
    let valrange: i64 = 8000000;
    let half: i64 = 4000000;

    let mut nums: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        nums.push((state % valrange) - half);
    }

    let mut sink = 0i64;
    for p in 0..pairs {
        let k = 32 + (p % 512);
        let t = p % 3;
        if contains(&nums, n, k, t) {
            sink += 1;
        }
    }
    println!("{}", sink);
}
