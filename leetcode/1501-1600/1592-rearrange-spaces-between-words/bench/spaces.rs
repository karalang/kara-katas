// LeetCode #1592: Rearrange Spaces Between Words -- the bench in Rust,
// mirroring spaces.kara.

fn reorder_spaces(text: &str) -> String {
    let words: Vec<&str> = text.split_whitespace().collect();
    let spaces = text.bytes().filter(|&c| c == b' ').count();
    let gaps = words.len() - 1;
    if gaps == 0 {
        return format!("{}{}", words[0], " ".repeat(spaces));
    }
    let between = " ".repeat(spaces / gaps);
    format!("{}{}", words.join(&between), " ".repeat(spaces % gaps))
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw(n: i64, seed: &mut i64) -> String {
    let mut b: Vec<u8> = (0..n)
        .map(|_| {
            let r = next_random(seed) % 6;
            if r < 2 { b' ' } else { b'a' + ((r - 2) as u8) % 3 }
        })
        .collect();
    let hi = next_random(seed);
    let at = (hi * 32768 + next_random(seed)) % n;
    b[at as usize] = b'a';
    String::from_utf8(b).unwrap()
}

fn main() {
    let mut seed = 1592;
    let texts: Vec<String> = (0..200).map(|_| draw(100000, &mut seed)).collect();
    let mut check: i64 = 0;
    let mut trailing = 0;
    for text in &texts {
        let answer = reorder_spaces(text);
        trailing += answer.len() - answer.trim_end().len();
        for &c in answer.as_bytes() {
            check = (check * 31 + c as i64 + 1) % 1000000007;
        }
    }
    println!("200 texts of 100000 characters: {} trailing spaces, checksum {}", trailing, check);
}
