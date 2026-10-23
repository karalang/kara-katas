// LeetCode #867: Transpose Matrix -- Rust mirror of the bench program (the
// ★ arm, one column at a time), on `Vec<Vec<i64>>` (LeetCode's signature
// uses `i32`; the entries here are 64-bit, as in the Kāra program).

fn transpose(matrix: &Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    let rows = matrix.len();
    let cols = matrix[0].len();
    let mut out: Vec<Vec<i64>> = Vec::new();
    for c in 0..cols {
        let mut row: Vec<i64> = Vec::new();
        for r in 0..rows {
            row.push(matrix[r][c]);
        }
        out.push(row);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    let lo = next_random(seed);
    (hi * 32768 + lo) % 2000000001 - 1000000000
}

fn main() {
    let mut seed = 867;
    let mut m: Vec<Vec<i64>> = Vec::new();
    for _ in 0..1000 {
        let mut row: Vec<i64> = Vec::new();
        for _ in 0..100 {
            row.push(random_value(&mut seed));
        }
        m.push(row);
    }
    let rounds = 6000;
    let mut check: i64 = 0;
    for round in 0..rounds {
        m = transpose(&m);
        let r = round * 7 % m.len();
        let c = round * 13 % m[0].len();
        check = (check * 31 + m[r][c] % 1000000007 + 1000000007) % 1000000007;
    }
    for row in m.iter() {
        for v in row.iter() {
            check = (check * 31 + *v % 1000000007 + 1000000007) % 1000000007;
        }
    }
    println!("{} transposes of a 1000 x 100 matrix: {} x {}, checksum {}", rounds, m.len(), m[0].len(), check);
}
