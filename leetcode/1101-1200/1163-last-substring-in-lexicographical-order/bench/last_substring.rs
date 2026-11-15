// LeetCode #1163: Last Substring in Lexicographical Order -- Rust mirror of
// the Kāra ★ arm: two pointers over the bytes, the answer copied out.

fn last_substring(s: &str) -> String {
    let b = s.as_bytes();
    let n = b.len();
    let (mut i, mut j, mut k) = (0, 1, 0);
    while j + k < n {
        if b[i + k] == b[j + k] {
            k += 1;
        } else if b[i + k] > b[j + k] {
            j = j + k + 1;
            k = 0;
        } else {
            i = (i + k + 1).max(j);
            j = i + 1;
            k = 0;
        }
    }
    s[i..].to_string()
}

fn main() {
    let mut seed: i64 = 1163;
    let mut next_random = move || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let n = 400000usize;
    let mut texts: Vec<String> = Vec::new();
    for k in 0..8 {
        let kind = k % 4;
        let block: Vec<u8> = (0..7).map(|_| b'a' + (next_random() % 26) as u8).collect();
        let b: Vec<u8> = (0..n)
            .map(|i| {
                if kind == 0 {
                    b'a' + (next_random() % 26) as u8
                } else if kind == 1 {
                    b'a' + (next_random() % 2) as u8
                } else if kind == 2 {
                    if next_random() % 1000 == 0 { b'a' + (next_random() % 26) as u8 } else { block[i % 7] }
                } else if next_random() % 10 == 0 {
                    b'y'
                } else {
                    b'z'
                }
            })
            .collect();
        texts.push(String::from_utf8(b).unwrap());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..150 {
        for t in texts.iter() {
            let from = (next_random() % (t.len() as i64 / 2)) as usize;
            let rest = &t[from..];
            let got = last_substring(rest);
            total += got.len() as i64;
            check = (check * 31 + (rest.len() - got.len()) as i64 * 7 + got.len() as i64) % 1000000007;
        }
    }
    println!("150 rounds over 8 strings of 4 * 10^5 letters: total {}, checksum {}", total, check);
}
