// LeetCode #1518 bench: the ★ arm (whole lots a round), as bottles.kara.

fn num_water_bottles(num_bottles: i64, num_exchange: i64) -> i64 {
    let mut drunk = 0;
    let mut full = num_bottles;
    let mut empty = 0;
    while full > 0 {
        drunk += full;
        empty += full;
        full = empty / num_exchange;
        empty %= num_exchange;
    }
    drunk
}

fn main() {
    let mut check: i64 = 0;
    for i in 0..20000000i64 {
        let bottles = i * 7919 % 1000000000 + 1;
        let exchange = i % 99 + 2;
        check = (check * 31 + num_water_bottles(bottles, exchange) + 1) % 1000000007;
    }
    println!("20000000 questions up to 10^9 bottles and 2 to 100 for 1: checksum {}", check);
}
