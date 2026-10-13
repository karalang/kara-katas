// Benchmark for #463: mirror of island_perimeter.kara (the ★ arm: four
// sides per land cell, less two per shared edge) on the same workload.

fn island_perimeter(grid: &Vec<Vec<i64>>) -> i64 {
    let mut land = 0;
    let mut shared = 0;
    for i in 0..grid.len() {
        for j in 0..grid[i].len() {
            if grid[i][j] == 1 {
                land += 1;
                if j + 1 < grid[i].len() && grid[i][j + 1] == 1 {
                    shared += 1;
                }
                if i + 1 < grid.len() && grid[i + 1][j] == 1 {
                    shared += 1;
                }
            }
        }
    }
    4 * land - 2 * shared
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// A random walk of land on a rows x cols sea, then every lake filled in.
fn random_island(rows: i64, cols: i64, steps: i64, seed: &mut i64) -> Vec<Vec<i64>> {
    let (rows, cols) = (rows as usize, cols as usize);
    let mut grid = vec![vec![0i64; cols]; rows];
    let mut i = (next_random(seed) % rows as i64) as usize;
    let mut j = (next_random(seed) % cols as i64) as usize;
    grid[i][j] = 1;
    for _ in 0..steps {
        let d = next_random(seed) % 4;
        if d == 0 && i > 0 {
            i -= 1;
        } else if d == 1 && i + 1 < rows {
            i += 1;
        } else if d == 2 && j > 0 {
            j -= 1;
        } else if d == 3 && j + 1 < cols {
            j += 1;
        }
        grid[i][j] = 1;
    }
    let mut sea = vec![vec![false; cols]; rows];
    let mut queue: Vec<(i64, i64)> = Vec::new();
    for r in 0..rows {
        for c in 0..cols {
            if (r == 0 || c == 0 || r == rows - 1 || c == cols - 1) && grid[r][c] == 0 {
                sea[r][c] = true;
                queue.push((r as i64, c as i64));
            }
        }
    }
    let mut head = 0;
    while head < queue.len() {
        let (r, c) = queue[head];
        head += 1;
        for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)] {
            let nr = r + dr;
            let nc = c + dc;
            if nr >= 0 && nr < rows as i64 && nc >= 0 && nc < cols as i64 {
                let (ur, uc) = (nr as usize, nc as usize);
                if grid[ur][uc] == 0 && !sea[ur][uc] {
                    sea[ur][uc] = true;
                    queue.push((nr, nc));
                }
            }
        }
    }
    for r in 0..rows {
        for c in 0..cols {
            if !sea[r][c] {
                grid[r][c] = 1;
            }
        }
    }
    grid
}

fn main() {
    let size: i64 = 1000;
    let islands = 2;
    let rounds = 200;
    let mut seed: i64 = 463;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut tops: Vec<usize> = Vec::new();
    let mut shores: Vec<Vec<usize>> = Vec::new();
    for _ in 0..islands {
        let inner = random_island(size - 2, size - 2, (size - 2) * (size - 2), &mut seed);
        let mut grid: Vec<Vec<i64>> = Vec::new();
        grid.push(vec![0; size as usize]);
        for row in inner {
            let mut wide = vec![0];
            for c in row {
                wide.push(c);
            }
            wide.push(0);
            grid.push(wide);
        }
        grid.push(vec![0; size as usize]);
        let mut top = 0;
        while !grid[top].contains(&1) {
            top += 1;
        }
        let mut shore: Vec<usize> = Vec::new();
        for j in 0..size as usize {
            if grid[top][j] == 1 {
                shore.push(j);
            }
        }
        grids.push(grid);
        tops.push(top);
        shores.push(shore);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for g in 0..islands {
            let j = shores[g][(next_random(&mut seed) % shores[g].len() as i64) as usize];
            let above = tops[g] - 1;
            grids[g][above][j] = 1;
            let perimeter = island_perimeter(&grids[g]);
            grids[g][above][j] = 0;
            total += perimeter;
            checksum = (checksum * 31 + perimeter) % 1000000007;
        }
    }
    println!("{} rounds on {} islands of {}x{}: perimeter {} in all, checksum {}", rounds, islands, size, size, total, checksum);
}
