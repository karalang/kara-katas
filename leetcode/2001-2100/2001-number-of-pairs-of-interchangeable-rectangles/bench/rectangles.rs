// LeetCode #2001: Number of Pairs of Interchangeable Rectangles -- the
// benchmark, the same algorithm as rectangles.kara.
use std::collections::HashMap;

fn gcd(a: i64, b: i64) -> i64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn interchangeable(rectangles: &[(i64, i64)]) -> i64 {
    let mut seen: HashMap<(i64, i64), i64> = HashMap::new();
    let mut pairs = 0;
    for &(w, h) in rectangles {
        let g = gcd(w, h);
        let key = (w / g, h / g);
        let before = *seen.get(&key).unwrap_or(&0);
        pairs += before;
        seen.insert(key, before + 1);
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 2001;
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for a in 0..20 {
        let shapes = [10i64, 100, 1000, 10000][a % 4];
        let mut bases: Vec<(i64, i64)> = Vec::new();
        for _ in 0..shapes {
            let w = next_random(&mut seed) % 300 + 1;
            let h = next_random(&mut seed) % 300 + 1;
            bases.push((w, h));
        }
        let mut rects: Vec<(i64, i64)> = Vec::new();
        for _ in 0..100000 {
            let (w, h) = bases[(next_random(&mut seed) % shapes) as usize];
            let m = next_random(&mut seed) % (100000 / w.max(h)) + 1;
            rects.push((w * m, h * m));
        }
        for _ in 0..10 {
            let answer = interchangeable(&rects);
            sum += answer;
            check = (check * 31 + answer % 1000003) % 1000000007;
            calls += 1;
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
