// LeetCode #694: Number of Distinct Islands -- bench program, Rust mirror of the union-find arm.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn find(parent: &mut [usize], x: usize) -> usize {
    let mut root = x;
    while parent[root] != root {
        root = parent[root];
    }
    let mut at = x;
    while parent[at] != root {
        let next = parent[at];
        parent[at] = root;
        at = next;
    }
    root
}

fn num_distinct_islands(grid: &[Vec<i64>]) -> i64 {
    let m = grid.len();
    let n = grid[0].len();
    let mut parent: Vec<usize> = (0..m * n).collect();
    for r in 0..m {
        for c in 0..n {
            if grid[r][c] == 0 {
                continue;
            }
            if r + 1 < m && grid[r + 1][c] == 1 {
                let a = find(&mut parent, r * n + c);
                let b = find(&mut parent, (r + 1) * n + c);
                parent[a] = b;
            }
            if c + 1 < n && grid[r][c + 1] == 1 {
                let a = find(&mut parent, r * n + c);
                let b = find(&mut parent, r * n + c + 1);
                parent[a] = b;
            }
        }
    }
    let mut first: Vec<i64> = vec![-1; m * n];
    let mut slot: Vec<usize> = vec![0; m * n];
    let mut shapes: Vec<Vec<i64>> = Vec::new();
    for r in 0..m {
        for c in 0..n {
            if grid[r][c] == 0 {
                continue;
            }
            let root = find(&mut parent, r * n + c);
            if first[root] < 0 {
                first[root] = (r * n + c) as i64;
                slot[root] = shapes.len();
                shapes.push(Vec::new());
            }
            let r0 = first[root] / n as i64;
            let c0 = first[root] % n as i64;
            shapes[slot[root]].push((r as i64 - r0) * 200 + (c as i64 - c0));
        }
    }
    shapes.sort();
    let mut distinct = 0;
    for i in 0..shapes.len() {
        if i == 0 || shapes[i] != shapes[i - 1] {
            distinct += 1;
        }
    }
    distinct
}

fn main() {
    let mut seed = 694;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..40 {
        let percent = 30 + next_random(&mut seed) % 31;
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..50 {
            let mut line: Vec<i64> = Vec::new();
            for _ in 0..50 {
                line.push(if next_random(&mut seed) % 100 < percent { 1 } else { 0 });
            }
            grid.push(line);
        }
        grids.push(grid);
    }
    let rounds = 150;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for grid in &grids {
            let r = num_distinct_islands(grid);
            total += r;
            checksum = (checksum * 31 + r) % 1000000007;
        }
    }
    println!("{} rounds of 40 grids of 50 by 50: {} distinct islands counted, checksum {}", rounds, total, checksum);
}
