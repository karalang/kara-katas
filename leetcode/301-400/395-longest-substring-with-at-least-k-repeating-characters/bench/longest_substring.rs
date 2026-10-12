// Benchmark for #395: mirror of longest_substring.kara (divide and conquer).

fn longest(b: &[u8], lo: usize, hi: usize, k: usize) -> usize {
    if hi - lo < k {
        return 0;
    }
    let mut count = [0usize; 26];
    for i in lo..hi {
        count[(b[i] - 97) as usize] += 1;
    }
    let mut best = 0;
    let mut start = lo;
    let mut split = false;
    for i in lo..hi {
        if count[(b[i] - 97) as usize] < k {
            split = true;
            best = best.max(longest(b, start, i, k));
            start = i + 1;
        }
    }
    if !split {
        return hi - lo;
    }
    best.max(longest(b, start, hi, k))
}

fn longest_substring(s: &str, k: usize) -> usize {
    let b = s.as_bytes();
    longest(b, 0, b.len(), k)
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 395;
    let mut pool = String::new();
    for _ in 0..1000000 {
        let x = step(&mut seed) % 26;
        let y = step(&mut seed) % 26;
        pool.push((x.min(y) + 97) as u8 as char);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..10000 {
        let hi = step(&mut seed);
        let a = ((hi * 32768 + step(&mut seed)) % (1000000 - 10000)) as usize;
        let k = (1 + step(&mut seed) % 30) as usize;
        let r = longest_substring(&pool[a..a + 10000], k) as i64;
        total += r;
        checksum = (checksum * 31 + r) % 1000000007;
    }
    println!("10000 windows: total {}, checksum {}", total, checksum);
}
