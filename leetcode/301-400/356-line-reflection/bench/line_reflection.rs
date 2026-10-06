// Benchmark for #356 -- same workload and algorithm as line_reflection.kara.
use std::collections::HashSet;

fn is_reflected(points: &[(i64, i64)]) -> bool {
    if points.is_empty() {
        return true;
    }
    let mut lo = points[0].0;
    let mut hi = points[0].0;
    let mut seen: HashSet<(i64, i64)> = HashSet::new();
    for &(x, y) in points {
        lo = lo.min(x);
        hi = hi.max(x);
        seen.insert((x, y));
    }
    let sum = lo + hi;
    for &(x, y) in points {
        if !seen.contains(&(sum - x, y)) {
            return false;
        }
    }
    true
}

fn main() {
    let mut seed: i64 = 356;
    let mut yes = 0;
    let mut checksum: i64 = 0;
    for round in 0..400 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let center2 = (seed / 16) % 2000001 - 1000000;
        let mut points: Vec<(i64, i64)> = Vec::with_capacity(5000);
        for _ in 0..2500 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let x = (seed / 16) % 2000001 - 1000000;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let y = (seed / 65536) % 1000;
            points.push((x, y));
            points.push((center2 - x, y));
        }
        if round % 3 == 0 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let i = ((seed / 65536) % points.len() as i64) as usize;
            points[i] = (points[i].0 + 1, points[i].1);
        }
        let r = is_reflected(&points);
        if r {
            yes += 1;
        }
        checksum = (checksum * 3 + if r { 1 } else { 2 }) % 1000000007;
    }
    println!("{} of 400 sets reflect, checksum {}", yes, checksum);
}
