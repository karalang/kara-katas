// Benchmark: LeetCode #1094 Car Pooling -- the ★ arm, a difference array
// over the stops. Mirrors car_pooling.kara.

fn car_pooling(trips: &[Vec<i64>], capacity: i64) -> bool {
    let mut change = vec![0i64; 1001];
    for t in trips.iter() {
        change[t[1] as usize] += t[0];
        change[t[2] as usize] -= t[0];
    }
    let mut aboard = 0;
    for c in change.iter() {
        aboard += c;
        if aboard > capacity {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1094;
    let mut lists: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..64 {
        let mut trips: Vec<Vec<i64>> = Vec::new();
        for _ in 0..1000 {
            let n = next_random(&mut seed) % 100 + 1;
            let a = next_random(&mut seed) % 1000;
            let b = a + 1 + next_random(&mut seed) % (1000 - a);
            trips.push(vec![n, a, b]);
        }
        lists.push(trips);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..100usize {
        for j in 0..lists.len() {
            let k = (round * 7 + j * 13) % 1000;
            lists[j][k][0] = 1 + (lists[j][k][0] + round as i64) % 100;
            let (mut lo, mut hi) = (1i64, 100000i64);
            while lo < hi {
                let mid = (lo + hi) / 2;
                if car_pooling(&lists[j], mid) {
                    hi = mid;
                } else {
                    lo = mid + 1;
                }
            }
            total += lo;
            check = (check * 31 + lo) % 1000000007;
        }
    }
    println!("100 rounds over 64 lists of 1000 trips: smallest capacities sum to {}, checksum {}", total, check);
}
