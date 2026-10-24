// Benchmark: LeetCode #963 Minimum Area Rectangle II -- the ★ arm,
// diagonals grouped by centre, on 50 points, LeetCode's largest, packed
// into small grids so that many pairs share a centre and a length. Each
// call first moves one point to a free spot. Mirrors
// min_area_free_rect.kara, .c, .py and go-seq/.
use std::collections::HashMap;

fn min_area_free_rect(points: &[[i64; 2]]) -> f64 {
    let n = points.len();
    let mut groups: HashMap<(i64, i64, i64), Vec<(usize, usize)>> = HashMap::new();
    for i in 0..n {
        for j in i + 1..n {
            let dx = points[i][0] - points[j][0];
            let dy = points[i][1] - points[j][1];
            let key = (
                points[i][0] + points[j][0],
                points[i][1] + points[j][1],
                dx * dx + dy * dy,
            );
            groups.entry(key).or_default().push((i, j));
        }
    }
    let mut best = 0;
    for pairs in groups.values() {
        for x in 0..pairs.len() {
            for y in x + 1..pairs.len() {
                let (i, _) = pairs[x];
                let (k, l) = pairs[y];
                let ux = points[k][0] - points[i][0];
                let uy = points[k][1] - points[i][1];
                let vx = points[l][0] - points[i][0];
                let vy = points[l][1] - points[i][1];
                let area = (ux * vy - uy * vx).abs();
                if best == 0 || area < best {
                    best = area;
                }
            }
        }
    }
    best as f64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn has(points: &[[i64; 2]], x: i64, y: i64) -> bool {
    points.iter().any(|p| p[0] == x && p[1] == y)
}

fn packed(seed: &mut i64, n: usize, top: i64) -> Vec<[i64; 2]> {
    let mut out = Vec::new();
    while out.len() < n {
        let x = next_random(seed) % (top + 1);
        let y = next_random(seed) % (top + 1);
        if !has(&out, x, y) {
            out.push([x, y]);
        }
    }
    out
}

fn main() {
    let rounds = 40;
    let mut seed = 963;
    let mut cases: Vec<Vec<[i64; 2]>> =
        (0..50).map(|i| packed(&mut seed, 50, 7 + i % 10)).collect();
    let mut total = 0.0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..50 {
            let c = (r + i) % 50;
            let top = 7 + (c % 10) as i64;
            let p = (next_random(&mut seed) % 50) as usize;
            let x = next_random(&mut seed) % (top + 1);
            let y = next_random(&mut seed) % (top + 1);
            if !has(&cases[c], x, y) {
                cases[c][p] = [x, y];
            }
            let a = min_area_free_rect(&cases[c]);
            total += a;
            check = (check * 31 + a as i64 + i as i64) % 1000000007;
        }
    }
    println!(
        "{rounds} rounds over 50 cases of 50 points: the areas sum to {total:.5}, checksum {check}"
    );
}
