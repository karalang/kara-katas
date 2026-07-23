use std::collections::HashMap;

struct TwoSum {
    counts: HashMap<i64, i64>,
}

fn new_two_sum() -> TwoSum {
    TwoSum { counts: HashMap::new() }
}

fn add(ds: &mut TwoSum, number: i64) {
    *ds.counts.entry(number).or_insert(0) += 1;
}

fn find(ds: &TwoSum, value: i64) -> bool {
    let mut found = false;
    for k in ds.counts.keys() {
        let complement = value - k;
        if complement == *k {
            if let Some(c) = ds.counts.get(k) {
                if *c >= 2 {
                    found = true;
                }
            }
        } else if ds.counts.get(&complement).is_some() {
            found = true;
        }
    }
    found
}

fn main() {
    let k_range: i64 = 6000;
    let n_add: i64 = 170;
    let m_query: i64 = 1200000;

    let mut ds = new_two_sum();
    let mut state: i64 = 12345;
    for _ in 0..n_add {
        state = (state * 1103515245 + 12345) & 2147483647;
        add(&mut ds, state % k_range);
    }

    let mut sink: i64 = 0;
    for _ in 0..m_query {
        state = (state * 1103515245 + 12345) & 2147483647;
        let target = state % (2 * k_range);
        if find(&ds, target) {
            sink += 1;
        }
    }
    println!("{}", sink);
}
