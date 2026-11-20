// LeetCode #2397: Maximum Rows Covered by Columns -- the bench, the ★ arm
// in Rust: each row as the mask of its 1s, every mask of numSelect
// columns tried.

fn maximum_rows(matrix: &[Vec<i64>], num_select: i64) -> i64 {
    let n = matrix[0].len();
    let masks: Vec<i64> = matrix
        .iter()
        .map(|row| {
            let mut mask = 0i64;
            for c in 0..n {
                if row[c] == 1 {
                    mask |= 1 << c;
                }
            }
            mask
        })
        .collect();
    let mut best = 0;
    for chosen in 0i64..1 << n {
        if chosen.count_ones() as i64 != num_select {
            continue;
        }
        let mut covered = 0;
        for &mask in &masks {
            if mask & chosen == mask {
                covered += 1;
            }
        }
        best = best.max(covered);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn grid(seed: &mut i64, m: i64, n: i64, odds: i64) -> Vec<Vec<i64>> {
    (0..m)
        .map(|_| (0..n).map(|_| if next_random(seed) % odds == 0 { 1 } else { 0 }).collect())
        .collect()
}

fn main() {
    let mut seed = 2397i64;
    let grids: Vec<Vec<Vec<i64>>> = (0..200).map(|g| grid(&mut seed, 12, 12, 2 + g % 4)).collect();
    let mut check = 0i64;
    for p in 0..10i64 {
        for g in &grids {
            for k in 1..13 {
                check = (check * 31 + maximum_rows(g, k) + p) % 1000000007;
            }
        }
    }
    println!("10 passes over 200 grids of 12 by 12, every choice: checksum {}", check);
}
