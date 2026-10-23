// LeetCode #887 bench: the floors a number of moves can cover, on 30000
// cases of 2 to 9 eggs and up to 10^9 floors. The same algorithm as
// super_egg_drop.kara.

fn super_egg_drop(k: usize, n: i64) -> i64 {
    let mut floors = vec![0i64; k + 1];
    let mut moves = 0;
    while floors[k] < n {
        moves += 1;
        for eggs in (1..=k).rev() {
            floors[eggs] = floors[eggs - 1] + floors[eggs] + 1;
        }
    }
    moves
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 887;
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..30000 {
        let k = 2 + next_random(&mut seed) % 8;
        let hi = next_random(&mut seed);
        let n = 1 + (hi * 32768 + next_random(&mut seed)) % 1000000000;
        let moves = super_egg_drop(k as usize, n);
        total += moves;
        check = (check * 131 + moves) % 1000000007;
    }
    println!("30000 cases of 2 to 9 eggs and up to 10^9 floors: {} moves, checksum {}", total, check);
}
