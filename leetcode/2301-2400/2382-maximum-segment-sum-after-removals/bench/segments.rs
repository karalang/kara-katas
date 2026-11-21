// LeetCode #2382: Maximum Segment Sum After Removals -- the bench, the ★
// arm in Rust: the removals undone in reverse with a union-find, each
// root keeping its segment's sum.

fn find(parent: &mut [i64], x: i64) -> i64 {
    let mut root = x;
    while parent[root as usize] != root {
        parent[root as usize] = parent[parent[root as usize] as usize];
        root = parent[root as usize];
    }
    root
}

fn join(parent: &mut [i64], sum: &mut [i64], a: i64, b: i64) {
    let ra = find(parent, a);
    let rb = find(parent, b);
    if ra != rb {
        parent[ra as usize] = rb;
        sum[rb as usize] += sum[ra as usize];
    }
}

fn maximum_segment_sum(nums: &[i64], remove_queries: &[i64]) -> Vec<i64> {
    let n = nums.len();
    let mut parent: Vec<i64> = (0..n as i64).collect();
    let mut sum: Vec<i64> = vec![0; n];
    let mut back: Vec<bool> = vec![false; n];
    let mut answer: Vec<i64> = vec![0; n];
    let mut best = 0i64;
    for k in (1..n).rev() {
        let x = remove_queries[k];
        let xi = x as usize;
        back[xi] = true;
        sum[xi] = nums[xi];
        if x > 0 && back[xi - 1] {
            join(&mut parent, &mut sum, x - 1, x);
        }
        if xi + 1 < n && back[xi + 1] {
            join(&mut parent, &mut sum, x + 1, x);
        }
        best = best.max(sum[find(&mut parent, x) as usize]);
        answer[k - 1] = best;
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    // 10 arrays of 10^5 values, array a's values from 1 to 10^a, each with
    // its own random order of removals
    let mut seed = 2382i64;
    let n = 100000i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut orders: Vec<Vec<i64>> = Vec::new();
    for a in 0..10 {
        let mut top = 1i64;
        for _ in 0..a {
            top *= 10;
        }
        arrays.push((0..n).map(|_| 1 + wide(&mut seed) % top).collect());
        let mut order: Vec<i64> = (0..n).collect();
        for i in (1..n).rev() {
            let j = wide(&mut seed) % (i + 1);
            order.swap(i as usize, j as usize);
        }
        orders.push(order);
    }
    let mut check = 0i64;
    for p in 0..10i64 {
        for a in 0..10 {
            let answer = maximum_segment_sum(&arrays[a], &orders[a]);
            for &v in &answer {
                check = (check * 31 + v + p) % 1000000007;
            }
        }
    }
    println!("10 passes over 10 arrays of 10^5 values: checksum {}", check);
}
