// LeetCode #934: Shortest Bridge -- bench: mark one island, then search
// outward. Mirrors shortest_bridge.kara, .c, .py and go-seq/.

const DR: [i64; 4] = [-1, 1, 0, 0];
const DC: [i64; 4] = [0, 0, -1, 1];

fn shortest_bridge(grid: &[Vec<i64>]) -> i64 {
    let n = grid.len() as i64;
    let mut dist: Vec<i64> = vec![-1; (n * n) as usize];
    let mut start: i64 = 0;
    while grid[(start / n) as usize][(start % n) as usize] == 0 {
        start += 1;
    }
    let mut stack: Vec<i64> = vec![start];
    let mut frontier: Vec<i64> = Vec::new();
    dist[start as usize] = 0;
    while let Some(cell) = stack.pop() {
        frontier.push(cell);
        for d in 0..4 {
            let r = cell / n + DR[d];
            let c = cell % n + DC[d];
            if r >= 0
                && r < n
                && c >= 0
                && c < n
                && grid[r as usize][c as usize] == 1
                && dist[(r * n + c) as usize] < 0
            {
                dist[(r * n + c) as usize] = 0;
                stack.push(r * n + c);
            }
        }
    }
    let mut head = 0;
    while head < frontier.len() {
        let cell = frontier[head];
        head += 1;
        for d in 0..4 {
            let r = cell / n + DR[d];
            let c = cell % n + DC[d];
            if r >= 0 && r < n && c >= 0 && c < n && dist[(r * n + c) as usize] < 0 {
                if grid[r as usize][c as usize] == 1 {
                    return dist[cell as usize];
                }
                dist[(r * n + c) as usize] = dist[cell as usize] + 1;
                frontier.push(r * n + c);
            }
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn beside(grid: &[Vec<i64>], r: i64, c: i64, mark: i64) -> bool {
    let n = grid.len() as i64;
    let (ru, cu) = (r as usize, c as usize);
    (r > 0 && grid[ru - 1][cu] == mark)
        || (r + 1 < n && grid[ru + 1][cu] == mark)
        || (c > 0 && grid[ru][cu - 1] == mark)
        || (c + 1 < n && grid[ru][cu + 1] == mark)
}

fn grow(
    seed: &mut i64,
    grid: &mut [Vec<i64>],
    cells: &mut Vec<i64>,
    size: i64,
    mark: i64,
    avoid: i64,
) {
    let n = grid.len() as i64;
    let mut tries = 0;
    while (cells.len() as i64) < size && tries < 4 * size {
        tries += 1;
        let cell = cells[(next_random(seed) % cells.len() as i64) as usize];
        let d = (next_random(seed) % 4) as usize;
        let r = cell / n + DR[d];
        let c = cell % n + DC[d];
        if r >= 0
            && r < n
            && c >= 0
            && c < n
            && grid[r as usize][c as usize] == 0
            && !beside(grid, r, c, avoid)
        {
            grid[r as usize][c as usize] = mark;
            cells.push(r * n + c);
        }
    }
}

fn random_islands(seed: &mut i64, n: i64, size_a: i64, size_b: i64) -> Vec<Vec<i64>> {
    loop {
        let mut grid: Vec<Vec<i64>> = vec![vec![0; n as usize]; n as usize];
        let a = next_random(seed) % (n * n);
        grid[(a / n) as usize][(a % n) as usize] = 2;
        let mut cells_a: Vec<i64> = vec![a];
        grow(seed, &mut grid, &mut cells_a, size_a, 2, -1);
        let mut b: i64 = -1;
        for _ in 0..100 {
            let x = next_random(seed) % (n * n);
            if b < 0
                && grid[(x / n) as usize][(x % n) as usize] == 0
                && !beside(&grid, x / n, x % n, 2)
            {
                b = x;
            }
        }
        if b >= 0 {
            grid[(b / n) as usize][(b % n) as usize] = 3;
            let mut cells_b: Vec<i64> = vec![b];
            grow(seed, &mut grid, &mut cells_b, size_b, 3, 2);
            for row in grid.iter_mut() {
                for v in row.iter_mut() {
                    if *v > 0 {
                        *v = 1;
                    }
                }
            }
            return grid;
        }
    }
}

fn main() {
    let rounds: i64 = 50;
    let count: i64 = 100;
    let n: i64 = 100;
    let mut seed: i64 = 934;
    // count n x n grids, each with two islands of up to 2500 cells grown at
    // random, built once
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        let size_a = 1 + next_random(&mut seed) % 2500;
        let size_b = 1 + next_random(&mut seed) % 2500;
        grids.push(random_islands(&mut seed, n, size_a, size_b));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        // each round visits every grid, starting from a different one
        for i in 0..count {
            let a = shortest_bridge(&grids[((r + i) % count) as usize]);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} grids of {n} x {n}: answers summing to {total}, checksum {check}");
}
