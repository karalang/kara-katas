// LeetCode #1284 bench, in Rust: the ★ arm (breadth-first search over bit
// masks) on every matrix of every shape, 1 by 1 to 3 by 3, 3000 rounds,
// every answer folded into a checksum.
use std::collections::VecDeque;

fn min_flips(mat: &[Vec<i64>]) -> i64 {
    let rows = mat.len();
    let cols = mat[0].len();
    let cells = rows * cols;
    let mut start: i64 = 0;
    let mut flip: Vec<i64> = Vec::new();
    for i in 0..rows {
        for j in 0..cols {
            if mat[i][j] == 1 {
                start |= 1 << (i * cols + j);
            }
            let mut mask: i64 = 1 << (i * cols + j);
            if i > 0 {
                mask |= 1 << ((i - 1) * cols + j);
            }
            if i + 1 < rows {
                mask |= 1 << ((i + 1) * cols + j);
            }
            if j > 0 {
                mask |= 1 << (i * cols + j - 1);
            }
            if j + 1 < cols {
                mask |= 1 << (i * cols + j + 1);
            }
            flip.push(mask);
        }
    }
    let mut dist = vec![-1i64; 1 << cells];
    dist[start as usize] = 0;
    let mut queue: VecDeque<i64> = VecDeque::new();
    queue.push_back(start);
    while let Some(state) = queue.pop_front() {
        if state == 0 {
            return dist[state as usize];
        }
        for &mask in flip.iter() {
            let next = state ^ mask;
            if dist[next as usize] < 0 {
                dist[next as usize] = dist[state as usize] + 1;
                queue.push_back(next);
            }
        }
    }
    -1
}

fn matrix(rows: i64, cols: i64, bits: i64) -> Vec<Vec<i64>> {
    let mut mat: Vec<Vec<i64>> = Vec::new();
    for i in 0..rows {
        let mut row: Vec<i64> = Vec::new();
        for j in 0..cols {
            row.push((bits >> (i * cols + j)) & 1);
        }
        mat.push(row);
    }
    mat
}

fn main() {
    let mut check: i64 = 0;
    for round in 0..3000i64 {
        for rows in 1..4i64 {
            for cols in 1..4i64 {
                for bits in 0..(1i64 << (rows * cols)) {
                    check = (check * 131 + min_flips(&matrix(rows, cols, bits)) + round + 2) % 1000000007;
                }
            }
        }
    }
    println!("3000 rounds of every matrix: checksum {}", check);
}
