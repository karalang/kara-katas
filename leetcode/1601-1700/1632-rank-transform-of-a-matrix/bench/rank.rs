// LeetCode #1632: Rank Transform of a Matrix -- the bench's Rust mirror:
// the ★ arm on 12 random 300 x 300 matrices of values 0 to 9999, all drawn
// first.

use std::collections::HashMap;

fn find(parent: &mut Vec<i64>, x: i64) -> i64 {
    let mut x = x;
    while parent[x as usize] != x {
        parent[x as usize] = parent[parent[x as usize] as usize];
        x = parent[x as usize];
    }
    x
}

fn matrix_rank_transform(matrix: &Vec<Vec<i32>>) -> Vec<Vec<i32>> {
    let (rows, cols) = (matrix.len() as i64, matrix[0].len() as i64);
    let mut cells: Vec<(i32, i64, i64)> = Vec::new();
    for r in 0..rows {
        for c in 0..cols {
            cells.push((matrix[r as usize][c as usize], r, c));
        }
    }
    cells.sort();
    let mut row_max = vec![0i32; rows as usize];
    let mut col_max = vec![0i32; cols as usize];
    let mut answer = vec![vec![0i32; cols as usize]; rows as usize];
    let mut parent: Vec<i64> = (0..rows * cols).collect();
    let mut start = 0;
    while start < cells.len() {
        let mut end = start;
        while end < cells.len() && cells[end].0 == cells[start].0 {
            end += 1;
        }
        let mut first_in_row: HashMap<i64, i64> = HashMap::new();
        let mut first_in_col: HashMap<i64, i64> = HashMap::new();
        for &(_, r, c) in &cells[start..end] {
            let id = r * cols + c;
            match first_in_row.get(&r) {
                Some(&other) => {
                    let (a, b) = (find(&mut parent, id), find(&mut parent, other));
                    parent[a as usize] = b;
                }
                None => {
                    first_in_row.insert(r, id);
                }
            }
            match first_in_col.get(&c) {
                Some(&other) => {
                    let (a, b) = (find(&mut parent, id), find(&mut parent, other));
                    parent[a as usize] = b;
                }
                None => {
                    first_in_col.insert(c, id);
                }
            }
        }
        let mut group_rank: HashMap<i64, i32> = HashMap::new();
        for &(_, r, c) in &cells[start..end] {
            let root = find(&mut parent, r * cols + c);
            let rank = row_max[r as usize].max(col_max[c as usize]) + 1;
            let best = *group_rank.get(&root).unwrap_or(&0);
            group_rank.insert(root, best.max(rank));
        }
        for &(_, r, c) in &cells[start..end] {
            let rank = group_rank[&find(&mut parent, r * cols + c)];
            answer[r as usize][c as usize] = rank;
            row_max[r as usize] = rank;
            col_max[c as usize] = rank;
        }
        start = end;
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1632;
    let mut matrices: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..12 {
        let mut matrix = Vec::new();
        for _ in 0..300 {
            let mut row = Vec::new();
            for _ in 0..300 {
                row.push((next_random(&mut seed) % 10000) as i32);
            }
            matrix.push(row);
        }
        matrices.push(matrix);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for matrix in &matrices {
        for row in matrix_rank_transform(matrix) {
            for rank in row {
                total += rank as i64;
                check = (check * 31 + rank as i64) % 1000000007;
            }
        }
    }
    println!("12 matrices of 300 x 300: ranks sum to {}, checksum {}", total, check);
}
