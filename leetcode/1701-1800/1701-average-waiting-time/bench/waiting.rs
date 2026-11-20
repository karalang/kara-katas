// LeetCode #1701: Average Waiting Time -- the bench's Rust mirror: the ★
// arm on 50 random lists of 100000 customers, arrivals and times up to
// 10^4, all drawn first, each answered 60 times.

fn average_waiting_time(customers: &[Vec<i32>]) -> f64 {
    let mut finish: i64 = 0;
    let mut waited: i64 = 0;
    for c in customers.iter() {
        finish = finish.max(c[0] as i64) + c[1] as i64;
        waited += finish - c[0] as i64;
    }
    waited as f64 / customers.len() as f64
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let rounds = 60;
    let n = 100000;
    let mut seed = 1701;
    let mut lists: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..count {
        let mut customers: Vec<Vec<i32>> = Vec::new();
        let mut arrival: i64 = 0;
        for _ in 0..n {
            if next_random(&mut seed) % 10 == 0 && arrival < 9999 {
                arrival += 1;
            }
            customers.push(vec![(arrival + 1) as i32, (next_random(&mut seed) % 10000 + 1) as i32]);
        }
        lists.push(customers);
    }
    let mut total = 0.0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for customers in lists.iter() {
            let answer = average_waiting_time(customers);
            total += answer;
            check = (check * 31 + (answer * 100000.0).round() as i64 + r) % 1000000007;
        }
    }
    println!("{count} lists of {n} customers, {rounds} rounds: answers sum to {total:.5}, checksum {check}");
}
