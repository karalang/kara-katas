// LeetCode #1576: Replace All ?'s to Avoid Consecutive Repeating
// Characters -- bench: the ★ arm (the first of a, b, c that fits, in a
// Vec[char]) over 20 strings of 500000 characters, half of them '?', built
// once; then 4 rounds answering all 20, each answer folded to its count of
// 'a's.

fn modify_string(s: &str) -> String {
    let mut cs: Vec<char> = s.chars().collect();
    let n = cs.len();
    for i in 0..n {
        if cs[i] == '?' {
            for c in ['a', 'b', 'c'] {
                if (i == 0 || cs[i - 1] != c) && (i + 1 == n || cs[i + 1] != c) {
                    cs[i] = c;
                    break;
                }
            }
        }
    }
    cs.iter().collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let n = 500000;
    let mut seed = 1576;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..20 {
        let mut s = String::new();
        let mut last = ' ';
        for _ in 0..n {
            if next_random(&mut seed) % 2 == 0 {
                s.push('?');
                last = '?';
            } else {
                let mut k = next_random(&mut seed) % 26;
                if (b'a' + k as u8) as char == last {
                    k = (k + 1) % 26;
                }
                let c = (b'a' + k as u8) as char;
                s.push(c);
                last = c;
            }
        }
        strings.push(s);
    }
    let (mut check, mut total) = (0i64, 0i64);
    for _ in 0..4 {
        for s in &strings {
            let a = modify_string(s).chars().filter(|&c| c == 'a').count() as i64;
            total += a;
            check = mix(check, a);
        }
    }
    println!("80 answers over 20 strings of {} characters: 'a' total {}, checksum {}", n, total, check);
}
