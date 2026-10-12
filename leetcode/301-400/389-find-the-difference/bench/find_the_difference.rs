// Benchmark for #389: mirror of find_the_difference.kara (XOR of every byte).

fn find_the_difference(s: &str, t: &str) -> char {
    let mut x: u8 = 0;
    for b in s.bytes() {
        x ^= b;
    }
    for b in t.bytes() {
        x ^= b;
    }
    x as char
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 389;
    let mut pool = String::new();
    for _ in 0..1000000 {
        pool.push((step(&mut seed) % 26 + 97) as u8 as char);
    }
    let bytes = pool.as_bytes();
    let mut right = 0;
    let mut checksum: i64 = 0;
    for _ in 0..8000000 {
        let len = (step(&mut seed) % 1001) as usize;
        let a = (step(&mut seed) % (1000000 - len as i64 - 1)) as usize;
        let c = find_the_difference(&pool[a..a + len], &pool[a..a + len + 1]);
        if c as u8 == bytes[a + len] {
            right += 1;
        }
        checksum = (checksum * 31 + c as i64) % 1000000007;
    }
    println!("8000000 pairs, {} right, checksum {}", right, checksum);
}
