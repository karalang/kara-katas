// LeetCode #2713: Maximum Strictly Increasing Cells in a Matrix -- the
// bench (increasing.kara in Rust): the cells sorted by value, each
// value's cells answered from their row's and column's best before any is
// recorded.

fn max_increasing_cells(mat: &Vec<Vec<i64>>) -> i64 {
    let m = mat.len();
    let n = mat[0].len();
    let mut cells: Vec<(i64, usize, usize)> = Vec::new();
    for r in 0..m {
        for c in 0..n {
            cells.push((mat[r][c], r, c));
        }
    }
    cells.sort();
    let mut row_best: Vec<i64> = vec![0; m];
    let mut col_best: Vec<i64> = vec![0; n];
    let mut found: Vec<i64> = Vec::new();
    let mut best = 0;
    let mut i = 0;
    while i < cells.len() {
        let mut j = i;
        while j < cells.len() && cells[j].0 == cells[i].0 {
            j += 1;
        }
        found.clear();
        for k in i..j {
            let (_, r, c) = cells[k];
            found.push(row_best[r].max(col_best[c]) + 1);
        }
        for k in i..j {
            let (_, r, c) = cells[k];
            row_best[r] = row_best[r].max(found[k - i]);
            col_best[c] = col_best[c].max(found[k - i]);
            best = best.max(found[k - i]);
        }
        i = j;
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 10;
    let rounds = 10;
    let mut seed: i64 = 2713;
    let mut mats: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        let spread = next_random(&mut seed) % 9991 + 10;
        let mat: Vec<Vec<i64>> = (0..300).map(|_| (0..300).map(|_| next_random(&mut seed) % spread).collect()).collect();
        mats.push(mat);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for mat in mats.iter() {
            let cells = max_increasing_cells(mat);
            sum += cells;
            check = (check * 31 + cells + r) % 1000000007;
        }
    }
    println!("{} matrices of 300 by 300, {} rounds: cells sum to {}, checksum {}", count, rounds, sum, check);
}
