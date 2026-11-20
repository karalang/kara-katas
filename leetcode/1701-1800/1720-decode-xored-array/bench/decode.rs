// LeetCode #1720: Decode XORed Array -- the bench (decode.kara): each
// value the one before it XORed with the code between them.

fn decode(encoded: &[i32], first: i32) -> Vec<i32> {
    let mut arr: Vec<i32> = Vec::with_capacity(encoded.len() + 1);
    arr.push(first);
    for &e in encoded.iter() {
        arr.push(arr[arr.len() - 1] ^ e);
    }
    arr
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let count = 200;
    let rounds: i64 = 100;
    let n: usize = 10000;
    let mut seed: i64 = 1720;
    let mut problems: Vec<(Vec<i32>, i32)> = Vec::new();
    for _ in 0..count {
        let encoded: Vec<i32> = (0..n).map(|_| (wide(&mut seed) % 100001) as i32).collect();
        let first = (wide(&mut seed) % 100001) as i32;
        problems.push((encoded, first));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (encoded, first) in problems.iter() {
            let arr = decode(encoded, *first);
            sum += arr[n] as i64;
            check = (check * 31 + arr[n / 2] as i64 + arr[n] as i64 + r) % 1000000007;
        }
    }
    println!("{} arrays of {} codes, {} rounds: last values sum to {}, checksum {}", count, n, rounds, sum, check);
}
