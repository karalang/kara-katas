// LeetCode #881 bench: Rust mirror of num_rescue_boats.kara (the ★ arm,
// sort, then two pointers) on the same 600 cases. The sort is
// `sort_unstable`, which `karac build --mir` uses for a `Vec` of integers.

fn num_rescue_boats(people: &[i64], limit: i64) -> i64 {
    let mut weights = people.to_vec();
    weights.sort_unstable();
    let mut light: i64 = 0;
    let mut heavy: i64 = weights.len() as i64 - 1;
    let mut boats = 0;
    while light <= heavy {
        if weights[light as usize] + weights[heavy as usize] <= limit {
            light += 1;
        }
        heavy -= 1;
        boats += 1;
    }
    boats
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 881;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..600 {
        let n = 40000 + next_random(&mut seed) % 10001;
        let x = next_random(&mut seed);
        let y = next_random(&mut seed);
        let limit = 1 + (x * 32768 + y) % 30000;
        let mut people: Vec<i64> = Vec::new();
        for _ in 0..n {
            let a = next_random(&mut seed);
            let b = next_random(&mut seed);
            people.push((a * 32768 + b) % limit + 1);
        }
        let boats = num_rescue_boats(&people, limit);
        total += boats;
        check = (check * 131 + boats) % 1000000007;
    }
    println!("600 cases of up to 50000 people: {} boats, checksum {}", total, check);
}
