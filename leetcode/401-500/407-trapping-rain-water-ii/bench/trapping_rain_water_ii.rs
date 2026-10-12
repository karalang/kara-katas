// Benchmark for #407: mirror of trapping_rain_water_ii.kara (a min-heap
// walking in from the border).
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn trap_rain_water(height: &[Vec<i64>]) -> i64 {
    let m = height.len() as i64;
    if m < 3 || height[0].len() < 3 {
        return 0;
    }
    let n = height[0].len() as i64;
    let mut seen = vec![vec![false; n as usize]; m as usize];
    let mut heap: BinaryHeap<Reverse<(i64, i64, i64)>> = BinaryHeap::new();
    for r in 0..m {
        for c in 0..n {
            if r == 0 || c == 0 || r == m - 1 || c == n - 1 {
                heap.push(Reverse((height[r as usize][c as usize], r, c)));
                seen[r as usize][c as usize] = true;
            }
        }
    }
    let dr = [1, -1, 0, 0];
    let dc = [0, 0, 1, -1];
    let mut water = 0;
    while let Some(Reverse((level, r, c))) = heap.pop() {
        for d in 0..4 {
            let nr = r + dr[d];
            let nc = c + dc[d];
            if nr >= 0 && nr < m && nc >= 0 && nc < n && !seen[nr as usize][nc as usize] {
                seen[nr as usize][nc as usize] = true;
                let h = height[nr as usize][nc as usize];
                if h < level {
                    water += level - h;
                }
                heap.push(Reverse((level.max(h), nr, nc)));
            }
        }
    }
    water
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let grids = 60;
    let size = 200;
    let mut seed: i64 = 407;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..grids {
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..size {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..size {
                let hi = step(&mut seed);
                row.push((hi * 32768 + step(&mut seed)) % 20000);
            }
            grid.push(row);
        }
        let w = trap_rain_water(&grid);
        total += w;
        checksum = (checksum * 31 + w) % 1000000007;
    }
    println!("{} grids of {} x {}: {} units of water, checksum {}", grids, size, size, total, checksum);
}
