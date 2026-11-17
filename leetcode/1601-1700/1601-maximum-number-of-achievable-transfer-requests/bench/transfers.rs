// LeetCode #1601: Maximum Number of Achievable Transfer Requests
// -- the bench in Rust, mirroring transfers.kara: every subset of the
// requests as a bit mask, a subset no larger than the best skipped, a
// fresh Vec of net changes per mask, on 100 problems of 16 requests among
// 6 buildings, all drawn first.

fn maximum_requests(n: i32, requests: &[Vec<i32>]) -> i32 {
    let r = requests.len();
    let mut best = 0;
    for mask in 0i64..1 << r {
        let size = mask.count_ones() as i32;
        if size <= best {
            continue;
        }
        let mut net = vec![0i64; n as usize];
        for i in 0..r {
            if mask >> i & 1 == 1 {
                net[requests[i][0] as usize] -= 1;
                net[requests[i][1] as usize] += 1;
            }
        }
        if net.iter().all(|d| *d == 0) {
            best = size;
        }
    }
    best
}

fn main() {
    let mut seed: i64 = 1601;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut problems: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..100 {
        let mut requests = Vec::new();
        for _ in 0..16 {
            let a = (next_random() % 6) as i32;
            let b = (next_random() % 6) as i32;
            requests.push(vec![a, b]);
        }
        problems.push(requests);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for requests in &problems {
        let answer = maximum_requests(6, requests);
        total += answer as i64;
        check = (check * 31 + answer as i64 + 1) % 1000000007;
    }
    println!("100 problems of 16 requests among 6 buildings: total {}, checksum {}", total, check);
}
