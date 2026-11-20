// LeetCode #1210 bench, in Rust: the ★ arm (a breadth-first search over the
// snake's states, its tail cell and whether it lies flat or upright) on 24
// grids of 100 by 100 drawn once, then 40 rounds over the grids, every
// answer folded into a checksum.

fn minimum_moves(grid: &[Vec<i64>]) -> i64 {
    let n = grid.len() as i64;
    let free = |r: i64, c: i64| r < n && c < n && grid[r as usize][c as usize] == 0;
    let mut dist = vec![-1i64; (n * n * 2) as usize];
    let mut queue: Vec<(i64, i64, i64)> = vec![(0, 0, 0)];
    dist[0] = 0;
    let mut head = 0;
    while head < queue.len() {
        let (r, c, up) = queue[head];
        head += 1;
        let d = dist[((r * n + c) * 2 + up) as usize];
        if r == n - 1 && c == n - 2 && up == 0 {
            return d;
        }
        let mut next: Vec<(i64, i64, i64)> = Vec::new();
        if up == 0 {
            if free(r, c + 2) {
                next.push((r, c + 1, 0));
            }
            if free(r + 1, c) && free(r + 1, c + 1) {
                next.push((r + 1, c, 0));
                next.push((r, c, 1));
            }
        } else {
            if free(r + 2, c) {
                next.push((r + 1, c, 1));
            }
            if free(r, c + 1) && free(r + 1, c + 1) {
                next.push((r, c + 1, 1));
                next.push((r, c, 0));
            }
        }
        for &(nr, nc, nu) in &next {
            let at = ((nr * n + nc) * 2 + nu) as usize;
            if dist[at] < 0 {
                dist[at] = d + 1;
                queue.push((nr, nc, nu));
            }
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_grid(seed: &mut i64, n: i64, percent: i64) -> Vec<Vec<i64>> {
    let mut grid = Vec::new();
    for r in 0..n {
        let mut row = Vec::new();
        for c in 0..n {
            let corner = (r == 0 && c < 2) || (r == n - 1 && c >= n - 2);
            row.push(if !corner && next_random(seed) % 100 < percent { 1 } else { 0 });
        }
        grid.push(row);
    }
    grid
}

fn staircase(n: i64, s: i64) -> Vec<Vec<i64>> {
    let mut grid = vec![vec![1i64; n as usize]; n as usize];
    let mut open = |r: i64, c: i64| {
        if r < n && c < n {
            grid[r as usize][c as usize] = 0;
        }
    };
    let mut k = 0;
    while k * s < n {
        let at = k * s;
        for c in at..at + s + 2 {
            open(at, c);
        }
        for r in at..at + s + 2 {
            open(r, at + s);
        }
        for d in 0..4 {
            open(at + d / 2, at + d % 2);
            open(at + d / 2, at + s + d % 2);
        }
        k += 1;
    }
    for i in 0..n {
        open(n - 1, i);
        open(n - 2, i);
        open(i, n - 1);
        open(i, n - 2);
    }
    grid
}

fn main() {
    let mut seed = 1210i64;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for i in 0..20 {
        let percent = if i < 8 { 5 } else if i < 16 { 10 } else { 14 };
        grids.push(random_grid(&mut seed, 100, percent));
    }
    for s in 3..7 {
        grids.push(staircase(100, s));
    }
    let mut check: i64 = 0;
    for round in 0..40 {
        for grid in &grids {
            check = (check * 131 + minimum_moves(grid) + 2 + round) % 1000000007;
        }
    }
    println!("40 rounds over 24 grids of 100 by 100: checksum {check}");
}
