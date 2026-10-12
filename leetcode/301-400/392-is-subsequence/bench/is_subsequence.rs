// Benchmark for #392: mirror of is_subsequence.kara (two pointers).

fn is_subsequence(s: &str, t: &str) -> bool {
    let a = s.as_bytes();
    let mut i = 0;
    for b in t.bytes() {
        if i < a.len() && a[i] == b {
            i += 1;
        }
    }
    i == a.len()
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big(seed: &mut i64) -> i64 {
    let hi = step(seed);
    hi * 32768 + step(seed)
}

fn main() {
    let mut seed: i64 = 392;
    let mut pool = String::new();
    for _ in 0..1000000 {
        pool.push((step(&mut seed) % 26 + 97) as u8 as char);
    }
    let mut yes = 0;
    let mut checksum: i64 = 0;
    for _ in 0..20000 {
        let a = (big(&mut seed) % (1000000 - 100)) as usize;
        let len = step(&mut seed) % 10001;
        let b = (big(&mut seed) % (1000000 - len)) as usize;
        let r = is_subsequence(&pool[a..a + 100], &pool[b..b + len as usize]);
        if r {
            yes += 1;
        }
        checksum = (checksum * 3 + if r { 1 } else { 2 }) % 1000000007;
    }
    println!("20000 pairs: {} subsequences, checksum {}", yes, checksum);
}
