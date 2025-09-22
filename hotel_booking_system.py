import datetime

class Room:
    """A class to represent a hotel room."""
    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.is_available = True

    def book(self):
        """Marks the room as unavailable."""
        if self.is_available:
            self.is_available = False
            return True
        return False

    def release(self):
        """Marks the room as available."""
        self.is_available = True

    def __str__(self):
        """String representation of the room."""
        status = "Available" if self.is_available else "Booked"
        return f"Room {self.room_number} ({self.room_type}) - Price: ${self.price}/night - Status: {status}"

class Booking:
    """A class to represent a booking."""
    def __init__(self, guest_name, room, check_in_date, check_out_date):
        self.guest_name = guest_name
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.total_cost = self.calculate_cost()

    def calculate_cost(self):
        """Calculates the total cost of the booking."""
        stay_duration = (self.check_out_date - self.check_in_date).days
        return stay_duration * self.room.price

    def __str__(self):
        """String representation of the booking."""
        return (
            f"Booking for {self.guest_name} in Room {self.room.room_number}.\n"
            f"  Check-in: {self.check_in_date.strftime('%Y-%m-%d')}\n"
            f"  Check-out: {self.check_out_date.strftime('%Y-%m-%d')}\n"
            f"  Total Cost: ${self.total_cost}"
        )

class Hotel:
    """A class to manage the hotel's rooms and bookings."""
    def __init__(self, name):
        self.name = name
        self.rooms = {}
        self.bookings = []

    def add_room(self, room_number, room_type, price):
        """Adds a new room to the hotel."""
        if room_number not in self.rooms:
            self.rooms[room_number] = Room(room_number, room_type, price)
        else:
            print(f"Room {room_number} already exists.")

    def list_all_rooms(self):
        """Prints the status of all rooms."""
        print(f"\n--- {self.name} Room Status ---")
        if not self.rooms:
            print("No rooms available.")
            return
        for room_number, room in self.rooms.items():
            print(room)

    def book_room(self, guest_name, room_number, check_in_str, check_out_str):
        """Books a room for a guest."""
        try:
            check_in_date = datetime.datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out_date = datetime.datetime.strptime(check_out_str, '%Y-%m-%d').date()

            if check_out_date <= check_in_date:
                print("Error: Check-out date must be after check-in date.")
                return

            if room_number in self.rooms and self.rooms[room_number].is_available:
                room = self.rooms[room_number]
                if room.book():
                    booking = Booking(guest_name, room, check_in_date, check_out_date)
                    self.bookings.append(booking)
                    print(f"\nBooking successful for {guest_name}!")
                    print(booking)
                else:
                    print(f"Room {room_number} is already booked.")
            else:
                print(f"Room {room_number} is not available or does not exist.")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    def checkout_guest(self, room_number):
        """Checks out a guest and releases the room."""
        if room_number in self.rooms:
            room = self.rooms[room_number]
            if not room.is_available:
                room.release()
                print(f"Guest in Room {room_number} checked out successfully.")
                
                # Remove the booking record
                self.bookings = [b for b in self.bookings if b.room.room_number != room_number]
            else:
                print(f"Room {room_number} is not currently occupied.")
        else:
            print(f"Room {room_number} does not exist.")

def main():
    """Main function to run the hotel booking system."""
    hotel = Hotel("The Grand Python Hotel")
    hotel.add_room(101, "Single", 100)
    hotel.add_room(102, "Double", 150)
    hotel.add_room(201, "Suite", 300)
    hotel.add_room(202, "Single", 120)

    while True:
        print("\n--- Hotel Management System Menu ---")
        print("1. List all rooms")
        print("2. Book a room")
        print("3. Check out a guest")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            hotel.list_all_rooms()
        elif choice == '2':
            guest_name = input("Enter guest name: ")
            room_number = int(input("Enter room number: "))
            check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
            check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
            hotel.book_room(guest_name, room_number, check_in_date, check_out_date)
        elif choice == '3':
            room_number = int(input("Enter room number to check out: "))
            hotel.checkout_guest(room_number)
        elif choice == '4':
            print("Thank you for using our system!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
