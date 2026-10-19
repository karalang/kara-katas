// LeetCode 766 — Toeplitz Matrix: benchmark, the ★ arm in Rust.
// Sixteen 200 by 200 Toeplitz matrices, built once; 30,000 rounds of
// changing one cell, asking, and putting it back.

fn is_toeplitz_matrix(matrix: &[Vec<i64>]) -> bool {
    for i in 1..matrix.len() {
        for j in 1..matrix[i].len() {
            if matrix[i][j] != matrix[i - 1][j - 1] {
                return false;
            }
        }
    }
    true
}

fn main() {
    let mut seed: i64 = 766;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let size: i64 = 200;
    let rounds = 30000;
    let mut pool: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..16 {
        let diag: Vec<i64> = (0..2 * size - 1).map(|_| next_random() % 10).collect();
        let matrix: Vec<Vec<i64>> = (0..size)
            .map(|i| (0..size).map(|j| diag[(i - j + size - 1) as usize]).collect())
            .collect();
        pool.push(matrix);
    }
    let mut yes: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..rounds {
        let k = round % 16;
        let i = next_random() % size;
        let j = next_random() % size;
        let old = pool[k][i as usize][j as usize];
        pool[k][i as usize][j as usize] = old + next_random() % 2;
        let answer = is_toeplitz_matrix(&pool[k]);
        pool[k][i as usize][j as usize] = old;
        if answer {
            yes += 1;
        }
        check = (check * 31 + if answer { 1 } else { 0 } + i * size + j) % 1000000007;
    }
    println!("{} rounds on 200 by 200: {} Toeplitz, checksum {}", rounds, yes, check);
}
