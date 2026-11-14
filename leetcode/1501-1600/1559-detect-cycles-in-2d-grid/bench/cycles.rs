// LeetCode #1559: Detect Cycles in 2D Grid -- bench: the ★ arm (a search
// on a stack, each cell with the cell it came from) over 20 comb grids of
// 500 by 500 with no cycle, half with two cells made `a` to join two teeth
// in one, built once, each asked 5 times.
// Rust mirror of cycles.kara.

fn contains_cycle(grid: &[Vec<char>]) -> bool {
    let rows = grid.len() as i64;
    let cols = grid[0].len() as i64;
    let mut seen = vec![false; (rows * cols) as usize];
    for start in 0..rows * cols {
        if seen[start as usize] {
            continue;
        }
        seen[start as usize] = true;
        let mut stack = vec![(start, -1i64)];
        while let Some((cell, from)) = stack.pop() {
            let (r, c) = (cell / cols, cell % cols);
            for (dr, dc) in [(0, 1), (1, 0), (0, -1), (-1, 0)] {
                let (nr, nc) = (r + dr, c + dc);
                if nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr as usize][nc as usize] != grid[r as usize][c as usize] {
                    continue;
                }
                let next = nr * cols + nc;
                if next == from {
                    continue;
                }
                if seen[next as usize] {
                    return true;
                }
                seen[next as usize] = true;
                stack.push((next, cell));
            }
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn comb(size: i64, seed: &mut i64) -> Vec<Vec<char>> {
    let alphabet: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut grid = Vec::new();
    for r in 0..size {
        let mut row = Vec::new();
        for c in 0..size {
            if r == 0 || c % 2 == 0 {
                row.push('a');
            } else {
                row.push(alphabet[(next_random(seed) % 25 + 1) as usize]);
            }
        }
        grid.push(row);
    }
    grid
}

fn main() {
    let size = 500i64;
    let mut seed = 1559;
    let mut grids: Vec<Vec<Vec<char>>> = Vec::new();
    for g in 0..20 {
        let mut grid = comb(size, &mut seed);
        if g % 2 == 1 {
            let r = (next_random(&mut seed) % (size - 2) + 1) as usize;
            let c = (next_random(&mut seed) % (size / 2 - 1) * 2 + 1) as usize;
            grid[r][c] = 'a';
            grid[r + 1][c] = 'a';
        }
        grids.push(grid);
    }
    let mut check = 0;
    let mut found = 0;
    for pass in 0..5i64 {
        for (g, grid) in grids.iter().enumerate() {
            let cycle = contains_cycle(grid);
            if cycle {
                found += 1;
            }
            check = mix(check, if cycle { pass * 20 + g as i64 } else { -1 });
        }
    }
    println!("5 passes over 20 grids of 500 by 500: {} with a cycle, checksum {}", found, check);
}
