import tkinter as tk
from tkinter import messagebox, ttk,PhotoImage
from tkcalendar import DateEntry 
import datetime
from PIL import Image, ImageTk, ImageSequence
import os
import oracledb
def connect_to_db():
    try:
        # Try connecting with localhost first
        connection = oracledb.connect(
            user="system",
            password="2006",
            dsn="SURIYAGANESH57:1521/orcl"  # Changed from specific hostname
        )
        print('Connection successful')
        return connection
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Oracle-Error-Code: {error.code}")
        print(f"Oracle-Error-Message: {error.message}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
db_conn = connect_to_db()


class FlightReservationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.flight_id = None
        self.travel_class = None
        # Remove window decorations (title bar and borders)
        self.overrideredirect(True)
        
        # Set window to full screen
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        
        # Add custom title and icon (optional)
        self.title("Flight Reservation System")
        self.iconbitmap(r"C:\Users\ganes\OneDrive\Desktop\or\image.ico")
        
        # Create and show all pages
        self.frames = {}
        for F in (HomePage, BookTicketPage, SelectFlightPage, SelectClassPage, PassengerDetailsPage, PaymentPage,ViewCancelPage):
            frame = F(parent=self, controller=self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(HomePage)

    def show_frame(self, container):
        """Show the given frame."""
        frame = self.frames[container]  # Retrieve the frame (page) to show
        frame.tkraise()  # Bring the frame to the front
        if hasattr(frame, "on_show"):  # If the frame has an `on_show` method
            frame.on_show()  # Call the `on_show` method

    def show_payment_page(self, passenger_details):
        """Pass details to PaymentPage and show it."""
        payment_page = self.frames[PaymentPage]
        payment_page.set_passenger_details(passenger_details, self.flight_id)
        self.show_frame(PaymentPage)

            
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Path to the GIF
        gif_path =r"C:\Users\ganes\OneDrive\Desktop\or\DIJ Airlines_2.gif"

        # Load GIF
        gif = Image.open(gif_path)
        self.frames = []
        try:
            while True:
                # Resize each frame for fullscreen alignment
                frame = gif.copy()
                resized_frame = frame.resize(
                    (self.controller.winfo_screenwidth(), self.controller.winfo_screenheight()), Image.Resampling.LANCZOS
                )
                self.frames.append(ImageTk.PhotoImage(resized_frame))
                gif.seek(len(self.frames))  # Move to the next frame
        except EOFError:
            pass  # End of GIF frames

        # Background Label for GIF (Full screen)
        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Start animation
        self.animate(0)

        # Create Classic Buttons
        self.create_classic_buttons(controller)

    def animate(self, frame_index):
        """Play the GIF frames one by one and stop at the last frame."""
        if frame_index < len(self.frames):
            frame = self.frames[frame_index]
            self.bg_label.configure(image=frame)
            self.bg_label.image = frame  # Keep reference to prevent garbage collection

            # Schedule the next frame
            self.after(100, self.animate, frame_index + 1)

    def create_classic_buttons(self, controller):
        """Create Book Ticket, View/Cancel Ticket, and Exit buttons with a classic design."""

        # Common Classic Button Style
        classic_button_style = {
            "font": ("Arial", 16, "bold"),
            "bg": "#1976d2",  # Classic blue shade
            "fg": "white",
            "activebackground": "#004ba0",  # Darker blue for active state
            "activeforeground": "white",
            "relief": "groove",
            "bd": 3,
            "width": 20,
            "height": 2,
        }

        # Book Ticket Button
        book_button = tk.Button(
            self, 
            text="Book Ticket", 
            command=lambda: controller.show_frame(BookTicketPage), 
            **classic_button_style
        )
        book_button.place(x=50, y=100)

        # View/Cancel Ticket Button
        view_button = tk.Button(
            self, 
            text="View or Cancel Ticket", 
            command=lambda: controller.show_frame(ViewCancelPage), 
            **classic_button_style
        )
        view_button.place(x=50, y=200)

        # Classic Exit Button
        self.create_exit_button()

    def create_exit_button(self):
        """Create a classic rectangular Exit button."""
        classic_exit_button_style = {
            "font": ("Arial", 16, "bold"),
            "bg": "#e63946",  # Classic red shade
            "fg": "white",
            "activebackground": "#a4161a",  # Darker shade when clicked
            "activeforeground": "white",
            "relief": "flat",
            "width": 20,
            "height": 2,
        }

        # Create Exit Button
        exit_button = tk.Button(self, text="Exit", command=self.confirm_exit, **classic_exit_button_style)
        exit_button.place(x=50, y=300)  # Adjust position as needed

    def confirm_exit(self):
        response = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?")
        if response:
            self.quit()


class BookTicketPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Path to the GIF
        self.connection = oracledb.connect(user="system", password="2006", dsn="SURIYAGANESH57:1521/orcl")
        self.cursor = self.connection.cursor()

        # Path to the GIF
        gif_path = r"C:\Users\ganes\OneDrive\Desktop\or\DIJ Airlines_window.gif"

        # Load GIF
        gif = Image.open(gif_path)
        self.frames = []
        try:
            while True:
                frame = gif.copy()
                resized_frame = frame.resize(
                    (self.controller.winfo_screenwidth(), self.controller.winfo_screenheight()),
                    Image.Resampling.LANCZOS
                )
                self.frames.append(ImageTk.PhotoImage(resized_frame))
                gif.seek(len(self.frames))
        except EOFError:
            pass

        # Background Label for GIF (Full screen)
        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Instance variables for form
        self.source_var = tk.StringVar()
        self.destination_var = tk.StringVar()
        self.date_var = tk.StringVar()

        # Cities for dropdown
        self.cities = ["Mumbai", "Delhi", "Goa", "Chennai", "Kolkata", "Pune", "Hyderabad", "Bangalore"]

        # Styling
        self.configure(bg="#f0f8ff")

        # Header
        header = tk.Label(
            self, text="Book Ticket", font=("Georgia", 24, "bold"),
            bg="#4682b4", fg="white", pady=10
        )
        header.pack(fill="x", pady=(0, 20))

        # Input Fields (Right-Aligned)
        input_frame = tk.Frame(self, bg="#f0f8ff")
        input_frame.place(relx=0.75, rely=0.2, anchor="n")

        # Source Field
        tk.Label(
            input_frame, text="Source:", font=("Arial", 14),
            bg="#f0f8ff", anchor="w"
        ).grid(row=0, column=0, pady=10, padx=10, sticky="w")
        ttk.Combobox(
            input_frame, textvariable=self.source_var, font=("Arial", 14),
            values=self.cities, state="normal", width=20
        ).grid(row=0, column=1, pady=10, padx=10, sticky="e")

        # Destination Field
        tk.Label(
            input_frame, text="Destination:", font=("Arial", 14),
            bg="#f0f8ff", anchor="w"
        ).grid(row=1, column=0, pady=10, padx=10, sticky="w")
        ttk.Combobox(
            input_frame, textvariable=self.destination_var, font=("Arial", 14),
            values=self.cities, state="normal", width=20
        ).grid(row=1, column=1, pady=10, padx=10, sticky="e")

        # Date Field
        tk.Label(
            input_frame, text="Date (YYYY-MM-DD):", font=("Arial", 14),
            bg="#f0f8ff", anchor="w"
        ).grid(row=2, column=0, pady=10, padx=10, sticky="w")
        DateEntry(
            input_frame, textvariable=self.date_var, font=("Arial", 14), width=22,
            background="#4682b4", foreground="white", borderwidth=2,
            date_pattern="yyyy-MM-dd", mindate=datetime.date.today()
        ).grid(row=2, column=1, pady=10, padx=10, sticky="e")

        # Buttons (Below Input Fields)
        button_frame = tk.Frame(self, bg="#f0f8ff")
        button_frame.place(relx=0.75, rely=0.5, anchor="n")

        search_button = tk.Button(
            button_frame, text="Search", command=self.search_flights,
            font=("Arial", 14), bg="#4a90e2", fg="white",
            width=15, height=1, activebackground="#357abd", activeforeground="white"
        )
        search_button.grid(row=0, column=0, padx=10, pady=20)
        back_button = tk.Button(
            button_frame, text="Back", command=lambda: controller.show_frame(HomePage),
            font=("Arial", 14), bg="#a5a5a5", fg="white",
            width=15, height=1, activebackground="#8c8c8c", activeforeground="white"
        )
        back_button.grid(row=0, column=1, padx=10, pady=20)

        # Footer
        footer = tk.Label(
            self, text="Enter the details to book a flight.",
            font=("Arial", 12), bg="#f0f8ff", fg="#4682b4", pady=10
        )
        footer.pack(side="bottom", fill="x", pady=(20, 0))

    def search_flights(self):
        source = self.source_var.get()
        destination = self.destination_var.get()
        date = self.date_var.get()

        if not source or not destination or not date:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            # Use different bind variable names to avoid potential conflicts
            query = """SELECT flight_id, source, destination, departure_time, arrival_time, flight_date, base_price
                    FROM Flights
                    WHERE source = :src AND destination = :dest AND flight_date = TO_DATE(:flt_date, 'YYYY-MM-DD')"""
            
            print(f"Executing query with source: {source}, destination: {destination}, date: {date}")
            print(f"Query: {query}")
            
            self.cursor.execute(query, {'src': source, 'dest': destination, 'flt_date': date})
            flights = self.cursor.fetchall()

            if not flights:
                messagebox.showerror("No Flights Found", "No flights available for the selected search criteria.")
                return

            self.controller.frames[SelectFlightPage].populate_flights(flights)
            self.controller.show_frame(SelectFlightPage)

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while fetching flights: {e}")
            print(f"Error: {e}")

    def animate(self, frame_index):
            """Play the GIF frames one by one and stop at the last frame."""
            if frame_index < len(self.frames):
                frame = self.frames[frame_index]
                self.bg_label.configure(image=frame)
                self.bg_label.image = frame  # Keep reference to prevent garbage collection

                # Schedule the next frame
                self.after(100, self.animate, frame_index + 1)
    def on_show(self):
        """Start animation when the frame is shown."""
        self.animate(0)

class SelectFlightPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.flight_id = None
        self.flights = []  # Store flights list

        
        # Set background color
        self.configure(bg="#f9f9f9")  # Soft gray background for a clean look
        
        # Header Section
        header = tk.Label(self, text="Select a Flight", font=("Georgia", 24, "bold"),
                          bg="#6c63ff", fg="white", pady=10)
        header.pack(fill="x", pady=(0, 20))
        
        # Treeview Frame
        tree_frame = tk.Frame(self, bg="#f9f9f9", padx=20, pady=20)
        tree_frame.pack(fill="both", expand=True)
        
        # Treeview with Scrollbars
        self.tree = ttk.Treeview(tree_frame, 
                                 columns=("ID", "Source", "Destination",  "Departure", "Arrival","Date", "Price"), 
                                 show="headings", 
                                 height=10)
        self.tree.heading("ID", text="Flight ID")
        self.tree.heading("Source", text="Source")
        self.tree.heading("Destination", text="Destination")
        self.tree.heading("Date", text="Flight Date")
        self.tree.heading("Departure", text="Departure Time")
        self.tree.heading("Arrival", text="Arrival Time")
        self.tree.heading("Price", text="Price")

        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Source", width=150, anchor="center")
        self.tree.column("Destination", width=150, anchor="center")
        self.tree.column("Date", width=150, anchor="center")
        self.tree.column("Departure", width=150, anchor="center")
        self.tree.column("Arrival", width=150, anchor="center")
        self.tree.column("Price", width=100, anchor="center")
        
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")
        
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Buttons Frame
        button_frame = tk.Frame(self, bg="#f9f9f9", pady=10)
        button_frame.pack(fill="x")

        # Enhanced Buttons
        select_button = tk.Button(button_frame, text="Select Flight", command=self.select_flight,
                                  font=("Arial", 14), bg="#4caf50", fg="white", width=15, height=2,
                                  bd=0, activebackground="#388e3c", activeforeground="white")
        select_button.pack(side="left", padx=20)

        back_button = tk.Button(button_frame, text="Back", command=lambda: controller.show_frame(BookTicketPage),
                                font=("Arial", 14), bg="#f44336", fg="white", width=15, height=2,
                                bd=0, activebackground="#d32f2f", activeforeground="white")
        back_button.pack(side="right", padx=20)
        
        # Footer Section
        footer = tk.Label(self, text="Select a flight from the list to proceed.", font=("Arial", 12),
                          bg="#f9f9f9", fg="#6c63ff", pady=10)
        footer.pack(side="bottom", fill="x", pady=(10, 0))

    def populate_flights(self, flights):
        """Populate the treeview with flight data and store it in self.flights."""
        self.flights = flights  # Store the flights for later reference
        print(f"Flights populated: {self.flights}")  # Debugging output
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Insert new rows
        for flight in flights:
            self.tree.insert("", "end", values=flight)
    
    def get_flight_details(self, flight_id):
        """Retrieve flight details by flight_id."""
        for flight in self.flights:  
            if flight[0] == flight_id:  
                print(f"Found flight: {flight}")  
                return {
                    'flight_id': flight[0],
                    'base_price': flight[6] 
                }  
        return None



    def select_flight(self):
        """Handle the flight selection."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a flight.")
            return
        
        flight = self.tree.item(selected_item, "values")
        self.selected_flight_id = flight[0]  # Assume flight ID is in the first column
        print(f"Selected Flight ID: {self.selected_flight_id}")  # Debugging output

        # Pass the selected flight_id to the controller
        self.controller.flight_id = self.selected_flight_id  # Ensure flight_id is set in controller

        # Proceed to the next page after selecting the flight
        self.controller.frames[SelectClassPage].set_flight_id(self.selected_flight_id)
        self.controller.show_frame(SelectClassPage)

class SelectClassPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.flight_id = None
    

        self.configure(bg="#e8f0f2")

        # Header Section
        header = tk.Label(self, text="Select Travel Class", font=("Georgia", 24, "bold"),
                          bg="#37474f", fg="white", pady=10)
        header.pack(fill="x", pady=(0, 20))

        # Buttons for selecting class
        self.class_button_frame = tk.Frame(self, bg="#e8f0f2")
        self.class_button_frame.pack()

        tk.Label(self, text="Select Travel Class", font=("Georgia", 24, "bold")).pack(pady=20)

        # Economy Class Button
        tk.Button(self, text="Economy", font=("Arial", 14), 
                  command=lambda: self.select_class("Economy", 1), bg="#ff9800", fg="white", width=20, height=2).pack(pady=10)
        
        # Business Class Button
        tk.Button(self, text="Business", font=("Arial", 14), 
                  command=lambda: self.select_class("Business", 1.5), bg="#4caf50", fg="white", width=20, height=2).pack(pady=10)
        
        # First Class Button
        tk.Button(self, text="First Class", font=("Arial", 14), 
                  command=lambda: self.select_class("First Class", 2), bg="#d32f2f", fg="white", width=20, height=2).pack(pady=10)

        # Back button
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(SelectFlightPage),
                                font=("Arial", 14), bg="#a5a5a5", fg="white", width=15, height=1,
                                activebackground="#8c8c8c", activeforeground="white")
        back_button.pack(pady=(20, 0))

    def set_flight_id(self, flight_id):
        self.flight_id = flight_id

    def select_class(self, travel_class, multiplier):
        self.controller.travel_class = travel_class
        self.controller.price_multiplier = multiplier

        self.controller.frames[PassengerDetailsPage].setup(self.flight_id, travel_class, multiplier)
        self.controller.show_frame(PassengerDetailsPage)
    def process_payment(self):
        travel_class = self.controller.travel_class
        multiplier = self.controller.price_multiplier
        base_price = 1000  # Example base price
        final_price = base_price * multiplier


class PassengerDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.flight_id = None
        self.travel_class = None

        # Set background color
        self.configure(bg="#e8f0f2")

        # Header Section
        header = tk.Label(self, text="Passenger Details", font=("Georgia", 24, "bold"),
                          bg="#37474f", fg="white", pady=10)
        header.pack(fill="x", pady=(0, 20))

        # Form fields for passenger details
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.dob_var = tk.StringVar()  # We'll use a string for simplicity
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.seat_var = tk.StringVar()

        form_frame = tk.Frame(self, bg="#e8f0f2")
        form_frame.pack()

        tk.Label(form_frame, text="First Name:", font=("Arial", 14), bg="#e8f0f2").grid(row=0, column=0, pady=10, padx=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.first_name_var, font=("Arial", 14)).grid(row=0, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Last Name:", font=("Arial", 14), bg="#e8f0f2").grid(row=1, column=0, pady=10, padx=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.last_name_var, font=("Arial", 14)).grid(row=1, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Date of Birth (YYYY-MM-DD):", font=("Arial", 14), bg="#e8f0f2").grid(row=2, column=0, pady=10, padx=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.dob_var, font=("Arial", 14)).grid(row=2, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Phone Number:", font=("Arial", 14), bg="#e8f0f2").grid(row=3, column=0, pady=10, padx=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.phone_var, font=("Arial", 14)).grid(row=3, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Email:", font=("Arial", 14), bg="#e8f0f2").grid(row=4, column=0, pady=10, padx=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.email_var, font=("Arial", 14)).grid(row=4, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Seat Number:", font=("Arial", 14), bg="#e8f0f2").grid(row=5, column=0, pady=10, padx=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.seat_var, font=("Arial", 14)).grid(row=5, column=1, pady=10, padx=10)

        # Button to submit passenger details
        submit_button = tk.Button(self, text="Submit", command=self.submit_details, font=("Arial", 14), bg="#4caf50", fg="white")
        submit_button.pack(pady=20)

        # Button to go back to the previous page
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(HomePage),
                                font=("Arial", 14), bg="#6c757d", fg="white")
        back_button.pack(pady=(0, 20))

    def setup(self, flight_id, travel_class, multiplier):
        self.flight_id = flight_id
        self.travel_class = travel_class
        self.multiplier = multiplier

    def submit_details(self):
        # Handle the submission of passenger details here
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()
        dob = self.dob_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        seat = self.seat_var.get()

        # Collect the passenger details
        passenger_details = {
            'first_name': first_name,
            'last_name': last_name,
            'dob': dob,
            'phone': phone,
            'email': email,
            'seat': seat
        }
        #self.controllshow_frameer.(PaymentPage)

        #def show_payment_page(self, passenger_details):
        #    payment_page = self.frames["PaymentPage"]
        #    payment_page.set_passenger_details(passenger_details)
        #    self.show_frame("PaymentPage")
        # Pass the passenger details to the next page (e.g., PaymentPage)
        self.controller.show_payment_page(passenger_details)


class PaymentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.passenger_details = None
        self.flight_id = None
        self.total_amount = 0.0  # Store the calculated total amount

        # Set background color
        self.configure(bg="#f8f9fa")  # Light background color for the payment page

        # Header Section
        header = tk.Label(self, text="Payment Information", font=("Georgia", 24, "bold"),
                          bg="#28a745", fg="white", pady=10)
        header.pack(fill="x", pady=(0, 20))

        # Content Frame for Payment Form
        content_frame = tk.Frame(self, bg="#f8f9fa", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)

        # Credit Card Fields (for simulation)
        self.card_number_var = tk.StringVar()
        self.expiry_date_var = tk.StringVar()
        self.cvc_var = tk.StringVar()

        payment_details = [
            ("Card Number", self.card_number_var),
            ("Expiry Date (MM/YY)", self.expiry_date_var),
            ("CVV", self.cvc_var)
        ]

        for label_text, var in payment_details:
            label = tk.Label(content_frame, text=label_text, font=("Arial", 14), bg="#f8f9fa", fg="#333")
            label.grid(row=payment_details.index((label_text, var)), column=0, sticky="e", padx=10, pady=10)
            entry = tk.Entry(content_frame, textvariable=var, font=("Arial", 14), bd=2, relief="solid", width=30)
            entry.grid(row=payment_details.index((label_text, var)), column=1, pady=10)

        # Display total amount
        self.amount_label = tk.Label(self, text="", font=("Arial", 16), bg="#f8f9fa", fg="#333")
        self.amount_label.pack(pady=(10, 20))

        # Buttons
        button_frame = tk.Frame(self, bg="#f8f9fa", pady=20)
        button_frame.pack(side="bottom", fill="x")

        confirm_button = tk.Button(button_frame, text="Confirm Payment", command=self.confirm_payment,
                                   font=("Arial", 14), bg="#28a745", fg="white", width=20, height=2,
                                   bd=0, activebackground="#218838", activeforeground="white")
        confirm_button.pack(pady=10)

        back_button = tk.Button(button_frame, text="Back", command=lambda: self.controller.show_frame(PassengerDetailsPage),
                                font=("Arial", 14), bg="#6c757d", fg="white", width=15, height=2,
                                bd=0, activebackground="#5a6268", activeforeground="white")
        back_button.pack(pady=10)

        # Footer Section
        footer = tk.Label(self, text="Enter your payment details to complete the booking.",
                          font=("Arial", 12), bg="#f8f9fa", fg="#28a745", pady=10)
        footer.pack(side="bottom", fill="x", pady=(20, 0))

    def set_passenger_details(self, passenger_details, flight_id):
        self.passenger_details = passenger_details
        self.flight_id = flight_id

        # Retrieve flight details from SelectFlightPage
        flight_details = self.controller.frames[SelectFlightPage].get_flight_details(flight_id)
        if flight_details:
            base_price = flight_details['base_price']
            final_price = self.controller.final_price
            self.total_amount = base_price * final_price

            # Update amount label
            self.amount_label.config(text=f"Total Amount to Pay: ₹{self.total_amount:.2f}")

    def confirm_payment(self):
        card_number = self.card_number_var.get()
        expiry_date = self.expiry_date_var.get()
        cvc = self.cvc_var.get()

        # Validate payment details
        if not card_number or not expiry_date or not cvc:
            messagebox.showerror("Input Error", "All payment fields are required.")
            return

        if len(card_number) == 16 and len(expiry_date) == 5 and len(cvc) == 3:
                if self.flight_id is None:
                    messagebox.showerror("Error", "Flight ID is missing. Cannot process payment.")
                    return

                booking_id = self.store_booking_details()
                messagebox.showinfo("Payment Confirmed", f"Your payment has been successfully processed! Booking ID: {booking_id}")
                self.controller.show_frame(HomePage) 
        else:
            messagebox.showerror("Payment Failed", "Invalid payment details. Please check your inputs.")

    def store_booking_details(self):
        booking_id = None
        try:
            connection = oracledb.connect(user="system", password="2006", dsn="SURIYAGANESH57:1521/orcl")
            cursor = connection.cursor()

            if self.flight_id is None:
                raise ValueError("Flight ID is required but is None")

            cursor.execute("SELECT passenger_seq.NEXTVAL FROM dual")
            passenger_id = cursor.fetchone()[0]

            cursor.execute(
                """INSERT INTO Passengers (passenger_id, first_name, last_name, dob, phone_number, email)
                VALUES (:passenger_id, :first_name, :last_name, :dob, :phone_number, :email)""",
                {
                    'passenger_id': passenger_id,
                    'first_name': self.passenger_details['first_name'],
                    'last_name': self.passenger_details['last_name'],
                    'dob': datetime.datetime.strptime(self.passenger_details['dob'], '%Y-%m-%d').date(),
                    'phone_number': self.passenger_details['phone'],
                    'email': self.passenger_details['email']
                }
            )

            cursor.execute("SELECT booking_seq.NEXTVAL FROM dual")
            booking_id = cursor.fetchone()[0]

            cursor.execute(
                """INSERT INTO Bookings (booking_id, flight_id, passenger_id, booking_date, class, seat_number, status, paid)
                VALUES (:booking_id, :flight_id, :passenger_id, :booking_date, :class, :seat_number, :status, :paid)""",
                {
                    'booking_id': booking_id,
                    'flight_id': self.flight_id,
                    'passenger_id': passenger_id,
                    'booking_date': datetime.date.today(),
                    'class': self.controller.travel_class,
                    'seat_number': self.passenger_details['seat'],
                    'status': "Confirmed",
                    'paid': True
                }
            )

            connection.commit()
            messagebox.showinfo("Success", "Booking details stored successfully!")

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            print(f"Error: {e}")

        finally:
            cursor.close()
            connection.close()

        return booking_id


class ViewCancelPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="#eaf2f8")  

        header = tk.Label(self, text="View or Cancel Ticket", font=("Georgia", 24, "bold"),
                          bg="#2c3e50", fg="white", pady=10)
        header.pack(fill="x", pady=(0, 20))

        content_frame = tk.Frame(self, bg="#eaf2f8", pady=20)
        content_frame.pack(expand=True)

        tk.Label(content_frame, text="Enter Booking ID to search:", font=("Arial", 14), bg="#eaf2f8", fg="#2c3e50").pack(pady=10)
        self.booking_id_entry = tk.Entry(content_frame, font=("Arial", 14), width=30)
        self.booking_id_entry.pack(pady=5)

        # Search Button
        tk.Button(content_frame, text="Search", font=("Arial", 14), bg="#5dade2", fg="white", width=15, height=2, bd=0,
                  activebackground="#1976d2", activeforeground="white", command=self.search_tickets).pack(pady=10)

        # Treeview for Displaying Passenger Details
        self.tree = ttk.Treeview(content_frame, columns=("Passenger ID", "First Name", "Last Name", "DOB", "Phone", "Email"), show="headings", height=5)
        self.tree.heading("Passenger ID", text="Passenger ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("DOB", text="DOB")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.column("Passenger ID", width=100, anchor="center")
        self.tree.column("First Name", width=120, anchor="center")
        self.tree.column("Last Name", width=120, anchor="center")
        self.tree.column("DOB", width=100, anchor="center")
        self.tree.column("Phone", width=120, anchor="center")
        self.tree.column("Email", width=200, anchor="center")
        self.tree.pack(pady=10, fill="x", expand=True)

        # Cancel Button
        tk.Button(content_frame, text="Cancel Ticket", font=("Arial", 14), bg="#e74c3c", fg="white", width=15, height=2, bd=0,
                  activebackground="#e63946", activeforeground="white", command=self.cancel_ticket).pack(pady=10)

        # Back Button
        tk.Button(self, text="Back", font=("Arial", 14), bg="#95a5a6", fg="white", width=15, height=2, bd=0,
                  activebackground="#7f8c8d", activeforeground="white", command=lambda: controller.show_frame(HomePage)).pack(side="bottom", pady=20)

    def search_tickets(self):
        # Get the Booking ID from the entry field
        booking_id = self.booking_id_entry.get().strip()

        if not booking_id:
            messagebox.showerror("Input Error", "Please enter a Booking ID.")
            return

        try:
            # Connect to Oracle database using oracledb
            connection = oracledb.connect(user='system', password='2006', dsn='SURIYAGANESH57:1521/orcl')
            cursor = connection.cursor()

            # Query to get passenger and booking details based on booking_id
            query = '''
                SELECT p.passenger_id, p.first_name, p.last_name, p.dob, p.phone_number, p.email
                FROM passengers p
                JOIN bookings b ON p.passenger_id = b.passenger_id
                WHERE b.booking_id = :booking_id
            '''
            cursor.execute(query, booking_id=booking_id)

            # Fetch the results
            results = cursor.fetchall()

            # Clear the treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert data into treeview
            if results:
                for result in results:
                    self.tree.insert("", "end", values=result)
            else:
                messagebox.showinfo("No Results", "No passengers found for the given Booking ID.")

            cursor.close()
            connection.close()

        except oracledb.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error fetching data from database: {str(e)}")

    def cancel_ticket(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a passenger to cancel their booking.")
            return

        # Get passenger details from the selected row
        passenger = self.tree.item(selected_item, "values")
        passenger_id = passenger[0]  # Passenger ID to use for cancellation

        # Confirm cancellation
        confirm = messagebox.askyesno("Cancel Ticket", "Are you sure you want to cancel this ticket?")
        if not confirm:
            return

        try:
            # Connect to Oracle database using oracledb
            connection = oracledb.connect(user='system', password='2006', dsn='SURIYAGANESH57:1521/orcl')
            cursor = connection.cursor()

            # Delete from Bookings table
            delete_booking_query = 'DELETE FROM bookings WHERE passenger_id = :passenger_id'
            cursor.execute(delete_booking_query, passenger_id=passenger_id)

            # Delete from Passengers table
            delete_passenger_query = 'DELETE FROM passengers WHERE passenger_id = :passenger_id'
            cursor.execute(delete_passenger_query, passenger_id=passenger_id)

            # Commit the changes
            connection.commit()

            # Remove the entry from the treeview
            self.tree.delete(selected_item)
            messagebox.showinfo("Success", "Ticket cancelled successfully.")

            cursor.close()
            connection.close()

        except oracledb.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error cancelling the ticket: {str(e)}")

if __name__ == "__main__":
    app = FlightReservationApp()
    app.mainloop()