// LeetCode #1499: Max Value of Equation -- the bench in Rust, mirroring
// find_max_value_of_equation.kara: a window of (y - x, x) kept largest first.
use std::collections::VecDeque;

fn find_max_value_of_equation(points: &[Vec<i32>], k: i32) -> i32 {
    let mut window: VecDeque<(i32, i32)> = VecDeque::new();
    let mut best = i32::MIN;
    for p in points.iter() {
        let (x, y) = (p[0], p[1]);
        while window.front().is_some_and(|f| x - f.1 > k) {
            window.pop_front();
        }
        if let Some(f) = window.front() {
            best = best.max(f.0 + y + x);
        }
        while window.back().is_some_and(|b| b.0 <= y - x) {
            window.pop_back();
        }
        window.push_back((y - x, x));
    }
    best
}

fn main() {
    let mut seed: i64 = 1499;
    let mut points: Vec<Vec<i32>> = Vec::new();
    let mut x: i64 = 0;
    for _ in 0..200000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        x += 1 + seed / 65536 % 10;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let y = seed / 65536 * 6151 % 200000001 - 100000000;
        points.push(vec![x as i32, y as i32]);
    }
    let mut check: i64 = 0;
    for call in 0..400i64 {
        let at = ((check + call * 7919) % 200000) as usize;
        points[at][1] = ((check * 17 + call) % 200000001 - 100000000) as i32;
        let k = 10 + (check + call) % 2000;
        check = (check * 31 + find_max_value_of_equation(&points, k as i32) as i64 + 300000000) % 1000000007;
    }
    println!("400 calls over 200000 points: checksum {}", check);
}
