// LeetCode #7 — rayon-parallel Rust mirror (par lane, reverse).
// Same pop-and-push reverse as ../reverse.rs; the K=50M reduction runs
// across a rayon pool. Hand-tuned-parallel comparator for Kāra's auto-par.
// Sink matches the kara/rust/c/go mirrors.

fn reverse(x: i32) -> i32 {
    let mut x = x;
    let mut result: i32 = 0;
    let int_max: i32 = 2_147_483_647;
    let int_min: i32 = -2_147_483_648;
    let max_div: i32 = int_max / 10;
    let min_div: i32 = int_min / 10;
    while x != 0 {
        let digit: i32 = x % 10;
        if result > max_div || (result == max_div && digit > 7) {
            return 0;
        }
        if result < min_div || (result == min_div && digit < -8) {
            return 0;
        }
        result = result * 10 + digit;
        x /= 10;
    }
    result
}

fn main() {
    use rayon::prelude::*;
    let n: i64 = 1024;
    let k_iters: i64 = 50_000_000;

    let mut inputs: Vec<i32> = Vec::with_capacity(n as usize);
    for i in 0..n {
        let raw: i64 = i.wrapping_mul(2_654_435_769).wrapping_add(305_419_896);
        let v32: i32 = raw as i32;
        inputs.push(v32);
    }

    let sum: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let idx = (k % n) as usize;
            reverse(inputs[idx]) as i64
        })
        .sum();
    println!("{}", sum);
}
