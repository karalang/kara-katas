// LeetCode #1397 bench -- Rust: the strings built a letter at a time,
// counted by how much of `evil` their end matches and whether they are
// still at s1's prefix and at s2's, the matches stepped through a KMP
// automaton table.

fn slot(j: i64, low: bool, high: bool) -> usize {
    (j * 4 + if low { 2 } else { 0 } + if high { 1 } else { 0 }) as usize
}

fn find_good_strings(n: i32, s1: &str, s2: &str, evil: &str) -> i32 {
    let modulus: i64 = 1000000007;
    let lo = s1.as_bytes();
    let hi = s2.as_bytes();
    let e = evil.as_bytes();
    let m = e.len();
    let mut border = vec![0i64; m];
    let mut k = 0i64;
    for i in 1..m {
        while k > 0 && e[i] != e[k as usize] {
            k = border[(k - 1) as usize];
        }
        if e[i] == e[k as usize] {
            k += 1;
        }
        border[i] = k;
    }
    let mut next = vec![0i64; m * 26];
    for j in 0..m {
        for c in 0..26i64 {
            if e[j] as i64 == 97 + c {
                next[j * 26 + c as usize] = j as i64 + 1;
            } else if j > 0 {
                next[j * 26 + c as usize] = next[border[j - 1] as usize * 26 + c as usize];
            }
        }
    }
    let mut ways = vec![0i64; m * 4];
    ways[slot(0, true, true)] = 1;
    for i in 0..n as usize {
        let mut after = vec![0i64; m * 4];
        for j in 0..m as i64 {
            for low in [false, true] {
                for high in [false, true] {
                    let w = ways[slot(j, low, high)];
                    if w == 0 {
                        continue;
                    }
                    let first = if low { lo[i] as i64 - 97 } else { 0 };
                    let last = if high { hi[i] as i64 - 97 } else { 25 };
                    for c in first..=last {
                        let to = next[j as usize * 26 + c as usize];
                        if to == m as i64 {
                            continue;
                        }
                        let at = slot(to, low && c == first, high && c == last);
                        after[at] = (after[at] + w) % modulus;
                    }
                }
            }
        }
        ways = after;
    }
    let mut total = 0;
    for w in &ways {
        total = (total + w) % modulus;
    }
    total as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1397;
    let mut low: Vec<u8> = (0..500).map(|_| (97 + next_random(&mut seed) % 3) as u8).collect();
    let mut high: Vec<u8> = (0..500).map(|_| (120 + next_random(&mut seed) % 3) as u8).collect();
    let mut evil: Vec<u8> = (0..50).map(|_| (97 + next_random(&mut seed) % 3) as u8).collect();
    let mut check: i64 = 0;
    for _ in 0..200 {
        seed = (seed + check) % 2147483648;
        let at = (next_random(&mut seed) % 500) as usize;
        low[at] = (97 + next_random(&mut seed) % 3) as u8;
        let at = (next_random(&mut seed) % 500) as usize;
        high[at] = (120 + next_random(&mut seed) % 3) as u8;
        let at = (next_random(&mut seed) % 50) as usize;
        evil[at] = (97 + next_random(&mut seed) % 3) as u8;
        let s1 = String::from_utf8(low.clone()).unwrap();
        let s2 = String::from_utf8(high.clone()).unwrap();
        let e = String::from_utf8(evil.clone()).unwrap();
        check = (check * 131 + find_good_strings(500, &s1, &s2, &e) as i64) % 1000000007;
    }
    println!("200 rounds at n = 500, evil of 50 letters: checksum {}", check);
}
