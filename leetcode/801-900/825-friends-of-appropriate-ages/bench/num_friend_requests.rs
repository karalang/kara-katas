// Benchmark for #825: Friends Of Appropriate Ages -- the ★ arm (counts by age).
//
// Mirrors num_friend_requests.kara: the people counted by age once, and
// every pair of ages tested with the statement's three conditions, each
// pair that passes adding one request from every person of the first age
// to every person of the second, but for a person and themself.

fn asks(x: i64, y: i64) -> bool {
    !(2 * y <= x + 14 || y > x || (y > 100 && x < 100))
}

fn num_friend_requests(ages: &[i64]) -> i64 {
    let mut count = vec![0i64; 121];
    for &a in ages {
        count[a as usize] += 1;
    }
    let mut requests = 0;
    for x in 1..121 {
        if count[x] == 0 {
            continue;
        }
        for y in 1..121 {
            if count[y] > 0 && asks(x as i64, y as i64) {
                requests += count[x] * count[y];
                if x == y {
                    requests -= count[x];
                }
            }
        }
    }
    requests
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64usize;
    let rounds = 50000usize;
    let mut seed: i64 = 825;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut ages = Vec::new();
        for _ in 0..20000 {
            ages.push(1 + next_random(&mut seed) % 120);
        }
        lists.push(ages);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let r = num_friend_requests(&lists[round % count]);
        total += r;
        checksum = (checksum * 131 + r) % 1000000007;
    }
    println!("{rounds} rounds of {count} lists: total {total}, checksum {checksum}");
}
