// LeetCode #1388 bench -- Rust: the ★ arm: the better of two straight
// runs, without the last slice and without the first; in each,
// best[i][j] is the most from at most j slices, no two adjacent, among
// the first i.

fn best_in_line(slices: &[i32], n: usize) -> i32 {
    let len = slices.len();
    let mut best = vec![vec![0i32; n + 1]; len + 1];
    for i in 1..len + 1 {
        for j in 1..n + 1 {
            let skip = best[i - 1][j];
            let take = if i >= 2 { best[i - 2][j - 1] } else { 0 } + slices[i - 1];
            best[i][j] = skip.max(take);
        }
    }
    best[len][n]
}

fn max_size_slices(slices: &[i32]) -> i32 {
    let n = slices.len() / 3;
    let len = slices.len();
    best_in_line(&slices[0..len - 1], n).max(best_in_line(&slices[1..len], n))
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let len: i64 = 498;
    let mut seed: i64 = 1388;
    let mut slices: Vec<i32> = Vec::new();
    for _ in 0..len {
        slices.push((1 + next_random(&mut seed) % 1000) as i32);
    }
    let mut check: i64 = 0;
    for _ in 0..1000 {
        seed = (seed + check) % 2147483648;
        let at = (next_random(&mut seed) % len) as usize;
        slices[at] = (1 + next_random(&mut seed) % 1000) as i32;
        check = (check * 131 + max_size_slices(&slices) as i64) % 1000000007;
    }
    println!("1000 rounds over 498 slices: checksum {}", check);
}
