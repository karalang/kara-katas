// LeetCode #2087: Minimum Cost Homecoming of a Robot in a Grid -- Rust
// mirror of the ★ arm's benchmark (homecoming.kara): the same grid and
// 2000 trips, each the two ranges of costs summed over slices.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn walk(costs: &[i64], from: usize, to: usize) -> i64 {
    if from < to {
        costs[from + 1..=to].iter().sum()
    } else {
        costs[to..from].iter().sum()
    }
}

fn min_cost(start: &[usize], home: &[usize], rows: &[i64], cols: &[i64]) -> i64 {
    walk(rows, start[0], home[0]) + walk(cols, start[1], home[1])
}

fn place(seed: &mut i64) -> usize {
    let hi = next_random(seed);
    ((hi * 32768 + next_random(seed)) % 1000000) as usize
}

fn main() {
    let mut seed = 2087i64;
    let rows: Vec<i64> = (0..1000000).map(|_| next_random(&mut seed) % 10001).collect();
    let cols: Vec<i64> = (0..1000000).map(|_| next_random(&mut seed) % 10001).collect();
    let (mut total, mut check) = (0i64, 0i64);
    for _ in 0..2000 {
        let start = vec![place(&mut seed), place(&mut seed)];
        let home = vec![place(&mut seed), place(&mut seed)];
        let a = min_cost(&start, &home, &rows, &cols);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    println!("2000 trips: sum {}, checksum {}", total, check);
}
