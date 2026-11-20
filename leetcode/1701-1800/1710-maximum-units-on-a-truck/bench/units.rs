// LeetCode #1710: Maximum Units on a Truck -- the Rust mirror of the
// bench (units.kara): the box types sorted by units, most first, and
// boxes taken from the front until the truck is full, on 1000 random
// problems of 1000 box types, each answered 10 times.

fn maximum_units(box_types: &[Vec<i32>], truck_size: i32) -> i32 {
    let mut order = box_types.to_vec();
    order.sort_by_key(|t| -t[1]);
    let mut room = truck_size;
    let mut total: i32 = 0;
    for t in order.iter() {
        let take = t[0].min(room);
        total += take * t[1];
        room -= take;
        if room == 0 {
            break;
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000;
    let rounds: i64 = 10;
    let n = 1000;
    let mut seed: i64 = 1710;
    let mut problems: Vec<(Vec<Vec<i32>>, i32)> = Vec::new();
    for _ in 0..count {
        let mut box_types: Vec<Vec<i32>> = Vec::new();
        for _ in 0..n {
            let b = next_random(&mut seed) % 1000 + 1;
            let u = next_random(&mut seed) % 1000 + 1;
            box_types.push(vec![b as i32, u as i32]);
        }
        let a = next_random(&mut seed);
        let size = (a * 32768 + next_random(&mut seed)) % 1000000 + 1;
        problems.push((box_types, size as i32));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (box_types, size) in problems.iter() {
            let answer = maximum_units(box_types, *size) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} problems of {n} box types, {rounds} rounds: answers sum to {sum}, checksum {check}");
}
