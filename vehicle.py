import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os
# ================= DATABASE =================

DB_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "autocare.db"
)

def connect_db():
    return sqlite3.connect(DB_FILE)

def initialize_database():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicles(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT UNIQUE NOT NULL,
            owner TEXT NOT NULL,
            phone TEXT,
            model TEXT,
            type TEXT,
            km INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS services(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle TEXT NOT NULL,
            service TEXT NOT NULL,
            date TEXT,
            mechanic TEXT,
            cost REAL,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()

# ================= COLORS =================

BG = "#F5F7FB"
WHITE = "#FFFFFF"
SIDEBAR = "#111827"
BLUE = "#2563EB"
BLUE_DARK = "#1D4ED8"
GREEN = "#16A34A"
RED = "#DC2626"
ORANGE = "#F59E0B"
PURPLE = "#7C3AED"
TEXT = "#1E293B"
MUTED = "#64748B"
BORDER = "#E5E7EB"

# ================= MAIN APPLICATION =================

def main_application():

    root = tk.Tk()
    root.title("AutoCare - Vehicle Service Management")
    root.geometry("1250x750")
    root.minsize(1100,680)
    root.configure(bg=BG)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background=WHITE,
        foreground=TEXT,
        fieldbackground=WHITE,
        rowheight=40,
        font=("Segoe UI",10)
    )

    style.configure(
        "Treeview.Heading",
        background="#F8FAFC",
        foreground=MUTED,
        font=("Segoe UI",10,"bold")
    )

    style.map(
        "Treeview",
        background=[("selected","#DBEAFE")],
        foreground=[("selected",TEXT)]
    )

    style.configure(
        "TCombobox",
        padding=7,
        font=("Segoe UI",10)
    )

    # ================= SIDEBAR =================

    sidebar = tk.Frame(
        root,
        bg=SIDEBAR,
        width=235
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    sidebar.pack_propagate(False)

    tk.Label(
        sidebar,
        text="AUTO",
        font=("Segoe UI",22,"bold"),
        fg="#60A5FA",
        bg=SIDEBAR
    ).pack(pady=(25,0))

    tk.Label(
        sidebar,
        text="CARE",
        font=("Segoe UI",22,"bold"),
        fg=WHITE,
        bg=SIDEBAR
    ).pack()

    tk.Label(
        sidebar,
        text="VEHICLE SERVICE SYSTEM",
        font=("Segoe UI",8,"bold"),
        fg="#64748B",
        bg=SIDEBAR
    ).pack(pady=(5,30))

    # ================= CONTENT =================

    content = tk.Frame(
        root,
        bg=BG
    )

    content.pack(
        side="right",
        fill="both",
        expand=True
    )

    header = tk.Frame(
        content,
        bg=WHITE,
        height=70
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    header_title = tk.Label(
        header,
        text="Dashboard",
        font=("Segoe UI",18,"bold"),
        fg=TEXT,
        bg=WHITE
    )

    header_title.pack(
        side="left",
        padx=30
    )

    tk.Label(
        header,
        text="Administrator",
        font=("Segoe UI",10,"bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(
        side="right",
        padx=30
    )

    page = tk.Frame(
        content,
        bg=BG
    )

    page.pack(
        fill="both",
        expand=True
    )

    def clear_page():
        for widget in page.winfo_children():
            widget.destroy()

    def set_title(title):
        header_title.config(text=title)

    # ================= DASHBOARD =================

    def dashboard():

        clear_page()
        set_title("Dashboard")

        tk.Label(
            page,
            text="Good morning, Administrator",
            font=("Segoe UI",24,"bold"),
            fg=TEXT,
            bg=BG
        ).pack(
            anchor="w",
            padx=30,
            pady=(30,2)
        )

        tk.Label(
            page,
            text="Manage vehicles, services and billing from one place.",
            font=("Segoe UI",10),
            fg=MUTED,
            bg=BG
        ).pack(
            anchor="w",
            padx=30
        )

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM vehicles")
        total_vehicles = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM services")
        total_services = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM services WHERE status='Pending'"
        )
        pending = cur.fetchone()[0]

        cur.execute(
            "SELECT COALESCE(SUM(cost),0) FROM services"
        )
        revenue = cur.fetchone()[0]

        conn.close()

        cards = tk.Frame(
            page,
            bg=BG
        )

        cards.pack(
            fill="x",
            padx=25,
            pady=25
        )

        card_data = [
            ("Total Vehicles",str(total_vehicles),BLUE),
            ("Total Services",str(total_services),GREEN),
            ("Pending Services",str(pending),ORANGE),
            ("Total Revenue",f"₹{revenue:,.2f}",PURPLE)
        ]

        for i,(title,value,color) in enumerate(card_data):

            cards.columnconfigure(i,weight=1)

            card = tk.Frame(
                cards,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1,
                height=130
            )

            card.grid(
                row=0,
                column=i,
                padx=7,
                sticky="nsew"
            )

            tk.Frame(
                card,
                bg=color,
                width=5
            ).pack(
                side="left",
                fill="y"
            )

            inside = tk.Frame(
                card,
                bg=WHITE
            )

            inside.pack(
                fill="both",
                expand=True,
                padx=18,
                pady=15
            )

            tk.Label(
                inside,
                text=title,
                font=("Segoe UI",10),
                fg=MUTED,
                bg=WHITE
            ).pack(anchor="w")

            tk.Label(
                inside,
                text=value,
                font=("Segoe UI",22,"bold"),
                fg=TEXT,
                bg=WHITE
            ).pack(
                anchor="w",
                pady=(10,0)
            )

        panel = tk.Frame(
            page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        panel.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0,30)
        )

        tk.Label(
            panel,
            text="Recent Service Records",
            font=("Segoe UI",15,"bold"),
            fg=TEXT,
            bg=WHITE
        ).pack(
            anchor="w",
            padx=20,
            pady=15
        )

        table = ttk.Treeview(
            panel,
            columns=(
                "Vehicle",
                "Service",
                "Date",
                "Mechanic",
                "Cost",
                "Status"
            ),
            show="headings"
        )

        for col in (
            "Vehicle",
            "Service",
            "Date",
            "Mechanic",
            "Cost",
            "Status"
        ):
            table.heading(col,text=col)
            table.column(
                col,
                width=140,
                anchor="center"
            )

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0,20)
        )

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT vehicle,service,date,mechanic,cost,status
            FROM services
            ORDER BY id DESC
            LIMIT 10
        """)

        rows = cur.fetchall()
        conn.close()

        for row in rows:

            table.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    f"₹{row[4]:,.2f}",
                    row[5]
                )
            )

    # ================= VEHICLES =================

    def vehicle_page():

        clear_page()
        set_title("Vehicle Management")

        tk.Label(
            page,
            text="Vehicle Management",
            font=("Segoe UI",24,"bold"),
            fg=TEXT,
            bg=BG
        ).pack(
            anchor="w",
            padx=30,
            pady=(30,2)
        )

        tk.Label(
            page,
            text="Register and manage customer vehicles.",
            font=("Segoe UI",10),
            fg=MUTED,
            bg=BG
        ).pack(
            anchor="w",
            padx=30
        )

        form = tk.Frame(
            page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        form.pack(
            fill="x",
            padx=30,
            pady=20
        )

        fields = [
            "Vehicle Number",
            "Owner Name",
            "Phone",
            "Vehicle Model",
            "Vehicle Type",
            "Current KM"
        ]

        entries = []

        for i,field in enumerate(fields):

            row = i // 3
            col = i % 3

            box = tk.Frame(
                form,
                bg=WHITE
            )

            box.grid(
                row=row,
                column=col,
                padx=15,
                pady=10,
                sticky="w"
            )

            tk.Label(
                box,
                text=field,
                font=("Segoe UI",9,"bold"),
                fg=MUTED,
                bg=WHITE
            ).pack(anchor="w")

            entry = tk.Entry(
                box,
                width=25,
                font=("Segoe UI",10),
                relief="solid",
                bd=1
            )

            entry.pack(
                pady=(5,0),
                ipady=6
            )

            entries.append(entry)

        panel = tk.Frame(
            page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        panel.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0,25)
        )

        table = ttk.Treeview(
            panel,
            columns=(
                "ID",
                "Number",
                "Owner",
                "Phone",
                "Model",
                "Type",
                "KM"
            ),
            show="headings"
        )

        for col in (
            "ID",
            "Number",
            "Owner",
            "Phone",
            "Model",
            "Type",
            "KM"
        ):
            table.heading(col,text=col)
            table.column(
                col,
                width=115,
                anchor="center"
            )

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        def refresh():

            for item in table.get_children():
                table.delete(item)

            conn = connect_db()
            cur = conn.cursor()

            cur.execute("""
                SELECT id,number,owner,phone,model,type,km
                FROM vehicles
                ORDER BY id DESC
            """)

            rows = cur.fetchall()
            conn.close()

            for row in rows:
                table.insert(
                    "",
                    "end",
                    values=row
                )

        def add_vehicle():

            try:

                number = entries[0].get().strip()
                owner = entries[1].get().strip()
                phone = entries[2].get().strip()
                model = entries[3].get().strip()
                vehicle_type = entries[4].get().strip()
                km = int(entries[5].get())

                if not number or not owner:

                    messagebox.showwarning(
                        "Required",
                        "Vehicle number and owner name are required."
                    )

                    return

                conn = connect_db()
                cur = conn.cursor()

                cur.execute("""
                    INSERT INTO vehicles
                    (number,owner,phone,model,type,km)
                    VALUES(?,?,?,?,?,?)
                """,(
                    number,
                    owner,
                    phone,
                    model,
                    vehicle_type,
                    km
                ))

                conn.commit()
                conn.close()

                for entry in entries:
                    entry.delete(0,tk.END)

                refresh()

                messagebox.showinfo(
                    "Success",
                    "Vehicle saved successfully."
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Input",
                    "Current KM must be a number."
                )

            except sqlite3.IntegrityError:

                messagebox.showerror(
                    "Duplicate Vehicle",
                    "This vehicle number already exists."
                )

        def delete_vehicle():

            selected = table.selection()

            if not selected:

                messagebox.showwarning(
                    "Select Vehicle",
                    "Please select a vehicle."
                )

                return

            values = table.item(
                selected[0],
                "values"
            )

            vehicle_id = values[0]

            if not messagebox.askyesno(
                "Delete Vehicle",
                "Are you sure you want to delete this vehicle?"
            ):
                return

            conn = connect_db()
            cur = conn.cursor()

            cur.execute(
                "DELETE FROM vehicles WHERE id=?",
                (vehicle_id,)
            )

            conn.commit()
            conn.close()

            refresh()

        button_frame = tk.Frame(
            form,
            bg=WHITE
        )

        button_frame.grid(
            row=2,
            column=0,
            columnspan=3,
            pady=12
        )

        tk.Button(
            button_frame,
            text="Add Vehicle",
            command=add_vehicle,
            bg=BLUE,
            fg=WHITE,
            activebackground=BLUE_DARK,
            font=("Segoe UI",10,"bold"),
            relief="flat",
            width=18,
            pady=8,
            cursor="hand2"
        ).pack(
            side="left",
            padx=8
        )

        tk.Button(
            button_frame,
            text="Delete Selected",
            command=delete_vehicle,
            bg=RED,
            fg=WHITE,
            activebackground="#B91C1C",
            font=("Segoe UI",10,"bold"),
            relief="flat",
            width=18,
            pady=8,
            cursor="hand2"
        ).pack(
            side="left",
            padx=8
        )

        refresh()

    # ================= SERVICES =================

    def service_page():

        clear_page()
        set_title("Service Management")

        tk.Label(
            page,
            text="Service Management",
            font=("Segoe UI",24,"bold"),
            fg=TEXT,
            bg=BG
        ).pack(
            anchor="w",
            padx=30,
            pady=(30,2)
        )

        tk.Label(
            page,
            text="Create and track vehicle service records.",
            font=("Segoe UI",10),
            fg=MUTED,
            bg=BG
        ).pack(
            anchor="w",
            padx=30
        )

        form = tk.Frame(
            page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        form.pack(
            fill="x",
            padx=30,
            pady=20
        )

        vehicle = tk.Entry(
            form,
            width=22,
            font=("Segoe UI",10)
        )

        service_type = ttk.Combobox(
            form,
            values=[
                "General Service",
                "Oil Change",
                "Brake Service",
                "Engine Service",
                "Tyre Replacement",
                "Battery Service"
            ],
            width=20
        )

        date = tk.Entry(
            form,
            width=22,
            font=("Segoe UI",10)
        )

        mechanic = tk.Entry(
            form,
            width=22,
            font=("Segoe UI",10)
        )

        cost = tk.Entry(
            form,
            width=22,
            font=("Segoe UI",10)
        )

        status = ttk.Combobox(
            form,
            values=[
                "Pending",
                "Completed"
            ],
            width=20
        )

        date.insert(
            0,
            datetime.now().strftime("%d-%m-%Y")
        )

        status.set("Pending")

        fields = [
            ("Vehicle Number",vehicle),
            ("Service Type",service_type),
            ("Date",date),
            ("Mechanic",mechanic),
            ("Cost",cost),
            ("Status",status)
        ]

        for i,(label,widget) in enumerate(fields):

            row = i // 3
            col = i % 3

            box = tk.Frame(
                form,
                bg=WHITE
            )

            box.grid(
                row=row,
                column=col,
                padx=15,
                pady=10
            )

            tk.Label(
                box,
                text=label,
                font=("Segoe UI",9,"bold"),
                fg=MUTED,
                bg=WHITE
            ).pack(anchor="w")

            widget.pack(
                pady=(5,0),
                ipady=5
            )

        def refresh():

            for item in table.get_children():
                table.delete(item)

            conn = connect_db()
            cur = conn.cursor()

            cur.execute("""
                SELECT id,vehicle,service,date,mechanic,cost,status
                FROM services
                ORDER BY id DESC
            """)

            rows = cur.fetchall()
            conn.close()

            for row in rows:

                table.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        f"₹{row[5]:,.2f}",
                        row[6]
                    )
                )

        def add_service():

            try:

                vehicle_number = vehicle.get().strip()
                service_name = service_type.get().strip()
                service_date = date.get().strip()
                mechanic_name = mechanic.get().strip()
                service_cost = float(cost.get())
                service_status = status.get()

                if not vehicle_number or not service_name:

                    messagebox.showwarning(
                        "Required",
                        "Vehicle number and service type are required."
                    )

                    return

                conn = connect_db()
                cur = conn.cursor()

                cur.execute("""
                    INSERT INTO services
                    (vehicle,service,date,mechanic,cost,status)
                    VALUES(?,?,?,?,?,?)
                """,(
                    vehicle_number,
                    service_name,
                    service_date,
                    mechanic_name,
                    service_cost,
                    service_status
                ))

                conn.commit()
                conn.close()

                vehicle.delete(0,tk.END)
                mechanic.delete(0,tk.END)
                cost.delete(0,tk.END)

                refresh()

                messagebox.showinfo(
                    "Success",
                    "Service record saved successfully."
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Cost",
                    "Please enter a valid numeric cost."
                )

        def delete_service():

            selected = table.selection()

            if not selected:

                messagebox.showwarning(
                    "Select Service",
                    "Please select a service record."
                )

                return

            values = table.item(
                selected[0],
                "values"
            )

            service_id = values[0]

            if not messagebox.askyesno(
                "Delete Service",
                "Are you sure you want to delete this service?"
            ):
                return

            conn = connect_db()
            cur = conn.cursor()

            cur.execute(
                "DELETE FROM services WHERE id=?",
                (service_id,)
            )

            conn.commit()
            conn.close()

            refresh()

        button_frame = tk.Frame(
            form,
            bg=WHITE
        )

        button_frame.grid(
            row=2,
            column=0,
            columnspan=3,
            pady=12
        )

        tk.Button(
            button_frame,
            text="Add Service",
            command=add_service,
            bg=BLUE,
            fg=WHITE,
            activebackground=BLUE_DARK,
            font=("Segoe UI",10,"bold"),
            relief="flat",
            width=18,
            pady=8,
            cursor="hand2"
        ).pack(
            side="left",
            padx=8
        )

        tk.Button(
            button_frame,
            text="Delete Selected",
            command=delete_service,
            bg=RED,
            fg=WHITE,
            activebackground="#B91C1C",
            font=("Segoe UI",10,"bold"),
            relief="flat",
            width=18,
            pady=8,
            cursor="hand2"
        ).pack(
            side="left",
            padx=8
        )

        panel = tk.Frame(
            page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        panel.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0,25)
        )

        table = ttk.Treeview(
            panel,
            columns=(
                "ID",
                "Vehicle",
                "Service",
                "Date",
                "Mechanic",
                "Cost",
                "Status"
            ),
            show="headings"
        )

        for col in (
            "ID",
            "Vehicle",
            "Service",
            "Date",
            "Mechanic",
            "Cost",
            "Status"
        ):

            table.heading(
                col,
                text=col
            )

            table.column(
                col,
                width=120,
                anchor="center"
            )

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        refresh()

    # ================= BILLING =================

    def billing_page():

        clear_page()
        set_title("Billing")

        tk.Label(
            page,
            text="Service Billing",
            font=("Segoe UI",24,"bold"),
            fg=TEXT,
            bg=BG
        ).pack(
            anchor="w",
            padx=30,
            pady=(30,2)
        )

        tk.Label(
            page,
            text="Calculate customer service bills.",
            font=("Segoe UI",10),
            fg=MUTED,
            bg=BG
        ).pack(
            anchor="w",
            padx=30
        )

        card = tk.Frame(
            page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            padx=150,
            pady=30,
            fill="x"
        )

        fields = [
            "Oil Change",
            "Brake Service",
            "Engine Service",
            "Labour Charge",
            "Other Charges"
        ]

        entries = []

        for i,field in enumerate(fields):

            tk.Label(
                card,
                text=field,
                font=("Segoe UI",10,"bold"),
                fg=MUTED,
                bg=WHITE
            ).grid(
                row=i,
                column=0,
                padx=30,
                pady=10,
                sticky="w"
            )

            entry = tk.Entry(
                card,
                width=30,
                font=("Segoe UI",10)
            )

            entry.grid(
                row=i,
                column=1,
                padx=30,
                pady=10,
                ipady=5
            )

            entries.append(entry)

        result = tk.Label(
            card,
            text="Total Amount\n₹0.00",
            font=("Segoe UI",17,"bold"),
            fg=BLUE,
            bg=WHITE
        )

        result.grid(
            row=7,
            column=0,
            columnspan=2,
            pady=20
        )

        def calculate():

            try:

                total = sum(
                    float(entry.get() or 0)
                    for entry in entries
                )

                if total >= 10000:
                    discount = total * 0.10
                else:
                    discount = total * 0.05

                final_amount = total - discount

                result.config(
                    text=(
                        f"Subtotal: ₹{total:,.2f}\n"
                        f"Discount: ₹{discount:,.2f}\n"
                        f"Final Bill: ₹{final_amount:,.2f}"
                    )
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Amount",
                    "Enter valid numeric amounts."
                )

        tk.Button(
            card,
            text="Calculate Bill",
            command=calculate,
            bg=GREEN,
            fg=WHITE,
            font=("Segoe UI",10,"bold"),
            relief="flat",
            width=22,
            pady=9,
            cursor="hand2"
        ).grid(
            row=6,
            column=0,
            columnspan=2
        )

    # ================= SERVICE DUE =================

    def service_due_page():

        clear_page()
        set_title("Service Due")

        tk.Label(
            page,
            text="Service Due Checker",
            font=("Segoe UI",24,"bold"),
            fg=TEXT,
            bg=BG
        ).pack(
            anchor="w",
            padx=30,
            pady=(30,2)
        )

        tk.Label(
            page,
            text="Check whether a vehicle requires service.",
            font=("Segoe UI",10),
            fg=MUTED,
            bg=BG
        ).pack(
            anchor="w",
            padx=30
        )

        card = tk.Frame(
            page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            padx=180,
            pady=40
        )

        tk.Label(
            card,
            text="Last Service KM",
            font=("Segoe UI",10,"bold"),
            fg=MUTED,
            bg=WHITE
        ).grid(
            row=0,
            column=0,
            padx=30,
            pady=20
        )

        last = tk.Entry(
            card,
            width=30,
            font=("Segoe UI",10)
        )

        last.grid(
            row=0,
            column=1,
            padx=30,
            ipady=5
        )

        tk.Label(
            card,
            text="Current KM",
            font=("Segoe UI",10,"bold"),
            fg=MUTED,
            bg=WHITE
        ).grid(
            row=1,
            column=0,
            padx=30,
            pady=20
        )

        current = tk.Entry(
            card,
            width=30,
            font=("Segoe UI",10)
        )

        current.grid(
            row=1,
            column=1,
            padx=30,
            ipady=5
        )

        result = tk.Label(
            card,
            text="",
            font=("Segoe UI",16,"bold"),
            bg=WHITE
        )

        result.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=25
        )

        def check():

            try:

                last_km = int(last.get())
                current_km = int(current.get())

                difference = current_km - last_km

                if difference < 0:

                    result.config(
                        text="Invalid KM values",
                        fg=RED
                    )

                elif difference >= 5000:

                    result.config(
                        text="SERVICE DUE",
                        fg=RED
                    )

                elif difference >= 4000:

                    result.config(
                        text="SERVICE DUE SOON",
                        fg=ORANGE
                    )

                else:

                    result.config(
                        text="SERVICE NOT DUE",
                        fg=GREEN
                    )

            except ValueError:

                messagebox.showerror(
                    "Invalid Input",
                    "Enter valid KM values."
                )

        tk.Button(
            card,
            text="Check Service",
            command=check,
            bg=BLUE,
            fg=WHITE,
            font=("Segoe UI",10,"bold"),
            relief="flat",
            width=22,
            pady=9,
            cursor="hand2"
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=10
        )

    # ================= NAVIGATION =================

    navigation = [
        ("Dashboard",dashboard),
        ("Vehicles",vehicle_page),
        ("Services",service_page),
        ("Billing",billing_page),
        ("Service Due",service_due_page)
    ]

    for name,command in navigation:

        tk.Button(
            sidebar,
            text=name,
            command=command,
            font=("Segoe UI",10,"bold"),
            bg=SIDEBAR,
            fg="#CBD5E1",
            activebackground="#1E293B",
            activeforeground=WHITE,
            relief="flat",
            anchor="w",
            padx=30,
            pady=15,
            cursor="hand2"
        ).pack(fill="x")

    tk.Frame(
        sidebar,
        bg=SIDEBAR
    ).pack(
        fill="both",
        expand=True
    )

    def logout():

        if messagebox.askyesno(
            "Logout",
            "Do you want to logout?"
        ):
            root.destroy()
            create_login()

    tk.Button(
        sidebar,
        text="Logout",
        command=logout,
        font=("Segoe UI",10,"bold"),
        bg="#7F1D1D",
        fg=WHITE,
        activebackground=RED,
        relief="flat",
        anchor="w",
        padx=30,
        pady=15,
        cursor="hand2"
    ).pack(
        fill="x",
        pady=15
    )

    dashboard()
    root.mainloop()

# ================= LOGIN =================

def create_login():

    login_window = tk.Tk()

    login_window.title(
        "AutoCare - Login"
    )

    login_window.geometry(
        "1000x600"
    )

    login_window.configure(
        bg=BG
    )

    login_window.resizable(
        False,
        False
    )

    # LEFT SIDE

    left = tk.Frame(
        login_window,
        bg=SIDEBAR,
        width=500
    )

    left.pack(
        side="left",
        fill="y"
    )

    left.pack_propagate(False)

    tk.Label(
        left,
        text="AUTOCARE",
        font=("Segoe UI",34,"bold"),
        fg=WHITE,
        bg=SIDEBAR
    ).pack(
        pady=(150,5)
    )

    tk.Label(
        left,
        text="VEHICLE SERVICE",
        font=("Segoe UI",12,"bold"),
        fg="#60A5FA",
        bg=SIDEBAR
    ).pack()

    tk.Label(
        left,
        text="MANAGEMENT SYSTEM",
        font=("Segoe UI",12,"bold"),
        fg="#60A5FA",
        bg=SIDEBAR
    ).pack()

    tk.Label(
        left,
        text="Manage vehicles, services\nand billing in one place.",
        font=("Segoe UI",12),
        fg="#94A3B8",
        bg=SIDEBAR,
        justify="center"
    ).pack(
        pady=30
    )

    # RIGHT SIDE

    right = tk.Frame(
        login_window,
        bg=WHITE
    )

    right.pack(
        side="right",
        fill="both",
        expand=True
    )

    tk.Label(
        right,
        text="Welcome Back",
        font=("Segoe UI",27,"bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(
        pady=(110,5)
    )

    tk.Label(
        right,
        text="Sign in to your dashboard",
        font=("Segoe UI",10),
        fg=MUTED,
        bg=WHITE
    ).pack(
        pady=(0,30)
    )

    form = tk.Frame(
        right,
        bg=WHITE
    )

    form.pack(
        padx=70,
        fill="x"
    )

    tk.Label(
        form,
        text="Username",
        font=("Segoe UI",10,"bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(
        anchor="w"
    )

    username = tk.Entry(
        form,
        font=("Segoe UI",11),
        relief="solid",
        bd=1
    )

    username.pack(
        fill="x",
        pady=(7,20),
        ipady=8
    )

    tk.Label(
        form,
        text="Password",
        font=("Segoe UI",10,"bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(
        anchor="w"
    )

    password = tk.Entry(
        form,
        font=("Segoe UI",11),
        show="*",
        relief="solid",
        bd=1
    )

    password.pack(
        fill="x",
        pady=(7,25),
        ipady=8
    )

    def login():

        user = username.get().strip()
        pwd = password.get().strip()

        if user == "admin" and pwd == "1234":

            login_window.destroy()
            main_application()

        else:

            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password."
            )

    tk.Button(
        form,
        text="SIGN IN",
        command=login,
        bg=BLUE,
        fg=WHITE,
        activebackground=BLUE_DARK,
        activeforeground=WHITE,
        font=("Segoe UI",11,"bold"),
        relief="flat",
        pady=11,
        cursor="hand2"
    ).pack(
        fill="x"
    )

    tk.Label(
        right,
        text="Username: admin    Password: 1234",
        font=("Segoe UI",9),
        fg=MUTED,
        bg=WHITE
    ).pack(
        pady=25
    )

    username.focus()

    login_window.bind(
        "<Return>",
        lambda event: login()
    )

    login_window.mainloop()

# ================= START PROGRAM =================

initialize_database()
create_login()