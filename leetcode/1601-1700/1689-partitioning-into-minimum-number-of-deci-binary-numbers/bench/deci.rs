// LeetCode #1689: Partitioning Into Minimum Number Of Deci-Binary Numbers
// -- the bench's Rust mirror: the ★ arm on 100 random numbers of 100000
// digits, all drawn first, each answered 50 times.

fn min_partitions(n: &str) -> i32 {
    let mut largest = 0;
    for b in n.bytes() {
        largest = largest.max(b - b'0');
    }
    largest as i32
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let size = 100000;
    let rounds = 50;
    let digits = b"0123456789";
    let mut seed = 1689;
    let mut numbers: Vec<String> = Vec::new();
    for _ in 0..count {
        let top = next_random(&mut seed) % 9 + 1;
        let mut n = String::with_capacity(size);
        n.push(digits[(next_random(&mut seed) % top + 1) as usize] as char);
        for _ in 1..size {
            n.push(digits[(next_random(&mut seed) % (top + 1)) as usize] as char);
        }
        numbers.push(n);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for n in numbers.iter() {
            let answer = min_partitions(n) as i64;
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} numbers of {size} digits, {rounds} rounds: answers sum to {total}, checksum {check}");
}
