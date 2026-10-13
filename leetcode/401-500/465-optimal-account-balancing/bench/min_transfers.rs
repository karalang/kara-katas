// Benchmark for #465: mirror of min_transfers.kara (the ★ arm:
// backtracking over the unsettled balances) on the same workload.

fn fewest_from(debts: &mut Vec<i64>, start: usize) -> i64 {
    let mut first = start;
    while first < debts.len() && debts[first] == 0 {
        first += 1;
    }
    if first == debts.len() {
        return 0;
    }
    let mut best = -1;
    for j in first + 1..debts.len() {
        if debts[j] * debts[first] < 0 {
            debts[j] += debts[first];
            let count = 1 + fewest_from(debts, first + 1);
            debts[j] -= debts[first];
            if best < 0 || count < best {
                best = count;
            }
        }
    }
    best
}

fn min_transfers(transactions: &[(i64, i64, i64)]) -> i64 {
    let mut people = 0;
    for &(from, to, _) in transactions {
        people = people.max(from + 1).max(to + 1);
    }
    let mut balance = vec![0i64; people as usize];
    for &(from, to, amount) in transactions {
        balance[from as usize] -= amount;
        balance[to as usize] += amount;
    }
    let mut debts: Vec<i64> = Vec::new();
    for b in balance {
        if b != 0 {
            debts.push(b);
        }
    }
    fewest_from(&mut debts, 0)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let ledgers = 20000;
    let mut seed: i64 = 465;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..ledgers {
        let mut transactions: Vec<(i64, i64, i64)> = Vec::new();
        for _ in 0..8 {
            let from = next_random(&mut seed) % 12;
            let to = (from + 1 + next_random(&mut seed) % 11) % 12;
            let amount = 1 + next_random(&mut seed) % 3;
            transactions.push((from, to, amount));
        }
        let fewest = min_transfers(&transactions);
        total += fewest;
        checksum = (checksum * 31 + fewest) % 1000000007;
    }
    println!("{} ledgers of 8 transactions: {} transfers in all, checksum {}", ledgers, total, checksum);
}
