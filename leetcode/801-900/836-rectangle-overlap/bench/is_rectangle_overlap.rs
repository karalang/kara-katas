// Benchmark for #836: Rectangle Overlap -- the ★ arm (the two projections).
//
// Mirrors is_rectangle_overlap.kara: two axis-aligned rectangles overlap
// with positive area exactly when their shadows on the x axis overlap in
// more than a point and so do their shadows on the y axis.

fn is_rectangle_overlap(rec1: &[i64], rec2: &[i64]) -> bool {
    let left = rec1[0].max(rec2[0]);
    let right = rec1[2].min(rec2[2]);
    let bottom = rec1[1].max(rec2[1]);
    let top = rec1[3].min(rec2[3]);
    left < right && bottom < top
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// a number below 2^32, from three draws
fn big_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed) * 32768 + next_random(seed);
    hi * 4 + next_random(seed) % 4
}

fn main() {
    // 4096 rectangles drawn once in LeetCode's range, their corners
    // anywhere and their sides up to 2 * 10^9 >> (k % 8) for rectangle k,
    // so they run from the size of the range down to a 128th of it.
    // Round s tests each rectangle i against rectangle (i + s + 1) % 4096.
    let n: i64 = 4096;
    let rounds: i64 = 100000;
    let mut seed: i64 = 836;
    let mut rects: Vec<Vec<i64>> = Vec::new();
    for k in 0..n {
        let reach = 2000000000i64 >> (k % 8);
        let x1 = big_random(&mut seed) % 2000000000 - 1000000000;
        let y1 = big_random(&mut seed) % 2000000000 - 1000000000;
        let x2 = (x1 + 1 + big_random(&mut seed) % reach).min(1000000000);
        let y2 = (y1 + 1 + big_random(&mut seed) % reach).min(1000000000);
        rects.push(vec![x1, y1, x2, y2]);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for s in 0..rounds {
        let mut overlapping = 0;
        for i in 0..n {
            if is_rectangle_overlap(&rects[i as usize], &rects[((i + s + 1) % n) as usize]) {
                overlapping += 1;
            }
        }
        total += overlapping;
        checksum = (checksum * 131 + overlapping) % 1000000007;
    }
    println!("{} rounds of {} pairs: {} overlapping, checksum {}", rounds, n, total, checksum);
}
