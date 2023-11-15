import logging
from datetime import datetime

# Configure logging to save logs to a file
logging.basicConfig(filename='satellite_logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a separate logging configuration for terminal output
terminal_logger = logging.StreamHandler()
terminal_logger.setLevel(logging.INFO)
terminal_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
terminal_logger.setFormatter(terminal_formatter)
logging.getLogger().addHandler(terminal_logger)

class Satellite:
    def __init__(self):
        self.state_file = "satellite_state.txt"
        self.load_state()

    def load_state(self):
        try:
            with open(self.state_file, "r") as file:
                lines = file.readlines()
                if len(lines) == 3:
                    self.orientation, self.solar_panels, self.data_collected = [line.strip() for line in lines]
                    logging.info("Satellite state loaded.")
                else:
                    logging.warning("Invalid state file. Using default state.")
                    self.initialize_default_state()
        except FileNotFoundError:
            logging.warning("State file not found. Using default state.")
            self.initialize_default_state()
        except Exception as e:
            logging.error(f"An error occurred while loading state: {str(e)}")
            self.initialize_default_state()

    def initialize_default_state(self):
        self.orientation = "North"
        self.solar_panels = "Inactive"
        self.data_collected = 0

    def save_state(self):
        try:
            with open(self.state_file, "w") as file:
                file.write(f"{self.orientation}\n{self.solar_panels}\n{self.data_collected}")
                logging.info("Satellite state saved.")
        except Exception as e:
            logging.error(f"An error occurred while saving state: {str(e)}")

    def log_state(self, instruction):
        logging.info(f"{instruction} - Current State: {self.get_state()}")

    def get_state(self):
        return {
            "Orientation": self.orientation,
            "Solar Panels": self.solar_panels,
            "Data Collected": self.data_collected
        }

    def rotate(self, direction):
        logging.info(f"Rotating satellite to {direction}.")
        self.orientation = direction
        self.save_state()
        self.log_state("Rotate")

    def activate_panels(self):
        logging.info("Activating solar panels.")
        self.solar_panels = "Active"
        self.save_state()
        self.log_state("Activate Panels")

    def deactivate_panels(self):
        logging.info("Deactivating solar panels.")
        self.solar_panels = "Inactive"
        self.save_state()
        self.log_state("Deactivate Panels")

    def collect_data(self):
        try:
            if self.solar_panels == "Active":
                logging.info("Collecting data.")
                self.data_collected += 10
                self.save_state()
                self.log_state("Collect Data")
            else:
                logging.warning("Cannot collect data. Solar panels are inactive.")
        except Exception as e:
            logging.error(f"An error occurred during data collection: {str(e)}")

class SatelliteController:
    def __init__(self, satellite):
        self.satellite = satellite

    def display_menu(self):
        print("\nSatellite Command System Menu:")
        print("1. Display State")
        print("2. Rotate")
        print("3. Activate Solar Panels")
        print("4. Deactivate Solar Panels")
        print("5. Collect Data")
        print("6. Exit")

    def execute_command(self, choice):
        try:
            if choice == '1':
                state = self.satellite.get_state()
                logging.info(f"Current State - {state}")
            elif choice == '2':
                direction = input("Enter the rotation direction (North/South/East/West): ").capitalize()
                self.satellite.rotate(direction)
            elif choice == '3':
                self.satellite.activate_panels()
            elif choice == '4':
                self.satellite.deactivate_panels()
            elif choice == '5':
                self.satellite.collect_data()
            elif choice == '6':
                logging.info("Exiting the Satellite Command System.")
                exit()
            else:
                logging.warning("Invalid choice. Please enter a valid option.")
        except Exception as e:
            logging.error(f"An error occurred while executing the command: {str(e)}")

if __name__ == "__main__":
    try:
        satellite = Satellite()
        controller = SatelliteController(satellite)

        while True:
            controller.display_menu()
            user_choice = input("Enter your choice (1-6): ")
            controller.execute_command(user_choice)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
