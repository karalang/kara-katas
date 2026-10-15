// LeetCode #680: Valid Palindrome II -- two pointers. Bench.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn is_palindrome(b: &[u8], mut i: usize, mut j: usize) -> bool {
    while i < j {
        if b[i] != b[j] {
            return false;
        }
        i += 1;
        j -= 1;
    }
    true
}

fn valid_palindrome(s: &str) -> bool {
    let b = s.as_bytes();
    let mut i = 0;
    let mut j = b.len() - 1;
    while i < j {
        if b[i] != b[j] {
            return is_palindrome(b, i + 1, j) || is_palindrome(b, i, j - 1);
        }
        i += 1;
        j -= 1;
    }
    true
}

fn main() {
    let count: i64 = 300;
    let len: i64 = 20000;
    let rounds: i64 = 100;
    let widths = [2i64, 3, 26];
    let mut seed: i64 = 680;
    let mut strings: Vec<String> = Vec::new();
    for k in 0..count {
        let width = widths[(k % 3) as usize];
        let extra = k / 3 % 3;
        let mut cs: Vec<char> = Vec::new();
        for _ in 0..len / 2 {
            cs.push((97 + next_random(&mut seed) % width) as u8 as char);
        }
        for i in (0..(len / 2) as usize).rev() {
            cs.push(cs[i]);
        }
        for _ in 0..extra {
            let at = next_random(&mut seed) % (cs.len() as i64 + 1);
            cs.insert(at as usize, (97 + next_random(&mut seed) % width) as u8 as char);
        }
        strings.push(cs.iter().collect());
    }
    let mut valid: i64 = 0;
    let mut sum: i64 = 0;
    for r in 0..rounds {
        for k in 0..count {
            let at = (k * 7 + r) % count;
            if valid_palindrome(&strings[at as usize]) {
                valid += 1;
                sum = (sum * 31 + at + 1) % 1000000007;
            } else {
                sum = (sum * 31 + 7) % 1000000007;
            }
        }
    }
    println!("{} strings checked: {} valid, checksum {}", count * rounds, valid, sum);
}
