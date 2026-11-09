// LeetCode #2033: Minimum Operations to Make a Uni-Value Grid -- the ★ arm
// in Rust, the same algorithm and workload as grid.kara: the values
// flattened out of the grid and sorted per call (`sort`, as Kāra's).

fn min_operations(grid: &[Vec<i64>], x: i64) -> i64 {
    let mut values: Vec<i64> = grid.iter().flat_map(|v| v.iter()).cloned().collect();
    let r = values[0] % x;
    if values.iter().any(|v| v % x != r) {
        return -1;
    }
    values.sort();
    let median = values[values.len() / 2];
    values.iter().map(|v| (v - median).abs() / x).sum()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2033;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for a in 0..20 {
        let x = a % 7 + 1;
        let base = next_random(&mut seed) % x + 1;
        let steps = (10000 - base) / x + 1;
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..200 {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..250 {
                let hi = next_random(&mut seed);
                let lo = next_random(&mut seed);
                row.push(base + (hi * 32768 + lo) % steps * x);
            }
            grid.push(row);
        }
        grids.push(grid);
    }
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for round in 0..30i64 {
        for a in 0..20i64 {
            let x = a % 7 + 1;
            let at = (round * 997 + a * 31) % 50000;
            let cell = &mut grids[a as usize][(at / 250) as usize][(at % 250) as usize];
            *cell = if *cell + x <= 10000 { *cell + x } else { *cell - x };
            let answer = min_operations(&grids[a as usize], x);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
