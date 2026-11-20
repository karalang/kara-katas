// LeetCode #1240: the benchmark, mirroring the Kāra file.

fn fill(heights: &mut Vec<i64>, n: i64, count: i64, best: &mut i64) {
    if count >= *best {
        return;
    }
    let mut at = 0;
    for j in 1..heights.len() {
        if heights[j] < heights[at] {
            at = j;
        }
    }
    let base = heights[at];
    if base == n {
        *best = count;
        return;
    }
    let mut width: i64 = 0;
    while at + (width as usize) < heights.len() && heights[at + width as usize] == base && width < n - base {
        width += 1;
    }
    for size in (1..=width).rev() {
        for j in at..at + size as usize {
            heights[j] = base + size;
        }
        fill(heights, n, count + 1, best);
        for j in at..at + size as usize {
            heights[j] = base;
        }
    }
}

fn tiling_rectangle(n: i64, m: i64) -> i64 {
    let mut heights = vec![0i64; m as usize];
    let mut best = n * m;
    fill(&mut heights, n, 0, &mut best);
    best
}

fn main() {
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..200 {
        for n in 1..=13 {
            for m in 1..=13 {
                let t = tiling_rectangle(n, m);
                total += t;
                check = (check * 131 + t) % 1000000007;
            }
        }
    }
    println!("169 rectangles, 200 passes: total {}, checksum {}", total, check);
}
