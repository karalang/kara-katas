// LeetCode #2500: Delete Greatest Value in Each Row -- Rust mirror of the
// benchmark (greatest.kara): the same grids, passes and checksum; each ask
// clones the grid and sorts every row.

fn delete_greatest_value(grid: &[Vec<i64>]) -> i64 {
    let mut rows = grid.to_vec();
    for row in rows.iter_mut() {
        row.sort();
    }
    let mut total = 0;
    for j in 0..rows[0].len() {
        let mut most = 0;
        for row in &rows {
            most = most.max(row[j]);
        }
        total += most;
    }
    total
}

fn main() {
    let passes: i64 = 32;
    let mut seed: i64 = 2500;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..1000 {
        let mut grid = Vec::new();
        for _ in 0..50 {
            let mut row = Vec::new();
            for _ in 0..50 {
                row.push(next_random() % 100 + 1);
            }
            grid.push(row);
        }
        grids.push(grid);
    }
    let mut check: i64 = 0;
    for p in 0..passes {
        for g in 0..1000 {
            let r = (check % 50) as usize;
            let c = (check / 50 % 50) as usize;
            let was = grids[g][r][c];
            grids[g][r][c] = (check + p) % 100 + 1;
            check = (check * 31 + delete_greatest_value(&grids[g]) + p) % 1000000007;
            grids[g][r][c] = was;
        }
    }
    println!("{passes} passes over 1000 grids of 50 by 50: checksum {check}");
}
