// LeetCode #911: Online Election -- bench program, Rust.
//
// The leader after every vote, and a binary search for the time, on one
// election of 1,000,000 votes among 1,000 people, built once. Each query
// asks for the leader at a random time and folds the answer into a
// checksum; 2,000,000 queries.

struct TopVotedCandidate {
    times: Vec<i64>,
    leaders: Vec<i64>,
}

impl TopVotedCandidate {
    fn new(persons: &[i64], times: &[i64]) -> TopVotedCandidate {
        let n = persons.len();
        let mut count: Vec<i64> = vec![0; n];
        let mut leaders: Vec<i64> = Vec::new();
        let mut leader = persons[0];
        for i in 0..n {
            let p = persons[i];
            count[p as usize] += 1;
            if count[p as usize] >= count[leader as usize] {
                leader = p;
            }
            leaders.push(leader);
        }
        TopVotedCandidate { times: times.to_vec(), leaders }
    }

    fn q(&self, t: i64) -> i64 {
        let mut lo = 0;
        let mut hi = self.times.len();
        while hi - lo > 1 {
            let mid = (lo + hi) / 2;
            if self.times[mid] <= t {
                lo = mid;
            } else {
                hi = mid;
            }
        }
        self.leaders[lo]
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 1000000;
    let queries = 2000000;
    let mut seed: i64 = 911;
    let mut persons: Vec<i64> = Vec::new();
    let mut times: Vec<i64> = Vec::new();
    let mut at: i64 = 0;
    for _ in 0..n {
        persons.push(next_random(&mut seed) % 1000);
        times.push(at);
        at += 1 + next_random(&mut seed) % 1000;
    }
    let e = TopVotedCandidate::new(&persons, &times);
    let mut check: i64 = 0;
    for _ in 0..queries {
        let high = next_random(&mut seed);
        let t = (high * 32768 + next_random(&mut seed)) % at;
        check = (check * 31 + e.q(t)) % 1000000007;
    }
    println!("{} votes, {} queries: checksum {}", n, queries, check);
}
