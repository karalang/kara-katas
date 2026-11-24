// LeetCode #1312 bench, Rust: the ★ arm (the interval costs kept in one
// row) on the same 20 strings and 50 passes.

fn min_insertions(s: &str) -> i64 {
    let b = s.as_bytes();
    let n = b.len();
    let mut row = vec![0i64; n];
    for i in (0..n).rev() {
        let mut inside = 0;
        for j in i + 1..n {
            let keep = row[j];
            row[j] = if b[i] == b[j] { inside } else { 1 + keep.min(row[j - 1]) };
            inside = keep;
        }
    }
    row[n - 1]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let n: i64 = 500;
    let mut seed = 1312;
    let mut strings: Vec<Vec<char>> = Vec::new();
    for g in 0..20 {
        let k = if g % 3 == 0 { 2 } else if g % 3 == 1 { 4 } else { 26 };
        let mut chars = Vec::new();
        for _ in 0..n {
            chars.push(letters[(next_random(&mut seed) % k) as usize]);
        }
        strings.push(chars);
    }
    let mut check: i64 = 0;
    for pass in 0..50 {
        for g in 0..20 {
            let k = if g % 3 == 0 { 2 } else if g % 3 == 1 { 4 } else { 26 };
            strings[g][(check % n) as usize] = letters[((check / 7) % k) as usize];
            let s: String = strings[g].iter().collect();
            let got = min_insertions(&s);
            check = (check * 31 + got + pass) % 1000000007;
        }
    }
    println!("50 passes over 20 strings of 500: checksum {}", check);
}
