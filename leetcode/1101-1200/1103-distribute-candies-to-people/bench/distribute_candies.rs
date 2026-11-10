// LeetCode #1103: Distribute Candies to People -- the bench in Rust: the
// ★ arm (gifts of 1, 2, 3, ... in turn, the last whatever is left) over
// 64 problems, each round moving every problem's candies.

fn distribute_candies(candies: i64, num_people: i64) -> Vec<i64> {
    let mut people = vec![0i64; num_people as usize];
    let mut left = candies;
    let mut gift = 1i64;
    while left > 0 {
        let given = gift.min(left);
        people[((gift - 1) % num_people) as usize] += given;
        left -= given;
        gift += 1;
    }
    people
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1103i64;
    let mut problems: Vec<(i64, i64)> = Vec::new();
    for _ in 0..64 {
        let hi = next_random(&mut seed);
        let candies = (hi * 32768 + next_random(&mut seed)) % 1000000000 + 1;
        let n = next_random(&mut seed) % 1000 + 1;
        problems.push((candies, n));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..200i64 {
        for j in 0..problems.len() {
            let (candies, n) = problems[j];
            let candies = (candies + round * 7919 + j as i64 * 104729) % 1000000000 + 1;
            problems[j] = (candies, n);
            let people = distribute_candies(candies, n);
            total += people[0] + people[(n - 1) as usize];
            for &c in &people {
                check = (check * 31 + c + 1) % 1000000007;
            }
        }
    }
    println!("200 rounds over 64 problems of up to 10^9 candies: first and last people hold {}, checksum {}", total, check);
}
