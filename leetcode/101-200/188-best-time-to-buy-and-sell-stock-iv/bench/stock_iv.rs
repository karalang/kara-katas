fn max_i64(a: i64, b: i64) -> i64 {
    if a > b {
        a
    } else {
        b
    }
}

fn max_profit(k: i64, prices: &[i64]) -> i64 {
    let n = prices.len() as i64;
    if n == 0 || k == 0 {
        return 0;
    }
    if k >= n / 2 {
        let mut profit: i64 = 0;
        let mut i: i64 = 1;
        while i < n {
            if prices[i as usize] > prices[(i - 1) as usize] {
                profit += prices[i as usize] - prices[(i - 1) as usize];
            }
            i += 1;
        }
        return profit;
    }

    let neg: i64 = -1000000000;
    let mut buy: Vec<i64> = vec![neg; (k + 1) as usize];
    let mut sell: Vec<i64> = vec![0; (k + 1) as usize];
    let mut d: i64 = 0;
    while d < n {
        let price = prices[d as usize];
        let mut t: i64 = 1;
        while t <= k {
            buy[t as usize] = max_i64(buy[t as usize], sell[(t - 1) as usize] - price);
            sell[t as usize] = max_i64(sell[t as usize], buy[t as usize] + price);
            t += 1;
        }
        d += 1;
    }
    sell[k as usize]
}

fn main() {
    let n: i64 = 2000;
    let kmax: i64 = 50;
    let rounds: i64 = 5000;

    let mut prices: Vec<i64> = Vec::with_capacity(n as usize);
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        prices.push((state >> 16) % 1000);
    }

    let mut sink: i64 = 0;
    for _ in 0..rounds {
        state = (state * 1103515245 + 12345) & 2147483647;
        let k = 1 + state % kmax;
        state = (state * 1103515245 + 12345) & 2147483647;
        let idx = (state % n) as usize;
        prices[idx] = (state >> 16) % 1000;
        sink += max_profit(k, &prices);
    }
    println!("{}", sink);
}
