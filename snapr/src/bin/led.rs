use std::thread;
use std::time::Duration;

use rppal::gpio::{Gpio, OutputPin};



fn main() {
    let gpio = Gpio::new().expect("Failed to initialize GPIO");
    let mut red_led = gpio.get(17).expect("Failed to get pin 17").into_output();

    let interval_duration = Duration::from_millis(500);
    println!("Staring loop");
    loop {
        red_led.set_high();
        thread::sleep(interval_duration);
        red_led.set_low();
        thread::sleep(interval_duration);
    }
}
