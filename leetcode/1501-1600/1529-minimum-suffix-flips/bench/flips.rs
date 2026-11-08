// LeetCode #1529: Minimum Suffix Flips -- bench: the ★ arm over 200
// random strings of 1 to 100000 bits, built once and answered 50 times.

fn min_flips(target: &str) -> i64 {
    let mut flips = 0;
    let mut prev = b'0';
    for &c in target.as_bytes() {
        if c != prev {
            flips += 1;
            prev = c;
        }
    }
    flips
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1529;
    let mut targets: Vec<String> = Vec::new();
    for _ in 0..200 {
        let n = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000 + 1;
        let ones = next_random(&mut seed) % 9 + 1;
        let mut target = String::new();
        for _ in 0..n {
            target.push(if next_random(&mut seed) % 10 < ones { '1' } else { '0' });
        }
        targets.push(target);
    }
    let mut check = 0;
    for _ in 0..50 {
        for target in targets.iter() {
            check = mix(check, min_flips(target));
        }
    }
    println!("50 passes over 200 strings of up to 100000 bits: checksum {}", check);
}
