// LeetCode #917: Reverse Only Letters -- bench: Rust mirror of the two
// pointers swapping letters in reverse_only_letters.kara.

fn is_letter(b: u8) -> bool {
    b.is_ascii_lowercase() || b.is_ascii_uppercase()
}

fn reverse_only_letters(s: &str) -> String {
    let mut bytes: Vec<u8> = s.bytes().collect();
    let mut i = 0;
    let mut j = bytes.len();
    while i < j {
        if !is_letter(bytes[i]) {
            i += 1;
        } else if !is_letter(bytes[j - 1]) {
            j -= 1;
        } else {
            bytes.swap(i, j - 1);
            i += 1;
            j -= 1;
        }
    }
    let mut out = String::new();
    for b in &bytes {
        out.push(*b as char);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_string(seed: &mut i64, letters: i64) -> String {
    let mut s = String::new();
    for _ in 0..100 {
        if next_random(seed) % 100 < letters {
            let k = next_random(seed) % 52;
            s.push(if k < 26 { (97 + k) as u8 as char } else { (65 + k - 26) as u8 as char });
        } else {
            let mut b = 34;
            while b == 34 || b == 92 {
                b = 33 + next_random(seed) % 90;
            }
            s.push(b as u8 as char);
        }
    }
    s
}

fn main() {
    let rounds = 1000;
    let n = 1000;
    let mut seed = 917;
    let mut pool: Vec<String> = Vec::new();
    for c in 0..n {
        pool.push(random_string(&mut seed, c % 101));
    }
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for s in &pool {
            let r = reverse_only_letters(s);
            let bytes = r.as_bytes();
            check = (check * 1000003 + bytes[0] as i64 * 256 + bytes[bytes.len() - 1] as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds over {n} strings of 100: checksum {check}");
}
