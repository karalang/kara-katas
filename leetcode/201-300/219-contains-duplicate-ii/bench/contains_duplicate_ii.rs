use std::collections::HashMap;

fn count_nearby(nums: &[i64], k: i64) -> i64 {
    let mut last: HashMap<i64, i64> = HashMap::new();
    let n = nums.len() as i64;
    let mut hits = 0i64;
    for i in 0..n {
        let x = nums[i as usize];
        if let Some(&j) = last.get(&x) {
            if i - j <= k {
                hits += 1;
            }
        }
        last.insert(x, i);
    }
    hits
}

fn main() {
    let n: i64 = 1000000;
    let kmax: i64 = 40;
    let m: i64 = 49999;

    let mut nums: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        nums.push(state % m);
    }

    let mut sink: i64 = 0;
    for k in 1..=kmax {
        sink += count_nearby(&nums, k);
    }
    println!("{}", sink);
}
