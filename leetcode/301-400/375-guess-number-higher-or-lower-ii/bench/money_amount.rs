// Benchmark for #375 -- mirror of money_amount.kara.

fn get_money_amount(n: usize) -> i64 {
    let mut cost = vec![vec![0i64; n + 2]; n + 2];
    for len in 2..n + 1 {
        for i in 1..n - len + 2 {
            let j = i + len - 1;
            let mut best = i64::MAX;
            for k in i..j + 1 {
                let worse = cost[i][k - 1].max(cost[k + 1][j]);
                best = best.min(k as i64 + worse);
            }
            cost[i][j] = best;
        }
    }
    cost[1][n]
}

fn main() {
    let mut checksum: i64 = 0;
    for n in 1..201 {
        checksum = (checksum * 1009 + get_money_amount(n)) % 1000000007;
    }
    println!("checksum {}", checksum);
}
