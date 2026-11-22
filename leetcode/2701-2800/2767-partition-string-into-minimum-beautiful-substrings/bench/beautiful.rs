// LeetCode #2767: Partition String Into Minimum Beautiful Substrings --
// the bench in Rust: the ★ arm over 100000 strings of 15 binary digits,
// all drawn first, then each answered 5 times.

fn is_power_of_five(v: i64) -> bool {
    let mut v = v;
    while v > 1 && v % 5 == 0 {
        v /= 5;
    }
    v == 1
}

fn minimum_beautiful_substrings(s: &str) -> i64 {
    let n = s.len();
    let mut best = vec![-1i64; n + 1];
    best[0] = 0;
    for i in 1..=n {
        for j in 0..i {
            if best[j] < 0 || &s[j..j + 1] != "1" {
                continue;
            }
            let value = i64::from_str_radix(&s[j..i], 2).unwrap();
            if is_power_of_five(value) && (best[i] < 0 || best[j] + 1 < best[i]) {
                best[i] = best[j] + 1;
            }
        }
    }
    best[n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100000;
    let rounds = 5;
    let powers = ["1", "101", "11001", "1111101", "1001110001", "110000110101", "11110100001001"];
    let mut seed: i64 = 2767;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        let mut s = String::new();
        loop {
            let p = powers[(next_random(&mut seed) % 7) as usize];
            if s.len() + p.len() > 15 {
                break;
            }
            s.push_str(p);
        }
        while s.len() < 15 {
            s.push_str(if next_random(&mut seed) % 2 == 1 { "1" } else { "0" });
        }
        if next_random(&mut seed) % 2 == 1 {
            let k = (next_random(&mut seed) % 15) as usize;
            let flipped = if &s[k..k + 1] == "1" { "0" } else { "1" };
            s = format!("{}{}{}", &s[..k], flipped, &s[k + 1..]);
        }
        strings.push(s);
    }
    let mut split: i64 = 0;
    let mut pieces: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for s in strings.iter() {
            let a = minimum_beautiful_substrings(s);
            if a > 0 {
                split += 1;
                pieces += a;
            }
            check = (check * 31 + a + 1 + r) % 1000000007;
        }
    }
    println!("{} strings of 15, {} rounds: {} split, pieces sum to {}, checksum {}", count, rounds, split, pieces, check);
}
