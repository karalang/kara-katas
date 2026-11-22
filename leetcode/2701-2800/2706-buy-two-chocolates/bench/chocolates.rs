// LeetCode #2706: Buy Two Chocolates -- the bench (chocolates.kara in
// Rust): one pass keeping the two cheapest prices.

fn buy_choco(prices: &[i64], money: i64) -> i64 {
    let mut first: i64 = 101;
    let mut second: i64 = 101;
    for &p in prices.iter() {
        if p < first {
            second = first;
            first = p;
        } else if p < second {
            second = p;
        }
    }
    let cost = first + second;
    if cost <= money { money - cost } else { money }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let lists = 100000;
    let rounds = 10;
    let mut seed: i64 = 2706;
    let mut problems: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..lists {
        let prices: Vec<i64> = (0..50).map(|_| next_random(&mut seed) % 100 + 1).collect();
        let money = next_random(&mut seed) % 100 + 1;
        problems.push((prices, money));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (prices, money) in problems.iter() {
            let left = buy_choco(prices, *money);
            sum += left;
            check = (check * 31 + left + r) % 1000000007;
        }
    }
    println!("{} lists of 50 prices, {} rounds: money left sums to {}, checksum {}", lists, rounds, sum, check);
}
