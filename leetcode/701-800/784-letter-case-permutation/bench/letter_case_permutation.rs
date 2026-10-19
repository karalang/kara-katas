// LeetCode 784 — Letter Case Permutation: the bench, in Rust.
// Mirrors letter_case_permutation.kara: backtracking over the same 64
// strings.

fn permute(at: usize, buf: &mut Vec<char>, out: &mut Vec<String>) {
    if at == buf.len() {
        let mut s = String::new();
        for &c in buf.iter() {
            s.push(c);
        }
        out.push(s);
        return;
    }
    let c = buf[at];
    if c.is_ascii_alphabetic() {
        buf[at] = c.to_ascii_lowercase();
        permute(at + 1, buf, out);
        buf[at] = c.to_ascii_uppercase();
        permute(at + 1, buf, out);
        buf[at] = c;
    } else {
        permute(at + 1, buf, out);
    }
}

fn letter_case_permutation(s: String) -> Vec<String> {
    let mut buf: Vec<char> = s.chars().collect();
    let mut out = Vec::new();
    permute(0, &mut buf, &mut out);
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".chars().collect();
    let digits: Vec<char> = "0123456789".chars().collect();
    let mut seed = 784;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..64 {
        let wanted = 6 + next_random(&mut seed) % 6;
        let mut is_letter: Vec<bool> = (0..12).map(|i| i < wanted).collect();
        let mut i: i64 = 11;
        while i > 0 {
            let j = next_random(&mut seed) % (i + 1);
            is_letter.swap(i as usize, j as usize);
            i -= 1;
        }
        let mut s = String::new();
        for i in 0..12 {
            s.push(if is_letter[i] {
                letters[(next_random(&mut seed) % 52) as usize]
            } else {
                digits[(next_random(&mut seed) % 10) as usize]
            });
        }
        strings.push(s);
    }
    let rounds: i64 = 20000;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let all = letter_case_permutation(strings[(r % 64) as usize].clone());
        total += all.len() as i64;
        for w in all.iter() {
            let bytes = w.as_bytes();
            check = (check * 31 + bytes[0] as i64 + 7 * bytes[11] as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds of 12-character strings: {total} permutations, checksum {check}");
}
