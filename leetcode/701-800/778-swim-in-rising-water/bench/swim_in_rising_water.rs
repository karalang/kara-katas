// Benchmark for #778: Swim in Rising Water -- mirror of the ★ arm
// (Dijkstra on the highest square), with the same workload as the Kāra
// program.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn swim_in_water(grid: &[Vec<i64>]) -> i64 {
    let n = grid.len() as i64;
    let mut done = vec![false; (n * n) as usize];
    let mut queue: BinaryHeap<Reverse<(i64, i64)>> = BinaryHeap::new();
    queue.push(Reverse((grid[0][0], 0)));
    while let Some(Reverse((t, at))) = queue.pop() {
        if done[at as usize] {
            continue;
        }
        done[at as usize] = true;
        let r = at / n;
        let c = at % n;
        if r == n - 1 && c == n - 1 {
            return t;
        }
        for (dr, dc) in [(0, 1), (1, 0), (0, -1), (-1, 0)] {
            let nr = r + dr;
            let nc = c + dc;
            if nr >= 0 && nr < n && nc >= 0 && nc < n && !done[(nr * n + nc) as usize] {
                let h = grid[nr as usize][nc as usize];
                queue.push(Reverse((if h > t { h } else { t }, nr * n + nc)));
            }
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let n: i64 = 50;
    let mut seed: i64 = 778;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for g in 0..count {
        let mut values: Vec<i64> = Vec::new();
        for r in 0..n {
            for c in 0..n {
                values.push(if g % 4 == 2 && r % 2 == 1 { r * n + n - 1 - c } else { r * n + c });
            }
        }
        if g % 4 < 2 {
            let mut i = n * n - 1;
            while i > 0 {
                let j = next_random(&mut seed) % (i + 1);
                values.swap(i as usize, j as usize);
                i -= 1;
            }
        } else {
            for _ in 0..50 {
                let i = next_random(&mut seed) % (n * n);
                let j = next_random(&mut seed) % (n * n);
                values.swap(i as usize, j as usize);
            }
        }
        let grid: Vec<Vec<i64>> = (0..n as usize).map(|r| values[r * n as usize..(r + 1) * n as usize].to_vec()).collect();
        grids.push(grid);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..3000i64 {
        let g = (round * 7) % count;
        let answer = swim_in_water(&grids[g as usize]);
        total += answer;
        checksum = (checksum * 31 + answer + g) % 1000000007;
    }
    println!("3000 rounds of 50 x 50 grids: answers sum to {total}, checksum {checksum}");
}
