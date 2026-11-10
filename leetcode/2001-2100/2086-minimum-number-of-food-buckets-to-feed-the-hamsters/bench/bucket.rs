// LeetCode #2086: Minimum Number of Food Buckets to Feed the Hamsters --
// Rust mirror of the ★ arm's benchmark (bucket.kara): the same street and
// 3000 windows, each a `&str` into the street, served by the same greedy.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn minimum_buckets(hamsters: &str) -> i64 {
    let cells = hamsters.as_bytes();
    let n = cells.len();
    let mut bucket = vec![false; n];
    let mut count = 0;
    for i in 0..n {
        if cells[i] != b'H' {
            continue;
        }
        if i > 0 && bucket[i - 1] {
            continue;
        }
        if i + 1 < n && cells[i + 1] == b'.' {
            bucket[i + 1] = true;
            count += 1;
        } else if i > 0 && cells[i - 1] == b'.' {
            bucket[i - 1] = true;
            count += 1;
        } else {
            return -1;
        }
    }
    count
}

fn main() {
    let pieces = [".", "H.", ".H", "H.H", ".H.H.", "..H"];
    let mut seed = 2086i64;
    let mut street = String::new();
    while street.len() < 1000000 {
        street.push_str(pieces[(next_random(&mut seed) % 6) as usize]);
    }
    let (mut total, mut impossible, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..3000 {
        let hi = next_random(&mut seed);
        let from = ((hi * 32768 + next_random(&mut seed)) % 900000) as usize;
        let a = minimum_buckets(&street[from..from + 100000]);
        if a < 0 {
            impossible += 1;
        } else {
            total += a;
        }
        check = (check * 31 + a + 1) % 1000000007;
    }
    println!("3000 windows: sum {}, {} impossible, checksum {}", total, impossible, check);
}
