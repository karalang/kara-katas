// LeetCode #2766: Relocate Marbles -- the bench (marbles.kara in Rust):
// the occupied positions in a `HashSet`, each move taking its from
// position out and putting its to position in, sorted at the end.
use std::collections::HashSet;

fn relocate_marbles(nums: &[i64], move_from: &[i64], move_to: &[i64]) -> Vec<i64> {
    let mut occupied: HashSet<i64> = nums.iter().copied().collect();
    for (a, b) in move_from.iter().zip(move_to.iter()) {
        occupied.remove(a);
        occupied.insert(*b);
    }
    let mut places: Vec<i64> = occupied.into_iter().collect();
    places.sort();
    places
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn case(n: i64, moves: i64, top: i64, seed: &mut i64) -> (Vec<i64>, Vec<i64>, Vec<i64>) {
    let nums: Vec<i64> = (0..n).map(|_| wide(seed) % top + 1).collect();
    let mut places: Vec<i64> = Vec::new();
    let mut slot: Vec<i64> = vec![-1; top as usize + 1];
    for &x in nums.iter() {
        if slot[x as usize] < 0 {
            slot[x as usize] = places.len() as i64;
            places.push(x);
        }
    }
    let mut move_from: Vec<i64> = Vec::new();
    let mut move_to: Vec<i64> = Vec::new();
    for _ in 0..moves {
        let a = places[(wide(seed) % places.len() as i64) as usize];
        let b = wide(seed) % top + 1;
        move_from.push(a);
        move_to.push(b);
        if a != b {
            let k = slot[a as usize];
            slot[a as usize] = -1;
            let last = places.pop().unwrap();
            if last != a {
                places[k as usize] = last;
                slot[last as usize] = k;
            }
            if slot[b as usize] < 0 {
                slot[b as usize] = places.len() as i64;
                places.push(b);
            }
        }
    }
    (nums, move_from, move_to)
}

fn main() {
    let count = 20;
    let rounds = 5;
    let mut seed = 2766;
    let cases: Vec<(Vec<i64>, Vec<i64>, Vec<i64>)> = (0..count).map(|_| case(100000, 100000, 1000000, &mut seed)).collect();
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, move_from, move_to) in cases.iter() {
            let places = relocate_marbles(nums, move_from, move_to);
            sum += places.len() as i64;
            check = (check * 31 + places.len() as i64 + r) % 1000000007;
            for &p in places.iter() {
                check = (check * 31 + p) % 1000000007;
            }
        }
    }
    println!("{count} cases of 100000 marbles and moves, {rounds} rounds: {sum} places, checksum {check}");
}
