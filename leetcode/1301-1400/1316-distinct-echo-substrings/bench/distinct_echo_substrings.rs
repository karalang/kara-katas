// LeetCode #1316 bench, Rust mirror of the Kāra bench: the ★ arm (a table of
// how far every two suffixes agree, each echo counted at the first place it
// starts) on 4 strings of 2000 letters built once; then 5 passes, each
// setting one letter of every string from the checksum so far, answering it
// and folding the count plus the pass into the checksum.

fn distinct_echo_substrings(text: &str) -> i32 {
    let s = text.as_bytes();
    let n = s.len();
    let mut agree = vec![vec![0i64; n + 1]; n + 1];
    for i in (0..n).rev() {
        for j in (i + 1..n).rev() {
            if s[i] == s[j] {
                agree[i][j] = agree[i + 1][j + 1] + 1;
            }
        }
    }
    let mut earlier = vec![0i64; n];
    for i in 0..n {
        for j in i + 1..n {
            earlier[j] = earlier[j].max(agree[i][j]);
        }
    }
    let mut count = 0i64;
    for i in 0..n {
        for h in 1..=(n - i) / 2 {
            if agree[i][i + h] >= h as i64 && 2 * h as i64 > earlier[i] {
                count += 1;
            }
        }
    }
    count as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 2000;
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed = 1316i64;
    let mut strings: Vec<Vec<char>> = Vec::new();
    for t in 0..4 {
        let mut chars: Vec<char> = Vec::new();
        if t == 3 {
            let block = [
                letters[(next_random(&mut seed) % 26) as usize],
                letters[(next_random(&mut seed) % 26) as usize],
                letters[(next_random(&mut seed) % 26) as usize],
            ];
            for i in 0..n {
                chars.push(block[(i % 3) as usize]);
            }
        } else {
            let k = if t == 0 { 2 } else if t == 1 { 3 } else { 26 };
            for _ in 0..n {
                chars.push(letters[(next_random(&mut seed) % k) as usize]);
            }
        }
        strings.push(chars);
    }
    let mut check: i64 = 0;
    for pass in 0..5i64 {
        for t in 0..4 {
            let chars = &mut strings[t];
            chars[(check % n) as usize] = letters[((check / 7) % 26) as usize];
            let s: String = chars.iter().collect();
            let count = distinct_echo_substrings(&s) as i64;
            check = (check * 31 + count + pass) % 1000000007;
        }
    }
    println!("5 passes over 4 strings of 2000: checksum {}", check);
}
