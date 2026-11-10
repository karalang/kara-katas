// LeetCode #2073: Time Needed to Buy Tickets -- Rust mirror of the ★
// arm's benchmark (tickets.kara): 20000 lines of 100 people, every place
// in every line asked about, 2000000 answers.

fn time_required_to_buy(tickets: &[i64], k: usize) -> i64 {
    let want = tickets[k];
    let mut time = 0;
    for (i, &t) in tickets.iter().enumerate() {
        time += if i <= k { t.min(want) } else { t.min(want - 1) };
    }
    time
}

fn main() {
    let mut seed: i64 = 2073;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut lines: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20000 {
        let mut tickets = Vec::new();
        for _ in 0..100 {
            tickets.push(next_random() % 100 + 1);
        }
        lines.push(tickets);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for tickets in &lines {
        for k in 0..100 {
            let a = time_required_to_buy(tickets, k);
            total += a;
            check = (check * 31 + a) % 1000000007;
        }
    }
    println!("2000000 answers: sum {total}, checksum {check}");
}
