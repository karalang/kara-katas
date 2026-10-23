// LeetCode #898 bench: the table arm (the ★ arm with a hash table of its
// own) on 12 arrays of 50,000 numbers, LeetCode's largest, each a random
// number below 2^30 AND-ed with a second, so that about a quarter of the
// bits are set. The ORs ending at each place are kept in a short list,
// and every one is gathered into an open-addressing hash table written
// here, with no library set, map or sort. The same algorithm as
// subarray_bitwise_ors.kara.

struct Table {
    slots: Vec<i64>,
    count: i64,
}

fn insert(t: &mut Table, v: i64) {
    let mask = t.slots.len() as i64 - 1;
    let mut i = ((v * 2654435761) % 4294967296) & mask;
    while t.slots[i as usize] != -1 {
        if t.slots[i as usize] == v {
            return;
        }
        i = (i + 1) & mask;
    }
    t.slots[i as usize] = v;
    t.count += 1;
    if t.count * 2 > t.slots.len() as i64 {
        let old = t.slots.clone();
        t.slots = vec![-1; old.len() * 2];
        t.count = 0;
        for &w in old.iter() {
            if w != -1 {
                insert(t, w);
            }
        }
    }
}

fn subarray_bitwise_ors(arr: &[i64]) -> i64 {
    let mut table = Table { slots: vec![-1; 64], count: 0 };
    let mut ending: Vec<i64> = Vec::new();
    for &x in arr.iter() {
        let mut next: Vec<i64> = Vec::new();
        next.push(x);
        for &y in ending.iter() {
            let v = y | x;
            if v != next[next.len() - 1] {
                next.push(v);
            }
        }
        for &v in next.iter() {
            insert(&mut table, v);
        }
        ending = next;
    }
    table.count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 898;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..12 {
        let mut arr: Vec<i64> = Vec::new();
        for _ in 0..50000 {
            let a = next_random(&mut seed) * 32768 + next_random(&mut seed);
            let b = next_random(&mut seed) * 32768 + next_random(&mut seed);
            arr.push(a & b);
        }
        let got = subarray_bitwise_ors(&arr);
        total += got;
        check = (check * 131 + got) % 1000000007;
    }
    println!("12 arrays of 50000 numbers: {} ORs in all, checksum {}", total, check);
}
