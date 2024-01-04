# E-Paper Currency Tracker
Python-based project displays real-time currency exchange rates on an e-paper screen, housed in a custom-crafted wooden box.

## Overview
Welcome to my e-Paper Currency Tracker Project! This project is designed to fetch and display currency exchange rates on an e-paper display. It's built using Python and integrates various technologies to create a seamless and efficient user experience. The project is perfect for anyone interested in hardware interfacing, web development, or financial data visualization. In addtion, I created a self-creafted wooden box to fit the e-paper as well as the Raspberry Pi Zero to make it a great addition to a desk.

## Features
- **Currency Exchange Rate Display:** Fetches and displays the latest exchange rates on the e-paper.
- **Trend Analysis:** Analyzes and displays the trend of exchange rates over a specified period.
- **Customizable Settings:** Allows users to select target currencies through a locally hosted web interface.
- **Elegant Wooden Enclosure:** A custom-crafted wooden box houses the e-paper display, adding a professional and aesthetic touch to the technology.

## Technologies Used
- **Python:** The core language used for scripting the project.
- **Flask:** A micro web framework used for handling web server operations.
- **Redis:** Utilized for caching exchange rate data to reduce API calls.
- **Pillow & Matplotlib:** Libraries used for image processing and graph plotting respectively.

## Hardware Requirements
This project is designed for an e-paper display with specific attributes. To run this project, ensure your setup meets the following requirements:
- Waveshare 2.9inch e-Paper Module
- Microcontroller such as an Arduino or Raspberry Pi

## Installation (For Compatible Setups)
If you have the necessary hardware, you can install and run this project as follows:
1. Clone the repository:
   ```bash
   git clone https://github.com/Vincent881909/e-paper.git
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
## Running the Project (For Compatible Setups)
To run the project on your compatible e-paper display:

1. Start the Redis server on your local machine.
2. Run the Flask web server:
    ```bash
    python web/app.py
3. Access the web server at http://localhost:5000 to configure your target currencies.

## Project Structure
- assets/: Contains fonts and screenshots.
- lib/: Includes all the necessary libraries and modules.
- main/: Contains the main script and configuration files.
- web/: Houses the Flask web application files.

## Wooden Box
This project features a sleek, minimalist wooden box, housing an e-paper display connected to a Raspberry Pi Zero, carefully crafted with CNC precision. It elegantly presents real-time currency exchange rates on your desk, combining functionality with a touch of natural aesthetic, thanks to its refined post-processed wood finish. The post-processing included grinding and finishing the process with wood oil to achieve a slight gloss. 

## Images
![Image 1](/assets/photo1.jpeg "Image 1")
![Image 2](/assets/photo2.jpeg "Image 2")

