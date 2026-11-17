// LeetCode #1183: Maximum Number of Ones -- the ★ arm in Rust: the cells
// on each position of the `side * side` square counted, sorted largest
// first, and the first `max_ones` summed.

fn maximum_number_of_ones(width: i64, height: i64, side_length: i64, max_ones: i64) -> i64 {
    let mut counts: Vec<i64> = Vec::new();
    for i in 0..side_length {
        for j in 0..side_length {
            let across = (width - i - 1) / side_length + 1;
            let down = (height - j - 1) / side_length + 1;
            counts.push(across * down);
        }
    }
    counts.sort_by(|a, b| b.cmp(a));
    counts.iter().take(max_ones as usize).sum()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1183;
    let mut cases: Vec<(i64, i64, i64, i64)> = Vec::new();
    for _ in 0..1000 {
        let width = 1 + next_random(&mut seed) % 100;
        let height = 1 + next_random(&mut seed) % 100;
        let side = 1 + next_random(&mut seed) % width.min(height);
        let max_ones = next_random(&mut seed) % (side * side + 1);
        cases.push((width, height, side, max_ones));
    }
    let rounds = 100;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &(width, height, side, max_ones) in cases.iter() {
            check = (check * 131 + maximum_number_of_ones(width, height, side, max_ones) + r) % 1000000007;
        }
    }
    println!("{rounds} rounds of 1000 cases: checksum {check}");
}
