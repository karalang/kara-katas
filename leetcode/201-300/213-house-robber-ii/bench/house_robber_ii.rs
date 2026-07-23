// Benchmark workload for LeetCode #213 — House Robber II.
fn rob_linear(nums: &[i64], lo: i64, hi: i64) -> i64 {
    let mut prev = 0i64;
    let mut cur = 0i64;
    let mut i = lo;
    while i < hi {
        let take = prev + nums[i as usize];
        let next = if take > cur { take } else { cur };
        prev = cur;
        cur = next;
        i += 1;
    }
    cur
}

fn rob_window(nums: &[i64], s: i64, w: i64) -> i64 {
    if w == 1 {
        return nums[s as usize];
    }
    let skip_last = rob_linear(nums, s, s + w - 1);
    let skip_first = rob_linear(nums, s + 1, s + w);
    if skip_last > skip_first {
        skip_last
    } else {
        skip_first
    }
}

fn main() {
    let n: i64 = 100000;
    let window: i64 = 2000;
    let windows: i64 = 130000;

    let mut nums: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        nums.push(1 + state % 1000); // 1..1000, all positive
    }

    let span = n - window;
    let mut sink: i64 = 0;
    for w in 0..windows {
        let s = (w * 977) % span;
        sink += rob_window(&nums, s, window);
    }

    println!("{}", sink);
}
