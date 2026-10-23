// LeetCode #932: Beautiful Array -- bench: divide and conquer with a
// memo. Mirrors beautiful_array.kara, .c, .py and go-seq/.

use std::collections::HashMap;

fn build(n: i64, memo: &mut HashMap<i64, Vec<i64>>) -> Vec<i64> {
    if let Some(done) = memo.get(&n) {
        return done.clone();
    }
    let mut out: Vec<i64> = Vec::new();
    if n == 1 {
        out.push(1);
    } else {
        for x in build((n + 1) / 2, memo).iter() {
            out.push(2 * *x - 1);
        }
        for x in build(n / 2, memo).iter() {
            out.push(2 * *x);
        }
    }
    memo.insert(n, out.clone());
    out
}

fn beautiful_array(n: i64) -> Vec<i64> {
    let mut memo: HashMap<i64, Vec<i64>> = HashMap::new();
    build(n, &mut memo)
}

fn main() {
    let rounds: i64 = 100;
    let top: i64 = 1000;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        // each round builds the array for every n from 1 to top, starting
        // from a different n
        for i in 0..top {
            let n = (r + i) % top + 1;
            let nums = beautiful_array(n);
            total += nums[(n / 2) as usize];
            check = (check * 1000003 + nums[(n - 1) as usize]) % 1000000007;
        }
    }
    println!(
        "{rounds} rounds over n from 1 to {top}: middles summing to {total}, checksum {check}"
    );
}
