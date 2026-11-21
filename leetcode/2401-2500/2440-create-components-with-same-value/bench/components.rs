// LeetCode #2440: Create Components With Same Value -- the bench, the ★
// arm: each component count dividing the total, from `n` down, checked by
// gathering subtree sums in reverse breadth-first order.

fn fits(order: &[usize], parent: &[usize], nums: &[i64], target: i64) -> bool {
    let mut sum = nums.to_vec();
    let mut i = order.len();
    while i > 0 {
        i -= 1;
        let u = order[i];
        if sum[u] > target {
            return false;
        }
        if sum[u] < target {
            if u == 0 {
                return false;
            }
            sum[parent[u]] += sum[u];
        }
    }
    true
}

fn component_value(nums: &[i64], edges: &[Vec<usize>]) -> i64 {
    let n = nums.len();
    let mut adjacent: Vec<Vec<usize>> = vec![Vec::new(); n];
    for e in edges {
        adjacent[e[0]].push(e[1]);
        adjacent[e[1]].push(e[0]);
    }
    let mut parent = vec![usize::MAX; n];
    let mut order = vec![0usize];
    let mut seen = vec![false; n];
    seen[0] = true;
    let mut head = 0;
    while head < order.len() {
        let u = order[head];
        head += 1;
        for &v in &adjacent[u] {
            if !seen[v] {
                seen[v] = true;
                parent[v] = u;
                order.push(v);
            }
        }
    }
    let mut total = 0i64;
    for &x in nums {
        total += x;
    }
    let mut k = n as i64;
    while k > 1 {
        if total % k == 0 && fits(&order, &parent, nums, total / k) {
            return k - 1;
        }
        k -= 1;
    }
    0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2440i64;
    let n = 20000usize;
    let mut trees: Vec<Vec<Vec<usize>>> = Vec::new();
    let mut values: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut edges = Vec::new();
        for i in 1..n {
            edges.push(vec![(next_random(&mut seed) % i as i64) as usize, i]);
        }
        let mut nums = Vec::new();
        for _ in 0..n {
            nums.push(1 + next_random(&mut seed) % 50);
        }
        trees.push(edges);
        values.push(nums);
    }
    let mut check = 0i64;
    for p in 0..50i64 {
        for c in 0..trees.len() {
            let at = ((p * 7919 + c as i64 * 104729) % n as i64) as usize;
            values[c][at] = 1 + next_random(&mut seed) % 50;
            check = (check * 31 + component_value(&values[c], &trees[c]) + p) % 1000000007;
        }
    }
    println!("50 passes over 10 trees of 2 * 10^4 nodes: checksum {}", check);
}
