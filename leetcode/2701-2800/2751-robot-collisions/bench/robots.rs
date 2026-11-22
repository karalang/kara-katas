// LeetCode #2751: Robot Collisions -- the bench (robots.kara in Rust): the
// robots in order of position, those moving right on a stack, and each
// robot moving left meeting the stack's top in turn.

fn survived_robots_healths(positions: &[i64], healths: &[i64], directions: &str) -> Vec<i64> {
    let n = positions.len();
    let facing = directions.as_bytes();
    let mut health = healths.to_vec();
    let mut order: Vec<usize> = (0..n).collect();
    order.sort_by_key(|&i| positions[i]);
    let mut rightward: Vec<usize> = Vec::new();
    for &i in order.iter() {
        if facing[i] == b'R' {
            rightward.push(i);
            continue;
        }
        while health[i] > 0 {
            let Some(&top) = rightward.last() else { break };
            if health[top] < health[i] {
                health[top] = 0;
                rightward.pop();
                health[i] -= 1;
            } else if health[top] > health[i] {
                health[top] -= 1;
                health[i] = 0;
            } else {
                health[top] = 0;
                rightward.pop();
                health[i] = 0;
            }
        }
    }
    health.into_iter().filter(|&h| h > 0).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 10;
    let rounds = 3;
    let n: i64 = 100000;
    let mut seed = 2751;
    let mut cases: Vec<(Vec<i64>, Vec<i64>, String)> = Vec::new();
    for _ in 0..count {
        let mut positions: Vec<i64> = (0..n).map(|i| i * 10000 + next_random(&mut seed) % 10000 + 1).collect();
        for i in (1..n).rev() {
            let hi = next_random(&mut seed);
            let j = (hi * 32768 + next_random(&mut seed)) % (i + 1);
            positions.swap(i as usize, j as usize);
        }
        let healths: Vec<i64> = (0..n)
            .map(|_| {
                let hi = next_random(&mut seed);
                (hi * 32768 + next_random(&mut seed)) % 1000000000 + 1
            })
            .collect();
        let directions: String = (0..n).map(|_| if next_random(&mut seed) % 2 == 0 { 'L' } else { 'R' }).collect();
        cases.push((positions, healths, directions));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (positions, healths, directions) in cases.iter() {
            let survivors = survived_robots_healths(positions, healths, directions);
            check = (check * 31 + survivors.len() as i64 + r) % 1000000007;
            for &h in survivors.iter() {
                sum += h;
                check = (check * 31 + h) % 1000000007;
            }
        }
    }
    println!("{count} cases of 100000 robots, {rounds} rounds: healths sum to {sum}, checksum {check}");
}
