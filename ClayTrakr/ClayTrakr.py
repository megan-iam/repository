import tkinter as tk
from PIL import ImageTk
from PIL import Image


class PotteryTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ClayTrackr ~ simple pottery tracker")

        # Initialize variables to store user input
        self.piece_name = tk.StringVar()
        self.type = tk.StringVar(value="Plate")
        self.stage_dates = {
            "Formed": {"var": tk.BooleanVar(), "date": tk.StringVar(), "checkbox": None, "entry": None},
            "Trimmed": {"var": tk.BooleanVar(), "date": tk.StringVar(), "checkbox": None, "entry": None},
            "Bisqued": {"var": tk.BooleanVar(), "date": tk.StringVar(), "checkbox": None, "entry": None},
            "Glazed": {"var": tk.BooleanVar(), "date": tk.StringVar(), "checkbox": None, "entry": None},
            "Finished": {"var": tk.BooleanVar(), "date": tk.StringVar(), "checkbox": None, "entry": None}
        }
        self.notes = tk.StringVar()
        
        #Place logo on top
        self.image_path="Logo.png"
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(master, image=self.photo)
        self.image_label.grid(row=0, column=0)
        
        # Create input field
        tk.Label(master, text="Piece Name:").grid(row=1, column=0, sticky="e")
        self.piece_name_entry = tk.Entry(master, textvariable=self.piece_name)
        self.piece_name_entry.grid(row=1, column=1)
        
        tk.Label(master, text="Type:").grid(row=2, column=0, sticky="e")
        types = ["Plate", "Bowl", "Mug", "Vase", "Pot", "Other"]
        self.type_optionmenu = tk.OptionMenu(master, self.type, *types)
        self.type_optionmenu.grid(row=2, column=1, sticky="w")
        
        # Create entry fields for stage dates and checkboxes for stages
        stages_frame = tk.LabelFrame(master, text="Stages")
        stages_frame.grid(row=3, column=0, columnspan=2, sticky="we", padx=10, pady=5)
        row_num = 0
        for stage in self.stage_dates:
            self.stage_dates[stage]["checkbox"] = tk.Checkbutton(stages_frame, text=stage, variable=self.stage_dates[stage]["var"], command=lambda stage=stage: self.toggle_stage_entry(stage))
            self.stage_dates[stage]["checkbox"].grid(row=row_num, column=0, sticky="w")
            self.stage_dates[stage]["entry"] = tk.Entry(stages_frame, textvariable=self.stage_dates[stage]["date"], state="disabled")
            self.stage_dates[stage]["entry"].grid(row=row_num, column=1, sticky="w")
            row_num += 1

        # Create text box for notes
        tk.Label(master, text="Notes:").grid(row=4, column=0, sticky="e")
        self.notes_text = tk.Text(master, height=4, width=30)
        self.notes_text.grid(row=4, column=1, columnspan=2)
        
        # Create button to add piece
        tk.Button(master, text="Add Piece", command=self.add_piece_to_listbox).grid(row=5, column=0, columnspan=2, pady=5)

        # Create listbox to display piece names
        self.piece_listbox = tk.Listbox(master, height=10, width=50)
        self.piece_listbox.grid(row=6, column=0, columnspan=2)
        self.piece_listbox.bind("<<ListboxSelect>>", self.show_timeline)

        # Create Edit button
        tk.Button(master, text="Edit", command=self.edit_selected_piece).grid(row=7, column=0, pady=5)
        
        # Create Delete button
        tk.Button(master, text="Delete", command=self.delete_selected_piece).grid(row=7, column=1, pady=5)

        # Center all widgets
        for child in master.winfo_children():
            child.grid_configure(padx=10, pady=5)
            child.grid_configure(sticky="nsew")
            
    def toggle_stage_entry(self, stage):
        if self.stage_dates[stage]["var"].get():
            self.stage_dates[stage]["entry"].config(state="normal")
        else:
            self.stage_dates[stage]["entry"].config(state="disabled")

    def clear_form(self):
        self.piece_name.set("")
        self.type.set("Plate")
        for stage in self.stage_dates:
            self.stage_dates[stage]["var"].set(False)
            self.stage_dates[stage]["date"].set("")
            self.stage_dates[stage]["entry"].config(state="disabled")
        self.notes_text.delete("1.0", tk.END)

    def add_piece_to_listbox(self):
        stages_info = []
        for stage in self.stage_dates:
            if self.stage_dates[stage]["var"].get():
                stages_info.append(f"{stage}: {self.stage_dates[stage]['date'].get()}")
        piece_info = f"{self.piece_name.get()} - {self.type.get()} - {', '.join(stages_info)} - Notes: {self.notes_text.get('1.0', tk.END).strip()}"
        self.piece_listbox.insert(tk.END, piece_info)
        self.clear_form()

    def show_timeline(self, event):
        selected_piece_index = self.piece_listbox.curselection()[0]
        selected_piece_info = self.piece_listbox.get(selected_piece_index)
        # self.open_timeline_window(selected_piece_info)

    def edit_selected_piece(self):
        selected_piece_index = self.piece_listbox.curselection()
        if selected_piece_index:  # Check if any item is selected
            selected_piece_index = selected_piece_index[0]  # Get the first selected index
            piece_info = self.piece_listbox.get(selected_piece_index)
            parts = piece_info.split(" - ")
            piece_name, piece_type = parts[0], parts[1]
            stages_info = parts[2].split(", ")
            notes = parts[3].split(": ")[1]

            self.piece_name.set(piece_name)
            self.type.set(piece_type)

            # Reset the stages
            for stage in self.stage_dates:
                self.stage_dates[stage]["var"].set(False)
                self.stage_dates[stage]["date"].set("")
                self.stage_dates[stage]["entry"].config(state="disabled")

            # Populate the stages
            for stage_info in stages_info:
                stage, date = stage_info.split(": ")
                if stage in self.stage_dates:
                    self.stage_dates[stage]["var"].set(True)
                    self.stage_dates[stage]["date"].set(date)
                    self.stage_dates[stage]["entry"].config(state="normal")

            self.notes_text.delete("1.0", tk.END)  # Clear existing notes
            self.notes_text.insert(tk.END, notes)  # Populate notes text box with the extracted notes
            self.piece_listbox.delete(selected_piece_index)  # Remove the selected piece from the listbox



    def delete_selected_piece(self):
        selected_piece_index = self.piece_listbox.curselection()
        if selected_piece_index:
            self.piece_listbox.delete(selected_piece_index)

    # def open_timeline_window(self, piece_info):
    #     # Create a new window for timeline
    #     timeline_window = tk.Toplevel(self.master)
    #     timeline_window.title("Pottery Piece Info")
        
    #     # Create label for piece info
    #     piece_label = tk.Label(timeline_window, text="Piece Information:", font=("Arial", 12, "bold"))
    #     piece_label.pack(pady=5)

    #     # Display piece info
    #     piece_info_label = tk.Label(timeline_window, text=piece_info)
    #     piece_info_label.pack(pady=5)

    #     # Create label for timeline
    #     timeline_label = tk.Label(timeline_window, text="Timeline:", font=("Arial", 12, "bold"))
    #     timeline_label.pack(pady=5)

    #     # Add timeline stages
    #     piece_name, piece_type, *stages_info = piece_info.split(" - ")
    #     for stage_info in stages_info:
    #         stage_label = tk.Label(timeline_window, text=stage_info)
    #         stage_label.pack()
        
    #     # Create label for notes
    #     timeline_notes = tk.Label(timeline_window, text="Notes:", font=("Arial", 12, "bold"))
    #     timeline_notes.pack(pady=5)
        
    #     # Display notes
    #     notes_text = tk.Text(timeline_window, height=4, width=30)
    #     notes_text.insert(tk.END, self.notes_text.get("1.0", tk.END))
    #     notes_text.config(state="disabled")
    #     notes_text.pack()



root = tk.Tk()
root.configure(bg="#E17B89")  # Set the background color of the root window

app = PotteryTrackerApp(root)

root.mainloop()

if __name__ == "__main__":
    main()