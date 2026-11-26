// LeetCode #1765: Map of Highest Peak -- the bench in Rust, mirroring
// highest_peak.kara: a breadth-first search from every water cell at once.
use std::collections::VecDeque;

fn highest_peak(is_water: &[Vec<i32>]) -> Vec<Vec<i32>> {
    let rows = is_water.len() as i64;
    let cols = is_water[0].len() as i64;
    let mut height = vec![vec![-1i32; cols as usize]; rows as usize];
    let mut queue: VecDeque<(i64, i64)> = VecDeque::new();
    for r in 0..rows {
        for c in 0..cols {
            if is_water[r as usize][c as usize] == 1 {
                height[r as usize][c as usize] = 0;
                queue.push_back((r, c));
            }
        }
    }
    while let Some((r, c)) = queue.pop_front() {
        for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)] {
            let nr = r + dr;
            let nc = c + dc;
            if nr >= 0 && nr < rows && nc >= 0 && nc < cols && height[nr as usize][nc as usize] == -1 {
                height[nr as usize][nc as usize] = height[r as usize][c as usize] + 1;
                queue.push_back((nr, nc));
            }
        }
    }
    height
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1765;
    let size: i64 = 800;
    let mut grid: Vec<Vec<i32>> = (0..size).map(|_| (0..size).map(|_| if next_random(&mut seed) % 5000 == 0 { 1 } else { 0 }).collect()).collect();
    grid[0][0] = 1;
    let mut check: i64 = 0;
    for call in 0..100i64 {
        let r = ((check + call * 7919) % size) as usize;
        let c = ((check / 7 + call * 104729) % size) as usize;
        grid[r][c] = 1 - grid[r][c];
        grid[0][0] = 1;
        let height = highest_peak(&grid);
        let s = size as usize;
        check = (check * 31 + height[c][r] as i64 + height[s - 1 - r][s - 1 - c] as i64) % 1000000007;
    }
    println!("100 calls on 800 by 800: checksum {}", check);
}
