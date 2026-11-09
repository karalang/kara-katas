// Benchmark: LeetCode #1081 Smallest Subsequence of Distinct Characters --
// the ★ arm. Mirrors smallest_subsequence.kara, .c, .py and go-seq/.

fn smallest_subsequence(s: &str) -> String {
    let bytes = s.as_bytes();
    let mut last = [0usize; 26];
    for i in 0..bytes.len() {
        last[(bytes[i] - b'a') as usize] = i;
    }
    let mut placed = [false; 26];
    let mut stack: Vec<u8> = Vec::new();
    for i in 0..bytes.len() {
        let b = bytes[i];
        if placed[(b - b'a') as usize] {
            continue;
        }
        while let Some(&top) = stack.last() {
            if top > b && last[(top - b'a') as usize] > i {
                placed[(top - b'a') as usize] = false;
                stack.pop();
            } else {
                break;
            }
        }
        stack.push(b);
        placed[(b - b'a') as usize] = true;
    }
    String::from_utf8(stack).unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds: i64 = 100;
    let mut seed = 1081;
    let mut texts: Vec<String> = Vec::new();
    for t in 0..2000i64 {
        let k = t % 26 + 1;
        let mut s = String::new();
        for _ in 0..1000 {
            s.push((b'a' + (next_random(&mut seed) % k) as u8) as char);
        }
        texts.push(s);
    }
    let mut kept: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..2000i64 {
            let out = smallest_subsequence(&texts[((r * 7 + i) % 2000) as usize]);
            kept += out.len() as i64;
            check = (check * 31 + out.as_bytes()[out.len() / 2] as i64 + i) % 1000000007;
        }
    }
    println!("{rounds} rounds over 2000 texts of 1000 letters: {kept} letters kept, checksum {check}");
}
