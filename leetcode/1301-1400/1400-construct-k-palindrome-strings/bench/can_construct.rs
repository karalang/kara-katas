// LeetCode #1400 bench -- Rust: at least k letters, and at most k letters
// that appear an odd number of times, the letters counted in an array of
// 26.

fn can_construct(s: &str, k: i32) -> bool {
    if (s.len() as i64) < k as i64 {
        return false;
    }
    let mut count = vec![0i64; 26];
    for &b in s.as_bytes() {
        count[(b - b'a') as usize] += 1;
    }
    let odd = count.iter().filter(|&&c| c % 2 == 1).count();
    odd as i64 <= k as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 100000;
    let mut seed = 1400;
    let mut letters: Vec<u8> = (0..n).map(|_| (97 + next_random(&mut seed) % 26) as u8).collect();
    let mut check: i64 = 0;
    for _ in 0..3000 {
        seed = (seed + check) % 2147483648;
        let at = next_random(&mut seed) % n;
        letters[at as usize] = (97 + next_random(&mut seed) % 26) as u8;
        let k = 1 + next_random(&mut seed) % 30;
        let s = String::from_utf8(letters.clone()).unwrap();
        let got = can_construct(&s, k as i32);
        check = (check * 131 + (if got { k } else { 0 }) + at) % 1000000007;
    }
    println!("3000 rounds over 10^5 letters: checksum {}", check);
}
