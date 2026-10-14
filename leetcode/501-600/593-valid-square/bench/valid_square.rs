// Benchmark for #593: Rust mirror of the ★ arm (the six distances,
// sorted); see valid_square.kara. The distances go into a fresh `Vec`
// each call, as the Kāra arm's do.

fn dist(a: &[i64], b: &[i64]) -> i64 {
    let dx = a[0] - b[0];
    let dy = a[1] - b[1];
    dx * dx + dy * dy
}

fn valid_square(p1: &[i64], p2: &[i64], p3: &[i64], p4: &[i64]) -> bool {
    let mut d = vec![dist(p1, p2), dist(p1, p3), dist(p1, p4), dist(p2, p3), dist(p2, p4), dist(p3, p4)];
    d.sort();
    d[0] > 0 && d[0] == d[3] && d[4] == d[5] && d[4] == 2 * d[0]
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_points(seed: &mut i64) -> Vec<Vec<i64>> {
    let kind = step(seed) % 3;
    let mut points: Vec<Vec<i64>> = Vec::new();
    if kind == 2 {
        for _ in 0..4 {
            let x = step(seed) % 7 - 3;
            let y = step(seed) % 7 - 3;
            points.push(vec![x, y]);
        }
        return points;
    }
    let x = step(seed) % 2001 - 1000;
    let y = step(seed) % 2001 - 1000;
    let mut dx = step(seed) % 41 - 20;
    let dy = step(seed) % 41 - 20;
    if dx == 0 && dy == 0 {
        dx = 1;
    }
    points.push(vec![x, y]);
    points.push(vec![x + dx, y + dy]);
    points.push(vec![x + dx - dy, y + dy + dx]);
    points.push(vec![x - dy, y + dx]);
    if kind == 1 {
        let k = (step(seed) % 4) as usize;
        let c = (step(seed) % 2) as usize;
        points[k][c] += if step(seed) % 2 == 0 { 1 } else { -1 };
    }
    for k in 0..3 {
        let j = k + (step(seed) % (4 - k as i64)) as usize;
        points.swap(k, j);
    }
    points
}

fn main() {
    let count = 1000;
    let rounds = 20000;
    let mut seed: i64 = 593;
    let mut cases: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        cases.push(random_points(&mut seed));
    }
    let mut squares = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let p = &cases[(round * 7 + g) % count];
            if valid_square(&p[0], &p[1], &p[2], &p[3]) {
                squares += 1;
                checksum = (checksum * 31 + g as i64 + 1) % 1000000007;
            }
        }
    }
    println!("{} cases, {} rounds: {} squares, checksum {}", count, rounds, squares, checksum);
}
