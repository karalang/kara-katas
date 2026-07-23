fn window_majority_sum(nums: &[i64], s: i64, win: i64) -> i64 {
    let mut cand1: i64 = 0;
    let mut cand2: i64 = 0;
    let mut count1: i64 = 0;
    let mut count2: i64 = 0;

    let end = s + win;
    let mut k = s;
    while k < end {
        let x = nums[k as usize];
        if count1 > 0 && x == cand1 {
            count1 += 1;
        } else if count2 > 0 && x == cand2 {
            count2 += 1;
        } else if count1 == 0 {
            cand1 = x;
            count1 = 1;
        } else if count2 == 0 {
            cand2 = x;
            count2 = 1;
        } else {
            count1 -= 1;
            count2 -= 1;
        }
        k += 1;
    }

    let mut real1: i64 = 0;
    let mut real2: i64 = 0;
    let mut j = s;
    while j < end {
        let x = nums[j as usize];
        if count1 > 0 && x == cand1 {
            real1 += 1;
        } else if count2 > 0 && x == cand2 {
            real2 += 1;
        }
        j += 1;
    }

    let threshold = win / 3;
    let mut total: i64 = 0;
    if count1 > 0 && real1 > threshold {
        total += cand1;
    }
    if count2 > 0 && real2 > threshold {
        total += cand2;
    }
    total
}

fn main() {
    let n: i64 = 3000000;
    let win: i64 = 16;

    let mut nums: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        nums.push((state % 3) + 1);
    }

    let mut sink: i64 = 0;
    let last = n - win;
    let mut s = 0i64;
    while s <= last {
        sink += window_majority_sum(&nums, s, win);
        s += 1;
    }
    println!("{}", sink);
}
