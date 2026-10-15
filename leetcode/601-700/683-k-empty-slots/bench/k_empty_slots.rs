// LeetCode #683: K Empty Slots -- a window over the days. Bench.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn k_empty_slots(bulbs: &[i64], k: i64) -> i64 {
    let n = bulbs.len() as i64;
    let mut days = vec![0i64; n as usize];
    for d in 0..n {
        days[(bulbs[d as usize] - 1) as usize] = d + 1;
    }
    let (mut best, mut left, mut right, mut i) = (-1i64, 0i64, k + 1, 1i64);
    while right < n {
        let (l, r, m) = (left as usize, right as usize, i as usize);
        if i == right {
            let day = days[l].max(days[r]);
            if best == -1 || day < best {
                best = day;
            }
            left = right;
            right = left + k + 1;
            i = left + 1;
        } else if days[m] < days[l] || days[m] < days[r] {
            left = i;
            right = left + k + 1;
            i = left + 1;
        } else {
            i += 1;
        }
    }
    best
}

fn main() {
    let (count, n, rounds) = (100i64, 20000i64, 30i64);
    let mut seed: i64 = 683;
    let mut orders: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut v: Vec<i64> = (1..=n).collect();
        let mut i = n - 1;
        while i > 0 {
            let a = next_random(&mut seed);
            let j = (a * 32768 + next_random(&mut seed)) % (i + 1);
            v.swap(i as usize, j as usize);
            i -= 1;
        }
        orders.push(v);
    }
    let (mut sum, mut none) = (0i64, 0i64);
    for r in 0..rounds {
        for c in 0..count {
            let k = (c * 7 + r) % 50;
            let day = k_empty_slots(&orders[c as usize], k);
            if day == -1 {
                none += 1;
            }
            sum = (sum * 31 + day + 2) % 1000000007;
        }
    }
    println!("{} answers: {} without a day, checksum {}", count * rounds, none, sum);
}
