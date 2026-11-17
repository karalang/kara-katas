// LeetCode #2214: Minimum Health to Beat Game -- bench mirror of
// health.kara: the damage summed in one pass with its largest, then the
// sum less what the armor saves on the largest, plus 1.

fn minimum_health(damage: &[i64], armor: i64) -> i64 {
    let mut total = 0;
    let mut worst = 0;
    for &d in damage {
        total += d;
        worst = worst.max(d);
    }
    total - worst.min(armor) + 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2214;
    let mut games: Vec<Vec<i64>> = Vec::new();
    for g in 0..100 {
        // 10^5 levels, the damage up to 10, 1000 and 10^5 in turn
        let top = [10, 1000, 100000][g % 3];
        games.push((0..100000).map(|_| next_random(&mut seed) % (top + 1)).collect());
    }
    let mut check: i64 = 0;
    for g in 0..100 {
        for a in 0..20 {
            // punch: one level hurts a little more before each answer
            games[g][a as usize * 4999] += 1;
            check = (check * 31 + minimum_health(&games[g], a * 5000)) % 1000000007;
        }
    }
    println!("100 games of 10^5, 20 armors: checksum {check}");
}
