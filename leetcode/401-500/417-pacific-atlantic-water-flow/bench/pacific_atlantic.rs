// LeetCode #417: Pacific Atlantic Water Flow -- Rust mirror of
// pacific_atlantic.kara (search up from each ocean).
use std::collections::VecDeque;

fn climb(heights: &[Vec<i64>], mut queue: VecDeque<(i64, i64)>) -> Vec<Vec<bool>> {
    let rows = heights.len() as i64;
    let cols = heights[0].len() as i64;
    let mut seen: Vec<Vec<bool>> = Vec::new();
    for _ in 0..rows {
        seen.push(vec![false; cols as usize]);
    }
    for &(r, c) in queue.iter() {
        seen[r as usize][c as usize] = true;
    }
    let dr = [-1, 1, 0, 0];
    let dc = [0, 0, -1, 1];
    while let Some((r, c)) = queue.pop_front() {
        for k in 0..4 {
            let nr = r + dr[k];
            let nc = c + dc[k];
            if nr >= 0
                && nr < rows
                && nc >= 0
                && nc < cols
                && !seen[nr as usize][nc as usize]
                && heights[nr as usize][nc as usize] >= heights[r as usize][c as usize]
            {
                seen[nr as usize][nc as usize] = true;
                queue.push_back((nr, nc));
            }
        }
    }
    seen
}

fn pacific_atlantic(heights: &[Vec<i64>]) -> Vec<(i64, i64)> {
    let rows = heights.len() as i64;
    let cols = heights[0].len() as i64;
    let mut pacific: VecDeque<(i64, i64)> = VecDeque::new();
    let mut atlantic: VecDeque<(i64, i64)> = VecDeque::new();
    for r in 0..rows {
        pacific.push_back((r, 0));
        atlantic.push_back((r, cols - 1));
    }
    for c in 0..cols {
        pacific.push_back((0, c));
        atlantic.push_back((rows - 1, c));
    }
    let to_pacific = climb(heights, pacific);
    let to_atlantic = climb(heights, atlantic);
    let mut cells: Vec<(i64, i64)> = Vec::new();
    for r in 0..rows {
        for c in 0..cols {
            if to_pacific[r as usize][c as usize] && to_atlantic[r as usize][c as usize] {
                cells.push((r, c));
            }
        }
    }
    cells
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn ridge(r: i64, c: i64, n: i64) -> i64 {
    let a = r + c;
    let b = 2 * n - 2 - r - c;
    if a < b { a } else { b }
}

fn main() {
    let n: i64 = 200;
    let rounds: i64 = 3000;
    let mut seed: i64 = 417;
    let mut heights: Vec<Vec<i64>> = Vec::new();
    for r in 0..n {
        let mut row: Vec<i64> = Vec::new();
        for c in 0..n {
            row.push(3 * ridge(r, c, n) + step(&mut seed) % 3);
        }
        heights.push(row);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let r = step(&mut seed) % n;
        let c = step(&mut seed) % n;
        heights[r as usize][c as usize] = step(&mut seed) % (3 * ridge(r, c, n) + 3);
        let cells = pacific_atlantic(&heights);
        total += cells.len() as i64;
        let (lr, lc) = cells[cells.len() - 1];
        checksum = (checksum * 31 + cells.len() as i64 + lr * n + lc) % 1000000007;
    }
    println!("{rounds} rounds on a {n}x{n} grid: {total} cells, checksum {checksum}");
}
