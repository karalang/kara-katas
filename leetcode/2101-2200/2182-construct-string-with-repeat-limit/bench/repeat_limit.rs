// LeetCode #2182: Construct String With Repeat Limit -- the benchmark's
// Rust mirror of repeat_limit.kara, over a string slice.

fn repeat_limited_string(s: &str, repeat_limit: i64) -> String {
    let mut counts = [0i64; 26];
    for b in s.bytes() {
        counts[(b - 97) as usize] += 1;
    }
    let mut out = String::new();
    let mut big: i64 = 25;
    loop {
        while big >= 0 && counts[big as usize] == 0 {
            big -= 1;
        }
        if big < 0 {
            break;
        }
        let take = counts[big as usize].min(repeat_limit);
        for _ in 0..take {
            out.push((97 + big) as u8 as char);
        }
        counts[big as usize] -= take;
        if counts[big as usize] == 0 {
            continue;
        }
        let mut small = big - 1;
        while small >= 0 && counts[small as usize] == 0 {
            small -= 1;
        }
        if small < 0 {
            break;
        }
        out.push((97 + small) as u8 as char);
        counts[small as usize] -= 1;
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2182i64;
    let mut row = String::new();
    for _ in 0..1000000 {
        row.push((97 + next_random(&mut seed) % 26) as u8 as char);
    }
    let mut check = 0i64;
    for _ in 0..400 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let start = ((a * 32768 + b) % 900001) as usize;
        let k = next_random(&mut seed) % 3 + 1;
        let t = repeat_limited_string(&row[start..start + 100000], k);
        for c in t.bytes() {
            check = (check * 31 + c as i64) % 1000000007;
        }
    }
    println!("400 solves: checksum {}", check);
}
