import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def return_to_menu(root):
    root.quit()  # Close current window (project window)
    root.after(100, root.deiconify)  # Show the main menu again
    
class ChargedRingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Charged Ring Potential and Field")

        # ورودی‌ها
        frame = ttk.Frame(root)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="Charge Q (μC):").grid(row=0, column=0)
        self.q_var = tk.DoubleVar(value=1)
        ttk.Entry(frame, textvariable=self.q_var).grid(row=0, column=1)

        ttk.Label(frame, text="Radius R (m):").grid(row=1, column=0)
        self.r_var = tk.DoubleVar(value=1)
        ttk.Entry(frame, textvariable=self.r_var).grid(row=1, column=1)

        ttk.Label(frame, text="Z min (m):").grid(row=2, column=0)
        self.zmin_var = tk.DoubleVar(value=-5)
        ttk.Entry(frame, textvariable=self.zmin_var).grid(row=2, column=1)

        ttk.Label(frame, text="Z max (m):").grid(row=3, column=0)
        self.zmax_var = tk.DoubleVar(value=5)
        ttk.Entry(frame, textvariable=self.zmax_var).grid(row=3, column=1)

        ttk.Button(frame, text="Calculate & Plot", command=self.calculate_and_plot).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Save Plot", command=self.save_plot).grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Exit", command=lambda: return_to_menu(root)).grid(row=5, column=0, columnspan=2, pady=5)

        # ناحیه رسم
        self.fig, self.axs = plt.subplots(2, 1, figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # نتیجه محاسبات
        self.result_label = ttk.Label(root, text="", font=("Arial", 10))
        self.result_label.pack(pady=5)

    def calculate_and_plot(self):
        q = self.q_var.get() * 1e-6  # μC to C
        R = self.r_var.get()
        epsilon_0 = 8.854e-12
        zmin = self.zmin_var.get()
        zmax = self.zmax_var.get()

        z = np.linspace(zmin, zmax, 500)
        V = (1 / (4 * np.pi * epsilon_0)) * q / np.sqrt(R**2 + z**2)
        E_z = (1 / (4 * np.pi * epsilon_0)) * q * z / (R**2 + z**2)**(1.5)

        # محاسبات عددی نمایش داده می‌شود
        potential_at_zmin = (1 / (4 * np.pi * epsilon_0)) * q / np.sqrt(R**2 + zmin**2)
        electric_field_at_zmin = (1 / (4 * np.pi * epsilon_0)) * q * zmin / (R**2 + zmin**2)**(1.5)

        self.result_label.config(
            text=f"At z={zmin} m:\nPotential (V) = {potential_at_zmin:.6f} V\nElectric Field (E) = {electric_field_at_zmin:.6f} V/m"
        )

        # رسم نمودار پتانسیل و میدان
        self.axs[0].clear()
        self.axs[0].plot(z, V, 'r')
        self.axs[0].set_title("Electric Potential V(z)")
        self.axs[0].set_xlabel("z (m)")
        self.axs[0].set_ylabel("V (Volts)")
        self.axs[0].grid(True)

        self.axs[1].clear()
        self.axs[1].plot(z, E_z, 'b')
        self.axs[1].set_title("Electric Field E_z(z)")
        self.axs[1].set_xlabel("z (m)")
        self.axs[1].set_ylabel("E (V/m)")
        self.axs[1].grid(True)

        self.fig.tight_layout()
        self.canvas.draw()

    def save_plot(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
        if file_path:
            self.fig.savefig(file_path)
            print(f"Saved to: {file_path}")

# اجرا
if __name__ == "__main__":
    root = tk.Tk()
    app = ChargedRingApp(root)
    root.mainloop()
