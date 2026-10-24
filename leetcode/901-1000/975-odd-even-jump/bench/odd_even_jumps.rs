// Benchmark: LeetCode #975 Odd Even Jump -- the stack arm (sorted order
// and a monotonic stack), on 20 arrays of 20000 random values. Mirrors
// odd_even_jumps.kara, .c, .py and go-seq/.

fn next_in(order: &[usize], n: usize) -> Vec<i64> {
    let mut next = vec![-1i64; n];
    let mut stack: Vec<usize> = Vec::new();
    for &i in order {
        while let Some(&top) = stack.last() {
            if top >= i {
                break;
            }
            stack.pop();
            next[top] = i as i64;
        }
        stack.push(i);
    }
    next
}

fn odd_even_jumps(arr: &[i64]) -> usize {
    let n = arr.len();
    let mut up: Vec<usize> = (0..n).collect();
    up.sort_by_key(|&i| (arr[i], i));
    let mut down: Vec<usize> = (0..n).collect();
    down.sort_by_key(|&i| (-arr[i], i));
    let odd = next_in(&up, n);
    let even = next_in(&down, n);
    let mut higher = vec![false; n];
    let mut lower = vec![false; n];
    higher[n - 1] = true;
    lower[n - 1] = true;
    for i in (0..n - 1).rev() {
        if odd[i] >= 0 {
            higher[i] = lower[odd[i] as usize];
        }
        if even[i] >= 0 {
            lower[i] = higher[even[i] as usize];
        }
    }
    higher.iter().filter(|&&h| h).count()
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let rounds = 10;
    let count = 20;
    let mut rng = Rng(975);
    let arrays: Vec<Vec<i64>> = (0..count)
        .map(|_| (0..20000).map(|_| rng.next() % 100000).collect())
        .collect();
    let mut total = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let good = odd_even_jumps(&arrays[(r + i) % count]);
            total += good;
            check = (check * 31 + good as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} arrays of 20000 values: {total} good starts, checksum {check}");
}
