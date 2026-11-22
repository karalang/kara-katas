// LeetCode #2792: Count Nodes That Are Great Enough -- the bench in Rust:
// the ★ arm over 20 random trees of 10^4 nodes with values up to 10^4
// and k = 10, all drawn first, then each answered 20 times.

fn count_great_enough_nodes(vals: &[i64], left: &[i64], right: &[i64], k: usize) -> i64 {
    let n = vals.len();
    let mut order = Vec::new();
    let mut stack = vec![0usize];
    while let Some(u) = stack.pop() {
        order.push(u);
        for &c in &[left[u], right[u]] {
            if c >= 0 {
                stack.push(c as usize);
            }
        }
    }
    let mut least: Vec<Vec<i64>> = vec![Vec::new(); n];
    let mut great = 0i64;
    for &u in order.iter().rev() {
        let mut mine = vec![vals[u]];
        for &c in &[left[u], right[u]] {
            if c >= 0 {
                mine.extend(least[c as usize].iter());
            }
        }
        mine.sort();
        mine.truncate(k);
        if mine.len() == k && mine[k - 1] < vals[u] {
            great += 1;
        }
        least[u] = mine;
    }
    great
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let count = 20;
    let rounds = 20;
    let n = 10000usize;
    let mut rng = Rng(2792);
    let mut cases = Vec::new();
    for _ in 0..count {
        let vals: Vec<i64> = (0..n).map(|_| rng.next_random() % 10000 + 1).collect();
        let mut left = vec![-1i64; n];
        let mut right = vec![-1i64; n];
        for i in 1..n {
            loop {
                let p = (rng.next_random() % i as i64) as usize;
                if rng.next_random() % 2 == 0 {
                    if left[p] < 0 {
                        left[p] = i as i64;
                        break;
                    }
                } else if right[p] < 0 {
                    right[p] = i as i64;
                    break;
                }
            }
        }
        cases.push((vals, left, right));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (vals, left, right) in &cases {
            let a = count_great_enough_nodes(vals, left, right, 10);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} trees of 10^4, {rounds} rounds: great enough sum to {total}, checksum {check}");
}
