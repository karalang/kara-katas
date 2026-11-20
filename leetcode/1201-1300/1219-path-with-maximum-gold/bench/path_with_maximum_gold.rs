// LeetCode #1219 bench, Rust mirror of the Kāra ★ arm: a depth-first
// search from every cell with gold that zeroes a cell while the search
// goes on from it and puts its gold back on the way out, on 160 grids of
// 15 by 15, each holding one blob of 25 cells with gold, drawn once.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn collect(grid: &mut Vec<Vec<i64>>, r: i64, c: i64) -> i64 {
    if r < 0 || c < 0 || r >= grid.len() as i64 || c >= grid[0].len() as i64 || grid[r as usize][c as usize] == 0 {
        return 0;
    }
    let gold = grid[r as usize][c as usize];
    grid[r as usize][c as usize] = 0;
    let mut best = 0;
    for (dr, dc) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
        best = best.max(collect(grid, r + dr, c + dc));
    }
    grid[r as usize][c as usize] = gold;
    gold + best
}

fn get_maximum_gold(grid: &[Vec<i64>]) -> i64 {
    let mut g = grid.to_vec();
    let mut best = 0;
    for r in 0..g.len() {
        for c in 0..g[0].len() {
            if g[r][c] > 0 {
                best = best.max(collect(&mut g, r as i64, c as i64));
            }
        }
    }
    best
}

fn main() {
    let mut seed = 1219;
    let steps = [(1, 0), (-1, 0), (0, 1), (0, -1)];
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..160 {
        let mut grid = vec![vec![0i64; 15]; 15];
        let r0 = next_random(&mut seed) % 15;
        let c0 = next_random(&mut seed) % 15;
        grid[r0 as usize][c0 as usize] = next_random(&mut seed) % 100 + 1;
        let mut cells: Vec<(i64, i64)> = vec![(r0, c0)];
        while cells.len() < 25 {
            let at = (next_random(&mut seed) % cells.len() as i64) as usize;
            let (dr, dc) = steps[(next_random(&mut seed) % 4) as usize];
            let (r, c) = (cells[at].0 + dr, cells[at].1 + dc);
            if r >= 0 && c >= 0 && r < 15 && c < 15 && grid[r as usize][c as usize] == 0 {
                grid[r as usize][c as usize] = next_random(&mut seed) % 100 + 1;
                cells.push((r, c));
            }
        }
        grids.push(grid);
    }
    let mut check = 0;
    let mut total = 0;
    for grid in &grids {
        let answer = get_maximum_gold(grid);
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    println!("160 grids of 15 by 15, one blob of 25 cells with gold each: gold total {}, checksum {}", total, check);
}
