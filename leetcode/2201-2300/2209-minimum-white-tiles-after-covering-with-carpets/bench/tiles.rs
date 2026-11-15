// benchmark's Rust mirror of tiles.kara (LeetCode #2209, the ★ arm): a
// table best[j][i], the fewest white tiles left visible among the first i
// tiles with j carpets, filled row by row.

fn minimum_white_tiles(floor: &str, num_carpets: usize, carpet_len: usize) -> i64 {
    let tiles: Vec<i64> = floor
        .chars()
        .map(|c| if c == '1' { 1 } else { 0 })
        .collect();
    let n = tiles.len();
    let mut best = vec![vec![0i64; n + 1]; num_carpets + 1];
    for j in 0..num_carpets + 1 {
        for i in 1..n + 1 {
            let left = best[j][i - 1] + tiles[i - 1];
            best[j][i] = if j == 0 {
                left
            } else {
                left.min(best[j - 1][i.saturating_sub(carpet_len)])
            };
        }
    }
    best[num_carpets][n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2209;
    let mut floors: Vec<String> = Vec::new();
    for f in 0..8 {
        let white_in_8 = f % 7 + 1;
        let mut floor = String::new();
        for _ in 0..1000 {
            floor.push(if next_random(&mut seed) % 8 < white_in_8 {
                '1'
            } else {
                '0'
            });
        }
        floors.push(floor);
    }
    // each floor asked 40 times, carpets 10 to 249, each 1 to 20 long
    let mut check: i64 = 0;
    for q in 0..40usize {
        for f in 0..8usize {
            let carpets = 10 + (q * 37 + f * 11) % 240;
            let len = 1 + (q * 7 + f * 3) % 20;
            check = (check * 31 + minimum_white_tiles(&floors[f], carpets, len)) % 1000000007;
        }
    }
    println!("40 passes over 8 floors: checksum {check}");
}
