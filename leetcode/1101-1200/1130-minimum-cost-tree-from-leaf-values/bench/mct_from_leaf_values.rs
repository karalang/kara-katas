// LeetCode #1130: Minimum Cost Tree From Leaf Values -- the bench in Rust,
// the ★ arm over `Vec<i64>` leaves with a `Vec` stack, the same 4096
// arrays and 400 rounds.

fn mct_from_leaf_values(arr: &[i64]) -> i64 {
    let mut cost = 0;
    let mut stack: Vec<i64> = Vec::new();
    for &a in arr {
        while !stack.is_empty() && stack[stack.len() - 1] <= a {
            let mid = stack.pop().unwrap();
            let partner = match stack.last() {
                Some(&left) => left.min(a),
                None => a,
            };
            cost += mid * partner;
        }
        stack.push(a);
    }
    while stack.len() > 1 {
        let top = stack.pop().unwrap();
        cost += top * stack[stack.len() - 1];
    }
    cost
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1130;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..4096 {
        let arr: Vec<i64> = (0..40).map(|_| next_random(&mut seed) % 15 + 1).collect();
        arrays.push(arr);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..400i64 {
        for j in 0..4096usize {
            let at = ((round * 7919 + j as i64 * 104729) % 40) as usize;
            arrays[j][at] = arrays[j][at] % 15 + 1;
            let c = mct_from_leaf_values(&arrays[j]);
            total += c;
            check = (check * 31 + c) % 1000000007;
        }
    }
    println!("400 rounds over 4096 arrays of 40 leaves: costs total {total}, checksum {check}");
}
