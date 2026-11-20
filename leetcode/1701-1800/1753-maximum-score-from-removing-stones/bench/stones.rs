// LeetCode #1753: Maximum Score From Removing Stones -- the bench
// (stones.kara in Rust): a closed form.

fn maximum_score(a: i32, b: i32, c: i32) -> i32 {
    let total = a + b + c;
    let largest = a.max(b.max(c));
    (total / 2).min(total - largest)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let count = 2000000;
    let rounds: i64 = 5;
    let mut seed: i64 = 1753;
    let piles: Vec<(i32, i32, i32)> = (0..count)
        .map(|_| {
            let a = (wide(&mut seed) % 100000 + 1) as i32;
            let b = (wide(&mut seed) % 100000 + 1) as i32;
            let c = (wide(&mut seed) % 100000 + 1) as i32;
            (a, b, c)
        })
        .collect();
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &(a, b, c) in piles.iter() {
            let answer = maximum_score(a, b, c) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{} sets of piles, {} rounds: scores add to {}, checksum {}", count, rounds, sum, check);
}
