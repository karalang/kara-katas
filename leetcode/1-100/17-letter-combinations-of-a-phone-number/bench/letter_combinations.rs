// Benchmark workload — Letter Combinations of a Phone Number (LeetCode #17).
// Rust mirror of bench/letter_combinations.kara. Same M/K, generator, BFS
// shape, and sink — see that file's header for the workload rationale.

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
    let m_cases: i64 = 8;
    let k_iters: i64 = 100_000;

    let cases: [&str; 8] = ["", "2", "7", "23", "79", "234", "279", "2349"];

    let mut sum: i64 = 0;
    let mut k: i64 = 0;
    while k < k_iters {
        let idx = (k % m_cases) as usize;
        let r = letter_combinations(cases[idx]);
        sum += r.len() as i64;
        k += 1;
    }
    println!("{}", sum);
}
