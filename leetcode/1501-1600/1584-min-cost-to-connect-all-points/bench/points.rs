// LeetCode #1584 bench: the same Prim's algorithm with no edge list, in
// Rust.
use std::collections::HashSet;

fn min_cost_connect_points(points: &[Vec<i64>]) -> i64 {
    let n = points.len();
    let mut nearest = vec![i64::MAX; n];
    let mut inside = vec![false; n];
    nearest[0] = 0;
    let mut cost = 0;
    for _ in 0..n {
        let mut next = usize::MAX;
        for i in 0..n {
            if !inside[i] && (next == usize::MAX || nearest[i] < nearest[next]) {
                next = i;
            }
        }
        inside[next] = true;
        cost += nearest[next];
        for i in 0..n {
            if !inside[i] {
                let d = (points[i][0] - points[next][0]).abs() + (points[i][1] - points[next][1]).abs();
                nearest[i] = nearest[i].min(d);
            }
        }
    }
    cost
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1584i64;
    let mut problems: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..100 {
        let mut seen: HashSet<(i64, i64)> = HashSet::new();
        let mut points: Vec<Vec<i64>> = Vec::new();
        while points.len() < 1000 {
            let x = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 2000001 - 1000000;
            let y = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 2000001 - 1000000;
            if seen.insert((x, y)) {
                points.push(vec![x, y]);
            }
        }
        problems.push(points);
    }
    let (mut check, mut total) = (0i64, 0i64);
    for points in problems.iter() {
        let cost = min_cost_connect_points(points);
        total += cost;
        check = mix(check, cost);
    }
    println!("100 problems of 1000 points: cost {}, checksum {}", total, check);
}
