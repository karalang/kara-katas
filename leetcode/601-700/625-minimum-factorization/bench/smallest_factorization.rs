// LeetCode #625: Minimum Factorization -- Rust mirror of the Kāra bench.
//
// The ★ arm's greedy from the largest digit over the same numbers and
// rounds.

fn smallest_factorization(num: i64) -> i64 {
    if num < 10 {
        return num;
    }
    let mut rest = num;
    let mut answer = 0;
    let mut place = 1;
    let mut d = 9;
    while d >= 2 {
        while rest % d == 0 {
            rest /= d;
            answer += d * place;
            place *= 10;
            if answer > 2147483647 {
                return 0;
            }
        }
        d -= 1;
    }
    if rest == 1 { answer } else { 0 }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_numbers(count: i64, seed: &mut i64) -> Vec<i64> {
    let mut numbers = Vec::new();
    for i in 0..count {
        if i % 2 == 0 {
            let mut product = 1;
            for _ in 0..1 + next_random(seed) % 10 {
                let d = 2 + next_random(seed) % 8;
                if product * d <= 2147483647 {
                    product *= d;
                }
            }
            numbers.push(product);
        } else {
            let high = next_random(seed);
            let low = next_random(seed);
            numbers.push(1 + (high * 65536 + low) % 2147483647);
        }
    }
    numbers
}

fn main() {
    let count = 200000;
    let rounds = 50;
    let mut seed: i64 = 625;
    let numbers = random_numbers(count, &mut seed);
    let mut found = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for i in 0..count as usize {
            let a = smallest_factorization(numbers[i]);
            if a != 0 {
                found += 1;
            }
            checksum = (checksum * 31 + a) % 1000000007;
        }
    }
    println!("{} numbers, {} rounds: {} answers, checksum {}", count, rounds, found, checksum);
}
