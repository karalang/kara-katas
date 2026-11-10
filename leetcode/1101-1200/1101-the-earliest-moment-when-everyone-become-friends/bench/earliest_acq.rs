// Benchmark: LeetCode #1101 The Earliest Moment When Everyone Become
// Friends -- union-find over the logs in time order, as the Kāra ★ arm.
// Mirrors earliest_acq.kara.

fn find(parent: &mut Vec<i64>, x: i64) -> i64 {
    let mut x = x;
    while parent[x as usize] != x {
        parent[x as usize] = parent[parent[x as usize] as usize];
        x = parent[x as usize];
    }
    x
}

fn earliest_acq(logs: &Vec<Vec<i64>>, n: i64) -> i64 {
    let mut logs = logs.clone();
    logs.sort_by_key(|log| log[0]);
    let mut parent: Vec<i64> = (0..n).collect();
    let mut size: Vec<i64> = vec![1; n as usize];
    let mut groups = n;
    for log in logs.iter() {
        let a = find(&mut parent, log[1]);
        let b = find(&mut parent, log[2]);
        if a == b {
            continue;
        }
        let (big, small) = if size[a as usize] >= size[b as usize] { (a, b) } else { (b, a) };
        parent[small as usize] = big;
        size[big as usize] += size[small as usize];
        groups -= 1;
        if groups == 1 {
            return log[0];
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1101;
    let mut groups: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..64 {
        let mut times: Vec<i64> = (0..4950).collect();
        for i in (1..4950usize).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            times.swap(i, j);
        }
        let mut logs: Vec<Vec<i64>> = Vec::new();
        for x in 0..100i64 {
            for y in x + 1..100 {
                logs.push(vec![times[logs.len()] * 1000, x, y]);
            }
        }
        groups.push(logs);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..20i64 {
        for j in 0..groups.len() {
            let a = ((round * 7919 + j as i64 * 104729) % 4950) as usize;
            let b = ((round * 31 + j as i64 * 17 + 1) % 4950) as usize;
            let t = groups[j][a][0];
            groups[j][a][0] = groups[j][b][0];
            groups[j][b][0] = t;
            let moment = earliest_acq(&groups[j], 100);
            total += moment;
            check = (check * 31 + moment + 2) % 1000000007;
        }
    }
    println!("20 rounds over 64 groups of 100 people: moments sum to {}, checksum {}", total, check);
}
