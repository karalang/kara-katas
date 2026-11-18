// LeetCode #2271: Maximum White Tiles Covered by a Carpet -- the bench,
// the ★ arm.

fn maximum_white_tiles(tiles: &Vec<Vec<i64>>, carpet_len: i64) -> i64 {
    let mut sorted = tiles.clone();
    sorted.sort();
    let m = sorted.len();
    let mut best = 0;
    let mut whole = 0;
    let mut j = 0;
    for i in 0..m {
        let end = sorted[i][0] + carpet_len - 1;
        while j < m && sorted[j][1] <= end {
            whole += sorted[j][1] - sorted[j][0] + 1;
            j += 1;
        }
        let part = if j < m && sorted[j][0] <= end { end - sorted[j][0] + 1 } else { 0 };
        best = best.max(whole + part);
        if j > i {
            whole -= sorted[i][1] - sorted[i][0] + 1;
        } else {
            j = i + 1;
        }
    }
    best
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2271;
    let mut check = 0;
    for t in 0..30 {
        let mut tiles: Vec<Vec<i64>> = Vec::new();
        let mut at = 1;
        for _ in 0..50000 {
            at += next_random(&mut seed) % 10001;
            let end = at + next_random(&mut seed) % 10000;
            tiles.push(vec![at, end]);
            at = end + 1;
        }
        for i in (1..50000usize).rev() {
            let k = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            tiles.swap(i, k);
        }
        let carpet_len = [1000, 1000000, 1000000000][t % 3];
        check = (check * 31 + maximum_white_tiles(&tiles, carpet_len)) % 1000000007;
    }
    println!("30 sets of 5 * 10^4: checksum {check}");
}
