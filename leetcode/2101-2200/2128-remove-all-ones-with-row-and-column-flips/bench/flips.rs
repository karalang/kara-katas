// LeetCode #2128: Remove All Ones With Row and Column Flips -- the
// benchmark, the same algorithm as flips.kara.

fn remove_ones(grid: &[Vec<i64>]) -> bool {
    let first = &grid[0];
    for row in grid.iter() {
        for j in 0..row.len() {
            if row[j] ^ row[0] != first[j] ^ first[0] {
                return false;
            }
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 300;
    let mut seed = 2128;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..20 {
        let mut columns: Vec<i64> = Vec::new();
        for _ in 0..n {
            columns.push(next_random(&mut seed) % 2);
        }
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..n {
            let r = next_random(&mut seed) % 2;
            grid.push(columns.iter().map(|c| c ^ r).collect());
        }
        grids.push(grid);
    }
    let mut cleared = 0;
    let mut check: i64 = 0;
    for round in 0..100i64 {
        for k in 0..20usize {
            let r = (next_random(&mut seed) % n) as usize;
            for c in grids[k][r].iter_mut() {
                *c = 1 - *c;
            }
            let broken = next_random(&mut seed) % 2 == 0;
            let i = (next_random(&mut seed) % n) as usize;
            let j = (next_random(&mut seed) % n) as usize;
            if broken {
                grids[k][i][j] = 1 - grids[k][i][j];
            }
            if remove_ones(&grids[k]) {
                cleared += 1;
                check = (check * 31 + round * 20 + k as i64) % 1000000007;
            }
            if broken {
                grids[k][i][j] = 1 - grids[k][i][j];
            }
        }
    }
    println!("2000 solves: {} cleared, checksum {}", cleared, check);
}
