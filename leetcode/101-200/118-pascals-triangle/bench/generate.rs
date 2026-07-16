// LeetCode #118 — Rust mirror, additive Pascal's triangle.
// Same algorithm + workload as generate.kara: each rep builds a full triangle of a data-dependent
// row count (30 + acc%16) as a nested `Vec<Vec<i64>>` (matched to Kara's `Vec[Vec[i64]]`), folding
// every entry. K = 80000. Kara checks integer overflow by default, so the like-for-like row is
// `rustc -O -C overflow-checks=on`.

const MOD: i64 = 1000000007;

fn generate(num_rows: i64) -> Vec<Vec<i64>> {
    let mut tri: Vec<Vec<i64>> = Vec::new();
    for i in 0..num_rows {
        let mut row: Vec<i64> = Vec::new();
        for j in 0..=i {
            if j == 0 || j == i {
                row.push(1);
            } else {
                row.push(tri[(i - 1) as usize][(j - 1) as usize] + tri[(i - 1) as usize][j as usize]);
            }
        }
        tri.push(row);
    }
    tri
}

fn triangle_hash(tri: &[Vec<i64>]) -> i64 {
    let mut h: i64 = 1;
    for row in tri {
        for &x in row {
            h = (h * 131 + x) % MOD;
        }
        h = (h * 31 + row.len() as i64 + 7) % MOD;
    }
    h
}

fn main() {
    let mut acc: i64 = 0;
    for _ in 0..80000 {
        let rows = 30 + (acc % 16);
        let tri = generate(rows);
        let h = triangle_hash(&tri);
        acc = (acc * 131 + h) % MOD;
    }
    println!("{}", acc);
}
