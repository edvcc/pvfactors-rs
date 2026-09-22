// Standalone numerical experiment. Not part of any product crate.
use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    for line in input.lines() {
        let v: Vec<f64> = line.split(',').map(|x| x.parse().unwrap()).collect();
        let (b, z, a) = (v[0].to_radians(), v[1].to_radians(), v[2].to_radians());
        let mu = b.cos() * z.cos() + b.sin() * z.sin() * a.cos();
        println!("{mu:.17e}");
    }
}
