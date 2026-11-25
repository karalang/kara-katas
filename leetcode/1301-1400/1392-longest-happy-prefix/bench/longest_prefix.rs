// LeetCode #1392 bench, Rust mirror of the ★ arm.

fn longest_prefix(s: String) -> String {
    let b = s.as_bytes();
    let n = b.len();
    let mut border: Vec<usize> = vec![0; n];
    let mut k = 0;
    for i in 1..n {
        while k > 0 && b[i] != b[k] {
            k = border[k - 1];
        }
        if b[i] == b[k] {
            k += 1;
        }
        border[i] = k;
    }
    s[0..border[n - 1]].to_string()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 100000;
    let block = "abacaba".as_bytes();
    let mut letters: Vec<u8> = (0..n).map(|i| block[(i % 7) as usize]).collect();
    let mut seed: i64 = 1392;
    let mut check: i64 = 0;
    for _ in 0..2000 {
        seed = (seed + check) % 2147483648;
        let at = next_random(&mut seed) % n;
        let was = letters[at as usize];
        letters[at as usize] = (97 + next_random(&mut seed) % 3) as u8;
        let s = String::from_utf8(letters.clone()).unwrap();
        let got = longest_prefix(s);
        letters[at as usize] = was;
        check = (check * 131 + got.len() as i64 * 7 + at) % 1000000007;
    }
    println!("2000 rounds over 10^5 letters: checksum {}", check);
}
