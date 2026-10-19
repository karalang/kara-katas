// LeetCode 767 — Reorganize String: benchmark, the ★ arm in Rust.
// Sixty-four random strings of 500 letters, built once; 400,000 rounds
// each reorganize the next of them.

fn reorganize_string(s: &str) -> String {
    let n = s.len();
    let mut counts = [0usize; 26];
    for b in s.bytes() {
        counts[(b - b'a') as usize] += 1;
    }
    let mut most = 0;
    for k in 1..26 {
        if counts[k] > counts[most] {
            most = k;
        }
    }
    if counts[most] > (n + 1) / 2 {
        return String::new();
    }
    let mut out = vec![0u8; n];
    let mut place = 0;
    for step in 0..27 {
        let k = if step == 0 { most } else { step - 1 };
        if step > 0 && k == most {
            continue;
        }
        for _ in 0..counts[k] {
            if place >= n {
                place = 1;
            }
            out[place] = b'a' + k as u8;
            place += 2;
        }
    }
    String::from_utf8(out).unwrap()
}

fn main() {
    let mut seed: i64 = 767;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let rounds: i64 = 400000;
    let mut pool: Vec<String> = Vec::new();
    for _ in 0..64 {
        let letters = 1 + next_random() % 26;
        let bytes: Vec<u8> = (0..500)
            .map(|_| {
                let k = next_random() % (letters + 1);
                b'a' + if k == letters { 0 } else { k as u8 }
            })
            .collect();
        pool.push(String::from_utf8(bytes).unwrap());
    }
    let mut possible: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..rounds {
        let answer = reorganize_string(&pool[(round % 64) as usize]);
        let mut letter = 0;
        if !answer.is_empty() {
            possible += 1;
            letter = answer.as_bytes()[(round % 500) as usize] as i64;
        }
        check = (check * 31 + answer.len() as i64 + letter) % 1000000007;
    }
    println!("{} strings of 500 letters: {} rearranged, checksum {}", rounds, possible, check);
}
