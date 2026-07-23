fn max_i64(a: i64, b: i64) -> i64 {
    if a > b {
        a
    } else {
        b
    }
}

fn rob(nums: &[i64], n: i64) -> i64 {
    let mut prev2: i64 = 0;
    let mut prev: i64 = 0;
    let mut i: i64 = 0;
    while i < n {
        let cur = max_i64(prev, prev2 + nums[i as usize]);
        prev2 = prev;
        prev = cur;
        i += 1;
    }
    prev
}

fn main() {
    let n: i64 = 5000;
    let passes: i64 = 90000;

    let mut nums: Vec<i64> = Vec::with_capacity(n as usize);
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        nums.push((state >> 16) % 1000);
    }

    let mut sink: i64 = 0;
    for _ in 0..passes {
        state = (state * 1103515245 + 12345) & 2147483647;
        let idx = (state % n) as usize;
        nums[idx] = (state >> 16) % 1000;
        sink += rob(&nums, n);
    }
    println!("{}", sink);
}
