// LeetCode #1162: As Far from Land as Possible -- Rust mirror of the Kāra
// ★ arm: a breadth-first search from every land cell at once, over a flat
// distance array and a queue of cell indices.

fn max_distance(grid: &[Vec<i64>]) -> i64 {
    let n = grid.len() as i64;
    let mut dist = vec![-1i64; (n * n) as usize];
    let mut queue: Vec<i64> = Vec::new();
    for i in 0..n {
        for j in 0..n {
            if grid[i as usize][j as usize] == 1 {
                dist[(i * n + j) as usize] = 0;
                queue.push(i * n + j);
            }
        }
    }
    if queue.is_empty() || queue.len() as i64 == n * n {
        return -1;
    }
    let mut head = 0;
    let mut far = 0;
    while head < queue.len() {
        let cell = queue[head];
        head += 1;
        let (i, j) = (cell / n, cell % n);
        far = dist[cell as usize];
        for (di, dj) in [(-1i64, 0i64), (1, 0), (0, -1), (0, 1)] {
            let (a, b) = (i + di, j + dj);
            if a >= 0 && a < n && b >= 0 && b < n && dist[(a * n + b) as usize] < 0 {
                dist[(a * n + b) as usize] = far + 1;
                queue.push(a * n + b);
            }
        }
    }
    far
}

fn main() {
    let mut seed: i64 = 1162;
    let mut next_random = move || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let odds = [1, 2, 5, 10, 50, 200, 500, 900];
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for k in 0..16 {
        let o = odds[k % 8];
        grids.push((0..100).map(|_| (0..100).map(|_| if next_random() % 1000 < o { 1 } else { 0 }).collect()).collect());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..300 {
        for k in 0..16 {
            let a = (next_random() % 100) as usize;
            let b = (next_random() % 100) as usize;
            grids[k][a][b] = 1 - grids[k][a][b];
            let d = max_distance(&grids[k]);
            total += d;
            check = (check * 31 + d + 1) % 1000000007;
        }
    }
    println!("300 rounds over 16 grids of 100 by 100: total {}, checksum {}", total, check);
}
