// LeetCode #1790: Check if One String Swap Can Make Strings Equal -- the
// bench in Rust, mirroring are_almost_equal.kara: the positions where the
// strings differ.

fn are_almost_equal(s1: &str, s2: &str) -> bool {
    let a = s1.as_bytes();
    let b = s2.as_bytes();
    let mut differ: Vec<usize> = Vec::new();
    for i in 0..a.len() {
        if a[i] != b[i] {
            differ.push(i);
            if differ.len() > 2 {
                return false;
            }
        }
    }
    match differ.len() {
        0 => true,
        2 => a[differ[0]] == b[differ[1]] && a[differ[1]] == b[differ[0]],
        _ => false,
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1790;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for k in 0..2000 {
        let mut a: Vec<u8> = Vec::new();
        for _ in 0..100 {
            a.push((97 + next_random(&mut seed) % 26) as u8);
        }
        let mut b = a.clone();
        for _ in 0..k % 4 {
            let i = (next_random(&mut seed) % 100) as usize;
            let j = (next_random(&mut seed) % 100) as usize;
            if k % 4 == 3 {
                b[i] = 97 + (b[i] - 97 + 1) % 26;
            } else {
                b.swap(i, j);
            }
        }
        pairs.push((String::from_utf8(a).unwrap(), String::from_utf8(b).unwrap()));
    }
    let mut check: i64 = 0;
    for call in 0..4000000i64 {
        let (s1, s2) = &pairs[((check + call) % 2000) as usize];
        check = (check * 3 + if are_almost_equal(s1, s2) { 2 } else { 1 }) % 1000000007;
    }
    println!("4000000 calls over 2000 pairs: checksum {}", check);
}
