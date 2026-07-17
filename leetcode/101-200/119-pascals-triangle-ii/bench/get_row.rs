// LeetCode #119 — Rust mirror, in-place single-row Pascal.
// Same algorithm + workload as get_row.kara: one Vec<i64> of length rowIndex+1 (data-dependent
// rowIndex = 30 + acc%20), updated in place right-to-left, folding every entry. K=440000. Kara
// checks integer overflow by default, so the like-for-like row is `rustc -O -C overflow-checks=on`.
const MOD: i64 = 1000000007;
fn get_row(ri: i64) -> Vec<i64> {
    let n = (ri + 1) as usize;
    let mut row = vec![1i64; n];
    for i in 2..=ri {
        let mut k = (i - 1) as usize;
        while k >= 1 {
            row[k] = row[k] + row[k - 1];
            k -= 1;
        }
    }
    row
}
fn row_hash(row: &[i64]) -> i64 {
    let mut h: i64 = 1;
    for &x in row { h = (h * 131 + x) % MOD; }
    (h * 31 + row.len() as i64 + 7) % MOD
}
fn main() {
    let mut acc: i64 = 0;
    for _ in 0..440000 {
        let ri = 30 + (acc % 20);
        acc = (acc * 131 + row_hash(&get_row(ri))) % MOD;
    }
    println!("{}", acc);
}
