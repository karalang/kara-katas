// LeetCode #1072: Flip Columns For Maximum Number of Equal Rows -- the
// benchmark's Rust mirror of equal_rows.kara: the same count of row
// patterns in a HashMap over 200 matrices built once, each answered 30
// times.

use std::collections::HashMap;

fn max_equal_rows(matrix: &[Vec<i64>]) -> i64 {
    let mut counts: HashMap<String, i64> = HashMap::new();
    let mut best = 0;
    for row in matrix.iter() {
        let mut key = String::new();
        for c in row.iter() {
            key.push(if *c != row[0] { '1' } else { '0' });
        }
        let seen = counts.get(&key).copied().unwrap_or(0) + 1;
        counts.insert(key, seen);
        best = best.max(seen);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_bits(n: i64, seed: &mut i64) -> Vec<i64> {
    (0..n).map(|_| next_random(seed) % 2).collect()
}

fn random_matrix(rows: i64, cols: i64, seed: &mut i64) -> Vec<Vec<i64>> {
    let m = next_random(seed) % rows + 1;
    let n = next_random(seed) % cols + 1;
    let mut patterns = Vec::new();
    for _ in 0..next_random(seed) % 3 + 1 {
        patterns.push(random_bits(n, seed));
    }
    let mut matrix = Vec::new();
    for _ in 0..m {
        let roll = next_random(seed) % 8;
        if roll < 2 {
            matrix.push(random_bits(n, seed));
        } else {
            let p: &Vec<i64> = &patterns[(next_random(seed) % patterns.len() as i64) as usize];
            if roll < 5 {
                matrix.push(p.iter().map(|c| 1 - c).collect());
            } else {
                matrix.push(p.clone());
            }
        }
    }
    matrix
}

fn main() {
    let mut seed = 1072;
    let matrices: Vec<Vec<Vec<i64>>> = (0..200).map(|_| random_matrix(300, 300, &mut seed)).collect();
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..30 {
        for matrix in matrices.iter() {
            let x = max_equal_rows(matrix);
            total += x;
            check = (check * 31 + x) % 1000000007;
        }
    }
    println!("6000 calls: answers sum {total}, checksum {check}");
}
