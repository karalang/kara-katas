// LeetCode #714: Best Time to Buy and Sell Stock with Transaction Fee
// -- two running states. Benchmark mirror of the Kara star arm: the
// best cash holding no share and the best holding one, day by day.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn max_profit(prices: &[i64], fee: i64) -> i64 {
    let mut cash = 0;
    let mut hold = -prices[0];
    for i in 1..prices.len() {
        let sold = hold + prices[i] - fee;
        if sold > cash {
            cash = sold;
        }
        let bought = cash - prices[i];
        if bought > hold {
            hold = bought;
        }
    }
    cash
}

fn main() {
    let mut seed: i64 = 714;
    let mut walks: Vec<Vec<i64>> = Vec::new();
    for w in 1..11 {
        let step = 10 * w;
        let mut prices: Vec<i64> = Vec::new();
        let mut price: i64 = 50000;
        for _ in 0..100000 {
            price += next_random(&mut seed) % (2 * step + 1) - step;
            if price < 1 {
                price = 1;
            }
            prices.push(price);
        }
        walks.push(prices);
    }
    let mut sum: i64 = 0;
    for round in 0..300 {
        let fee = 3 * round;
        for prices in walks.iter() {
            sum += max_profit(prices, fee);
        }
    }
    println!("300 rounds of 10 walks of 100000 days: sum {}", sum);
}
