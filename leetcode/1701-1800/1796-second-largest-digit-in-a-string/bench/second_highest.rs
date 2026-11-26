// LeetCode #1796: Second Largest Digit in a String -- the bench in Rust: the
// ★ arm over 1000 random strings of 100 characters built once, 1000000
// calls.

fn second_highest(s: &str) -> i32 {
    let mut first = -1;
    let mut second = -1;
    for c in s.chars() {
        if let Some(d) = c.to_digit(10) {
            let d = d as i32;
            if d > first {
                second = first;
                first = d;
            } else if d < first && d > second {
                second = d;
            }
        }
    }
    second
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1796;
    let letters: Vec<char> = "abcdef".chars().collect();
    let mut texts: Vec<String> = Vec::new();
    for _ in 0..1000 {
        let digits = 1 + next_random(&mut seed) % 9;
        let mut s = String::new();
        for _ in 0..100 {
            if next_random(&mut seed) % 10 < digits {
                s.push(char::from_digit((next_random(&mut seed) % 10) as u32, 10).unwrap());
            } else {
                s.push(letters[(next_random(&mut seed) % 6) as usize]);
            }
        }
        texts.push(s);
    }
    let mut check: i64 = 0;
    for call in 0..1000000i64 {
        let s = &texts[((check + call) % 1000) as usize];
        check = (check * 31 + second_highest(s) as i64 + 1) % 1000000007;
    }
    println!("1000000 calls over 1000 strings: checksum {}", check);
}
