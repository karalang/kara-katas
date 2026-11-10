// LeetCode #2109: Adding Spaces to a String -- the benchmark, the same
// algorithm as spaces.kara: one walk over the letters with an index into
// the spaces.

fn add_spaces(s: &str, spaces: &[i64]) -> String {
    let mut out = String::with_capacity(s.len() + spaces.len());
    let mut next = 0;
    for (i, c) in s.chars().enumerate() {
        if next < spaces.len() && spaces[next] == i as i64 {
            out.push(' ');
            next += 1;
        }
        out.push(c);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".chars().collect();
    let mut seed = 2109;
    let mut rows: Vec<(String, Vec<i64>)> = Vec::new();
    for _ in 0..20 {
        let mut s = String::new();
        let mut spaces: Vec<i64> = Vec::new();
        for i in 0..300000 {
            s.push(letters[(next_random(&mut seed) % 52) as usize]);
            if next_random(&mut seed) % 3 == 0 {
                spaces.push(i);
            }
        }
        rows.push((s, spaces));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for (s, spaces) in &rows {
        for _ in 0..5 {
            let got = add_spaces(s, spaces);
            total += got.len() as i64;
            let b = got.as_bytes();
            let mut j = 0;
            while j < b.len() {
                check = (check * 31 + b[j] as i64) % 1000000007;
                j += 997;
            }
        }
    }
    println!("100 strings: {} characters, checksum {}", total, check);
}
