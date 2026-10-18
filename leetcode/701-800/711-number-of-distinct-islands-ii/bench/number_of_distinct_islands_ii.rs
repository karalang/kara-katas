// LeetCode #711: Number of Distinct Islands II -- canonical forms
// counted by sorting.
// Benchmark mirror of the Kara sorted arm: each island by depth-first
// search with a stack; its canonical form the smallest of its eight
// symmetries, sorted and moved to the origin; forms sorted and counted.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn canonical(cells: &[(i64, i64)]) -> Vec<i64> {
    let mut best: Vec<i64> = Vec::new();
    for k in 0..8 {
        let mut moved: Vec<(i64, i64)> = Vec::new();
        for &(r, c) in cells.iter() {
            let (a, b) = if k < 4 { (r, c) } else { (c, r) };
            let x = if k % 2 == 1 { -a } else { a };
            let y = if k % 4 >= 2 { -b } else { b };
            moved.push((x, y));
        }
        moved.sort();
        let (r0, c0) = moved[0];
        let mut flat: Vec<i64> = Vec::new();
        for &(r, c) in moved.iter() {
            flat.push(r - r0);
            flat.push(c - c0);
        }
        if k == 0 || flat < best {
            best = flat;
        }
    }
    best
}

fn num_distinct_islands2(grid: &[Vec<i64>]) -> i64 {
    let rows = grid.len();
    let cols = grid[0].len();
    let mut seen = vec![false; rows * cols];
    let mut forms: Vec<Vec<i64>> = Vec::new();
    for start in 0..rows * cols {
        if grid[start / cols][start % cols] == 0 || seen[start] {
            continue;
        }
        let mut cells: Vec<(i64, i64)> = Vec::new();
        let mut stack: Vec<usize> = vec![start];
        seen[start] = true;
        while let Some(at) = stack.pop() {
            let r = at / cols;
            let c = at % cols;
            cells.push((r as i64, c as i64));
            if r > 0 && grid[r - 1][c] == 1 && !seen[at - cols] {
                seen[at - cols] = true;
                stack.push(at - cols);
            }
            if r + 1 < rows && grid[r + 1][c] == 1 && !seen[at + cols] {
                seen[at + cols] = true;
                stack.push(at + cols);
            }
            if c > 0 && grid[r][c - 1] == 1 && !seen[at - 1] {
                seen[at - 1] = true;
                stack.push(at - 1);
            }
            if c + 1 < cols && grid[r][c + 1] == 1 && !seen[at + 1] {
                seen[at + 1] = true;
                stack.push(at + 1);
            }
        }
        forms.push(canonical(&cells));
    }
    forms.sort();
    let mut count = 0;
    for i in 0..forms.len() {
        if i == 0 || forms[i] != forms[i - 1] {
            count += 1;
        }
    }
    count
}

fn main() {
    let mut seed: i64 = 711;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for g in 0..100 {
        let pct = 30 + g * 2 / 5;
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..50 {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..50 {
                row.push(if next_random(&mut seed) % 100 < pct { 1 } else { 0 });
            }
            grid.push(row);
        }
        grids.push(grid);
    }
    let mut sum: i64 = 0;
    for _ in 0..10 {
        for grid in grids.iter() {
            sum += num_distinct_islands2(grid);
        }
    }
    println!("10 rounds of 100 grids of 50 by 50: {} distinct islands", sum);
}
