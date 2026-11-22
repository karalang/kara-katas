// LeetCode #2711: Difference of Number of Distinct Values on Diagonals --
// the bench (diagonals.kara in Rust): each diagonal swept down and then
// up with a table of the values seen.

fn difference_of_distinct_values(grid: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let m = grid.len();
    let n = grid[0].len();
    let mut answer = vec![vec![0i64; n]; m];
    let mut starts: Vec<(usize, usize)> = (0..n).map(|c| (0, c)).collect();
    for r in 1..m {
        starts.push((r, 0));
    }
    for &(r0, c0) in starts.iter() {
        let length = (m - r0).min(n - c0);
        let mut seen = [false; 51];
        let mut distinct = 0i64;
        for k in 0..length {
            answer[r0 + k][c0 + k] = distinct;
            let v = grid[r0 + k][c0 + k] as usize;
            if !seen[v] {
                seen[v] = true;
                distinct += 1;
            }
        }
        seen = [false; 51];
        distinct = 0;
        for k in (0..length).rev() {
            answer[r0 + k][c0 + k] = (answer[r0 + k][c0 + k] - distinct).abs();
            let v = grid[r0 + k][c0 + k] as usize;
            if !seen[v] {
                seen[v] = true;
                distinct += 1;
            }
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 2000;
    let rounds = 5;
    let mut seed: i64 = 2711;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        let cap = next_random(&mut seed) % 50 + 1;
        let grid: Vec<Vec<i64>> = (0..50).map(|_| (0..50).map(|_| next_random(&mut seed) % cap + 1).collect()).collect();
        grids.push(grid);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for grid in grids.iter() {
            let answer = difference_of_distinct_values(grid);
            for row in answer.iter() {
                for &v in row.iter() {
                    sum += v;
                    check = (check * 31 + v) % 1000000007;
                }
            }
            check = (check + r) % 1000000007;
        }
    }
    println!("{} grids of 50 by 50, {} rounds: differences sum to {}, checksum {}", count, rounds, sum, check);
}
