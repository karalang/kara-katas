// LeetCode #2732: Find a Good Subset of the Matrix -- the bench
// (subset.kara in Rust): a row of zeros alone, or the first rows of two
// disjoint masks among the 32.

fn good_subsetof_binary_matrix(grid: &[Vec<i64>]) -> Vec<i64> {
    let mut first = [-1i64; 32];
    for (i, row) in grid.iter().enumerate() {
        let mut mask: i64 = 0;
        for (j, &x) in row.iter().enumerate() {
            mask |= x << j;
        }
        if mask == 0 {
            return vec![i as i64];
        }
        if first[mask as usize] < 0 {
            first[mask as usize] = i as i64;
        }
    }
    for a in 1..32 {
        for b in a + 1..32 {
            if a & b == 0 && first[a] >= 0 && first[b] >= 0 {
                return vec![first[a].min(first[b]), first[a].max(first[b])];
            }
        }
    }
    Vec::new()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let grids = 100;
    let m: i64 = 10000;
    let n: i64 = 5;
    let rounds = 10;
    let mut seed: i64 = 2732;
    let mut all: Vec<Vec<Vec<i64>>> = Vec::new();
    for g in 0..grids {
        let kind = g % 3;
        let column = next_random(&mut seed) % n;
        let free = next_random(&mut seed) % m;
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for r in 0..m {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..n {
                row.push(next_random(&mut seed) % 2);
            }
            if kind == 1 || (kind == 2 && r != free) {
                row[column as usize] = 1;
            }
            grid.push(row);
        }
        all.push(grid);
    }
    let mut found = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for grid in all.iter() {
            let rows = good_subsetof_binary_matrix(grid);
            if !rows.is_empty() {
                found += 1;
            }
            let named: i64 = rows.iter().sum();
            check = (check * 31 + named + rows.len() as i64 + r) % 1000000007;
        }
    }
    println!("{} grids of {} rows, {} rounds: {} good subsets found, checksum {}", grids, m, rounds, found, check);
}
