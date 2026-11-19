// LeetCode #2335: Minimum Amount of Time to Fill Cups -- the bench, the ★
// arm in Rust: the larger of the most cups of one kind and half of all
// the cups, rounded up.

fn fill_cups(amount: &[i64]) -> i64 {
    let most = amount[0].max(amount[1]).max(amount[2]);
    let all = amount[0] + amount[1] + amount[2];
    most.max((all + 1) / 2)
}

fn main() {
    let mut amount: Vec<i64> = vec![0, 0, 0];
    let mut check = 0i64;
    for p in 0..3 {
        for a in 0..=100 {
            for b in 0..=100 {
                for c in 0..=100 {
                    amount[0] = a;
                    amount[1] = b;
                    amount[2] = c;
                    check = (check * 31 + fill_cups(&amount) + p) % 1000000007;
                }
            }
        }
    }
    println!("3 passes over 101^3 amounts: checksum {}", check);
}
