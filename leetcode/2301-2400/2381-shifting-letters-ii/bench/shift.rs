// LeetCode #2381: Shifting Letters II -- the bench, the ★ arm in Rust: a
// difference array of the shifts, its running sum each letter's step.

fn shifting_letters(s: &str, shifts: &[[i64; 3]]) -> String {
    let b = s.as_bytes();
    let n = b.len();
    let mut diff: Vec<i64> = vec![0; n + 1];
    for shift in shifts {
        let step = if shift[2] == 1 { 1 } else { -1 };
        diff[shift[0] as usize] += step;
        diff[shift[1] as usize + 1] -= step;
    }
    let mut out: Vec<u8> = Vec::new();
    let mut total = 0i64;
    for i in 0..n {
        total += diff[i];
        let letter = ((b[i] - b'a') as i64 + total).rem_euclid(26);
        out.push(b'a' + letter as u8);
    }
    String::from_utf8(out).unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // a string of 5 * 10^4 letters and 10 lists of 5 * 10^4 shifts, list
    // l's shifts up to 10^l letters long, capped at the string; pass p
    // applies list p % 10
    let mut seed = 2381i64;
    let n = 50000i64;
    let s = String::from_utf8((0..n).map(|_| b'a' + (next_random(&mut seed) % 26) as u8).collect()).unwrap();
    let mut lists: Vec<Vec<[i64; 3]>> = Vec::new();
    for l in 0..10 {
        let mut reach = 1i64;
        for _ in 0..l {
            reach = (reach * 10).min(n);
        }
        let list: Vec<[i64; 3]> = (0..n)
            .map(|_| {
                let start = next_random(&mut seed) % n;
                let end = (start + next_random(&mut seed) % reach).min(n - 1);
                [start, end, next_random(&mut seed) % 2]
            })
            .collect();
        lists.push(list);
    }
    let mut check = 0i64;
    for p in 0..200i64 {
        let t = shifting_letters(&s, &lists[(p % 10) as usize]);
        for &b in t.as_bytes() {
            check = (check * 31 + (b - b'a') as i64 + p) % 1000000007;
        }
    }
    println!("200 passes over 5 * 10^4 letters: checksum {}", check);
}
