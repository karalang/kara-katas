// LeetCode #2177: Find Three Consecutive Integers That Sum to a Given
// Number -- the benchmark's Rust mirror of three.kara.

fn sum_of_three(num: i64) -> Vec<i64> {
    if num % 3 != 0 {
        return Vec::new();
    }
    let x = num / 3;
    vec![x - 1, x, x + 1]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2177i64;
    let mut row: Vec<i64> = Vec::new();
    for _ in 0..1000000 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let c = next_random(&mut seed);
        row.push(((a * 32768 + b) * 32768 + c) % 1000000000000001);
    }
    let mut found = 0i64;
    let mut check = 0i64;
    for pass in 0..2 {
        for &num in row.iter() {
            let three = sum_of_three(num + pass);
            if three.len() == 3 {
                found += 1;
                check = (check * 31 + three[2] % 1000000007) % 1000000007;
            }
        }
    }
    println!("2000000 solves: {} found, checksum {}", found, check);
}
