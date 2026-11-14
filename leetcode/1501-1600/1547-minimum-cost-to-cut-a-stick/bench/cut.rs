// LeetCode #1547: Minimum Cost to Cut a Stick -- bench: the ★ arm (interval
// DP) over 100 sticks of 2 to 1000000 with 1 to 100 distinct cuts, built
// once, each asked 4 times. Rust mirror of cut.kara.

use std::collections::HashSet;

fn min_cost(n: i64, cuts: Vec<i64>) -> i64 {
    let mut points = cuts.clone();
    points.push(0);
    points.push(n);
    points.sort();
    let m = points.len();
    let mut cost = vec![vec![0i64; m]; m];
    for gap in 2..m {
        for i in 0..m - gap {
            let j = i + gap;
            let mut best = i64::MAX;
            for k in i + 1..j {
                best = best.min(cost[i][k] + cost[k][j]);
            }
            cost[i][j] = best + points[j] - points[i];
        }
    }
    cost[0][m - 1]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1547i64;
    let mut sticks = Vec::new();
    for _ in 0..100 {
        let n = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 999999 + 2;
        let want = (next_random(&mut seed) % 100 + 1).min(n - 1);
        let mut taken = HashSet::new();
        let mut cuts = Vec::new();
        while (cuts.len() as i64) < want {
            let c = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (n - 1) + 1;
            if taken.insert(c) {
                cuts.push(c);
            }
        }
        sticks.push((n, cuts));
    }
    let mut check = 0i64;
    for _ in 0..4 {
        for (n, cuts) in &sticks {
            check = mix(check, min_cost(*n, cuts.clone()));
        }
    }
    println!("4 passes over 100 sticks of up to 1000000 with up to 100 cuts: checksum {}", check);
}
