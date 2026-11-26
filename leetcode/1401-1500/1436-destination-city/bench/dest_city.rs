use std::collections::HashSet;

fn dest_city(paths: &[Vec<String>]) -> String {
    let starts: HashSet<String> = paths.iter().map(|path| path[0].clone()).collect();
    paths.iter().map(|path| path[1].clone()).find(|city| !starts.contains(city)).unwrap()
}

fn main() {
    let mut seed: i64 = 1436;
    let mut trips: Vec<Vec<Vec<String>>> = Vec::new();
    for _ in 0..1000 {
        let mut cities: Vec<String> = Vec::new();
        for c in 0..101i64 {
            let mut name = String::new();
            for _ in 0..8 {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                name.push((b'a' + (seed / 65536 % 26) as u8) as char);
            }
            name.push((b'a' + (c / 26) as u8) as char);
            name.push((b'a' + (c % 26) as u8) as char);
            cities.push(name);
        }
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let turn = (seed / 65536 % 100) as usize;
        let paths: Vec<Vec<String>> = (0..100)
            .map(|i| {
                let at = (i + turn) % 100;
                vec![cities[at].clone(), cities[at + 1].clone()]
            })
            .collect();
        trips.push(paths);
    }
    let mut check: i64 = 0;
    for _ in 0..100 {
        for paths in trips.iter() {
            let city = dest_city(paths);
            check = (check * 131 + city.bytes().fold(0i64, |h, b| (h * 31 + b as i64) % 1000000007)) % 1000000007;
        }
    }
    println!("10^5 trips of 100 paths: checksum {}", check);
}
