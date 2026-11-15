// LeetCode #2178: Maximum Split of Positive Even Integers -- the
// benchmark's Rust mirror of split.kara.

fn maximum_even_split(final_sum: i64) -> Vec<i64> {
    let mut parts: Vec<i64> = Vec::new();
    if final_sum % 2 != 0 {
        return parts;
    }
    let mut left = final_sum;
    let mut next = 2i64;
    while left >= next {
        parts.push(next);
        left -= next;
        next += 2;
    }
    let last = parts.len() - 1;
    parts[last] += left;
    parts
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2178i64;
    let mut parts_in_all = 0usize;
    let mut check = 0i64;
    for _ in 0..400 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let c = next_random(&mut seed);
        let final_sum = ((a * 32768 + b) * 32768 + c) % 10000000000 + 1;
        let parts = maximum_even_split(final_sum);
        parts_in_all += parts.len();
        for &p in parts.iter() {
            check = (check * 31 + p) % 1000000007;
        }
    }
    println!("400 solves: {} parts, checksum {}", parts_in_all, check);
}
