// LeetCode #2124: Check if All A's Appears Before All B's -- the
// benchmark, the same algorithm as abba.kara: the answer is that "ba"
// does not occur.

fn check_string(s: &str) -> bool {
    !s.contains("ba")
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2124;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..100000 {
        let split = next_random(&mut seed) % 101;
        let mut letters: Vec<u8> = (0..100).map(|i| if i < split { b'a' } else { b'b' }).collect();
        if next_random(&mut seed) % 4 == 0 {
            let at = (next_random(&mut seed) % 100) as usize;
            letters[at] = if letters[at] == b'a' { b'b' } else { b'a' };
        }
        strings.push(String::from_utf8(letters).unwrap());
    }
    let mut ordered = 0;
    let mut check: i64 = 0;
    for round in 0..50usize {
        let k = round * 7919 % 100000;
        let at = round * 31 % 100;
        let mut letters = strings[k].as_bytes().to_vec();
        letters[at] = if letters[at] == b'a' { b'b' } else { b'a' };
        strings[k] = String::from_utf8(letters).unwrap();
        for i in 0..strings.len() {
            if check_string(&strings[i]) {
                ordered += 1;
                check = (check * 31 + i as i64) % 1000000007;
            }
        }
    }
    println!("5000000 checks: {} in order, checksum {}", ordered, check);
}
