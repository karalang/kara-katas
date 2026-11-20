// LeetCode #1744: Can You Eat Your Favorite Candy on Your Favorite Day?
// -- the bench (eat.kara in Rust): prefix sums, then two comparisons a
// query.

fn can_eat(candies_count: &[i32], queries: &[Vec<i32>]) -> Vec<bool> {
    let mut before: Vec<i64> = vec![0];
    for &c in candies_count.iter() {
        before.push(before[before.len() - 1] + c as i64);
    }
    let mut answers: Vec<bool> = Vec::new();
    for q in queries.iter() {
        let (t, day, cap) = (q[0] as usize, q[1] as i64, q[2] as i64);
        answers.push(day + 1 <= before[t + 1] && (day + 1) * cap > before[t]);
    }
    answers
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let count = 10;
    let rounds: i64 = 30;
    let n: i64 = 100000;
    let mut seed: i64 = 1744;
    let mut problems: Vec<(Vec<i32>, Vec<Vec<i32>>)> = Vec::new();
    for _ in 0..count {
        let candies: Vec<i32> = (0..n).map(|_| (next_random(&mut seed) % 20 + 1) as i32).collect();
        let total: i64 = candies.iter().map(|&c| c as i64).sum();
        let mut queries: Vec<Vec<i32>> = Vec::new();
        for _ in 0..n {
            let t = wide(&mut seed) % n;
            let day = wide(&mut seed) % total;
            let cap = next_random(&mut seed) % 30 + 1;
            queries.push(vec![t as i32, day as i32, cap as i32]);
        }
        problems.push((candies, queries));
    }
    let mut yes: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (candies, queries) in problems.iter() {
            let answers = can_eat(candies, queries);
            let mut here = 0;
            for (i, &a) in answers.iter().enumerate() {
                if a {
                    here += 1;
                    check = (check + i as i64 * 7 + r) % 1000000007;
                }
            }
            yes += here;
        }
    }
    println!("{} problems of {} types and {} queries, {} rounds: {} yes, checksum {}", count, n, n, rounds, yes, check);
}
