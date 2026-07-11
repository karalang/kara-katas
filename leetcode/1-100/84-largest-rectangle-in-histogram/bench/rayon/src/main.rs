// LeetCode #84 — rayon-parallel Rust mirror (par lane).
// Same batch of K=108000 independent largest-rectangle computations as
// ../largest_rectangle.rs; the associative sum reduction runs across a rayon pool.
// Hand-tuned-parallel comparator for Kāra's auto-par. Sink matches the seq mirrors.
use rayon::prelude::*;

const N: i64 = 2000;

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

fn compute(seed: i64) -> i64 {
    let mut h: Vec<i64> = Vec::with_capacity(N as usize);
    for j in 0..N {
        h.push((j + seed) % 50);
    }
    largest_rectangle(&h, N)
}

fn main() {
    let sum: i64 = (0..108000_i64).into_par_iter().map(compute).sum();
    println!("{}", sum);
}
