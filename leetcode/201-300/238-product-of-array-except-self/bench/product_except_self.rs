// Benchmark harness for LeetCode #238 — Product of Array Except Self.
// Mirrors product_except_self.kara algorithm-for-algorithm.

fn product_except_self(nums: &[i64]) -> Vec<i64> {
    let n = nums.len();
    let mut out: Vec<i64> = Vec::new();

    let mut prefix: i64 = 1;
    for i in 0..n {
        out.push(prefix);
        prefix *= nums[i];
    }

    let mut suffix: i64 = 1;
    let mut j = n as i64 - 1;
    while j >= 0 {
        out[j as usize] *= suffix;
        suffix *= nums[j as usize];
        j -= 1;
    }

    out
}

fn lcg_vals(seed: i64, n: i64) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    let mut x = seed;
    for _ in 0..n {
        x = (x * 1103515245 + 12345) % 2147483648;
        out.push(1 - 2 * ((x / 65536) % 2));
    }
    out
}

fn main() {
    let np: i64 = 8;
    let n: i64 = 100000;
    let iters: i64 = 400;

    let arrays: Vec<Vec<i64>> = (0..np).map(|j| lcg_vals(j + 1, n)).collect();

    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = ((it * 3) % np) as usize;
        let res = product_except_self(&arrays[idx]);
        for (v, &val) in res.iter().enumerate() {
            sink = (sink + (v as i64 + 1) * val) % 1000000007;
        }
    }
    println!("{}", sink);
}
