// LeetCode #1446 Consecutive Characters: the bench, a mirror of
// max_power.kara.

fn max_power(s: &str) -> i32 {
    // the length of the run the letter so far ends, and the longest run
    let mut best: i32 = 0;
    let mut run: i32 = 0;
    let mut last = ' ';
    for ch in s.chars() {
        if ch == last {
            run += 1;
        } else {
            run = 1;
            last = ch;
        }
        best = best.max(run);
    }
    best
}

fn main() {
    // 200 strings of 10^5 letters, each drawn from the first 2 to 4 of the
    // alphabet, each string's power asked 10 times, the powers folded to a
    // checksum
    let mut seed: i64 = 1446;
    let mut strings: Vec<String> = Vec::new();
    for j in 0..200 {
        let k = 2 + j % 3;
        let mut s = String::new();
        for _ in 0..100000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            s.push((b'a' + (seed / 65536 % k) as u8) as char);
        }
        strings.push(s);
    }
    let mut check: i64 = 0;
    for _ in 0..10 {
        for s in strings.iter() {
            check = (check * 131 + max_power(s) as i64) % 1000000007;
        }
    }
    println!("2000 strings of 10^5 letters: checksum {}", check);
}
