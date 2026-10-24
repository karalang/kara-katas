// Benchmark: LeetCode #939 Minimum Area Rectangle -- the ★ arm, pairs as
// diagonals, on 20 sets of 500 points, LeetCode's most, in 10 rounds.
// Mirrors min_area_rect.kara, .c, .py and go-seq/.
use std::collections::HashSet;

fn min_area_rect(points: &[Vec<i64>]) -> i64 {
    let mut seen: HashSet<i64> = HashSet::new();
    for p in points {
        seen.insert(p[0] * 40001 + p[1]);
    }
    let mut best = 0;
    let n = points.len();
    for i in 0..n {
        let (x1, y1) = (points[i][0], points[i][1]);
        for j in (i + 1)..n {
            let (x2, y2) = (points[j][0], points[j][1]);
            if x1 != x2
                && y1 != y2
                && seen.contains(&(x1 * 40001 + y2))
                && seen.contains(&(x2 * 40001 + y1))
            {
                let area = (x1 - x2).abs() * (y1 - y2).abs();
                if best == 0 || area < best {
                    best = area;
                }
            }
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 10;
    let count = 20;
    let mut seed = 939;
    let mut sets: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        let step = 1 + next_random(&mut seed) % 100;
        let ox = next_random(&mut seed) % 1000;
        let oy = next_random(&mut seed) % 1000;
        let mut taken = vec![false; 1600];
        let mut points: Vec<Vec<i64>> = Vec::new();
        while points.len() < 500 {
            let hi = next_random(&mut seed);
            let c = ((hi * 32768 + next_random(&mut seed)) % 1600) as usize;
            if !taken[c] {
                taken[c] = true;
                points.push(vec![
                    ox + (c as i64 % 40) * step,
                    oy + (c as i64 / 40) * step,
                ]);
            }
        }
        sets.push(points);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let a = min_area_rect(&sets[(r + i) % count]);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    println!(
        "{} rounds over {} sets of 500 points: areas adding to {}, checksum {}",
        rounds, count, total, check
    );
}
