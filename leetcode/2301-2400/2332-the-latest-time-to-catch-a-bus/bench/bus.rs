// LeetCode #2332: The Latest Time to Catch a Bus -- the bench, the ★ arm
// in Rust. Both lists sorted, the buses fill in order from the earliest
// passengers; the last bus's departure if it leaves with room, else its
// last passenger's time, then a step back past every passenger standing
// at the time tried. O((n + m) log(n + m)).

fn latest_time_catch_the_bus(mut buses: Vec<i64>, mut passengers: Vec<i64>, capacity: i64) -> i64 {
    buses.sort();
    passengers.sort();
    let mut next = 0usize;
    let mut aboard = 0i64;
    for &bus in buses.iter() {
        aboard = 0;
        while aboard < capacity && next < passengers.len() && passengers[next] <= bus {
            aboard += 1;
            next += 1;
        }
    }
    let mut latest = if aboard < capacity { buses[buses.len() - 1] } else { passengers[next - 1] };
    let mut k = next as i64 - 1;
    while k >= 0 && passengers[k as usize] == latest {
        latest -= 1;
        k -= 1;
    }
    latest
}

fn scrambled(index: i64) -> i64 {
    index * 2654435761 % 2147483647 + 2
}

fn main() {
    let mut cases: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for k in 0..10i64 {
        let base = k * 150000;
        let buses: Vec<i64> = (0..50000).map(|i| scrambled(base + i)).collect();
        let passengers: Vec<i64> = (50000..150000).map(|i| scrambled(base + i)).collect();
        cases.push((buses, passengers));
    }
    let mut check: i64 = 0;
    for p in 0..5i64 {
        for k in 0..10usize {
            let (buses, passengers) = cases[k].clone();
            check = (check * 31 + latest_time_catch_the_bus(buses, passengers, 1 + (k as i64 + p) % 5)) % 1000000007;
        }
    }
    println!("5 passes over 10 cases of 5*10^4 buses and 10^5 passengers: checksum {}", check);
}
