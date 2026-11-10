// LeetCode #2110: Number of Smooth Descent Periods of a Stock -- the
// benchmark, the same algorithm as descent.kara: the descent run's length
// up to each day, summed.

fn get_descent_periods(prices: &[i64]) -> i64 {
    let mut run: i64 = 1;
    let mut total: i64 = 1;
    for i in 1..prices.len() {
        if prices[i - 1] - prices[i] == 1 {
            run += 1;
        } else {
            run = 1;
        }
        total += run;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2110;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut p: i64 = 5000000;
        let mut prices: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            prices.push(p);
            p = if next_random(&mut seed) % 4 != 0 { p - 1 } else { p + next_random(&mut seed) % 20 };
        }
        arrays.push(prices);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..10 {
        for a in 0..20 {
            arrays[a][round * 9973] += 1;
            let got = get_descent_periods(&arrays[a]);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    println!("200 counts: {} periods, checksum {}", total, check);
}
