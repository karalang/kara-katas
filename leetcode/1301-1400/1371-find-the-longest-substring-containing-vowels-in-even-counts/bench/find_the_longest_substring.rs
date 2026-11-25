// LeetCode #1371 bench -- Rust: each vowel's count kept as a parity bit,
// and the answer the furthest apart two prefixes with the same bits are.

fn find_the_longest_substring(s: &str) -> i32 {
    let mut first = [-2i64; 32];
    first[0] = -1;
    let mut bits = 0usize;
    let mut best = 0i64;
    for (i, c) in s.chars().enumerate() {
        match c {
            'a' => bits ^= 1,
            'e' => bits ^= 2,
            'i' => bits ^= 4,
            'o' => bits ^= 8,
            'u' => bits ^= 16,
            _ => {}
        }
        if first[bits] == -2 {
            first[bits] = i as i64;
        } else {
            best = best.max(i as i64 - first[bits]);
        }
    }
    best as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 4 strings of 5 * 10^5 letters, the constraints' most, drawn from
    // "aeioubcxyz", built once; then 80 rounds, each changing one letter
    // of one string to a copy, both drawn from the checksum so far, and
    // finding that string's longest substring
    let pool = b"aeioubcxyz";
    let mut seed = 1371i64;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..4 {
        let bytes: Vec<u8> = (0..500000).map(|_| pool[(next_random(&mut seed) % 10) as usize]).collect();
        strings.push(String::from_utf8(bytes).unwrap());
    }
    let mut check: i64 = 0;
    for r in 0..80i64 {
        let i = (check % 4) as usize;
        let at = ((check / 4) % 500000) as usize;
        let mut bytes: Vec<u8> = strings[i].bytes().collect();
        bytes[at] = pool[((check / 2000000) % 10) as usize];
        strings[i] = String::from_utf8(bytes).unwrap();
        let got = find_the_longest_substring(&strings[i]) as i64;
        check = (check * 31 + got + r) % 1000000007;
    }
    println!("80 rounds over 4 strings of 500000 letters: checksum {}", check);
}
