// LeetCode #1520: Maximum Number of Non-Overlapping Substrings -- the
// bench in Rust: the ★ arm over 200000 random strings of 1 to 64 letters
// over 5, built once and answered 3 times.

fn max_num_of_substrings(s: &str) -> Vec<String> {
    let bytes: Vec<u8> = s.bytes().collect();
    let n = bytes.len() as i64;
    let mut first: Vec<i64> = vec![n; 26];
    let mut last: Vec<i64> = vec![-1; 26];
    for i in 0..n {
        let c = (bytes[i as usize] - 97) as usize;
        first[c] = first[c].min(i);
        last[c] = i;
    }
    let mut spans: Vec<(i64, i64)> = Vec::new();
    let mut right = -1;
    for i in 0..n {
        let c = (bytes[i as usize] - 97) as usize;
        if i != first[c] {
            continue;
        }
        let mut end = last[c];
        let mut ok = true;
        let mut j = i;
        while j <= end {
            let d = (bytes[j as usize] - 97) as usize;
            if first[d] < i {
                ok = false;
                break;
            }
            end = end.max(last[d]);
            j += 1;
        }
        if !ok {
            continue;
        }
        if i > right {
            spans.push((i, end));
        } else {
            let k = spans.len() - 1;
            spans[k] = (i, end);
        }
        right = end;
    }
    spans
        .iter()
        .map(|&(a, b)| s[a as usize..b as usize + 1].to_string())
        .collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let count = 200000;
    let mut seed = 1520;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        let n = next_random(&mut seed) % 64 + 1;
        let mut s = String::new();
        for _ in 0..n {
            s.push((97 + next_random(&mut seed) % 5) as u8 as char);
        }
        strings.push(s);
    }
    let mut check = 0;
    let mut pieces = 0;
    for _ in 0..3 {
        for s in strings.iter() {
            for piece in max_num_of_substrings(s).iter() {
                pieces += 1;
                check = mix(check, piece.len() as i64);
                check = mix(check, piece.as_bytes()[0] as i64);
            }
        }
    }
    println!("3 passes over 200000 strings of up to 64 letters: {pieces} substrings, checksum {check}");
}
