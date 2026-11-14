// LeetCode #2139: Minimum Moves to Reach Target Score -- the benchmark,
// the same algorithm as moves.kara.

fn min_moves(target: i64, max_doubles: i64) -> i64 {
    let mut target = target;
    let mut doubles = max_doubles;
    let mut moves = 0;
    while target > 1 && doubles > 0 {
        if target % 2 == 1 {
            target -= 1;
        } else {
            target /= 2;
            doubles -= 1;
        }
        moves += 1;
    }
    moves + target - 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2139;
    let mut targets: Vec<i64> = Vec::new();
    for _ in 0..1000 {
        let hi = next_random(&mut seed);
        targets.push((hi * 32768 + next_random(&mut seed)) % 1000000000 + 1);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..4000i64 {
        for i in 0..1000 {
            let moves = min_moves(targets[i] + r, r % 40);
            total += moves;
            check = (check * 31 + moves) % 1000000007;
        }
    }
    println!("4000000 solves: {} moves in all, checksum {}", total, check);
}
