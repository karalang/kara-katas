// LeetCode #2852: Sum of Remoteness of All Cells -- the bench: the ★ arm
// over 20 grids of 300 x 300, LeetCode's most, values up to 10^6, a
// cell blocked from 1 time in 10 to 6 in 10, all drawn first, then each
// answered 10 times.
use std::collections::VecDeque;

fn sum_remoteness(grid: &Vec<Vec<i64>>) -> i64 {
    let n = grid.len() as i64;
    let mut total = 0;
    for row in grid.iter() {
        for &v in row.iter() {
            if v > 0 {
                total += v;
            }
        }
    }
    let mut seen = vec![vec![false; n as usize]; n as usize];
    let mut answer = 0;
    for i in 0..n {
        for j in 0..n {
            if grid[i as usize][j as usize] < 0 || seen[i as usize][j as usize] {
                continue;
            }
            seen[i as usize][j as usize] = true;
            let mut queue: VecDeque<(i64, i64)> = VecDeque::new();
            queue.push_back((i, j));
            let mut size = 0;
            let mut sum = 0;
            while let Some((r, c)) = queue.pop_front() {
                size += 1;
                sum += grid[r as usize][c as usize];
                for &(dr, dc) in [(0, 1), (1, 0), (0, -1), (-1, 0)].iter() {
                    let (nr, nc) = (r + dr, c + dc);
                    if nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr as usize][nc as usize] > 0 && !seen[nr as usize][nc as usize] {
                        seen[nr as usize][nc as usize] = true;
                        queue.push_back((nr, nc));
                    }
                }
            }
            answer += size * (total - sum);
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 20;
    let rounds = 10;
    let n = 300;
    let mut seed = 2852;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        let blocked = next_random(&mut seed) % 6 + 1;
        let grid: Vec<Vec<i64>> = (0..n)
            .map(|_| (0..n).map(|_| if next_random(&mut seed) % 10 < blocked { -1 } else { wide(&mut seed) % 1000000 + 1 }).collect())
            .collect();
        grids.push(grid);
    }
    let mut check = 0i64;
    for r in 0..rounds {
        for grid in grids.iter() {
            check = (check * 31 + sum_remoteness(grid) % 1000000007 + r) % 1000000007;
        }
    }
    println!("{count} grids of {n} x {n}, {rounds} rounds: checksum {check}");
}
