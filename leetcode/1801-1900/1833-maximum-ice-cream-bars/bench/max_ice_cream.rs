// LeetCode #1833: Maximum Ice Cream Bars -- the bench in Rust: the ★ arm over
// 1000 calls on the first 50000 to 99999 of one list of 10^5 bars of 1 to 10^5
// coins, built once, with 10^6 to 10^8 coins, each run's length and coins
// drawn from the checksum so far. Each call copies its run, as the arm takes
// its list by value.

fn max_ice_cream(costs: Vec<i64>, coins: i64) -> i64 {
    let dearest = *costs.iter().max().unwrap();
    let mut count: Vec<i64> = vec![0; dearest as usize + 1];
    for &c in costs.iter() {
        count[c as usize] += 1;
    }
    let mut left = coins;
    let mut bars = 0;
    for price in 1..dearest + 1 {
        if price > left {
            break;
        }
        let bought = count[price as usize].min(left / price);
        bars += bought;
        left -= bought * price;
    }
    bars
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1833;
    let mut base: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        let hi = next_random(&mut seed);
        base.push(1 + (hi * 32768 + next_random(&mut seed)) % 100000);
    }
    let mut check: i64 = 0;
    for call in 0..1000 {
        let n = (50000 + (check + call) % 50000) as usize;
        let coins = 1000000 + (check * 7 + call) % 99000000;
        check = (check * 31 + max_ice_cream(base[..n].to_vec(), coins)) % 1000000007;
    }
    println!("1000 calls: checksum {}", check);
}
