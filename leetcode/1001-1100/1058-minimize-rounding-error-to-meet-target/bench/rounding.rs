// LeetCode #1058: Minimize Rounding Error to Meet Target -- the benchmark,
// the same algorithm as rounding.kara.

fn thousandths(p: &str) -> i64 {
    let mut value = 0i64;
    for c in p.chars() {
        if c != '.' {
            value = value * 10 + c.to_digit(10).unwrap() as i64;
        }
    }
    value
}

fn minimize_error(prices: &[String], target: i64) -> String {
    let mut floor_sum = 0i64;
    let mut fractions: Vec<i64> = Vec::new();
    for p in prices {
        let t = thousandths(p);
        floor_sum += t / 1000;
        if t % 1000 != 0 {
            fractions.push(t % 1000);
        }
    }
    let up = target - floor_sum;
    if up < 0 || up > fractions.len() as i64 {
        return "-1".to_string();
    }
    fractions.sort_by(|a, b| b.cmp(a));
    let mut error = 0i64;
    for (k, f) in fractions.iter().enumerate() {
        error += if (k as i64) < up { 1000 - f } else { *f };
    }
    format!("{}.{:03}", error / 1000, error % 1000)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_price(seed: &mut i64) -> String {
    let whole = next_random(seed) % 1000;
    let part = if next_random(seed) % 4 == 0 {
        0
    } else {
        next_random(seed) % 999 + 1
    };
    format!("{}.{:03}", whole, part)
}

fn main() {
    let mut seed = 1058i64;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..40 {
        let mut prices = Vec::new();
        for _ in 0..500 {
            prices.push(random_price(&mut seed));
        }
        lists.push(prices);
    }
    let mut calls = 0i64;
    let mut check = 0i64;
    for _ in 0..8 {
        for prices in &lists {
            let mut floor_sum = 0i64;
            let mut with_fraction = 0i64;
            for p in prices {
                let t = thousandths(p);
                floor_sum += t / 1000;
                if t % 1000 != 0 {
                    with_fraction += 1;
                }
            }
            for target in floor_sum - 1..floor_sum + with_fraction + 2 {
                let answer = minimize_error(prices, target);
                for c in answer.bytes() {
                    check = (check * 131 + c as i64) % 1000000007;
                }
                calls += 1;
            }
        }
    }
    println!("{} calls: checksum {}", calls, check);
}
