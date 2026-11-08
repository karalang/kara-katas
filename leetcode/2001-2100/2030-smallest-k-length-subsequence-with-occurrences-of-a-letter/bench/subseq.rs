// LeetCode #2030: Smallest K-Length Subsequence With Occurrences of a
// Letter -- the ★ arm in Rust, the same algorithm and workload as
// subseq.kara.

fn smallest_subsequence(s: &str, k: i64, letter: char, repetition: i64) -> String {
    let bytes = s.as_bytes();
    let want = letter as u8;
    let n = bytes.len() as i64;
    let mut remain = bytes.iter().filter(|&&b| b == want).count() as i64;
    let mut stack: Vec<u8> = Vec::new();
    let mut have = 0i64;
    for i in 0..n {
        let c = bytes[i as usize];
        while let Some(&top) = stack.last() {
            if top > c && stack.len() as i64 - 1 + n - i >= k && (top != want || have - 1 + remain >= repetition) {
                stack.pop();
                if top == want {
                    have -= 1;
                }
            } else {
                break;
            }
        }
        if (stack.len() as i64) < k {
            if c == want {
                stack.push(c);
                have += 1;
            } else if k - stack.len() as i64 > repetition - have {
                stack.push(c);
            }
        }
        if c == want {
            remain -= 1;
        }
    }
    String::from_utf8(stack).unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2030;
    let mut texts: Vec<String> = Vec::new();
    for a in 0..10i64 {
        let span = 2 + 3 * a;
        let mut s = String::new();
        let mut c = 0;
        for _ in 0..50000 {
            let r = next_random(&mut seed) % 10;
            if r < 4 {
                c = (c + 1) % span;
            } else if r < 7 {
                c = next_random(&mut seed) % span;
            }
            s.push((97 + c) as u8 as char);
        }
        texts.push(s);
    }
    let (mut calls, mut kept, mut check) = (0i64, 0i64, 0i64);
    for round in 0..20i64 {
        for a in 0..10i64 {
            let s = &texts[a as usize];
            let k = (round * 2477 + a * 911) % 50000 + 1;
            let letter = (97 + (round + a) % (2 + 3 * a)) as u8 as char;
            let copies = s.chars().filter(|&c| c == letter).count() as i64;
            let repetition = (round * 131 + a * 17) % k.min(copies) + 1;
            let got = smallest_subsequence(s, k, letter, repetition);
            calls += 1;
            let bytes = got.as_bytes();
            let len = bytes.len();
            kept += len as i64;
            check = (check * 31 + len as i64) % 1000000007;
            check = (check * 31 + bytes[0] as i64 + bytes[len / 2] as i64 + bytes[len - 1] as i64) % 1000000007;
        }
    }
    println!("{} calls: {} letters kept, checksum {}", calls, kept, check);
}
