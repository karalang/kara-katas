// LeetCode #2258: Escape the Spreading Fire -- Rust mirror of the ★ arm:
// fire times by one breadth-first search from every fire, then a binary
// search over the wait, each wait tried by a breadth-first search of the
// person. Same workload and checksum as escape.kara.
use std::collections::VecDeque;

const NEVER: i64 = 1_000_000_000_000;
const STEPS: [(i64, i64); 4] = [(-1, 0), (1, 0), (0, -1), (0, 1)];

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn fire_times(grid: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let (m, n) = (grid.len() as i64, grid[0].len() as i64);
    let mut at = vec![vec![NEVER; n as usize]; m as usize];
    let mut queue = VecDeque::new();
    for r in 0..m {
        for c in 0..n {
            if grid[r as usize][c as usize] == 1 {
                at[r as usize][c as usize] = 0;
                queue.push_back((r, c));
            }
        }
    }
    while let Some((r, c)) = queue.pop_front() {
        for (dr, dc) in STEPS {
            let (nr, nc) = (r + dr, c + dc);
            if nr >= 0 && nr < m && nc >= 0 && nc < n {
                let (a, b) = (nr as usize, nc as usize);
                if grid[a][b] == 0 && at[a][b] == NEVER {
                    at[a][b] = at[r as usize][c as usize] + 1;
                    queue.push_back((nr, nc));
                }
            }
        }
    }
    at
}

fn escapes(grid: &[Vec<i64>], fire: &[Vec<i64>], wait: i64) -> bool {
    let (m, n) = (grid.len() as i64, grid[0].len() as i64);
    if wait >= fire[0][0] {
        return false;
    }
    let mut seen = vec![vec![false; n as usize]; m as usize];
    seen[0][0] = true;
    let mut queue = VecDeque::new();
    queue.push_back((0i64, 0i64, wait));
    while let Some((r, c, t)) = queue.pop_front() {
        for (dr, dc) in STEPS {
            let (nr, nc) = (r + dr, c + dc);
            if nr < 0 || nr >= m || nc < 0 || nc >= n {
                continue;
            }
            let (a, b) = (nr as usize, nc as usize);
            if grid[a][b] != 0 || seen[a][b] {
                continue;
            }
            if nr == m - 1 && nc == n - 1 {
                if t + 1 <= fire[a][b] {
                    return true;
                }
                continue;
            }
            if t + 1 < fire[a][b] {
                seen[a][b] = true;
                queue.push_back((nr, nc, t + 1));
            }
        }
    }
    false
}

fn maximum_minutes(grid: &[Vec<i64>]) -> i64 {
    let fire = fire_times(grid);
    let cells = (grid.len() * grid[0].len()) as i64;
    if !escapes(grid, &fire, 0) {
        return -1;
    }
    if escapes(grid, &fire, cells) {
        return 1000000000;
    }
    let (mut lo, mut hi) = (0, cells);
    while hi - lo > 1 {
        let mid = (lo + hi) / 2;
        if escapes(grid, &fire, mid) {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    lo
}

fn chase(seed: &mut i64, m: i64, n: i64, walls: i64) -> Vec<Vec<i64>> {
    let mut grid = Vec::new();
    for r in 0..m {
        let mut row = Vec::new();
        for c in 0..n {
            let roll = next_random(seed) % 100;
            row.push(if c == 1 && r > 0 { 2 } else if c >= 2 && roll < walls { 2 } else { 0 });
        }
        grid.push(row);
    }
    grid[0][2] = 0;
    grid[(m - 1) as usize][(n - 1) as usize] = 0;
    let r = next_random(seed) % (m - 1) + 1;
    grid[r as usize][0] = 1;
    grid
}

fn main() {
    let mut seed = 2258;
    let mut check = 0;
    let mut waits = 0;
    let shapes = [(100, 200), (200, 100), (125, 160)];
    for t in 0..300 {
        let (m, n) = shapes[t % 3];
        let answer = maximum_minutes(&chase(&mut seed, m, n, 8));
        if answer >= 0 && answer < 1000000000 {
            waits += 1;
        }
        check = (check * 31 + answer + 1) % 1000000007;
    }
    println!("300 grids of 2 * 10^4 cells: {} with a wait, checksum {}", waits, check);
}
