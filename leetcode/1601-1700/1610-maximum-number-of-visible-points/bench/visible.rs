// LeetCode #1610: Maximum Number of Visible Points -- the bench in Rust,
// mirroring visible.kara: each direction in degrees by `atan2` and
// `to_degrees`, sorted by `total_cmp` and doubled with 360 more, and a
// window slid along it.

fn visible_points(points: &[Vec<i32>], angle: i32, location: &[i32]) -> i32 {
    let mut here = 0;
    let mut dirs: Vec<f64> = Vec::new();
    for p in points {
        let (dx, dy) = (p[0] - location[0], p[1] - location[1]);
        if dx == 0 && dy == 0 {
            here += 1;
        } else {
            dirs.push((dy as f64).atan2(dx as f64).to_degrees());
        }
    }
    dirs.sort_by(f64::total_cmp);
    let m = dirs.len();
    for i in 0..m {
        dirs.push(dirs[i] + 360.0);
    }
    let reach = angle as f64 + 1e-9;
    let mut best = 0;
    let mut j = 0;
    for i in 0..dirs.len() {
        while dirs[i] - dirs[j] > reach {
            j += 1;
        }
        best = best.max(i - j + 1);
    }
    best as i32 + here
}

fn main() {
    let mut seed: i64 = 1610;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut problems = Vec::new();
    for _ in 0..20 {
        let mut points = Vec::with_capacity(100000);
        for _ in 0..100000 {
            let x = (next_random() % 101) as i32;
            let y = (next_random() % 101) as i32;
            points.push(vec![x, y]);
        }
        let angle = (next_random() % 360) as i32;
        let lx = (next_random() % 101) as i32;
        let ly = (next_random() % 101) as i32;
        problems.push((points, angle, vec![lx, ly]));
    }
    let mut check: i64 = 0;
    let mut visible: i64 = 0;
    for (points, angle, location) in &problems {
        let v = visible_points(points, *angle, location) as i64;
        check = (check * 31 + v + 1) % 1000000007;
        visible += v;
    }
    println!("20 problems of 100000 points from 0 to 100: {visible} visible, checksum {check}");
}
