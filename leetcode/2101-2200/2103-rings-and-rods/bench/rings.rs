// LeetCode #2103: Rings and Rods -- bench, Rust mirror of rings.kara.

fn count_points(rings: &str) -> i64 {
    let bytes = rings.as_bytes();
    let mut masks = [0i64; 10];
    let mut i = 0;
    while i < bytes.len() {
        let bit = match bytes[i] {
            b'R' => 1,
            b'G' => 2,
            _ => 4,
        };
        masks[(bytes[i + 1] - b'0') as usize] |= bit;
        i += 2;
    }
    masks.iter().filter(|&&m| m == 7).count() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2103;
    let mut strings: Vec<String> = Vec::new();
    for s in 0..4096 {
        let rods = if s % 2 == 0 { 10 } else { 3 };
        let mut rings = String::new();
        for _ in 0..100 {
            rings.push(b"RGB"[(next_random(&mut seed) % 3) as usize] as char);
            rings.push((b'0' + (next_random(&mut seed) % rods) as u8) as char);
        }
        strings.push(rings);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for k in 0..300000usize {
        let got = count_points(&strings[k * 7919 % 4096]);
        total += got;
        check = (check * 31 + got) % 1000000007;
    }
    println!("300000 counts: {} rods with all three, checksum {}", total, check);
}
