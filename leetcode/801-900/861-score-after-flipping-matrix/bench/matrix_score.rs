// LeetCode #861: Score After Flipping Matrix -- Rust mirror of the bench
// program (the ★ arm, count each column against the first).

fn matrix_score(grid: &[Vec<i64>]) -> i64 {
    let m = grid.len() as i64;
    let n = grid[0].len();
    let mut score: i64 = 0;
    for j in 0..n {
        let mut ones: i64 = 0;
        for row in grid {
            if row[j] == row[0] {
                ones += 1;
            }
        }
        score = score * 2 + ones.max(m - ones);
    }
    score
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let size: i64 = 20;
    let rounds: i64 = 1000000;
    let mut seed: i64 = 861;
    let mut grid: Vec<Vec<i64>> = Vec::new();
    for _ in 0..size {
        let mut row: Vec<i64> = Vec::new();
        for _ in 0..size {
            row.push(next_random(&mut seed) % 2);
        }
        grid.push(row);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let cell = next_random(&mut seed) % (size * size);
        let i = (cell / size) as usize;
        let j = (cell % size) as usize;
        grid[i][j] = 1 - grid[i][j];
        let s = matrix_score(&grid);
        grid[i][j] = 1 - grid[i][j];
        total += s;
        check = (check * 31 + s) % 1000000007;
    }
    println!("{} rounds on a {} by {} grid: scores sum to {}, checksum {}", rounds, size, size, total, check);
}
