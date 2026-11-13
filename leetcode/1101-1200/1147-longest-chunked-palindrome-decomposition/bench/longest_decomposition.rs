// LeetCode #1147: Longest Chunked Palindrome Decomposition -- the Rust
// mirror of the ★ arm: greedy from both ends, the shortest equal chunks
// taken off, the middle one more.

fn longest_decomposition(text: &str) -> i64 {
    let t = text.as_bytes();
    let (mut i, mut j, mut k) = (0usize, t.len(), 0i64);
    while i < j {
        let mut size = 1;
        while 2 * size <= j - i && t[i..i + size] != t[j - size..j] {
            size += 1;
        }
        if 2 * size > j - i {
            return k + 1;
        }
        k += 2;
        i += size;
        j -= size;
    }
    k
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn text(seed: &mut i64) -> String {
    let size = (1 + next_random(seed) % 4) as usize;
    let mut unit: Vec<u8> = Vec::new();
    for _ in 0..size {
        unit.push(b'a' + (next_random(seed) % 2) as u8);
    }
    let mut b: Vec<u8> = (0..1000).map(|i| unit[i % size]).collect();
    let at = (next_random(seed) % 1000) as usize;
    b[at] = b'a' + (next_random(seed) % 2) as u8;
    String::from_utf8(b).unwrap()
}

fn main() {
    let mut seed = 1147;
    let mut texts: Vec<String> = (0..20).map(|_| text(&mut seed)).collect();
    let (mut total, mut check) = (0i64, 0i64);
    for r in 0..20000 {
        texts[r % 20] = text(&mut seed);
        for t in &texts {
            let k = longest_decomposition(t);
            total += k;
            check = (check * 31 + k) % 1000000007;
        }
    }
    println!("20000 rounds over 20 texts of 1000 letters: chunks total {total}, checksum {check}");
}
