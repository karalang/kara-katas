// LeetCode #11 — rayon-parallel Rust mirror (par lane, container).
// Same two-pointer max_area_off as ../container.rs; the K=10M reduction runs
// across a rayon pool. Hand-tuned-parallel comparator for Kāra's auto-par.
// Sink matches the kara/rust/c/go mirrors.

fn max_area_off(heights: &[i64], lo: usize, hi: usize) -> i64 {
    let mut l = lo;
    let mut r = hi;
    let mut best: i64 = 0;
    while l < r {
        let h_l = heights[l];
        let h_r = heights[r];
        let h = if h_l < h_r { h_l } else { h_r };
        let area = h * (r - l) as i64;
        if area > best {
            best = area;
        }
        if h_l < h_r {
            l += 1;
        } else {
            r -= 1;
        }
    }
    best
}

fn main() {
    use rayon::prelude::*;
    let n: i64 = 8;
    let w: i64 = 16;
    let total = (n * w) as usize;
    let k_iters: i64 = 10_000_000;

    let mut heights: Vec<i64> = vec![0; total];
    for i in 0..total as i64 {
        let raw: i64 = i.wrapping_mul(2_654_435_769).wrapping_add(305_419_896);
        let v: i64 = (raw % 50).rem_euclid(50);
        heights[i as usize] = v;
    }

    let sum: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let idx = k % n;
            let lo = (idx * w) as usize;
            let hi = lo + w as usize - 1;
            max_area_off(&heights, lo, hi)
        })
        .sum();
    println!("{}", sum);
}
