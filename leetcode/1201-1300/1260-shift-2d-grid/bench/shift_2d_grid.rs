// LeetCode #1260 bench, in Rust: the ★ arm (each value at flat place p
// written to (p + k) % (m * n) of a new grid) on 200 random grids of 50 by
// 50 built once, each shifted by a random 0 to 100, 150 rounds; a corner and
// the middle of each result folded into a checksum.

fn shift_grid(grid: &[Vec<i64>], k: i64) -> Vec<Vec<i64>> {
    let m = grid.len();
    let n = grid[0].len();
    let total = m * n;
    let mut shifted = vec![vec![0i64; n]; m];
    for i in 0..m {
        for j in 0..n {
            let to = (i * n + j + k as usize) % total;
            shifted[to / n][to % n] = grid[i][j];
        }
    }
    shifted
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1260;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut shifts: Vec<i64> = Vec::new();
    for _ in 0..200 {
        grids.push((0..50).map(|_| (0..50).map(|_| next_random(&mut seed) % 2001 - 1000).collect()).collect());
        shifts.push(next_random(&mut seed) % 101);
    }
    let mut check: i64 = 0;
    for _ in 0..150 {
        for g in 0..200 {
            let shifted = shift_grid(&grids[g], shifts[g]);
            check = (check * 131 + shifted[0][0] + 1000) % 1000000007;
            check = (check * 131 + shifted[25][25] + 1000) % 1000000007;
        }
    }
    println!("150 rounds of 200 grids of 50 by 50: checksum {check}");
}
