// LeetCode #2379: Minimum Recolors to Get K Consecutive Black Blocks --
// the bench, the ★ arm in Rust: the whites of the first window counted,
// then the window slid along one block at a time.

fn minimum_recolors(blocks: &str, k: i64) -> i64 {
    let b = blocks.as_bytes();
    let k = k as usize;
    let mut whites = 0i64;
    for i in 0..k {
        if b[i] == b'W' {
            whites += 1;
        }
    }
    let mut fewest = whites;
    for i in k..b.len() {
        if b[i] == b'W' {
            whites += 1;
        }
        if b[i - k] == b'W' {
            whites -= 1;
        }
        fewest = fewest.min(whites);
    }
    fewest
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 1000 strings of 100 blocks, string s white with a chance of s % 10
    // in 10; pass p asks string s for k = 1 + (7 p + s) % 100
    let mut seed = 2379i64;
    let mut strings: Vec<String> = Vec::new();
    for s in 0..1000i64 {
        let letters: Vec<u8> = (0..100).map(|_| if next_random(&mut seed) % 10 < s % 10 { b'W' } else { b'B' }).collect();
        strings.push(String::from_utf8(letters).unwrap());
    }
    let mut check = 0i64;
    for p in 0..500i64 {
        for s in 0..1000i64 {
            let k = 1 + (7 * p + s) % 100;
            check = (check * 31 + minimum_recolors(&strings[s as usize], k) + p) % 1000000007;
        }
    }
    println!("500 passes over 1000 strings of 100 blocks: checksum {}", check);
}
