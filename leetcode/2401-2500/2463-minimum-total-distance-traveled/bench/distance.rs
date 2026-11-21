// LeetCode #2463: Minimum Total Distance Traveled -- the bench, the ★ arm
// in Rust: a table over the sorted robots and factories, each factory
// either skipped or given the next run of robots up to its limit.
use std::collections::HashSet;

const NONE: i64 = 9000000000000000000;

fn minimum_total_distance(robot: &[i64], factory: &[Vec<i64>]) -> i64 {
    let mut robots = robot.to_vec();
    robots.sort();
    let mut factories = factory.to_vec();
    factories.sort();
    let n = robots.len();
    let m = factories.len();
    let mut best = vec![vec![NONE; m + 1]; n + 1];
    for j in 0..m + 1 {
        best[n][j] = 0;
    }
    for j in (0..m).rev() {
        let (at, limit) = (factories[j][0], factories[j][1] as usize);
        for i in (0..n).rev() {
            let mut least = best[i][j + 1];
            let mut run = 0;
            for t in 1..limit.min(n - i) + 1 {
                run += (robots[i + t - 1] - at).abs();
                if best[i + t][j + 1] < NONE {
                    least = least.min(run + best[i + t][j + 1]);
                }
            }
            best[i][j] = least;
        }
    }
    best[0][0]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn random_case(n: usize, m: usize, top: i64, cap: i64, seed: &mut i64) -> (Vec<i64>, Vec<Vec<i64>>) {
    let mut taken = HashSet::new();
    let mut robot = Vec::new();
    while robot.len() < n {
        let p = wide_random(seed) % (2 * top + 1) - top;
        if taken.insert(p) {
            robot.push(p);
        }
    }
    let mut places = HashSet::new();
    let mut factory: Vec<Vec<i64>> = Vec::new();
    while factory.len() < m {
        let p = wide_random(seed) % (2 * top + 1) - top;
        if places.insert(p) {
            factory.push(vec![p, next_random(seed) % (cap + 1)]);
        }
    }
    let mut room: i64 = factory.iter().map(|f| f[1]).sum();
    let mut j = 0;
    while room < n as i64 {
        factory[j % m][1] += 1;
        room += 1;
        j += 1;
    }
    (robot, factory)
}

fn main() {
    // 40 cases of 100 robots and 100 factories over 2 10^9 places, limits
    // up to 2, built once; then 72 passes, each raising one limit of every
    // case, chosen by the checksum so far, then answering every case and
    // folding the answer plus the pass into the checksum
    let mut seed = 2463;
    let mut cases: Vec<(Vec<i64>, Vec<Vec<i64>>)> = (0..40).map(|_| random_case(100, 100, 1000000000, 2, &mut seed)).collect();
    let mut check = 0i64;
    for p in 0..72i64 {
        for c in 0..cases.len() {
            cases[c].1[((check + c as i64) % 100) as usize][1] += 1;
            check = (check * 31 + minimum_total_distance(&cases[c].0, &cases[c].1) % 1000000007 + p) % 1000000007;
        }
    }
    println!("72 passes over 40 cases of 100 robots: checksum {check}");
}
