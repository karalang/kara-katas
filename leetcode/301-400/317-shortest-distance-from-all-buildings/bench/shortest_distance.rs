// Benchmark lane for LeetCode 317 — Rust mirror of bench/shortest_distance.kara.
// Build the grid once (20% obstacles, BUILDINGS buildings on corner-reachable
// empty cells), then PASSES one-BFS-per-building passes, each after relocating
// one building to an empty cell chosen from the checksum (moved back after).

const ROWS: i64 = 360;
const COLS: i64 = 360;
const BUILDINGS: i64 = 20;
const OBSTACLE_PCT: i64 = 20;
const PASSES: i64 = 30;
const MASK: i64 = 1073741823;

fn lcg(s: i64) -> i64 {
    (s * 1103515245 + 12345) & 0x7fffffff
}

fn shortest_distance(grid: &[i64], rows: i64, cols: i64) -> i64 {
    let n = (rows * cols) as usize;
    let mut total = vec![0i64; n];
    let mut reach = vec![0i64; n];
    let mut seen = vec![0i64; n];
    let mut dist = vec![0i64; n];
    let mut b: i64 = 0;
    for src in 0..n {
        if grid[src] != 1 {
            continue;
        }
        b += 1;
        seen[src] = b;
        dist[src] = 0;
        let mut q: Vec<usize> = Vec::new();
        q.push(src);
        let mut head = 0;
        while head < q.len() {
            let cell = q[head];
            head += 1;
            let r = cell as i64 / cols;
            let c = cell as i64 % cols;
            let d = dist[cell] + 1;
            let mut visit = |nb: usize, q: &mut Vec<usize>| {
                if grid[nb] == 0 && seen[nb] != b {
                    seen[nb] = b;
                    dist[nb] = d;
                    total[nb] += d;
                    reach[nb] += 1;
                    q.push(nb);
                }
            };
            if r > 0 { visit(cell - cols as usize, &mut q); }
            if r < rows - 1 { visit(cell + cols as usize, &mut q); }
            if c > 0 { visit(cell - 1, &mut q); }
            if c < cols - 1 { visit(cell + 1, &mut q); }
        }
    }
    let mut best: i64 = -1;
    for i in 0..n {
        if grid[i] == 0 && reach[i] == b && (best < 0 || total[i] < best) {
            best = total[i];
        }
    }
    best
}

fn main() {
    let n = (ROWS * COLS) as usize;
    let mut seed: i64 = 317;
    let mut grid: Vec<i64> = Vec::with_capacity(n);
    for _ in 0..n {
        seed = lcg(seed);
        grid.push(if (seed / 65536) % 100 < OBSTACLE_PCT { 2 } else { 0 });
    }
    grid[0] = 0;

    let mut reachable = vec![false; n];
    let mut q: Vec<usize> = Vec::new();
    reachable[0] = true;
    q.push(0);
    let mut head = 0;
    while head < q.len() {
        let cell = q[head];
        head += 1;
        let r = cell as i64 / COLS;
        let c = cell as i64 % COLS;
        let cols = COLS as usize;
        if r > 0 && grid[cell - cols] != 2 && !reachable[cell - cols] { reachable[cell - cols] = true; q.push(cell - cols); }
        if r < ROWS - 1 && grid[cell + cols] != 2 && !reachable[cell + cols] { reachable[cell + cols] = true; q.push(cell + cols); }
        if c > 0 && grid[cell - 1] != 2 && !reachable[cell - 1] { reachable[cell - 1] = true; q.push(cell - 1); }
        if c < COLS - 1 && grid[cell + 1] != 2 && !reachable[cell + 1] { reachable[cell + 1] = true; q.push(cell + 1); }
    }

    let mut sites: Vec<usize> = Vec::new();
    while (sites.len() as i64) < BUILDINGS {
        seed = lcg(seed);
        let p = ((seed / 256) % n as i64) as usize;
        if grid[p] == 0 && reachable[p] {
            grid[p] = 1;
            sites.push(p);
        }
    }

    let mut checksum: i64 = 0;
    for pass in 0..PASSES {
        let old = sites[(pass % BUILDINGS) as usize];
        let mut i = (checksum % n as i64) as usize;
        while grid[i] != 0 {
            i = (i + 1) % n;
        }
        grid[old] = 0;
        grid[i] = 1;
        let ans = shortest_distance(&grid, ROWS, COLS);
        checksum = (checksum * 31 + ans + 7) & MASK;
        grid[i] = 0;
        grid[old] = 1;
    }
    println!("checksum {}", checksum);
}
