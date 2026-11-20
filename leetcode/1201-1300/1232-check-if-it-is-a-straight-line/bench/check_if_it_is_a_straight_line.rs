// LeetCode #1232 bench: the ★ arm in Rust, over the same 1000 sets of 1000
// points and 200 passes as the Kāra bench.

fn check_straight_line(coordinates: &[Vec<i64>]) -> bool {
    let dx = coordinates[1][0] - coordinates[0][0];
    let dy = coordinates[1][1] - coordinates[0][1];
    for p in coordinates {
        if (p[0] - coordinates[0][0]) * dy != (p[1] - coordinates[0][1]) * dx {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1232;
    let mut sets: Vec<Vec<Vec<i64>>> = Vec::new();
    for s in 0..1000 {
        let mut dx = next_random(&mut seed) % 21 - 10;
        let dy = next_random(&mut seed) % 21 - 10;
        if dx == 0 && dy == 0 {
            dx = 1;
        }
        let mut pts: Vec<Vec<i64>> = (0..1000).map(|t| vec![t * dx, t * dy]).collect();
        if s % 2 == 1 {
            if dx == 0 {
                pts[999][0] += 1;
            } else {
                pts[999][1] += 1;
            }
        }
        sets.push(pts);
    }
    let mut straight = 0;
    for _ in 0..200 {
        for pts in &sets {
            if check_straight_line(pts) {
                straight += 1;
            }
        }
    }
    println!("1000 sets of 1000 points, 200 passes: {} straight", straight);
}
