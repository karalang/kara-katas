// LeetCode #2140: Solving Questions With Brainpower -- the benchmark, the
// same algorithm as brainpower.kara.

fn most_points(questions: &[Vec<i64>]) -> i64 {
    let n = questions.len();
    let mut best = vec![0i64; n + 1];
    for i in (0..n).rev() {
        let next = (i + 1 + questions[i][1] as usize).min(n);
        best[i] = best[i + 1].max(questions[i][0] + best[next]);
    }
    best[0]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2140;
    let mut lists: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..10 {
        let mut questions = Vec::new();
        for _ in 0..100000 {
            let points = next_random(&mut seed) % 100000 + 1;
            let brainpower = next_random(&mut seed) % 21;
            questions.push(vec![points, brainpower]);
        }
        lists.push(questions);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..20 {
        for l in 0..10 {
            let hi = next_random(&mut seed);
            let at = ((hi * 32768 + next_random(&mut seed)) % 100000) as usize;
            lists[l][at][0] = next_random(&mut seed) % 100000 + 1;
            lists[l][at][1] = next_random(&mut seed) % 21;
            let points = most_points(&lists[l]);
            total += points;
            check = (check * 31 + points + round) % 1000000007;
        }
    }
    println!("200 solves: {} points in all, checksum {}", total, check);
}
