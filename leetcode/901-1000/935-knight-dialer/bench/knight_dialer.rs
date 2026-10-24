// LeetCode #935: Knight Dialer -- bench: counts by last digit, one jump
// at a time. Mirrors knight_dialer.kara, .c, .py and go-seq/.

fn knight_dialer(n: i64) -> i64 {
    let modulus: i64 = 1000000007;
    let jumps: Vec<Vec<usize>> = vec![
        vec![4, 6],
        vec![6, 8],
        vec![7, 9],
        vec![4, 8],
        vec![0, 3, 9],
        Vec::new(),
        vec![0, 1, 7],
        vec![2, 6],
        vec![1, 3],
        vec![2, 4],
    ];
    let mut counts: Vec<i64> = vec![1; 10];
    for _ in 1..n {
        let mut next: Vec<i64> = vec![0; 10];
        for d in 0..10 {
            for from in jumps[d].iter() {
                next[d] = (next[d] + counts[*from]) % modulus;
            }
        }
        counts = next;
    }
    let mut total: i64 = 0;
    for c in counts.iter() {
        total = (total + *c) % modulus;
    }
    total
}

fn main() {
    let rounds: i64 = 20;
    let low: i64 = 4901;
    let high: i64 = 5000;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        // each round counts every length from low to high, starting from a
        // different one
        for i in 0..high - low + 1 {
            let n = low + (r + i) % (high - low + 1);
            let a = knight_dialer(n);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    println!(
        "{rounds} rounds over n from {low} to {high}: answers summing to {total}, checksum {check}"
    );
}
