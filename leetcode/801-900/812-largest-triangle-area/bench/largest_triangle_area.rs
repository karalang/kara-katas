// LeetCode 812 -- Largest Triangle Area: the bench, with the ★ arm's
// every triple of points.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn largest_triangle_area(points: &[(i64, i64)]) -> f64 {
    let n = points.len();
    let mut best = 0;
    for i in 0..n {
        for j in i + 1..n {
            for k in j + 1..n {
                let twice = twice_area(points[i], points[j], points[k]);
                if twice > best {
                    best = twice;
                }
            }
        }
    }
    best as f64 / 2.0
}

fn twice_area(a: (i64, i64), b: (i64, i64), c: (i64, i64)) -> i64 {
    ((b.0 - a.0) * (c.1 - a.1) - (b.1 - a.1) * (c.0 - a.0)).abs()
}

// A point with coordinates from -50 to 50 that is not in `points`.
fn new_point(seed: &mut i64, points: &[(i64, i64)]) -> (i64, i64) {
    loop {
        let p = (next_random(seed) % 101 - 50, next_random(seed) % 101 - 50);
        if !points.contains(&p) {
            return p;
        }
    }
}

// 64 sets of 50 distinct points are made once. Each round moves one point
// of the next set to a new place and finds that set's largest triangle.
fn main() {
    let mut seed = 812;
    let mut sets: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..64 {
        let mut points = Vec::new();
        for _ in 0..50 {
            let p = new_point(&mut seed, &points);
            points.push(p);
        }
        sets.push(points);
    }
    let rounds: i64 = 60000;
    let mut total = 0.0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let k = (r % 64) as usize;
        let p = new_point(&mut seed, &sets[k]);
        sets[k][(r / 64 % 50) as usize] = p;
        let area = largest_triangle_area(&sets[k]);
        total += area;
        check = (check * 131 + (area * 2.0) as i64) % 1000000007;
    }
    println!("{} rounds of 50 points: total area {:.1}, checksum {}", rounds, total, check);
}
