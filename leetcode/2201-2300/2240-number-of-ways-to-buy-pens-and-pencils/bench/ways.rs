// LeetCode #2240: Number of Ways to Buy Pens and Pencils -- the
// benchmark's Rust mirror of ways.kara: for each number of pens, the
// pencils the rest buys plus none, summed.

fn ways_to_buy_pens_pencils(total: i64, cost1: i64, cost2: i64) -> i64 {
    let mut ways = 0i64;
    let mut pens = 0i64;
    while pens * cost1 <= total {
        ways += (total - pens * cost1) / cost2 + 1;
        pens += 1;
    }
    ways
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2240i64;
    let mut check = 0i64;
    for _ in 0..300 {
        // the money at 10^6, a pen from 1 to 10, a pencil up to 10^6
        let cost1 = next_random(&mut seed) % 10 + 1;
        let cost2 = wide_random(&mut seed) % 1000000 + 1;
        check = (check * 31 + ways_to_buy_pens_pencils(1000000, cost1, cost2)) % 1000000007;
    }
    println!("300 cases of 10^6 money: checksum {}", check);
}
