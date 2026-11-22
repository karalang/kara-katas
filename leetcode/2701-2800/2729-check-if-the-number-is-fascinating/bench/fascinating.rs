// LeetCode #2729: Check if The Number is Fascinating -- the bench
// (fascinating.kara in Rust): n, 2 n and 3 n joined by `format!`, the
// digits sorted and compared with "123456789".

fn is_fascinating(n: i64) -> bool {
    let joined = format!("{}{}{}", n, 2 * n, 3 * n);
    let mut digits: Vec<char> = joined.chars().collect();
    digits.sort();
    let sorted: String = digits.into_iter().collect();
    sorted == "123456789"
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000000;
    let rounds = 5;
    let mut seed: i64 = 2729;
    let fascinating = [192, 219, 273, 327];
    let mut numbers: Vec<i64> = Vec::new();
    for i in 0..count {
        if i % 50 == 0 {
            numbers.push(fascinating[(next_random(&mut seed) % 4) as usize]);
        } else {
            numbers.push(next_random(&mut seed) % 900 + 100);
        }
    }
    let mut yes: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &n in numbers.iter() {
            let answer = is_fascinating(n);
            if answer {
                yes += 1;
            }
            check = (check * 31 + if answer { 2 } else { 1 } + r) % 1000000007;
        }
    }
    println!("{} numbers, {} rounds: {} fascinating, checksum {}", count, rounds, yes, check);
}
