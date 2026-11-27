// LeetCode #1832: Check if the Sentence Is Pangram -- the bench in Rust: the ★
// arm over 100000 calls on runs of 500 to 999 letters cut from one string of
// 2000 letters, built once, each letter a z one time in 600 and otherwise one
// of a to y; each run's start and length are drawn from the checksum so far.
// Each call makes its run a string of its own.

fn check_if_pangram(sentence: String) -> bool {
    let mut seen: i64 = 0;
    for &b in sentence.as_bytes().iter() {
        seen |= 1 << (b - b'a');
    }
    seen == (1 << 26) - 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1832;
    let mut letters: Vec<u8> = Vec::new();
    for _ in 0..2000 {
        if next_random(&mut seed) % 600 == 0 {
            letters.push(b'z');
        } else {
            letters.push(b'a' + (next_random(&mut seed) % 25) as u8);
        }
    }
    let mut check: i64 = 0;
    let mut pangrams = 0;
    for call in 0..100000 {
        let start = ((check + call) % 1000) as usize;
        let len = (500 + (check * 7 + call) % 500) as usize;
        let s: String = letters[start..start + len].iter().map(|&b| b as char).collect();
        let yes = check_if_pangram(s);
        if yes {
            pangrams += 1;
        }
        check = (check * 31 + if yes { 2 } else { 1 }) % 1000000007;
    }
    println!("100000 calls: {} pangrams, checksum {}", pangrams, check);
}
