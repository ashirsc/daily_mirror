use anyhow::Result; 
use opencv::{
    core::{Point, Scalar, ToInputOutputArray},
    imgcodecs, imgproc,highgui,
    prelude::*,
    videoio,
};
use rppal::gpio::{Gpio, InputPin, OutputPin};
use std::sync::mpsc::channel;
use std::thread;
use std::time::{Duration, SystemTime};

fn blink(led_pin: &u8, num_intervals: i32, interval_duration: Duration) {
    let gpio = Gpio::new().expect("Failed to initialize GPIO");
    let mut led: OutputPin = gpio
        .get(*led_pin)
        .expect("Failed to get pin {}")
        .into_output();

    led.set_low();
    for _ in 0..num_intervals - 1 {
        led.set_high();
        thread::sleep(interval_duration);
        led.set_low();
        thread::sleep(interval_duration);
    }
    led.set_high();
    thread::sleep(interval_duration);
    led.set_low();
}

fn draw_fps(frame: &mut Mat, prev_time: &SystemTime) -> SystemTime {
    let new_frame_time = SystemTime::now();

    let fps = 1.0
        / (new_frame_time
            .duration_since(*prev_time)
            .unwrap()
            .as_secs_f32());

    let _ = imgproc::put_text(
        &mut frame.input_output_array().unwrap(),
        fps.to_string().as_str(),
        Point::new(7, 70),
        0,
        2.0,
        Scalar::new(100.0, 255.0, 0.0, 0.0),
        3,
        imgproc::LINE_AA,
        false,
    );

    new_frame_time
}

#[tokio::main]
async fn main() -> Result<()> {
    highgui::named_window("Preview", highgui::WINDOW_FULLSCREEN)?;

    let mut cam = videoio::VideoCapture::new(2, videoio::CAP_ANY)?;
    let mut frame = Mat::default();

    let gpio = Gpio::new().expect("Failed to initialize GPIO");
    let red_led_pin = 17;
    let button: InputPin = gpio.get(2).expect("Failed to get pin 2").into_input();

    let (sender, receiver) = channel();


    loop {
        cam.read(&mut frame)?;
        if frame.empty() {
            continue;
        }

        // let mut gray = Mat::default();
        // imgproc::cvt_color(
        //     &frame,
        //     &mut gray.output_array().unwrap(),
        //     imgproc::COLOR_BGR2GRAY,
        //     0,
        // )
        // .unwrap();

        if button.is_low() {
            let sender = sender.clone();
            thread::spawn(move || {
                blink(&red_led_pin, 3, Duration::from_millis(500));
                println!("Finished blinking");
                sender.send(()).unwrap();
            });
        }
        highgui::imshow("window", &frame)?;

        if receiver.try_recv() == Ok(()) {
            imgcodecs::imwrite(
                "images/capture.jpg",
                &frame,
                &opencv::types::VectorOfi32::new(),
            )
            .unwrap();
        }
    }
    // Ok(())
}
