// LeetCode #1358 bench -- Rust: where each of a, b and c was last seen; a
// substring ending at i holds all three when it starts at or before the
// earliest of those places.
fn number_of_substrings(s: &[u8]) -> i64 {
    let mut last: [i64; 3] = [-1, -1, -1];
    let mut count: i64 = 0;
    for (i, &b) in s.iter().enumerate() {
        last[(b - b'a') as usize] = i as i64;
        count += last.iter().cloned().min().unwrap() + 1;
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 strings of 5 * 10^4 letters, the constraints' most, c drawn one
    // time in 1000 and a and b evenly, built once; then 1000 rounds, each
    // setting one letter of one string, both drawn from the checksum so
    // far, and counting that string's substrings
    let mut seed = 1358;
    let mut texts: Vec<Vec<u8>> = Vec::new();
    for _ in 0..20 {
        let text: Vec<u8> = (0..50000)
            .map(|_| {
                let r = next_random(&mut seed) % 1000;
                if r == 0 {
                    b'c'
                } else if r % 2 == 0 {
                    b'a'
                } else {
                    b'b'
                }
            })
            .collect();
        texts.push(text);
    }
    let mut check: i64 = 0;
    for r in 0..1000 {
        let k = (check % 20) as usize;
        texts[k][((check / 20) % 50000) as usize] = (97 + (check / 7) % 3) as u8;
        check = (check * 31 + number_of_substrings(&texts[k]) + r) % 1000000007;
    }
    println!("1000 rounds over 20 strings of 5 * 10^4 letters: checksum {}", check);
}
