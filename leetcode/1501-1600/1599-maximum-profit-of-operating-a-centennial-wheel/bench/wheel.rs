// LeetCode #1599: Maximum Profit of Operating a Centennial Wheel
// -- the bench in Rust, mirroring wheel.kara: the wheel run rotation by
// rotation in i64, on 300 days of 100000 arrivals, all drawn first.

fn min_operations_max_profit(customers: &[i32], boarding_cost: i32, running_cost: i32) -> i32 {
    let mut waiting: i64 = 0;
    let mut profit: i64 = 0;
    let mut best: i64 = 0;
    let mut answer: i32 = -1;
    let mut rotations: usize = 0;
    while rotations < customers.len() || waiting > 0 {
        if rotations < customers.len() {
            waiting += customers[rotations] as i64;
        }
        let board = waiting.min(4);
        waiting -= board;
        profit += board * boarding_cost as i64 - running_cost as i64;
        rotations += 1;
        if profit > best {
            best = profit;
            answer = rotations as i32;
        }
    }
    answer
}

fn main() {
    let mut seed: i64 = 1599;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut days: Vec<(Vec<i32>, i32, i32)> = Vec::new();
    for _ in 0..300 {
        let customers: Vec<i32> = (0..100000).map(|_| (next_random() % 9) as i32).collect();
        let boarding = (next_random() % 100 + 1) as i32;
        let running = (next_random() % 100 + 1) as i32;
        days.push((customers, boarding, running));
    }
    let mut check: i64 = 0;
    for (customers, boarding, running) in &days {
        let answer = min_operations_max_profit(customers, *boarding, *running);
        check = (check * 31 + answer as i64 + 1) % 1000000007;
    }
    println!("300 days of 100000 arrivals: checksum {}", check);
}
