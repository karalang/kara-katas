fn summary_metric(nums: &[i64], n: i64) -> i64 {
    let mut i: i64 = 1;
    let mut start = nums[0];
    let mut ranges: i64 = 0;
    let mut esum: i64 = 0;
    while i <= n {
        if i == n || nums[i as usize] != nums[(i - 1) as usize] + 1 {
            let end = nums[(i - 1) as usize];
            ranges += 1;
            esum += start + end;
            if i < n {
                start = nums[i as usize];
            }
        }
        i += 1;
    }
    ranges + esum
}

fn main() {
    let n: i64 = 1000000;
    let passes: i64 = 250;

    let mut nums: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    let mut v: i64 = 0;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        v = v + 1 + (state % 3);
        nums.push(v);
    }

    let mut sink: i64 = 0;
    for _ in 0..passes {
        sink += summary_metric(&nums, n);
    }
    println!("{}", sink);
}
