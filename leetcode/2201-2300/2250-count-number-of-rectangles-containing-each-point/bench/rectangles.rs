// LeetCode #2250: Count Number of Rectangles Containing Each Point -- the
// benchmark's Rust mirror of rectangles.kara: rectangles bucketed by
// height, each bucket's lengths sorted, a point summing over the buckets
// of height y to 100 how many lengths are at least x (`partition_point`).

fn count_rectangles(rectangles: &[[i64; 2]], points: &[[i64; 2]]) -> Vec<i64> {
    let mut by_height: Vec<Vec<i64>> = vec![Vec::new(); 101];
    for r in rectangles {
        by_height[r[1] as usize].push(r[0]);
    }
    for lengths in by_height.iter_mut() {
        lengths.sort();
    }
    let mut counts = Vec::new();
    for p in points {
        let mut count = 0i64;
        for h in p[1] as usize..101 {
            let lengths = &by_height[h];
            count += (lengths.len() - lengths.partition_point(|&l| l < p[0])) as i64;
        }
        counts.push(count);
    }
    counts
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2250i64;
    let mut check = 0i64;
    for _ in 0..4 {
        let rectangles: Vec<[i64; 2]> = (0..50000)
            .map(|_| {
                let l = wide_random(&mut seed) % 1000000000 + 1;
                let h = next_random(&mut seed) % 100 + 1;
                [l, h]
            })
            .collect();
        let points: Vec<[i64; 2]> = (0..50000)
            .map(|_| {
                let x = wide_random(&mut seed) % 1000000000 + 1;
                let y = next_random(&mut seed) % 100 + 1;
                [x, y]
            })
            .collect();
        for c in count_rectangles(&rectangles, &points) {
            check = (check * 31 + c) % 1000000007;
        }
    }
    println!("4 cases of 5 * 10^4 rectangles and points: checksum {}", check);
}
