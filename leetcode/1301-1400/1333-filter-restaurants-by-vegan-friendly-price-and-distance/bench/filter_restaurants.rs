// LeetCode #1333 bench, Rust mirror of the Kāra bench: the ★ arm on 20
// lists of 10^4 restaurants built once, then 100 passes, each setting one
// rating of every list from the checksum so far and drawing the filters
// from it too, answering every list.

fn filter_restaurants(restaurants: &[Vec<i32>], vegan_friendly: i32, max_price: i32, max_distance: i32) -> Vec<i32> {
    let mut kept: Vec<(i32, i32)> = Vec::new();
    for r in restaurants.iter() {
        if (vegan_friendly == 0 || r[2] == 1) && r[3] <= max_price && r[4] <= max_distance {
            kept.push((r[1], r[0]));
        }
    }
    kept.sort_by(|a, b| b.0.cmp(&a.0).then(b.1.cmp(&a.1)));
    kept.iter().map(|p| p.1).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 10000i64;
    let mut seed = 1333i64;
    let mut lists: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..20 {
        let mut list: Vec<Vec<i32>> = Vec::new();
        for i in 0..n {
            let id = (i * 10 + 1 + next_random(&mut seed) % 10) as i32;
            let rating = (1 + next_random(&mut seed) % 100000) as i32;
            let vegan = (next_random(&mut seed) % 2) as i32;
            let price = (1 + next_random(&mut seed) % 100000) as i32;
            let distance = (1 + next_random(&mut seed) % 100000) as i32;
            list.push(vec![id, rating, vegan, price, distance]);
        }
        lists.push(list);
    }
    let mut check: i64 = 0;
    for pass in 0..100i64 {
        let vegan = (pass % 2) as i32;
        let max_price = (50000 + check % 50001) as i32;
        let max_distance = (50000 + check / 7 % 50001) as i32;
        for t in 0..20 {
            let at = (check % n) as usize;
            lists[t][at][1] = (1 + check / 3 % 100000) as i32;
            let ids = filter_restaurants(&lists[t], vegan, max_price, max_distance);
            let k = ids.len();
            check = (check * 31 + k as i64 + ids[0] as i64 + ids[k / 2] as i64 + pass) % 1000000007;
        }
    }
    println!("100 passes over 20 lists of 10^4: checksum {}", check);
}
