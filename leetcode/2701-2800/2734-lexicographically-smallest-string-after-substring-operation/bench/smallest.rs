// LeetCode #2734: Lexicographically Smallest String After Substring
// Operation -- the bench (smallest.kara in Rust): the run from the first
// letter that is not an 'a' up to the next 'a' moved back a letter,
// edited in a `Vec<u8>`.

fn smallest_string(s: &str) -> String {
    let mut b: Vec<u8> = s.as_bytes().to_vec();
    let n = b.len();
    let mut i = 0;
    while i < n && b[i] == b'a' {
        i += 1;
    }
    if i == n {
        b[n - 1] = b'z';
    } else {
        while i < n && b[i] != b'a' {
            b[i] -= 1;
            i += 1;
        }
    }
    String::from_utf8(b).unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let n: i64 = 100000;
    let rounds = 20;
    let mut seed: i64 = 2734;
    let mut words: Vec<String> = Vec::new();
    for _ in 0..count {
        let lead = next_random(&mut seed) % (n / 2);
        let mut word = String::new();
        for k in 0..n {
            let letter = if k < lead || next_random(&mut seed) % 5000 == 0 { b'a' } else { b'b' + (next_random(&mut seed) % 25) as u8 };
            word.push(letter as char);
        }
        words.push(word);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for word in words.iter() {
            let answer = smallest_string(word);
            let b = answer.as_bytes();
            let w = word.as_bytes();
            let mut moved: i64 = 0;
            for k in 0..b.len() {
                if b[k] != w[k] {
                    moved += 1;
                }
            }
            sum += moved;
            check = (check * 31 + moved + (b[b.len() / 2] - b'a') as i64 + r) % 1000000007;
        }
    }
    println!("{} words of {} letters, {} rounds: letters moved sum to {}, checksum {}", count, n, rounds, sum, check);
}
