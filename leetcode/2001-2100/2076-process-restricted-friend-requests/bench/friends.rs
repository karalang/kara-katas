// LeetCode #2076: Process Restricted Friend Requests -- Rust mirror of the
// ★ arm's benchmark (friends.kara): 400 problems of 1000 people, 1000
// restrictions and 1000 requests; a union-find of parents in a `Vec`,
// found with path halving, every restriction tried against a request
// between two groups.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_pairs(n: i64, count: i64, seed: &mut i64) -> Vec<Vec<i64>> {
    let mut pairs = Vec::new();
    for _ in 0..count {
        let a = next_random(seed) % n;
        let b = (a + 1 + next_random(seed) % (n - 1)) % n;
        pairs.push(vec![a, b]);
    }
    pairs
}

fn find(parent: &mut Vec<i64>, x: i64) -> i64 {
    let mut x = x;
    while parent[x as usize] != x {
        parent[x as usize] = parent[parent[x as usize] as usize];
        x = parent[x as usize];
    }
    x
}

fn friend_requests(n: i64, restrictions: &[Vec<i64>], requests: &[Vec<i64>]) -> Vec<bool> {
    let mut parent: Vec<i64> = (0..n).collect();
    let mut answers = Vec::new();
    for request in requests {
        let a = find(&mut parent, request[0]);
        let b = find(&mut parent, request[1]);
        let mut allowed = true;
        if a != b {
            for r in restrictions {
                let x = find(&mut parent, r[0]);
                let y = find(&mut parent, r[1]);
                if (x == a && y == b) || (x == b && y == a) {
                    allowed = false;
                    break;
                }
            }
            if allowed {
                parent[a as usize] = b;
            }
        }
        answers.push(allowed);
    }
    answers
}

fn main() {
    let mut seed = 2076;
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..400 {
        let restrictions = random_pairs(1000, 1000, &mut seed);
        let requests = random_pairs(1000, 1000, &mut seed);
        for a in friend_requests(1000, &restrictions, &requests) {
            let bit = if a { 1 } else { 0 };
            total += bit;
            check = (check * 3 + bit + 1) % 1000000007;
        }
    }
    println!("400 problems: {} accepted, checksum {}", total, check);
}
