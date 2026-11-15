// benchmark's Rust mirror of jumbled.kara (LeetCode #2191, the ★ arm),
// over a slice of the row: (value, place) pairs sorted.

fn mapped(mapping: &[i64], n: i64) -> i64 {
    if n == 0 {
        return mapping[0];
    }
    let mut rest = n;
    let mut value = 0;
    let mut place = 1;
    while rest > 0 {
        value += mapping[(rest % 10) as usize] * place;
        place *= 10;
        rest /= 10;
    }
    value
}

fn sort_jumbled(mapping: &[i64], nums: &[i64]) -> Vec<i64> {
    let mut keyed: Vec<(i64, usize)> = Vec::new();
    for i in 0..nums.len() {
        keyed.push((mapped(mapping, nums[i]), i));
    }
    keyed.sort();
    keyed.into_iter().map(|(_, i)| nums[i]).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big_random(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    let b = next_random(seed);
    a * 32768 + b
}

fn main() {
    let mut seed = 2191;
    let row: Vec<i64> = (0..1000000).map(|_| big_random(&mut seed) % 1000000000).collect();
    let mut check: i64 = 0;
    for _ in 0..200 {
        let mut mapping: Vec<i64> = (0..10).collect();
        for i in (1..10).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            mapping.swap(i, j);
        }
        let start = (big_random(&mut seed) % 970001) as usize;
        for x in sort_jumbled(&mapping, &row[start..start + 30000]) {
            check = (check * 31 + x % 1000003) % 1000000007;
        }
    }
    println!("200 solves: checksum {}", check);
}
