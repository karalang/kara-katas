// LeetCode 279 bench mirror — Rust. Same DP, same checksum.
const N: usize = 300000;
fn main() {
    let mut least = vec![0i64; N + 1];
    for i in 1..=N {
        let mut best = i as i64;
        let mut j = 1usize;
        while j * j <= i {
            let cand = least[i - j * j] + 1;
            if cand < best { best = cand; }
            j += 1;
        }
        least[i] = best;
    }
    let mut sum = 0i64;
    for k in 0..=N { sum = (sum * 31 + least[k]) % 1000000007; }
    println!("{}", (sum * 10 + least[N]) % 1000000007);
}
