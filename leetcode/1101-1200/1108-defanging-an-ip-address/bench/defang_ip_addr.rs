// LeetCode #1108: Defanging an IP Address -- the bench in Rust: the ★ arm
// (one pass, each period written as `[.]`) over 1024 random addresses,
// each round replacing one address with a new one and defanging every
// address again.

fn defang_ip_addr(address: &str) -> String {
    let mut out = String::with_capacity(address.len() + 6);
    for c in address.chars() {
        if c == '.' {
            out.push_str("[.]");
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

fn random_address(seed: &mut i64) -> String {
    let a = next_random(seed) % 256;
    let b = next_random(seed) % 256;
    let c = next_random(seed) % 256;
    let d = next_random(seed) % 256;
    format!("{}.{}.{}.{}", a, b, c, d)
}

fn main() {
    let mut seed = 1108;
    let mut addresses: Vec<String> = (0..1024).map(|_| random_address(&mut seed)).collect();
    let mut length = 0;
    let mut check: i64 = 0;
    let mut calls: i64 = 0;
    for round in 0..10000usize {
        addresses[(round * 7919) % 1024] = random_address(&mut seed);
        for a in addresses.iter() {
            let d = defang_ip_addr(a);
            length += d.len();
            if calls % 64 == 0 {
                for c in d.chars() {
                    check = (check * 31 + c as i64) % 1000000007;
                }
            }
            calls += 1;
        }
    }
    println!("10000 rounds over 1024 addresses: {} calls, {} characters, checksum {}", calls, length, check);
}
