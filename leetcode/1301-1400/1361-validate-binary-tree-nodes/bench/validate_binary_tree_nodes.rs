// LeetCode #1361 bench -- Rust: every node's parents counted, one root and
// no node with two, then a search from the root that must reach all n.

fn validate_binary_tree_nodes(n: i32, left_child: &[i32], right_child: &[i32]) -> bool {
    let n = n as usize;
    let mut parents = vec![0i64; n];
    for i in 0..n {
        for child in [left_child[i], right_child[i]] {
            if child != -1 {
                parents[child as usize] += 1;
            }
        }
    }
    let mut root: i64 = -1;
    for i in 0..n {
        if parents[i] > 1 {
            return false;
        }
        if parents[i] == 0 {
            if root != -1 {
                return false;
            }
            root = i as i64;
        }
    }
    if root == -1 {
        return false;
    }
    let mut seen = vec![false; n];
    let mut queue = vec![root as usize];
    let mut head = 0;
    while head < queue.len() {
        let node = queue[head];
        head += 1;
        if seen[node] {
            return false;
        }
        seen[node] = true;
        for child in [left_child[node], right_child[node]] {
            if child != -1 {
                queue.push(child as usize);
            }
        }
    }
    head == n
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// n nodes made into one binary tree, each node after the first hung on a
// free side of a node already placed; then, one time in two, broken or not
fn random_case(seed: &mut i64, n: i64) -> (Vec<i32>, Vec<i32>) {
    let mut left = vec![-1i32; n as usize];
    let mut right = vec![-1i32; n as usize];
    let mut order: Vec<i64> = (0..n).collect();
    for i in 1..n {
        let j = next_random(seed) % (i + 1);
        order.swap(i as usize, j as usize);
    }
    for i in 1..n {
        loop {
            let parent = order[(next_random(seed) % i) as usize] as usize;
            if next_random(seed) % 2 == 0 {
                if left[parent] == -1 {
                    left[parent] = order[i as usize] as i32;
                    break;
                }
            } else if right[parent] == -1 {
                right[parent] = order[i as usize] as i32;
                break;
            }
        }
    }
    let node = (next_random(seed) % n) as usize;
    let other = (next_random(seed) % n) as i32;
    match next_random(seed) % 6 {
        0 => {
            if left[node] == -1 {
                left[node] = other;
            } else if right[node] == -1 {
                right[node] = other;
            }
        }
        1 => left[node] = -1,
        2 => {
            if right[node] != -1 {
                right[node] = other;
            }
        }
        _ => {}
    }
    (left, right)
}

fn main() {
    // 20 sets of 5000 nodes made once; then 5000 questions, each set drawn
    // from the checksum so far, every answer folded into it
    let mut seed = 1361;
    let sets: Vec<(Vec<i32>, Vec<i32>)> = (0..20).map(|_| random_case(&mut seed, 5000)).collect();
    let mut check: i64 = 0;
    for r in 0..5000 {
        let (left, right) = &sets[(check % 20) as usize];
        let got = validate_binary_tree_nodes(5000, left, right);
        check = (check * 31 + if got { 1 } else { 0 } + r) % 1000000007;
    }
    println!("5000 questions: checksum {}", check);
}
