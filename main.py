import tkinter as tk
import ttkbootstrap as ttk

app = ttk.Window()
style = ttk.Style()
style.configure('TombolMain.TButton', font=('Futura', 30), foreground='white', background='#2596be', padding=10,
                borderwidth = 0, relief = "flat", bordercolor = "black", borderradius=20)
style.map("TombolMain.TButton", background = [("active", "#154c79"), ("pressed", "black")])
def klik_tombol_jadwal():
    print("JADWAL")

def klik_tombol_peserta_kelas():
    print("PESERTA KELAS")
app.title("Mesin Absensi dan Rekap Kehadiran (MARK)")

background = ttk.PhotoImage(file=r"itboy.png")
canvas = ttk.Canvas(app, width=background.width(), height=background.height())
canvas.create_image(0, 0, image=background, anchor='nw')
canvas.pack()

gedung = ttk.Label(canvas, text="K2.9654", font=("Helvetica", 40, "bold"))
matkul = ttk.Label(canvas, text="Pengantar Rekaya dan Desain", font=("Helvetica", 40, "bold"))
kelas = ttk.Label(canvas, text="K-69", font=("Helvetica", 40, "bold"))
nama = ttk.Label(canvas, text=f"Nama                     :  ", font=("Helvetica", 20, "bold"))
nim = ttk.Label(canvas, text="NIM                        : ", font=("Helvetica", 20, "bold"))
status = ttk.Label(canvas, text="Status Kehadiran : ", font=("Helvetica", 20, "bold"))
tombol_jadwal = ttk.Button(canvas, text="Jadwal", command=klik_tombol_jadwal(), style="TombolMain.TButton")
tombol_peserta_kelas = ttk.Button(canvas, text="Peserta Kelas", command=klik_tombol_peserta_kelas(), style="TombolMain.TButton")

canvas.create_window(720, 100, window = gedung)
canvas.create_window(720, 200, window = matkul)
canvas.create_window(720, 300, window = kelas)
canvas.create_window(350, 600, window = nama)
canvas.create_window(350, 650, window = nim)
canvas.create_window(350, 700, window = status)
# canvas.create_window(250, 650, window = tombol_jadwal)
# canvas.create_window(1110, 650, window = tombol_peserta_kelas)
app.mainloop()