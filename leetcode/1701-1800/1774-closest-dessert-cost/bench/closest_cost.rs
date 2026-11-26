// LeetCode #1774: Closest Dessert Cost -- the bench in Rust, mirroring
// closest_cost.kara: a depth-first search over the toppings for each base.
fn better(cost: i32, best: i32, target: i32) -> bool {
    let (d, e) = ((cost - target).abs(), (best - target).abs());
    d < e || (d == e && cost < best)
}

fn add_toppings(toppings: &[i32], i: usize, cost: i32, target: i32, best: &mut i32) {
    if better(cost, *best, target) {
        *best = cost;
    }
    if i == toppings.len() || cost >= target {
        return;
    }
    for times in 0..3 {
        add_toppings(toppings, i + 1, cost + times * toppings[i], target, best);
    }
}

fn closest_cost(base_costs: &[i32], topping_costs: &[i32], target: i32) -> i32 {
    let mut best = base_costs[0];
    for &base in base_costs {
        add_toppings(topping_costs, 0, base, target, &mut best);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_costs(seed: &mut i64, n: usize, most: i64) -> Vec<i32> {
    (0..n).map(|_| (1 + next_random(seed) % most) as i32).collect()
}

fn main() {
    let mut seed: i64 = 1774;
    let mut bases: Vec<Vec<i32>> = Vec::new();
    let mut toppings: Vec<Vec<i32>> = Vec::new();
    for _ in 0..100 {
        bases.push(random_costs(&mut seed, 10, 5000));
        toppings.push(random_costs(&mut seed, 8, 1000));
    }
    let mut check: i64 = 0;
    for call in 0..1000i64 {
        let target = (1 + (check + call * 7919) % 10000) as i32;
        let cost = closest_cost(&bases[((check + call) % 100) as usize], &toppings[((check / 100 + call * 31) % 100) as usize], target);
        check = (check * 31 + cost as i64) % 1000000007;
    }
    println!("1000 calls over 100 menus: checksum {}", check);
}
