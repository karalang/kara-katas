// LeetCode #880 bench: Rust mirror of decode_at_index.kara (the ★ arm, the
// tape's length, then back from the end) on the same 1,000,000 queries.

fn decode_at_index(s: &str, k: i64) -> String {
    let bytes = s.as_bytes();
    let mut size: i64 = 0;
    for &b in bytes {
        if b.is_ascii_digit() {
            size *= (b - b'0') as i64;
        } else {
            size += 1;
        }
    }
    let mut k = k;
    let mut i = bytes.len() - 1;
    loop {
        k %= size;
        if k == 0 && !bytes[i].is_ascii_digit() {
            return s[i..i + 1].to_string();
        }
        if bytes[i].is_ascii_digit() {
            size /= (bytes[i] - b'0') as i64;
        } else {
            size -= 1;
        }
        i -= 1;
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn up_to(seed: &mut i64, limit: i64) -> i64 {
    let x = next_random(seed);
    let y = next_random(seed);
    (x * 32768 + y) % limit + 1
}

fn encoded(seed: &mut i64, length: i64) -> (String, i64) {
    let letters = b"abcdefghijklmnopqrstuvwxyz";
    let bound: i64 = 1000000000000000000;
    let mut s = String::new();
    let mut size: i64 = 0;
    for i in 0..length {
        let d = next_random(seed) % 8 + 2;
        if i > 0 && next_random(seed) % 3 == 0 && size * d <= bound {
            s.push((b'0' + d as u8) as char);
            size *= d;
        } else if size < bound {
            let x = next_random(seed) % 26;
            s.push(letters[x as usize] as char);
            size += 1;
        }
    }
    (s, size)
}

fn main() {
    let mut seed = 880;
    let mut strings: Vec<String> = Vec::new();
    let mut sizes: Vec<i64> = Vec::new();
    for _ in 0..1000 {
        let length = next_random(&mut seed) % 99 + 2;
        let (s, size) = encoded(&mut seed, length);
        strings.push(s);
        sizes.push(size);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for q in 0..1000000 {
        let j = q % 1000;
        let k = up_to(&mut seed, sizes[j].min(1000000000));
        let answer = decode_at_index(&strings[j], k).as_bytes()[0] as i64;
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    println!("1000000 queries over 1000 strings: letters sum to {}, checksum {}", total, check);
}
