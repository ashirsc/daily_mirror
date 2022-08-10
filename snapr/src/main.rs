use std::thread;
use std::time::Duration;
use opencv::{
    prelude::*,
    videoio,
    highgui
};
use rppal::gpio::{Gpio, OutputPin};

fn blink(led: &mut OutputPin, num_intervals: i32, interval_duration: u64) {
    for _ in 0..num_intervals - 1 {
        led.set_high();
        thread::sleep(Duration::from_millis(interval_duration));
        led.set_low();
        thread::sleep(Duration::from_millis(interval_duration));
    }
    led.set_high();
    thread::sleep(Duration::from_millis(interval_duration));
    led.set_low();
}

fn main() {
    let gpio = Gpio::new().expect("Failed to initialize GPIO");
    let mut red_led = gpio.get(17).expect("Failed to get pin 17").into_output();
    let mut button = gpio.get(2).expect("Failed to get pin 2").into_input();

    loop {
        button
            .poll_interrupt(true, None)
            .expect("Failed to poll button");
        println!("Button pressed");
        blink(&mut red_led, 3, 500);
    }
}
