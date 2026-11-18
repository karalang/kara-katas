// LeetCode #2319: Check if Matrix Is X-Matrix -- the bench, the ★ arm in
// Rust. One walk over the cells, a cell on either diagonal nonzero and
// any other zero, the first cell that breaks its rule ending the walk.
// O(n^2).

fn check_x_matrix(grid: &Vec<Vec<i64>>) -> bool {
    let n = grid.len();
    for i in 0..n {
        for j in 0..n {
            let on = i == j || i + j == n - 1;
            if on != (grid[i][j] != 0) {
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
    let n: usize = 100;
    let mut seed: i64 = 2319;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..200 {
        let mut g: Vec<Vec<i64>> = Vec::new();
        for i in 0..n {
            let mut row: Vec<i64> = Vec::new();
            for j in 0..n {
                let value = next_random(&mut seed) % 100000 + 1;
                row.push(if i == j || i + j == n - 1 { value } else { 0 });
            }
            g.push(row);
        }
        grids.push(g);
    }
    let mut check: i64 = 0;
    for p in 0..400i64 {
        for g in 0..200 {
            let punch = next_random(&mut seed) % 2 == 0;
            let i = (next_random(&mut seed) % n as i64) as usize;
            let j = (next_random(&mut seed) % n as i64) as usize;
            let old = grids[g][i][j];
            if punch {
                grids[g][i][j] = if old == 0 { p + 1 } else { 0 };
            }
            let is_x = check_x_matrix(&grids[g]);
            grids[g][i][j] = old;
            check = (check * 31 + if is_x { 2 } else { 1 } + p) % 1000000007;
        }
    }
    println!("400 passes over 200 grids of 100 by 100: checksum {}", check);
}
