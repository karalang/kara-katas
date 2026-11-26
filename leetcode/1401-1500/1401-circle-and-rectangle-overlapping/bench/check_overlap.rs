// LeetCode #1401 bench, Rust: the same clamp and squared distance,
// workload and checksum as check_overlap.kara.

fn check_overlap(radius: i32, x_center: i32, y_center: i32, x1: i32, y1: i32, x2: i32, y2: i32) -> bool {
    let dx = x_center.clamp(x1, x2) - x_center;
    let dy = y_center.clamp(y1, y2) - y_center;
    dx * dx + dy * dy <= radius * radius
}

fn main() {
    let mut seed: i64 = 1401;
    let mut cases: Vec<Vec<i32>> = Vec::new();
    for _ in 0..100000 {
        let mut v: Vec<i32> = Vec::new();
        for _ in 0..5 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            v.push((seed % 2001 - 1000) as i32);
        }
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let w = (1 + seed % 300) as i32;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let h = (1 + seed % 300) as i32;
        v[0] = v[0].abs() / 10 + 1;
        let (a, b) = (v[3] + w, v[4] + h);
        v.push(a);
        v.push(b);
        cases.push(v);
    }
    let mut check: i64 = 0;
    for round in 0..1000i32 {
        let mut overlaps: i64 = 0;
        for c in cases.iter() {
            if check_overlap(c[0] + round, c[1], c[2], c[3], c[4], c[5], c[6]) {
                overlaps += 1;
            }
        }
        check = (check * 131 + overlaps) % 1000000007;
    }
    println!("1000 rounds over 10^5 circles and rectangles: checksum {}", check);
}
