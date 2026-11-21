// LeetCode #2469: Convert the Temperature -- the bench, the ★ arm in Rust:
// the two formulas as given, returned in a `Vec`.

fn convert_temperature(celsius: f64) -> Vec<f64> {
    vec![celsius + 273.15, celsius * 1.80 + 32.00]
}

fn main() {
    // 230 passes over every temperature from 0 to 1000 in hundredths,
    // each pass starting at a hundredth chosen from the checksum so far;
    // every answer's kelvin in hundredths and Fahrenheit in thousandths,
    // rounded, folded into the checksum
    let mut check = 0i64;
    for p in 0..230i64 {
        let start = check % 100001;
        for i in 0..100001i64 {
            let h = (start + i) % 100001;
            let got = convert_temperature(h as f64 / 100.0);
            let kelvin = (got[0] * 100.0).round() as i64;
            let fahrenheit = (got[1] * 1000.0).round() as i64;
            check = (check * 31 + kelvin + fahrenheit + p) % 1000000007;
        }
    }
    println!("230 passes over every hundredth from 0 to 1000: checksum {}", check);
}
