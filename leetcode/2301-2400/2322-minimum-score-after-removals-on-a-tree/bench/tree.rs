// LeetCode #2322: Minimum Score After Removals on a Tree -- the bench, the
// ★ arm in Rust. Rooted at 0, two removals are two nodes other than the
// root; one walk gives each subtree's XOR and each node's entry and exit
// times, and the three parts follow from whether one node is the other's
// ancestor. O(n^2).

fn visit(node: usize, parent: usize, adjacent: &[Vec<usize>], nums: &[i64], xor: &mut [i64], enter: &mut [usize], leave: &mut [usize], clock: &mut usize) {
    enter[node] = *clock;
    *clock += 1;
    xor[node] = nums[node];
    for &next in &adjacent[node] {
        if next != parent {
            visit(next, node, adjacent, nums, xor, enter, leave, clock);
            xor[node] ^= xor[next];
        }
    }
    leave[node] = *clock;
}

fn minimum_score(nums: &[i64], edges: &[[usize; 2]]) -> i64 {
    let n = nums.len();
    let mut adjacent: Vec<Vec<usize>> = vec![Vec::new(); n];
    for e in edges {
        adjacent[e[0]].push(e[1]);
        adjacent[e[1]].push(e[0]);
    }
    let mut xor = vec![0i64; n];
    let mut enter = vec![0usize; n];
    let mut leave = vec![0usize; n];
    let mut clock = 0;
    visit(0, usize::MAX, &adjacent, nums, &mut xor, &mut enter, &mut leave, &mut clock);
    let whole = xor[0];
    let mut best = i64::MAX;
    for a in 1..n {
        for b in (a + 1)..n {
            let (x, y, z) = if enter[a] <= enter[b] && leave[b] <= leave[a] {
                (xor[b], xor[a] ^ xor[b], whole ^ xor[a])
            } else if enter[b] <= enter[a] && leave[a] <= leave[b] {
                (xor[a], xor[b] ^ xor[a], whole ^ xor[b])
            } else {
                (xor[a], xor[b], whole ^ xor[a] ^ xor[b])
            };
            best = best.min(x.max(y).max(z) - x.min(y).min(z));
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: usize = 1000;
    let mut seed: i64 = 2322;
    let mut values: Vec<Vec<i64>> = Vec::new();
    let mut shapes: Vec<Vec<[usize; 2]>> = Vec::new();
    for _ in 0..10 {
        values.push((0..n).map(|_| next_random(&mut seed) % 100000000 + 1).collect());
        shapes.push((1..n).map(|i| [(next_random(&mut seed) % i as i64) as usize, i]).collect());
    }
    let mut check: i64 = 0;
    for _ in 0..30 {
        for k in 0..10 {
            let i = (next_random(&mut seed) % n as i64) as usize;
            values[k][i] = next_random(&mut seed) % 100000000 + 1;
            check = (check * 31 + minimum_score(&values[k], &shapes[k])) % 1000000007;
        }
    }
    println!("30 passes over 10 trees of 1000 nodes: checksum {}", check);
}
