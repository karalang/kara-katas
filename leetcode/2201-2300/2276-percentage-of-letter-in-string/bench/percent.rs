// LeetCode #2276: Percentage of Letter in String -- the bench, the ★ arm.

fn percentage_letter(s: &str, letter: char) -> i64 {
    let mut count = 0;
    for c in s.chars() {
        if c == letter {
            count += 1;
        }
    }
    count * 100 / s.len() as i64
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2276;
    let mut check = 0;
    for _ in 0..100000 {
        let mut s = String::new();
        for _ in 0..100 {
            s.push((b'a' + (next_random(&mut seed) % 4) as u8) as char);
        }
        let letter = (b'a' + (next_random(&mut seed) % 4) as u8) as char;
        check = (check * 31 + percentage_letter(&s, letter)) % 1000000007;
    }
    println!("100000 strings of 100: checksum {check}");
}
