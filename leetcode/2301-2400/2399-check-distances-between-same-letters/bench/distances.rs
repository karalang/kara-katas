// LeetCode #2399: Check Distances Between Same Letters -- the bench, the
// ★ arm in Rust: the first index of each letter, checked at its second.

fn check_distances(s: &str, distance: &[i64]) -> bool {
    let mut first = vec![-1i64; 26];
    let b = s.as_bytes();
    for i in 0..b.len() {
        let c = (b[i] - b'a') as usize;
        if first[c] < 0 {
            first[c] = i as i64;
        } else if i as i64 - first[c] - 1 != distance[c] {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// All 26 letters, each twice, shuffled, and the distances true of it;
// when `off`, one letter's distance is one away from its true one.
fn case(seed: &mut i64, off: bool) -> (String, Vec<i64>) {
    let mut b: Vec<u8> = (0..52).map(|i| b'a' + (i / 2) as u8).collect();
    for i in 1..52 {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        b.swap(i, j);
    }
    let mut distance = vec![0i64; 26];
    let mut first = vec![-1i64; 26];
    for i in 0..52 {
        let c = (b[i] - b'a') as usize;
        if first[c] < 0 {
            first[c] = i as i64;
        } else {
            distance[c] = i as i64 - first[c] - 1;
        }
    }
    if off {
        let letter = (next_random(seed) % 26) as usize;
        distance[letter] += if distance[letter] == 0 { 1 } else { -1 };
    }
    (String::from_utf8(b).unwrap(), distance)
}

fn main() {
    let mut seed = 2399;
    let cases: Vec<(String, Vec<i64>)> = (0..1000).map(|i| case(&mut seed, i % 2 == 1)).collect();
    let mut check: i64 = 0;
    let mut yes = 0;
    for p in 0..2000 {
        for (s, distance) in &cases {
            let answer = check_distances(s, distance);
            if answer {
                yes += 1;
            }
            check = (check * 31 + if answer { 2 } else { 1 } + p) % 1000000007;
        }
    }
    println!("2000 passes over 1000 strings of 52 letters: checksum {}, {} yes", check, yes);
}
