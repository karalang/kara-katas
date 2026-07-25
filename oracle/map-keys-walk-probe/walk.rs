// Equal-safety Rust mirror of walk.kara — same algorithm, same extra xor.
use std::collections::HashMap;

#[inline(never)]
fn walk(m: &HashMap<i64, i64>, i: i64) -> i64 {
    let mut s = 0i64;
    for k in m.keys() {
        s ^= k + i;
    }
    s
}

fn main() {
    let mut m: HashMap<i64, i64> = HashMap::new();
    for j in 0..170i64 {
        m.insert(j * 7919, j);
    }
    let mut total = 0i64;
    for i in 0..1_200_000i64 {
        total += walk(&m, i);
    }
    println!("{total}");
}
