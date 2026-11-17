// LeetCode #2222: Number of Ways to Select Buildings -- bench mirror of
// buildings.kara: one pass keeping the 0s and 1s behind and the pairs
// "01" and "10", each character closing the pairs it completes.

fn number_of_ways(s: &str) -> i64 {
    let (mut zeros, mut ones, mut zero_ones, mut one_zeros, mut ways) = (0i64, 0i64, 0i64, 0i64, 0i64);
    for c in s.chars() {
        if c == '0' {
            ways += zero_ones;
            one_zeros += ones;
            zeros += 1;
        } else {
            ways += one_zeros;
            zero_ones += zeros;
            ones += 1;
        }
    }
    ways
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2222;
    let mut streets: Vec<Vec<char>> = Vec::new();
    for _ in 0..30 {
        // 10^5 buildings, each a 1 with chance one half
        streets.push((0..100000).map(|_| if next_random(&mut seed) % 2 == 1 { '1' } else { '0' }).collect());
    }
    let mut check: i64 = 0;
    for a in 0..30 {
        for r in 0..10 {
            // punch: one building is drawn again before each answer
            streets[a][r * 9999] = if next_random(&mut seed) % 2 == 1 { '1' } else { '0' };
            let s: String = streets[a].iter().collect();
            check = (check * 31 + number_of_ways(&s)) % 1000000007;
        }
    }
    println!("30 streets of 10^5, 10 punches: checksum {check}");
}
