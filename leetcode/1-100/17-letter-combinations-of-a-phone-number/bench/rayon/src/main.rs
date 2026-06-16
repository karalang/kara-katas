// LeetCode #17 — rayon-parallel Rust mirror (par lane, letter_combinations).
// Same BFS letter_combinations as ../letter_combinations.rs; the K=100k
// reduction runs across a rayon pool. Hand-tuned-parallel comparator for
// Kāra's auto-par. Sink matches the kara/rust/c/go mirrors.

fn letter_combinations(digits: &str) -> Vec<String> {
    let mut out: Vec<String> = Vec::new();
    if digits.is_empty() {
        return out;
    }
    let groups: [&str; 8] = ["abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"];

    out.push(String::new());
    for d in digits.bytes() {
        let idx = (d - b'2') as usize;
        let letters = groups[idx];
        let prev_len = out.len();
        let mut next: Vec<String> = Vec::new();
        for i in 0..prev_len {
            for letter in letters.chars() {
                let mut s = String::new();
                s.push_str(&out[i]);
                s.push(letter);
                next.push(s);
            }
        }
        out = next;
    }
    out
}

fn main() {
    use rayon::prelude::*;
    let m_cases: i64 = 8;
    let k_iters: i64 = 100_000;

    let cases: [&str; 8] = ["", "2", "7", "23", "79", "234", "279", "2349"];

    let sum: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let idx = (k % m_cases) as usize;
            letter_combinations(cases[idx]).len() as i64
        })
        .sum();
    println!("{}", sum);
}
