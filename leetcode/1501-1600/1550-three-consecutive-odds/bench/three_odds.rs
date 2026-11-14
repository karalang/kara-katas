// LeetCode #1550: Three Consecutive Odds -- bench: the ★ arm (the run of
// odd values) over 1000 arrays of 1 to 1000 values, each with its own
// chance of an odd value, built once, each asked 2000 times with one value
// raised by one before every ask, so no ask repeats the last. Rust mirror
// of three_odds.kara.

fn three_consecutive_odds(arr: &[i64]) -> bool {
    let mut run = 0;
    for &x in arr {
        if x % 2 == 1 {
            run += 1;
            if run == 3 {
                return true;
            }
        } else {
            run = 0;
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1550i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..1000 {
        let length = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000 + 1;
        let odds = next_random(&mut seed) % 101;
        let mut arr = Vec::new();
        for _ in 0..length {
            let odd = next_random(&mut seed) % 100 < odds;
            let half = next_random(&mut seed) % 500;
            arr.push(if odd { 2 * half + 1 } else { 2 * half + 2 });
        }
        arrays.push(arr);
    }
    let mut yes = 0i64;
    let mut check = 0i64;
    for pass in 0..2000i64 {
        for g in 0..arrays.len() {
            let at = ((pass * 7 + g as i64) % arrays[g].len() as i64) as usize;
            arrays[g][at] += 1;
            if three_consecutive_odds(&arrays[g]) {
                yes += 1;
                check = (check * 31 + pass + g as i64 + 1) % 1000000007;
            }
        }
    }
    println!("2000 passes over 1000 arrays of up to 1000 values: {} true, checksum {}", yes, check);
}
