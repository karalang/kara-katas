// LeetCode #2812: Find the Safest Path in a Grid -- the bench in Rust:
// the ★ arm over 10 grids of 400 by 400, a thief in about one cell of
// 2000, all drawn first, then each answered 3 times.
use std::collections::VecDeque;

const DIRS: [(i64, i64); 4] = [(0, 1), (1, 0), (0, -1), (-1, 0)];

fn thief_distances(grid: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let n = grid.len() as i64;
    let mut dist = vec![vec![-1i64; n as usize]; n as usize];
    let mut queue = VecDeque::new();
    for r in 0..n {
        for c in 0..n {
            if grid[r as usize][c as usize] == 1 {
                dist[r as usize][c as usize] = 0;
                queue.push_back((r, c));
            }
        }
    }
    while let Some((r, c)) = queue.pop_front() {
        for (dr, dc) in DIRS {
            let (nr, nc) = (r + dr, c + dc);
            if nr >= 0 && nr < n && nc >= 0 && nc < n && dist[nr as usize][nc as usize] == -1 {
                dist[nr as usize][nc as usize] = dist[r as usize][c as usize] + 1;
                queue.push_back((nr, nc));
            }
        }
    }
    dist
}

fn reachable(dist: &[Vec<i64>], s: i64) -> bool {
    let n = dist.len() as i64;
    if dist[0][0] < s {
        return false;
    }
    let mut seen = vec![vec![false; n as usize]; n as usize];
    seen[0][0] = true;
    let mut queue = VecDeque::new();
    queue.push_back((0i64, 0i64));
    while let Some((r, c)) = queue.pop_front() {
        if r == n - 1 && c == n - 1 {
            return true;
        }
        for (dr, dc) in DIRS {
            let (nr, nc) = (r + dr, c + dc);
            if nr >= 0
                && nr < n
                && nc >= 0
                && nc < n
                && !seen[nr as usize][nc as usize]
                && dist[nr as usize][nc as usize] >= s
            {
                seen[nr as usize][nc as usize] = true;
                queue.push_back((nr, nc));
            }
        }
    }
    false
}

fn maximum_safeness_factor(grid: &[Vec<i64>]) -> i64 {
    let n = grid.len();
    let dist = thief_distances(grid);
    let mut lo = 0;
    let mut hi = dist[0][0].min(dist[n - 1][n - 1]);
    while lo < hi {
        let mid = (lo + hi + 1) / 2;
        if reachable(&dist, mid) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    lo
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let count = 10;
    let rounds = 3;
    let n = 400i64;
    let mut rng = Rng(2812);
    let mut grids = Vec::new();
    for _ in 0..count {
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..n {
            let row: Vec<i64> = (0..n).map(|_| if rng.next_random() % 2000 == 0 { 1 } else { 0 }).collect();
            grid.push(row);
        }
        let r = rng.next_random() % n;
        let c = rng.next_random() % n;
        grid[r as usize][c as usize] = 1;
        grids.push(grid);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for grid in &grids {
            let a = maximum_safeness_factor(grid);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} grids of {n}, {rounds} rounds: safeness sums to {total}, checksum {check}");
}
