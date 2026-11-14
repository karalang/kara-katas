// LeetCode #2127: Maximum Employees to Be Invited to a Meeting -- the
// benchmark, the same algorithm as invitations.kara.
use std::collections::VecDeque;

fn maximum_invitations(favorite: &[i64]) -> i64 {
    let n = favorite.len();
    let mut indegree = vec![0i64; n];
    for &f in favorite {
        indegree[f as usize] += 1;
    }
    let mut chain = vec![0i64; n];
    let mut queue: VecDeque<usize> = VecDeque::new();
    for i in 0..n {
        if indegree[i] == 0 {
            queue.push_back(i);
        }
    }
    while let Some(i) = queue.pop_front() {
        let f = favorite[i] as usize;
        chain[f] = chain[f].max(chain[i] + 1);
        indegree[f] -= 1;
        if indegree[f] == 0 {
            queue.push_back(f);
        }
    }
    let mut largest_cycle = 0;
    let mut pairs = 0;
    for i in 0..n {
        if indegree[i] == 0 {
            continue;
        }
        let mut length = 0;
        let mut j = i;
        while indegree[j] != 0 {
            indegree[j] = 0;
            length += 1;
            j = favorite[j] as usize;
        }
        if length == 2 {
            pairs += 2 + chain[i] + chain[favorite[i] as usize];
        } else {
            largest_cycle = largest_cycle.max(length);
        }
    }
    largest_cycle.max(pairs)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    let n: i64 = 100000;
    let mut seed = 2127;
    let mut tables: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut favorite: Vec<i64> = Vec::new();
        for i in 0..n {
            if i < n / 4 {
                favorite.push(i ^ 1);
            } else {
                favorite.push((i + 1 + big(&mut seed) % (n - 1)) % n);
            }
        }
        tables.push(favorite);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..10 {
        for t in 0..20 {
            let i = n / 4 + big(&mut seed) % (n - n / 4);
            tables[t][i as usize] = (i + 1 + big(&mut seed) % (n - 1)) % n;
            let invited = maximum_invitations(&tables[t]);
            total += invited;
            check = (check * 31 + invited + round) % 1000000007;
        }
    }
    println!("200 solves: {} invited, checksum {}", total, check);
}
