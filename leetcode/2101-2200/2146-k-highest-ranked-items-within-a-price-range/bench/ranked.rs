// LeetCode #2146: K Highest Ranked Items Within a Price Range -- the
// benchmark, the same algorithm as ranked.kara.
use std::collections::VecDeque;

fn highest_ranked_k_items(grid: &[Vec<i64>], pricing: [i64; 2], start: [i64; 2], k: usize) -> Vec<[i64; 2]> {
    let m = grid.len() as i64;
    let n = grid[0].len() as i64;
    let mut seen = vec![vec![false; n as usize]; m as usize];
    seen[start[0] as usize][start[1] as usize] = true;
    let mut queue = VecDeque::new();
    queue.push_back((start[0], start[1], 0i64));
    let mut found: Vec<(i64, i64, i64, i64)> = Vec::new();
    while let Some((r, c, dist)) = queue.pop_front() {
        let price = grid[r as usize][c as usize];
        if price >= pricing[0] && price <= pricing[1] {
            found.push((dist, price, r, c));
        }
        for (dr, dc) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
            let nr = r + dr;
            let nc = c + dc;
            if nr >= 0 && nr < m && nc >= 0 && nc < n && !seen[nr as usize][nc as usize] && grid[nr as usize][nc as usize] != 0 {
                seen[nr as usize][nc as usize] = true;
                queue.push_back((nr, nc, dist + 1));
            }
        }
    }
    found.sort();
    found.iter().take(k).map(|&(_, _, r, c)| [r, c]).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw(seed: &mut i64) -> i64 {
    if next_random(seed) % 5 == 0 { 0 } else { next_random(seed) % 99999 + 2 }
}

fn main() {
    let mut seed = 2146;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..4 {
        let mut grid = Vec::new();
        for _ in 0..316 {
            let mut row = Vec::new();
            for _ in 0..316 {
                row.push(draw(&mut seed));
            }
            grid.push(row);
        }
        grids.push(grid);
    }
    let mut total = 0usize;
    let mut check = 0i64;
    for round in 0..25 {
        for g in 0..4 {
            let r = (next_random(&mut seed) % 316) as usize;
            let c = (next_random(&mut seed) % 316) as usize;
            grids[g][r][c] = draw(&mut seed);
            let sr = next_random(&mut seed) % 316;
            let sc = next_random(&mut seed) % 316;
            if grids[g][sr as usize][sc as usize] == 0 {
                grids[g][sr as usize][sc as usize] = 1;
            }
            let cells = highest_ranked_k_items(&grids[g], [2, 50000], [sr, sc], 1000);
            total += cells.len();
            for cell in &cells {
                check = (check * 31 + cell[0] * 1000 + cell[1] + round) % 1000000007;
            }
        }
    }
    println!("100 searches: {} items in all, checksum {}", total, check);
}
