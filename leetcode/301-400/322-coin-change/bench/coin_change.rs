// Benchmark mirror of LeetCode #322 — same bottom-up table as
// bench/coin_change.kara.

const AMOUNT: i64 = 1000000;
const COINS: usize = 20;
const TOP: i64 = 3000;
const PASSES: i64 = 24;
const STRIDE: i64 = 9973;
const MODULUS: i64 = 1073741789;

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw(seed: &mut i64, bound: i64) -> i64 {
    let hi = next(seed);
    let lo = next(seed);
    (hi * 32768 + lo) % bound
}

fn fewest(coins: &[i64], amount: i64, best: &mut [i64]) -> i64 {
    let unreachable = amount + 1;
    best[0] = 0;
    for a in 1..=amount {
        let mut b = unreachable;
        for &c in coins {
            if c <= a && best[(a - c) as usize] + 1 < b {
                b = best[(a - c) as usize] + 1;
            }
        }
        best[a as usize] = b;
    }
    if best[amount as usize] == unreachable {
        return -1;
    }
    best[amount as usize]
}

fn main() {
    let mut seed: i64 = 322;
    let mut sink: i64 = 0;
    let mut reached: i64 = 0;
    let mut best = vec![0i64; (AMOUNT + 1) as usize];

    for p in 0..PASSES {
        let g = 1 + p % 3;
        let mut coins: Vec<i64> = Vec::new();
        while coins.len() < COINS {
            let c = g * (draw(&mut seed, TOP / g) + 1);
            if !coins.contains(&c) {
                coins.push(c);
            }
        }
        let amount = AMOUNT / 2 + draw(&mut seed, AMOUNT / 2 + 1);
        let ans = fewest(&coins, amount, &mut best);
        if ans >= 0 {
            reached += 1;
        }
        let mut probe: i64 = 0;
        let mut a: i64 = 0;
        while a <= amount {
            probe = (probe * 31 + best[a as usize]) % MODULUS;
            a += STRIDE;
        }
        sink = (sink * 131 + ans + 1 + probe) % MODULUS;
    }

    println!("sink {} reached {}", sink, reached);
}
