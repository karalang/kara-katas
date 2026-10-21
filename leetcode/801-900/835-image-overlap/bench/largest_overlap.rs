// Benchmark for #835: Image Overlap -- the ★ arm (shifts counted over pairs of ones).
//
// Mirrors largest_overlap.kara: every pair of a one in the first image and
// a one in the second votes for the shift that lays the first on the
// second, and the shift with the most votes is the answer.

fn largest_overlap(img1: &[Vec<i64>], img2: &[Vec<i64>]) -> i64 {
    let n = img1.len() as i64;
    let mut ones1: Vec<(i64, i64)> = Vec::new();
    let mut ones2: Vec<(i64, i64)> = Vec::new();
    for r in 0..n {
        for c in 0..n {
            if img1[r as usize][c as usize] == 1 {
                ones1.push((r, c));
            }
            if img2[r as usize][c as usize] == 1 {
                ones2.push((r, c));
            }
        }
    }
    let width = 2 * n - 1;
    let mut votes = vec![0i64; (width * width) as usize];
    let mut best = 0;
    for &(r1, c1) in &ones1 {
        for &(r2, c2) in &ones2 {
            let k = ((r2 - r1 + n - 1) * width + (c2 - c1 + n - 1)) as usize;
            votes[k] += 1;
            if votes[k] > best {
                best = votes[k];
            }
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 64 pairs of images drawn once, each of LeetCode's largest size, 30
    // by 30, the share of ones running from 2% to 98% over the pairs, the
    // two images of pair k at 2k and 2k + 1 in one list. Each round solves
    // the next pair.
    let count: i64 = 64;
    let rounds: i64 = 4000;
    let n: i64 = 30;
    let mut seed: i64 = 835;
    let mut images: Vec<Vec<Vec<i64>>> = Vec::new();
    for g in 0..count {
        let percent = 2 + g * 96 / (count - 1);
        for _ in 0..2 {
            let mut img: Vec<Vec<i64>> = Vec::new();
            for _ in 0..n {
                let mut row: Vec<i64> = Vec::new();
                for _ in 0..n {
                    row.push(if next_random(&mut seed) % 100 < percent { 1 } else { 0 });
                }
                img.push(row);
            }
            images.push(img);
        }
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let k = (round % count) as usize;
        let x = largest_overlap(&images[2 * k], &images[2 * k + 1]);
        total += x;
        checksum = (checksum * 131 + x) % 1000000007;
    }
    println!("{} rounds of {} pairs: overlaps total {}, checksum {}", rounds, count, total, checksum);
}
