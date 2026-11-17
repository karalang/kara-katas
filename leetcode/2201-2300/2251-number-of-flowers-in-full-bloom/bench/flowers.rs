// LeetCode #2251: Number of Flowers in Full Bloom -- the benchmark's Rust
// mirror of flowers.kara: the starts and the ends sorted once, and each
// person the starts of at most t less the ends before t, by two
// `partition_point`s.

fn full_bloom_flowers(flowers: &[[i64; 2]], people: &[i64]) -> Vec<i64> {
    let mut starts: Vec<i64> = flowers.iter().map(|f| f[0]).collect();
    let mut ends: Vec<i64> = flowers.iter().map(|f| f[1]).collect();
    starts.sort();
    ends.sort();
    people
        .iter()
        .map(|&t| (starts.partition_point(|&s| s <= t) - ends.partition_point(|&e| e < t)) as i64)
        .collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2251i64;
    let mut check = 0i64;
    for _ in 0..20 {
        let flowers: Vec<[i64; 2]> = (0..50000)
            .map(|_| {
                let a = wide_random(&mut seed) % 1000000000 + 1;
                let b = wide_random(&mut seed) % 1000000000 + 1;
                [a.min(b), a.max(b)]
            })
            .collect();
        let people: Vec<i64> = (0..50000).map(|_| wide_random(&mut seed) % 1000000000 + 1).collect();
        for c in full_bloom_flowers(&flowers, &people) {
            check = (check * 31 + c) % 1000000007;
        }
    }
    println!("20 cases of 5 * 10^4 flowers and people: checksum {}", check);
}
