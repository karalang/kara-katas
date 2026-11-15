// LeetCode #1583 bench: the same table of ranks, in Rust.

fn unhappy_friends(n: usize, preferences: &[Vec<i64>], pairs: &[Vec<i64>]) -> i64 {
    let mut rank = vec![vec![0usize; n]; n];
    for x in 0..n {
        for (r, &f) in preferences[x].iter().enumerate() {
            rank[x][f as usize] = r;
        }
    }
    let mut partner = vec![0usize; n];
    for p in pairs.iter() {
        partner[p[0] as usize] = p[1] as usize;
        partner[p[1] as usize] = p[0] as usize;
    }
    let mut unhappy = 0;
    for x in 0..n {
        let y = partner[x];
        for &u in preferences[x].iter().take(rank[x][y]) {
            let u = u as usize;
            if rank[u][x] < rank[u][partner[u]] {
                unhappy += 1;
                break;
            }
        }
    }
    unhappy
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn shuffled(n: i64, seed: &mut i64) -> Vec<i64> {
    let mut v: Vec<i64> = (0..n).collect();
    for i in (1..n as usize).rev() {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        v.swap(i, j);
    }
    v
}

fn main() {
    let n = 500i64;
    let mut seed = 1583i64;
    let mut problems: Vec<(Vec<Vec<i64>>, Vec<Vec<i64>>)> = Vec::new();
    for _ in 0..40 {
        let mut preferences: Vec<Vec<i64>> = Vec::new();
        for x in 0..n {
            let order = shuffled(n, &mut seed);
            preferences.push(order.iter().copied().filter(|&f| f != x).collect());
        }
        let line = shuffled(n, &mut seed);
        let pairs: Vec<Vec<i64>> = (0..(n / 2) as usize).map(|k| vec![line[2 * k], line[2 * k + 1]]).collect();
        problems.push((preferences, pairs));
    }
    let (mut check, mut total) = (0i64, 0i64);
    for (preferences, pairs) in problems.iter() {
        let unhappy = unhappy_friends(n as usize, preferences, pairs);
        total += unhappy;
        check = mix(check, unhappy);
    }
    println!("40 problems of 500 friends: unhappy {}, checksum {}", total, check);
}
