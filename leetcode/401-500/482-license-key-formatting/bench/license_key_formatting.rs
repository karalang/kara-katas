// Benchmark for #482: Rust mirror of the ★ arm (back to front); see
// license_key_formatting.kara.

fn license_key_formatting(s: &str, k: i64) -> String {
    let mut backwards: Vec<char> = Vec::new();
    let mut in_group = 0;
    for c in s.chars().rev() {
        if c == '-' {
            continue;
        }
        if in_group == k {
            backwards.push('-');
            in_group = 0;
        }
        backwards.push(c.to_ascii_uppercase());
        in_group += 1;
    }
    backwards.reverse();
    let mut key = String::new();
    for c in backwards {
        key.push(c);
    }
    key
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let alphabet: Vec<char> = "abcxyzABCXYZ0189".chars().collect();
    let mut seed: i64 = 482;
    let mut s = String::new();
    for _ in 0..100000 {
        if next_random(&mut seed) % 4 == 0 {
            s.push('-');
        } else {
            s.push(alphabet[(next_random(&mut seed) % alphabet.len() as i64) as usize]);
        }
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for k in 1..501i64 {
        let key = license_key_formatting(&s, k);
        let bytes = key.as_bytes();
        let len = key.len() as i64;
        total += len;
        checksum = (checksum * 31 + len * 7 + bytes[key.len() / 2] as i64 + bytes[k as usize] as i64) % 1000000007;
    }
    println!("k = 1 to 500 on 100000 characters: keys add up to {total} characters, checksum {checksum}");
}
