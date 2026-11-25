// LeetCode #1370 bench -- Rust: the letters counted, then sweeps up from a
// to z and down from z to a, each taking one of every letter still left,
// until none is.

fn sort_string(s: &str) -> String {
    let mut counts = [0i64; 26];
    for b in s.bytes() {
        counts[(b - b'a') as usize] += 1;
    }
    let mut out = String::new();
    let mut left = s.len();
    while left > 0 {
        for i in 0..26 {
            if counts[i] > 0 {
                out.push((b'a' + i as u8) as char);
                counts[i] -= 1;
                left -= 1;
            }
        }
        for i in (0..26).rev() {
            if counts[i] > 0 {
                out.push((b'a' + i as u8) as char);
                counts[i] -= 1;
                left -= 1;
            }
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 strings of 500 letters, the constraints' most, each from the
    // first 2 to 26 letters of the alphabet, built once; then 60000
    // rounds, each changing one letter of one string and sorting that
    // string, all drawn from the checksum so far
    let mut seed = 1370i64;
    let mut strings: Vec<String> = Vec::new();
    for k in 0..20i64 {
        let letters = 2 + k * 24 / 19;
        let s: String = (0..500).map(|_| (b'a' + (next_random(&mut seed) % letters) as u8) as char).collect();
        strings.push(s);
    }
    let mut check: i64 = 0;
    for r in 0..60000i64 {
        let i = (check % 20) as usize;
        let at = ((check / 20) % 500) as usize;
        let mut bytes: Vec<u8> = strings[i].bytes().collect();
        bytes[at] = b'a' + ((check / 10000) % 26) as u8;
        strings[i] = String::from_utf8(bytes).unwrap();
        for b in sort_string(&strings[i]).bytes() {
            check = (check * 31 + b as i64) % 1000000007;
        }
        check = (check + r) % 1000000007;
    }
    println!("60000 rounds over 20 strings of 500 letters: checksum {}", check);
}
