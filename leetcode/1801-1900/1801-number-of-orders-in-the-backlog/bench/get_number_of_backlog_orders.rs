// LeetCode #1801: Number of Orders in the Backlog -- the bench in Rust: the
// ★ arm over 400 random lists of 500 orders built once, 10000 calls.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn get_number_of_backlog_orders(orders: &[Vec<i32>]) -> i32 {
    let mut buys: BinaryHeap<(i32, i64)> = BinaryHeap::new();
    let mut sells: BinaryHeap<Reverse<(i32, i64)>> = BinaryHeap::new();
    for order in orders {
        let price = order[0];
        let mut amount = order[1] as i64;
        if order[2] == 0 {
            while amount > 0 {
                match sells.peek() {
                    Some(Reverse((p, _))) if *p <= price => {}
                    _ => break,
                }
                let Reverse((p, a)) = sells.pop().unwrap();
                if a > amount {
                    sells.push(Reverse((p, a - amount)));
                    amount = 0;
                } else {
                    amount -= a;
                }
            }
            if amount > 0 {
                buys.push((price, amount));
            }
        } else {
            while amount > 0 {
                match buys.peek() {
                    Some((p, _)) if *p >= price => {}
                    _ => break,
                }
                let (p, a) = buys.pop().unwrap();
                if a > amount {
                    buys.push((p, a - amount));
                    amount = 0;
                } else {
                    amount -= a;
                }
            }
            if amount > 0 {
                sells.push(Reverse((price, amount)));
            }
        }
    }
    let total: i64 = buys.iter().map(|(_, a)| a).sum::<i64>() + sells.iter().map(|Reverse((_, a))| a).sum::<i64>();
    (total % 1000000007) as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1801;
    let mut lists: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..400 {
        let orders: Vec<Vec<i32>> = (0..500)
            .map(|_| {
                let p = (1 + next_random(&mut seed) % 1000) as i32;
                let a = (1 + next_random(&mut seed) % 1000) as i32;
                let t = (next_random(&mut seed) % 2) as i32;
                vec![p, a, t]
            })
            .collect();
        lists.push(orders);
    }
    let mut check: i64 = 0;
    for call in 0..10000i64 {
        let orders = &lists[((check + call) % 400) as usize];
        check = (check * 31 + get_number_of_backlog_orders(orders) as i64) % 1000000007;
    }
    println!("10000 calls over 400 lists of 500 orders: checksum {}", check);
}
