// Benchmark for #638: mirror of shopping_offers.kara (the ★ arm: search
// over what is still needed, with a memo keyed by the needs) on the same
// workload. The memo is a HashMap keyed by the Vec of needs, and every
// offer tried builds the Vec it leaves, as the Kāra does.
use std::collections::HashMap;

fn cheapest(price: &[i64], special: &[Vec<i64>], needs: &Vec<i64>, memo: &mut HashMap<Vec<i64>, i64>) -> i64 {
    if let Some(&known) = memo.get(needs) {
        return known;
    }
    let n = needs.len();
    let mut best = 0;
    for i in 0..n {
        best += needs[i] * price[i];
    }
    for offer in special {
        let mut rest: Vec<i64> = Vec::new();
        let mut fits = true;
        let mut any = false;
        for i in 0..n {
            if offer[i] > needs[i] {
                fits = false;
            }
            if offer[i] > 0 {
                any = true;
            }
            rest.push(needs[i] - offer[i]);
        }
        if fits && any {
            let cost = offer[n] + cheapest(price, special, &rest, memo);
            if cost < best {
                best = cost;
            }
        }
    }
    memo.insert(needs.clone(), best);
    best
}

fn shopping_offers(price: &[i64], special: &[Vec<i64>], needs: &Vec<i64>) -> i64 {
    let mut memo: HashMap<Vec<i64>, i64> = HashMap::new();
    cheapest(price, special, needs, &mut memo)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

const ROUNDS: i64 = 800;

fn main() {
    let mut seed: i64 = 638;
    let mut prices: Vec<Vec<i64>> = Vec::new();
    let mut needs: Vec<Vec<i64>> = Vec::new();
    let mut offers: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..20 {
        let mut price = Vec::new();
        let mut need = Vec::new();
        for _ in 0..6 {
            price.push(1 + next_random(&mut seed) % 10);
            need.push(next_random(&mut seed) % 5);
        }
        let mut special = Vec::new();
        for _ in 0..100 {
            let mut offer = Vec::new();
            for _ in 0..6 {
                offer.push(next_random(&mut seed) % 3);
            }
            offer.push(next_random(&mut seed) % 51);
            special.push(offer);
        }
        prices.push(price);
        needs.push(need);
        offers.push(special);
    }
    let mut total = 0;
    let mut checksum = 0;
    for round in 0..ROUNDS {
        let s = (round % 20) as usize;
        let paid = shopping_offers(&prices[s], &offers[s], &needs[s]);
        total += paid;
        checksum = (checksum * 31 + paid) % 1000000007;
    }
    println!("20 shops, {} rounds: total {}, checksum {}", ROUNDS, total, checksum);
}
