// LeetCode #695: Max Area of Island -- bench program, Rust mirror of the union-find arm.

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

fn join(parent: &mut [usize], size: &mut [i64], a: usize, b: usize) {
    let mut x = find(parent, a);
    let mut y = find(parent, b);
    if x == y {
        return;
    }
    if size[x] < size[y] {
        std::mem::swap(&mut x, &mut y);
    }
    parent[y] = x;
    size[x] += size[y];
}

fn max_area_of_island(grid: &[Vec<i64>]) -> i64 {
    let m = grid.len();
    let n = grid[0].len();
    let mut parent: Vec<usize> = (0..m * n).collect();
    let mut size: Vec<i64> = vec![1; m * n];
    for r in 0..m {
        for c in 0..n {
            if grid[r][c] == 0 {
                continue;
            }
            if r + 1 < m && grid[r + 1][c] == 1 {
                join(&mut parent, &mut size, r * n + c, (r + 1) * n + c);
            }
            if c + 1 < n && grid[r][c + 1] == 1 {
                join(&mut parent, &mut size, r * n + c, r * n + c + 1);
            }
        }
    }
    let mut best = 0;
    for r in 0..m {
        for c in 0..n {
            if grid[r][c] == 1 && find(&mut parent, r * n + c) == r * n + c {
                best = best.max(size[r * n + c]);
            }
        }
    }
    best
}

fn main() {
    let mut seed = 695;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..40 {
        let percent = 30 + next_random(&mut seed) % 41;
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
    let rounds = 300;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for grid in &grids {
            let r = max_area_of_island(grid);
            total += r;
            checksum = (checksum * 31 + r) % 1000000007;
        }
    }
    println!("{} rounds of 40 grids of 50 by 50: largest areas sum to {}, checksum {}", rounds, total, checksum);
}
