// LeetCode #1758: Minimum Changes To Make Alternating Binary String -- the
// bench in Rust, mirroring min_operations.kara: one pass counting the
// characters that differ from "0101...".
fn min_operations(s: &str) -> i32 {
    let bytes = s.as_bytes();
    let mut differ: i64 = 0;
    for (i, &b) in bytes.iter().enumerate() {
        if (b - b'0') as i64 != (i % 2) as i64 {
            differ += 1;
        }
    }
    differ.min(bytes.len() as i64 - differ) as i32
}

fn main() {
    let mut seed: i64 = 1758;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..2000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let n = 1 + seed / 65536 % 20000;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let chance = seed / 65536 % 101;
        let mut s = String::new();
        for _ in 0..n {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            s.push(if seed / 65536 % 100 < chance { '1' } else { '0' });
        }
        strings.push(s);
    }
    let mut check: i64 = 0;
    for call in 0..30000i64 {
        let s = &strings[((check + call * 7919) % 2000) as usize];
        check = (check * 31 + min_operations(s) as i64) % 1000000007;
    }
    println!("30000 calls over 2000 strings: checksum {}", check);
}
