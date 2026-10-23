// LeetCode #914: X of a Kind in a Deck of Cards -- bench: Rust mirror of
// the counts' greatest common divisor in has_groups_size_x.kara.

fn gcd(a: i64, b: i64) -> i64 {
    if b == 0 {
        a
    } else {
        gcd(b, a % b)
    }
}

fn has_groups_size_x(deck: &[i64]) -> bool {
    let mut largest = 0;
    for &card in deck {
        largest = largest.max(card);
    }
    let mut count = vec![0i64; (largest + 1) as usize];
    for &card in deck {
        count[card as usize] += 1;
    }
    let mut g = 0;
    for &c in &count {
        g = gcd(g, c);
    }
    g >= 2
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 20000;
    let mut seed = 914;
    let mut deck: Vec<i64> = Vec::new();
    for v in 0..1666 {
        for _ in 0..6 {
            deck.push(v * 6);
        }
    }
    let n = deck.len() as i64;
    let mut yes = 0;
    let mut check = 0i64;
    for r in 0..rounds {
        let high = next_random(&mut seed);
        let i = ((high * 32768 + next_random(&mut seed)) % n) as usize;
        let old = deck[i];
        deck[i] = old + next_random(&mut seed) % 3 * 6;
        if deck[i] > 9995 {
            deck[i] = old;
        }
        if has_groups_size_x(&deck) {
            yes += 1;
            check = (check * 31 + r) % 1000000007;
        }
        deck[i] = old;
    }
    println!(
        "{} rounds over {} cards: {} partitioned, checksum {}",
        rounds, n, yes, check
    );
}
