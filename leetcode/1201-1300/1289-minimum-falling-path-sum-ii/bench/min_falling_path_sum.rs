// LeetCode #1289 bench, in Rust: the ★ arm (the row above's two smallest
// path sums) on 100 grids of 200 by 200, built once, 300 rounds, every
// answer folded into a checksum.

fn min_falling_path_sum(grid: &[Vec<i64>]) -> i64 {
    let (mut first, mut first_col, mut second) = (0i64, -1i64, 0i64);
    for row in grid.iter() {
        let (mut next_first, mut next_col, mut next_second) = (i64::MAX, -1i64, i64::MAX);
        for (j, &x) in row.iter().enumerate() {
            let j = j as i64;
            let sum = x + if j == first_col { second } else { first };
            if sum < next_first {
                next_second = next_first;
                next_first = sum;
                next_col = j;
            } else if sum < next_second {
                next_second = sum;
            }
        }
        first = next_first;
        first_col = next_col;
        second = next_second;
    }
    first
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn problem(seed: &mut i64, n: i64) -> Vec<Vec<i64>> {
    let mut grid: Vec<Vec<i64>> = Vec::new();
    for _ in 0..n {
        let mut row: Vec<i64> = Vec::new();
        for _ in 0..n {
            row.push(next_random(seed) % 199 - 99);
        }
        grid.push(row);
    }
    grid
}

fn main() {
    let mut seed = 1289;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..100 {
        grids.push(problem(&mut seed, 200));
    }
    let mut check: i64 = 0;
    for round in 0..300i64 {
        for grid in grids.iter() {
            check = (check * 131 + min_falling_path_sum(grid) + round + 1000000) % 1000000007;
        }
    }
    println!("300 rounds of 100 grids of 200 by 200: checksum {}", check);
}
