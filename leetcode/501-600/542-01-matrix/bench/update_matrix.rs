// Benchmark for #542: Rust mirror of the ★ arm (breadth-first search from
// every 0 at once); see update_matrix.kara.
use std::collections::VecDeque;

fn update_matrix(mat: &Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    let m = mat.len() as i64;
    let n = mat[0].len() as i64;
    let mut dist = vec![vec![-1i64; n as usize]; m as usize];
    let mut queue: VecDeque<(i64, i64)> = VecDeque::new();
    for r in 0..m {
        for c in 0..n {
            if mat[r as usize][c as usize] == 0 {
                dist[r as usize][c as usize] = 0;
                queue.push_back((r, c));
            }
        }
    }
    let steps = [(-1, 0), (1, 0), (0, -1), (0, 1)];
    while let Some((r, c)) = queue.pop_front() {
        for (dr, dc) in steps {
            let (nr, nc) = (r + dr, c + dc);
            if nr >= 0 && nr < m && nc >= 0 && nc < n && dist[nr as usize][nc as usize] < 0 {
                dist[nr as usize][nc as usize] = dist[r as usize][c as usize] + 1;
                queue.push_back((nr, nc));
            }
        }
    }
    dist
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 random 100 by 100 grids (the problem's 10,000 cells), from half
    // ones to 88 in a hundred, built once. Then 50 times over every grid
    // is answered; one row of the answer, picked by the round and the
    // grid, is summed, and one cell goes into the checksum.
    let grids = 20;
    let mut seed: i64 = 542;
    let mut all: Vec<Vec<Vec<i64>>> = Vec::new();
    for g in 0..grids {
        let ones = 50 + 2 * g;
        let mat: Vec<Vec<i64>> = (0..100)
            .map(|_| (0..100).map(|_| if next_random(&mut seed) % 100 < ones { 1 } else { 0 }).collect())
            .collect();
        all.push(mat);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..50i64 {
        for t in 0..grids {
            let answer = update_matrix(&all[t as usize]);
            for d in answer[((r * 7 + t * 13) % 100) as usize].iter() {
                total += *d;
            }
            let cell = answer[((r * 11 + t * 3) % 100) as usize][((r * 5 + t * 17) % 100) as usize];
            checksum = (checksum * 31 + cell) % 1000000007;
        }
    }
    println!("{grids} grids, 50 times each: row sum {total}, checksum {checksum}");
}
