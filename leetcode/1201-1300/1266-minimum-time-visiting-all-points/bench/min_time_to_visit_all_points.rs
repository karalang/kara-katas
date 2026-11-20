// LeetCode #1266 bench, in Rust: the ★ arm (the larger of the two gaps
// between neighbouring points, summed over `windows(2)`) on 1000 random
// walks of 100 points from -1000 to 1000 built once, 3000 rounds; every
// answer folded into a checksum.

fn min_time_to_visit_all_points(points: &[Vec<i64>]) -> i64 {
    points
        .windows(2)
        .map(|w| (w[1][0] - w[0][0]).abs().max((w[1][1] - w[0][1]).abs()))
        .sum()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1266i64;
    let walks: Vec<Vec<Vec<i64>>> = (0..1000)
        .map(|_| {
            (0..100)
                .map(|_| {
                    let x = next_random(&mut seed) % 2001 - 1000;
                    let y = next_random(&mut seed) % 2001 - 1000;
                    vec![x, y]
                })
                .collect()
        })
        .collect();
    let mut check: i64 = 0;
    for round in 0..3000 {
        for w in &walks {
            check = (check * 131 + min_time_to_visit_all_points(w) + round) % 1000000007;
        }
    }
    println!("3000 rounds of 1000 walks of 100 points: checksum {}", check);
}
