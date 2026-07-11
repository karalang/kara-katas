// Benchmark workload — Largest Rectangle in Histogram (LeetCode #84).
// Rust mirror of bench/largest_rectangle.kara. Each iteration builds a fresh sawtooth
// histogram (heights[j] = (j + iter) % 50, N=2000) as a Vec<i64>, runs the
// monotonic-stack largest_rectangle (its stack a fresh Vec<i64>), and folds the area
// through a rolling polynomial hash. Same N/K. Compiled with `rustc -O`.
// See ../README.md § Benchmarks.

fn largest_rectangle(heights: &[i64], n: i64) -> i64 {
    let mut stack: Vec<i64> = Vec::new();
    let mut max_area = 0i64;
    let mut i = 0i64;
    while i <= n {
        let h = if i < n { heights[i as usize] } else { 0 };
        while !stack.is_empty() && heights[stack[stack.len() - 1] as usize] > h {
            let top = stack[stack.len() - 1];
            stack.pop();
            let height = heights[top as usize];
            let width = if stack.is_empty() {
                i
            } else {
                i - stack[stack.len() - 1] - 1
            };
            let area = height * width;
            if area > max_area {
                max_area = area;
            }
        }
        stack.push(i);
        i += 1;
    }
    max_area
}

fn build(n: i64, iter: i64) -> Vec<i64> {
    let mut h: Vec<i64> = Vec::with_capacity(n as usize);
    let mut j = 0i64;
    while j < n {
        h.push((j + iter) % 50);
        j += 1;
    }
    h
}

fn main() {
    const N: i64 = 2000;
    const TOTAL: i64 = 108000;
    const MODULUS: i64 = 1_000_000_007;

    let mut sum = 0i64;
    for k in 0..TOTAL {
        let h = build(N, k);
        let area = std::hint::black_box(largest_rectangle(&h, N));
        sum = (sum * 131 + (area + 1)) % MODULUS;
    }
    println!("{}", sum);
}
