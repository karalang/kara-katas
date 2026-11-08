// LeetCode #1515 bench: the ★ arm's ternary search twice, as centre.kara.

fn cost(positions: &[(i64, i64)], x: f64, y: f64) -> f64 {
    let mut total = 0.0;
    for &(px, py) in positions {
        let dx = px as f64 - x;
        let dy = py as f64 - y;
        total += (dx * dx + dy * dy).sqrt();
    }
    total
}

fn best_on(positions: &[(i64, i64)], x: f64) -> f64 {
    let (mut lo, mut hi) = (0.0f64, 100.0f64);
    for _ in 0..60 {
        let m1 = lo + (hi - lo) / 3.0;
        let m2 = hi - (hi - lo) / 3.0;
        if cost(positions, x, m1) < cost(positions, x, m2) {
            hi = m2;
        } else {
            lo = m1;
        }
    }
    cost(positions, x, (lo + hi) / 2.0)
}

fn get_min_dist_sum(positions: &[(i64, i64)]) -> f64 {
    let (mut lo, mut hi) = (0.0f64, 100.0f64);
    for _ in 0..60 {
        let m1 = lo + (hi - lo) / 3.0;
        let m2 = hi - (hi - lo) / 3.0;
        if best_on(positions, m1) < best_on(positions, m2) {
            hi = m2;
        } else {
            lo = m1;
        }
    }
    best_on(positions, (lo + hi) / 2.0)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1515i64;
    let mut check: i64 = 0;
    for _ in 0..100 {
        let mut positions: Vec<(i64, i64)> = Vec::new();
        for _ in 0..50 {
            let x = next_random(&mut seed) % 101;
            let y = next_random(&mut seed) % 101;
            positions.push((x, y));
        }
        let answer = get_min_dist_sum(&positions);
        check = (check * 31 + (answer * 100.0 + 0.5).floor() as i64 + 1) % 1000000007;
    }
    println!("100 sets of 50 customers on 0..100: checksum {}", check);
}
