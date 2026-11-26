// LeetCode #1406 bench, Rust: the same lead from the last stone back,
// workload and checksum as stone_game_iii.kara.

fn stone_game_iii(stone_value: &Vec<i32>) -> String {
    let n = stone_value.len();
    let mut best: Vec<i32> = vec![0; n + 1];
    for i in (0..n).rev() {
        let mut taken: i32 = 0;
        best[i] = i32::MIN;
        for k in 1..=3 {
            if i + k > n {
                break;
            }
            taken += stone_value[i + k - 1];
            best[i] = best[i].max(taken - best[i + k]);
        }
    }
    if best[0] > 0 {
        String::from("Alice")
    } else if best[0] < 0 {
        String::from("Bob")
    } else {
        String::from("Tie")
    }
}

fn main() {
    let mut seed: i64 = 1406;
    let mut pool: Vec<i32> = Vec::new();
    for _ in 0..100000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool.push((seed / 65536 % 41 - 20) as i32);
    }
    let mut check: i64 = 0;
    for r in 0..1000i64 {
        let at = ((check + r * 7919) % 50001) as usize;
        let row = pool[at..at + 50000].to_vec();
        let winner = stone_game_iii(&row);
        let code = if winner == "Alice" { 1 } else if winner == "Bob" { 2 } else { 3 };
        check = (check * 131 + code) % 1000000007;
    }
    println!("1000 rows of 5 * 10^4 stones: checksum {}", check);
}
