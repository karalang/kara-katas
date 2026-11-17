// LeetCode #2220: Minimum Bit Flips to Convert Number -- bench mirror of
// flips.kara: the 1 bits of start ^ goal, counted by clearing the lowest
// with x & (x - 1).

fn min_bit_flips(start: i64, goal: i64) -> i64 {
    let mut differ = start ^ goal;
    let mut flips = 0;
    while differ != 0 {
        differ &= differ - 1;
        flips += 1;
    }
    flips
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// a draw of 30 bits, since one draw stops at 32767
fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2220;
    // 10^5 pairs up to 10^9
    let mut starts: Vec<i64> = Vec::new();
    let mut goals: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        starts.push(wide_random(&mut seed) % 1000000001);
        goals.push(wide_random(&mut seed) % 1000000001);
    }
    let mut check: i64 = 0;
    for r in 0..50 {
        // punch: one goal is drawn again before each round
        goals[r * 1999] = wide_random(&mut seed) % 1000000001;
        let mut total = 0;
        for i in 0..100000 {
            total += min_bit_flips(starts[i], goals[i]);
        }
        check = (check * 31 + total) % 1000000007;
    }
    println!("10^5 pairs, 50 punches: checksum {check}");
}
