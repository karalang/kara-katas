// LeetCode #2351: First Letter to Appear Twice -- the bench, the ★ arm in
// Rust: a table of 26 marks, one per letter, the first letter already
// marked is the answer.

fn repeated_character(s: &str) -> char {
    let mut seen = vec![false; 26];
    for c in s.chars() {
        let i = c as usize - 'a' as usize;
        if seen[i] {
            return c;
        }
        seen[i] = true;
    }
    ' '
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // string t is the first 2 to 26 letters of the alphabet shuffled, then
    // one of them again
    let mut seed = 2351i64;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..100000 {
        let k = 2 + next_random(&mut seed) % 25;
        let mut letters: Vec<char> = (0..k).map(|i| (97 + i) as u8 as char).collect();
        for i in (1..k).rev() {
            let j = next_random(&mut seed) % (i + 1);
            letters.swap(i as usize, j as usize);
        }
        let again = letters[(next_random(&mut seed) % k) as usize];
        letters.push(again);
        strings.push(letters.iter().collect());
    }
    let mut check = 0i64;
    for p in 0..50i64 {
        for s in &strings {
            check = (check * 31 + repeated_character(s) as i64 + p) % 1000000007;
        }
    }
    println!("50 passes over 10^5 strings: checksum {}", check);
}
