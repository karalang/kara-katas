// LeetCode #1528: Shuffle String -- bench: the ★ arm over 100000 random
// strings of 1 to 100 letters with shuffled indices, built once and
// answered 30 times.

fn restore_string(s: &str, indices: &[i64]) -> String {
    let b = s.as_bytes();
    let mut out = vec![0u8; b.len()];
    for i in 0..b.len() {
        out[indices[i] as usize] = b[i];
    }
    String::from_utf8(out).unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1528;
    let mut cases: Vec<(String, Vec<i64>)> = Vec::new();
    for _ in 0..100000 {
        let n = next_random(&mut seed) % 100 + 1;
        let mut s = String::new();
        for _ in 0..n {
            s.push((97 + next_random(&mut seed) % 26) as u8 as char);
        }
        let mut indices: Vec<i64> = (0..n).collect();
        for i in (1..n).rev() {
            let j = next_random(&mut seed) % (i + 1);
            indices.swap(i as usize, j as usize);
        }
        cases.push((s, indices));
    }
    let mut check = 0;
    for pass in 0..30usize {
        for (s, indices) in cases.iter() {
            let answer = restore_string(s, indices);
            check = mix(check, answer.as_bytes()[pass % answer.len()] as i64);
        }
    }
    println!("30 passes over 100000 strings of up to 100 letters: checksum {}", check);
}
