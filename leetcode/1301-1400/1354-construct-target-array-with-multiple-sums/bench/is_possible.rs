// LeetCode #1354 bench -- Rust: the moves undone from the target, largest
// value first, in a BinaryHeap with a running total, many undos of one
// value as one remainder.
use std::collections::BinaryHeap;

fn is_possible(target: &[i32]) -> bool {
    if target.len() == 1 {
        return target[0] == 1;
    }
    let mut total: i64 = 0;
    let mut heap: BinaryHeap<i64> = BinaryHeap::new();
    for &x in target {
        total += x as i64;
        heap.push(x as i64);
    }
    loop {
        let x = heap.pop().unwrap();
        let rest = total - x;
        if x == 1 || rest == 1 {
            return true;
        }
        if x <= rest || x % rest == 0 {
            return false;
        }
        let before = x % rest;
        heap.push(before);
        total = rest + before;
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn reached(seed: &mut i64, n: i64, moves: i64, top: i64) -> Vec<i32> {
    let mut arr = vec![1i64; n as usize];
    let mut total = n;
    for _ in 0..moves {
        if total > top {
            break;
        }
        let i = (next_random(seed) % n) as usize;
        let was = arr[i];
        arr[i] = total;
        total = 2 * total - was;
    }
    arr.iter().map(|&x| x as i32).collect()
}

fn main() {
    // 20 targets of 5 * 10^4 values, each reached from the ones by moves
    // until a value would pass 10^9, built once; then 2000 rounds, each
    // changing one place of one target, drawn from the checksum so far,
    // answering, and putting the place back; one round in four leaves the
    // value as it was
    let mut seed = 1354;
    let mut targets: Vec<Vec<i32>> = Vec::new();
    for _ in 0..20 {
        targets.push(reached(&mut seed, 50000, 100, 1000000000));
    }
    let mut check: i64 = 0;
    for r in 0..2000 {
        let k = (check % 20) as usize;
        let at = ((check / 20) % 50000) as usize;
        let was = targets[k][at];
        if r % 4 != 0 {
            targets[k][at] = was + 1 + ((check / 7) % 3) as i32;
        }
        let got = if is_possible(&targets[k]) { 1 } else { 0 };
        targets[k][at] = was;
        check = (check * 31 + got * 1000 + r) % 1000000007;
    }
    println!("2000 rounds over 20 targets of 5 * 10^4 values: checksum {}", check);
}
