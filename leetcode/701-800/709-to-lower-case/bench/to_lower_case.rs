// LeetCode #709: To Lower Case -- character by character.
// Benchmark mirror of the Kara star arm: copy each character into a new
// string, moving 'A' to 'Z' up by 32.

fn to_lower_case(s: &str) -> String {
    let mut out = String::new();
    for c in s.chars() {
        if ('A'..='Z').contains(&c) {
            out.push((c as u32 + 32) as u8 as char);
        } else {
            out.push(c);
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 709;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..10000 {
        let mut s = String::new();
        for _ in 0..100 {
            s.push((32 + next_random(&mut seed) % 95) as u8 as char);
        }
        strings.push(s);
    }
    let mut results: Vec<String> = strings.clone();
    let mut sum: i64 = 0;
    for round in 0..50 {
        for i in 0..10000 {
            results[i] = to_lower_case(&strings[i]);
            sum += results[i].as_bytes()[(round + i) % 100] as i64;
        }
    }
    for t in results.iter() {
        for b in t.bytes() {
            sum += b as i64;
        }
    }
    println!("50 rounds of 10000 strings of 100 characters: sum {}", sum);
}
