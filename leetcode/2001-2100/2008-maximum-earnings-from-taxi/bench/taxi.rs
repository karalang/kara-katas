// LeetCode #2008: Maximum Earnings From Taxi -- the ★ arm's benchmark, a
// mirror of taxi.kara.

fn max_taxi_earnings(n: i64, rides: &[(i64, i64, i64)]) -> i64 {
    let mut ending: Vec<Vec<(i64, i64)>> = vec![Vec::new(); (n + 1) as usize];
    for &(start, end, tip) in rides {
        ending[end as usize].push((start, end - start + tip));
    }
    let mut best = vec![0i64; (n + 1) as usize];
    for p in 2..=n as usize {
        best[p] = best[p - 1];
        for &(start, earned) in &ending[p] {
            best[p] = best[p].max(best[start as usize] + earned);
        }
    }
    best[n as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2008i64;
    let mut roads: Vec<Vec<(i64, i64, i64)>> = Vec::new();
    for _ in 0..80 {
        let mut rides = Vec::new();
        for _ in 0..5000 {
            let length = next_random(&mut seed) % 100 + 1;
            let start = next_random(&mut seed) % (9900 - length) + 1;
            rides.push((start, start + length, next_random(&mut seed) % 1001));
        }
        roads.push(rides);
    }
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for r in 0..25 {
        for road in &roads {
            let answer = max_taxi_earnings(10000 - r * 4, road);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("{calls} calls: sum {sum}, checksum {check}");
}
