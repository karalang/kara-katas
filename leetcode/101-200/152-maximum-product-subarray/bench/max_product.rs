//! Benchmark workload — Maximum Product Subarray, O(n) running max/min DP.
//! Algorithmic mirror of bench/max_product.kara / .c / .py / go-seq. See
//! ../README.md § Benchmarks for N / K and the deterministic LCG generator.

fn max_product(nums: &[i64]) -> i64 {
    if nums.is_empty() {
        return 0;
    }
    let mut best = nums[0];
    let mut cur_max = nums[0];
    let mut cur_min = nums[0];
    for &x in &nums[1..] {
        if x < 0 {
            std::mem::swap(&mut cur_max, &mut cur_min);
        }
        cur_max = x.max(cur_max * x);
        cur_min = x.min(cur_min * x);
        if cur_max > best {
            best = cur_max;
        }
    }
    best
}

fn main() {
    const N: usize = 2_000_000;
    let mut data = vec![0i64; N];
    let mut state: i64 = 12345;
    for d in data.iter_mut() {
        state = (state.wrapping_mul(1103515245).wrapping_add(12345)) & 2_147_483_647;
        *d = (state % 5) - 2;
    }
    let mut sum: i64 = 0;
    for _ in 0..10 {
        sum += max_product(&data);
    }
    println!("{}", sum);
}
