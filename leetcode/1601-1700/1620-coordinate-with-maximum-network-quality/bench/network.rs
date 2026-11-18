// LeetCode #1620: Coordinate With Maximum Network Quality -- the bench in
// Rust, mirroring network.kara: every point, every tower, f64 distances.

fn best_coordinate(towers: &[Vec<i32>], radius: i32) -> Vec<i32> {
    let mut best = [0, 0];
    let mut most = 0;
    for x in 0i32..=50 {
        for y in 0i32..=50 {
            let mut quality = 0;
            for t in towers {
                let (dx, dy) = (t[0] - x, t[1] - y);
                let d = ((dx * dx + dy * dy) as f64).sqrt();
                if d <= radius as f64 {
                    quality += (t[2] as f64 / (1.0 + d)).floor() as i32;
                }
            }
            if quality > most {
                most = quality;
                best = [x, y];
            }
        }
    }
    best.to_vec()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1620;
    let mut cases: Vec<(Vec<Vec<i32>>, i32)> = Vec::new();
    for _ in 0..1000 {
        let towers: Vec<Vec<i32>> = (0..50)
            .map(|_| {
                let x = (next_random(&mut seed) % 51) as i32;
                let y = (next_random(&mut seed) % 51) as i32;
                let q = (next_random(&mut seed) % 51) as i32;
                vec![x, y, q]
            })
            .collect();
        let radius = (next_random(&mut seed) % 50 + 1) as i32;
        cases.push((towers, radius));
    }
    let mut check: i64 = 0;
    let mut spread: i64 = 0;
    for (towers, radius) in &cases {
        let best = best_coordinate(towers, *radius);
        spread += (best[0] + best[1]) as i64;
        check = (check * 31 + (best[0] * 51 + best[1]) as i64 + 1) % 1000000007;
    }
    println!("1000 cases of 50 towers: coordinates sum to {spread}, checksum {check}");
}
