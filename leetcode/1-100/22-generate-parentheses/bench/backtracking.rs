// Bench mirror of backtracking.kara — same owned-snapshot recursive
// backtracking (each child call gets a freshly concatenated String),
// same K x n=10 full-set generation, same total-bytes sink.

fn backtrack(cur: String, open: i64, close: i64, n: i64, out: &mut Vec<String>) {
    if close == n {
        out.push(cur);
        return;
    }
    if open < n {
        backtrack(format!("{cur}("), open + 1, close, n, out);
    }
    if close < open {
        backtrack(format!("{cur})"), open, close + 1, n, out);
    }
}

fn generate_parenthesis(n: i64) -> Vec<String> {
    let mut out = Vec::new();
    backtrack(String::new(), 0, 0, n, &mut out);
    out
}

fn main() {
    let n = 10i64;
    let iters = 150;
    let mut total: u64 = 0;
    for _ in 0..iters {
        let combos = generate_parenthesis(n);
        let mut bytes: u64 = 0;
        for c in &combos {
            bytes += c.len() as u64;
        }
        total += bytes;
    }
    println!("{total}"); // 150 * 16796 * 20 = 50,388,000
}
