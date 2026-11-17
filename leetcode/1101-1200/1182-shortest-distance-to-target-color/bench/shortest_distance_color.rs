// LeetCode #1182: Shortest Distance to Target Color -- the ★ arm in Rust: a
// nearest-distance table per colour, filled from each side, then a lookup a
// query.

fn shortest_distance_color(colors: &[i64], queries: &[Vec<i64>]) -> Vec<i64> {
    let n = colors.len() as i64;
    let far = n + 1;
    let mut nearest: Vec<Vec<i64>> = Vec::new();
    for c in 1..=3 {
        let mut dist = vec![far; n as usize];
        let mut last: i64 = -1;
        for i in 0..n {
            if colors[i as usize] == c {
                last = i;
            }
            if last >= 0 {
                dist[i as usize] = i - last;
            }
        }
        last = -1;
        for i in (0..n).rev() {
            if colors[i as usize] == c {
                last = i;
            }
            if last >= 0 && last - i < dist[i as usize] {
                dist[i as usize] = last - i;
            }
        }
        nearest.push(dist);
    }
    let mut answer = Vec::new();
    for q in queries.iter() {
        let d = nearest[(q[1] - 1) as usize][q[0] as usize];
        answer.push(if d == far { -1 } else { d });
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1182;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut asks: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..4 {
        let colors: Vec<i64> = (0..50000)
            .map(|_| if next_random(&mut seed) % 997 == 0 { 3 } else { 1 + next_random(&mut seed) % 2 })
            .collect();
        arrays.push(colors);
        let queries: Vec<Vec<i64>> = (0..50000)
            .map(|_| {
                let i = next_random(&mut seed) % 50000;
                vec![i, 1 + next_random(&mut seed) % 3]
            })
            .collect();
        asks.push(queries);
    }
    let rounds = 40;
    let mut check: i64 = 0;
    for round in 0..rounds {
        for a in 0..4 {
            for d in shortest_distance_color(&arrays[a], &asks[a]) {
                check = (check * 131 + d + 2 + round) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds of 4 arrays of 50000 queries: checksum {check}");
}
