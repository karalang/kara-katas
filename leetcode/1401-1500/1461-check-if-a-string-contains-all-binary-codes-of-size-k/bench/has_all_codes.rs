// LeetCode #1461 bench in Rust: the ★ arm (the last k digits kept as a
// number, each window marked once) on the same 20 strings of 5 * 10^5
// digits, k from 11 to 20.

fn has_all_codes(s: &str, k: usize) -> bool {
    let need = 1usize << k;
    let mut seen = vec![false; need];
    let mut found = 0;
    let mut window = 0usize;
    for (i, b) in s.bytes().enumerate() {
        window = ((window << 1) | (b - b'0') as usize) & (need - 1);
        if i + 1 >= k && !seen[window] {
            seen[window] = true;
            found += 1;
            if found == need {
                return true;
            }
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1461i64;
    let mut texts: Vec<Vec<u8>> = Vec::new();
    for _ in 0..20 {
        let digits: Vec<u8> = (0..500000).map(|_| if next_random(&mut seed) % 2 == 0 { b'0' } else { b'1' }).collect();
        texts.push(digits);
    }
    let mut check: i64 = 0;
    for t in 0..20 {
        for k in 11..=20usize {
            let at = (check % 500000) as usize;
            texts[t][at] = if texts[t][at] == b'0' { b'1' } else { b'0' };
            let s = String::from_utf8(texts[t].clone()).unwrap();
            let all = has_all_codes(&s, k);
            check = (check * 31 + if all { 1 } else { 0 } + k as i64) % 1000000007;
        }
    }
    println!("20 strings of 5 * 10^5 digits, k from 11 to 20: checksum {check}");
}
