// LeetCode #1052: Grumpy Bookstore Owner -- Rust mirror of
// bench/grumpy.kara.

fn max_satisfied(customers: &[i64], grumpy: &[i64], minutes: usize) -> i64 {
    let mut base = 0;
    let mut saved = 0;
    let mut best = 0;
    for i in 0..customers.len() {
        if grumpy[i] == 0 {
            base += customers[i];
        } else {
            saved += customers[i];
        }
        if i >= minutes && grumpy[i - minutes] == 1 {
            saved -= customers[i - minutes];
        }
        best = best.max(saved);
    }
    base + best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (days, n, techniques) = (200, 20000i64, 10);
    let mut seed = 1052;
    let mut all: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..days {
        let mut customers = Vec::new();
        let mut grumpy = Vec::new();
        for _ in 0..n {
            customers.push(next_random(&mut seed) % 1001);
            grumpy.push(next_random(&mut seed) % 2);
        }
        all.push((customers, grumpy));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for (customers, grumpy) in &all {
        for _ in 0..techniques {
            let minutes = next_random(&mut seed) % n + 1;
            let answer = max_satisfied(customers, grumpy, minutes as usize);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    println!("{days} days of {n} minutes, {techniques} techniques each: total {total}, checksum {check}");
}
