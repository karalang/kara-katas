// LeetCode #2088: Count Fertile Pyramids in a Land -- Rust mirror of the ★
// arm's benchmark (pyramids.kara): the same 20 lands, each counted 20 times
// by the same two passes over `Vec`s.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn count_one_way(grid: &[Vec<i64>], order: &[usize]) -> i64 {
    let n = grid[0].len();
    let mut below = vec![0i64; n];
    let mut count = 0;
    for &r in order {
        let mut tall = vec![0i64; n];
        for c in 0..n {
            if grid[r][c] == 0 {
                continue;
            }
            tall[c] = if c == 0 || c == n - 1 {
                1
            } else {
                below[c - 1].min(below[c]).min(below[c + 1]) + 1
            };
            count += tall[c] - 1;
        }
        below = tall;
    }
    count
}

fn count_pyramids(grid: &[Vec<i64>]) -> i64 {
    let m = grid.len();
    let up: Vec<usize> = (0..m).rev().collect();
    let down: Vec<usize> = (0..m).collect();
    count_one_way(grid, &up) + count_one_way(grid, &down)
}

fn main() {
    let mut seed = 2088i64;
    let mut lands: Vec<Vec<Vec<i64>>> = Vec::new();
    for t in 0..20 {
        let odds = 15 + t % 5;
        let land: Vec<Vec<i64>> = (0..316)
            .map(|_| (0..316).map(|_| if next_random(&mut seed) % 20 < odds { 1 } else { 0 }).collect())
            .collect();
        lands.push(land);
    }
    let (mut total, mut check) = (0i64, 0i64);
    for round in 0..20 {
        for t in 0..20 {
            let a = count_pyramids(&lands[(t + round) % 20]);
            total += a;
            check = (check * 31 + a) % 1000000007;
        }
    }
    println!("400 counts: sum {}, checksum {}", total, check);
}
