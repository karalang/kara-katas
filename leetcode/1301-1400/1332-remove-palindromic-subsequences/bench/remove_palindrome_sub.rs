// LeetCode #1332 bench, Rust mirror of the Kāra bench: the ★ arm on 1000
// strings of 1000 letters built once, then 500 passes, each setting one
// letter of one string from the checksum so far, rebuilding that string,
// and answering every string.

fn remove_palindrome_sub(s: &str) -> i32 {
    let b = s.as_bytes();
    let n = b.len();
    for i in 0..n / 2 {
        if b[i] != b[n - 1 - i] {
            return 2;
        }
    }
    1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000usize;
    let n = 1000usize;
    let mut seed = 1332i64;
    let mut letters: Vec<Vec<char>> = Vec::new();
    let mut strings: Vec<String> = Vec::new();
    for t in 0..count {
        let mut row = vec!['a'; n];
        for i in 0..n / 2 {
            let c = if next_random(&mut seed) % 2 == 0 { 'a' } else { 'b' };
            row[i] = c;
            row[n - 1 - i] = c;
        }
        if t % 2 == 1 {
            let k = n / 2 - 1 - t % 3;
            row[k] = if row[k] == 'a' { 'b' } else { 'a' };
        }
        strings.push(row.iter().collect());
        letters.push(row);
    }
    let mut check: i64 = 0;
    for pass in 0..500i64 {
        let t = (check % count as i64) as usize;
        let at = (check / count as i64 % n as i64) as usize;
        let c = if check / 7 % 2 == 0 { 'a' } else { 'b' };
        letters[t][at] = c;
        if pass % 2 == 0 {
            letters[t][n - 1 - at] = c;
        }
        strings[t] = letters[t].iter().collect();
        for s in strings.iter() {
            check = (check * 31 + remove_palindrome_sub(s) as i64 + pass) % 1000000007;
        }
    }
    println!("500 passes over 1000 strings of 1000 letters: checksum {}", check);
}
