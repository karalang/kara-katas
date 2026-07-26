// Benchmark harness for LeetCode #239 — Sliding Window Maximum.
// Mirrors sliding_window_max.kara algorithm-for-algorithm, including the
// Vec-plus-head-cursor deque rather than VecDeque, so the data structure
// matches.

fn max_sliding_window(nums: &[i64], k: i64) -> Vec<i64> {
    let n = nums.len() as i64;
    let mut out: Vec<i64> = Vec::new();
    let mut dq: Vec<i64> = Vec::new();
    let mut head: i64 = 0;

    let mut i: i64 = 0;
    while i < n {
        while dq.len() as i64 > head {
            let back = dq[dq.len() - 1];
            if nums[back as usize] <= nums[i as usize] {
                dq.pop();
            } else {
                break;
            }
        }
        dq.push(i);

        if dq[head as usize] <= i - k {
            head += 1;
        }

        if i >= k - 1 {
            out.push(nums[dq[head as usize] as usize]);
        }
        i += 1;
    }
    out
}

fn lcg(seed: i64, n: i64, cap: i64) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    let mut x = seed;
    for _ in 0..n {
        x = (x * 1103515245 + 12345) % 2147483648;
        out.push(x % cap);
    }
    out
}

fn main() {
    let np: i64 = 8;
    let n: i64 = 50000;
    let cap: i64 = 100000;
    let k: i64 = 64;
    let iters: i64 = 300;

    let arrays: Vec<Vec<i64>> = (0..np).map(|j| lcg(j + 1, n, cap)).collect();

    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = ((it * 3) % np) as usize;
        let res = max_sliding_window(&arrays[idx], k);
        for (v, &val) in res.iter().enumerate() {
            sink = (sink + (v as i64 + 1) * val) % 1000000007;
        }
    }
    println!("{}", sink);
}
