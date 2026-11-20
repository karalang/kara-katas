// LeetCode #1663 bench: the ★ arm, from the back.
//
// 400 problems with n = 10^5, LeetCode's largest, and k drawn from n to
// 26n, all drawn first; then each string is built and every letter of it
// folded into a checksum.

fn get_smallest_string(n: i32, k: i32) -> String {
    let n = n as i64;
    let mut letters = vec![b'a'; n as usize];
    let mut left = k as i64 - n;
    let mut i = n - 1;
    while left > 0 {
        let more = left.min(25);
        letters[i as usize] += more as u8;
        left -= more;
        i -= 1;
    }
    String::from_utf8(letters).unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 400;
    let n: i64 = 100000;
    let mut seed = 1663i64;
    let mut ks: Vec<i32> = Vec::new();
    for _ in 0..count {
        let r = next_random(&mut seed) * 32768 + next_random(&mut seed);
        ks.push((n + r % (25 * n + 1)) as i32);
    }
    let mut zs = 0i64;
    let mut check = 0i64;
    for &k in ks.iter() {
        let s = get_smallest_string(n as i32, k);
        for &b in s.as_bytes() {
            if b == b'z' {
                zs += 1;
            }
            check = (check * 31 + b as i64) % 1000000007;
        }
    }
    println!("{count} problems with n = {n}: {zs} z's, checksum {check}");
}
