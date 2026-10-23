// LeetCode #879 bench: Rust mirror of profitable_schemes.kara (the ★ arm,
// a knapsack over members and profit) on the same 600 cases.

fn profitable_schemes(n: i64, min_profit: i64, group: &[i64], profit: &[i64]) -> i64 {
    let modulus = 1000000007;
    let mut ways: Vec<Vec<i64>> = Vec::new();
    for _ in 0..n + 1 {
        ways.push(vec![0; (min_profit + 1) as usize]);
    }
    ways[0][0] = 1;
    for c in 0..group.len() {
        let g = group[c];
        let gain = profit[c];
        let mut m = n;
        while m >= g {
            for p in 0..min_profit + 1 {
                let q = (p + gain).min(min_profit);
                ways[m as usize][q as usize] = (ways[m as usize][q as usize] + ways[(m - g) as usize][p as usize]) % modulus;
            }
            m -= 1;
        }
    }
    let mut total = 0;
    for m in 0..n + 1 {
        total = (total + ways[m as usize][min_profit as usize]) % modulus;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 879;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for k in 0..600 {
        let n = 50 + next_random(&mut seed) % 51;
        let min_profit = 50 + next_random(&mut seed) % 51;
        let wide = k % 2 == 0;
        let mut group: Vec<i64> = Vec::new();
        let mut profit: Vec<i64> = Vec::new();
        for _ in 0..100 {
            group.push(next_random(&mut seed) % (if wide { 100 } else { 10 }) + 1);
            profit.push(next_random(&mut seed) % (if wide { 101 } else { 11 }));
        }
        let answer = profitable_schemes(n, min_profit, &group, &profit);
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    println!("600 cases of 100 crimes: counts sum to {}, checksum {}", total, check);
}
