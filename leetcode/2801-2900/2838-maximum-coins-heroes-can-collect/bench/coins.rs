// LeetCode #2838: Maximum Coins Heroes Can Collect -- the bench, mirrored
// from coins.kara: sorted monsters, prefix sums, a binary search a hero.

fn maximum_coins(heroes: &[i64], monsters: &[i64], coins: &[i64]) -> Vec<i64> {
    let mut pairs: Vec<(i64, i64)> = monsters.iter().cloned().zip(coins.iter().cloned()).collect();
    pairs.sort();
    let mut prefix: Vec<i64> = vec![0];
    for &(_, c) in pairs.iter() {
        prefix.push(prefix[prefix.len() - 1] + c);
    }
    heroes.iter().map(|&h| prefix[pairs.partition_point(|&(p, _)| p <= h)]).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let count = 10;
    let rounds = 5;
    let n = 100000;
    let mut seed = 2838;
    let mut battles: Vec<(Vec<i64>, Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..count {
        let heroes: Vec<i64> = (0..n).map(|_| wide(&mut seed) % 1000000000 + 1).collect();
        let monsters: Vec<i64> = (0..n).map(|_| wide(&mut seed) % 1000000000 + 1).collect();
        let coins: Vec<i64> = (0..n).map(|_| wide(&mut seed) % 1000000000 + 1).collect();
        battles.push((heroes, monsters, coins));
    }
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (heroes, monsters, coins) in battles.iter() {
            for &x in maximum_coins(heroes, monsters, coins).iter() {
                check = (check * 31 + x % 1000000007 + r) % 1000000007;
            }
        }
    }
    println!("{count} battles of {n}, {rounds} rounds: checksum {check}");
}
