// LeetCode #1575: Count All Possible Routes -- bench: the ★ arm (routes to
// the finish filled from no fuel up) over 100 problems of 60 distinct
// locations below 300 and a fuel of 200, every problem drawn first.

fn count_routes(locations: &[i64], start: usize, finish: usize, fuel: usize) -> i64 {
    let m = 1000000007;
    let n = locations.len();
    let mut ways = vec![vec![0i64; n]; fuel + 1];
    for f in 0..fuel + 1 {
        for c in 0..n {
            let mut total = if c == finish { 1 } else { 0 };
            for d in 0..n {
                let cost = (locations[c] - locations[d]).unsigned_abs() as usize;
                if d != c && cost <= f {
                    total = (total + ways[f - cost][d]) % m;
                }
            }
            ways[f][c] = total;
        }
    }
    ways[fuel][start]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let n = 60;
    let mut seed = 1575;
    let mut problems: Vec<(Vec<i64>, usize, usize)> = Vec::new();
    for _ in 0..100 {
        let mut locations: Vec<i64> = Vec::new();
        while locations.len() < n {
            let x = next_random(&mut seed) % 300;
            if !locations.contains(&x) {
                locations.push(x);
            }
        }
        let start = (next_random(&mut seed) % n as i64) as usize;
        let finish = (next_random(&mut seed) % n as i64) as usize;
        problems.push((locations, start, finish));
    }
    let (mut check, mut total) = (0i64, 0i64);
    for (locations, start, finish) in &problems {
        let routes = count_routes(locations, *start, *finish, 200);
        total += routes;
        check = mix(check, routes);
    }
    println!("100 problems of {} locations and fuel 200: routes total {}, checksum {}", n, total, check);
}
