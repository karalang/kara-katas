// LeetCode #2022: Convert 1D Array Into 2D Array -- the ★ arm in Rust, the
// same algorithm and workload as convert.kara.

fn construct_2d_array(original: &[i64], m: i64, n: i64) -> Vec<Vec<i64>> {
    if original.len() as i64 != m * n {
        return Vec::new();
    }
    (0..m)
        .map(|i| original[(i * n) as usize..((i + 1) * n) as usize].to_vec())
        .collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2022;
    let rows_of: [i64; 20] = [1, 2, 4, 5, 8, 10, 16, 20, 25, 40, 50, 80, 100, 125, 200, 250, 400, 500, 1000, 20000];
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        arrays.push((0..20000).map(|_| next_random(&mut seed) % 100000 + 1).collect());
    }
    let mut calls: i64 = 0;
    let mut rows: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..200 {
        for a in 0..20 {
            let m = rows_of[a];
            let n = if a % 5 == 4 { 20000 / m + 1 } else { 20000 / m };
            let grid = construct_2d_array(&arrays[a], m, n);
            calls += 1;
            if grid.is_empty() {
                check = (check * 31 + 1000000006) % 1000000007;
            }
            for row in grid.iter() {
                rows += 1;
                check = (check * 31 + row[0] + row[row.len() - 1]) % 1000000007;
            }
        }
    }
    println!("{} calls: {} rows, checksum {}", calls, rows, check);
}
