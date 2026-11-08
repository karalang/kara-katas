// LeetCode #1526: Minimum Number of Increments on Subarrays to Form a
// Target Array -- bench: the ★ arm over 100 random arrays of 1 to 100000 numbers up to 10000, built once and answered 50 times.

fn min_number_operations(target: &[i64]) -> i64 {
    let mut total = target[0];
    for i in 1..target.len() {
        if target[i] > target[i - 1] {
            total += target[i] - target[i - 1];
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1526i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..100 {
        let n = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000 + 1;
        let mut target: Vec<i64> = Vec::new();
        for _ in 0..n {
            target.push((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 10000 + 1);
        }
        arrays.push(target);
    }
    let mut check = 0;
    for _ in 0..50 {
        for target in &arrays {
            check = mix(check, min_number_operations(target));
        }
    }
    println!("50 passes over 100 arrays of up to 100000 numbers: checksum {}", check);
}
