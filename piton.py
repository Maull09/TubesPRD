import openpyxl
import serial
import datetime
import time
import tkinter as tk
import ttkbootstrap as ttk

wb = openpyxl.load_workbook('data.xlsx')
mahasiswa_ws = wb['Mahasiswa']
kelas_ws = wb['Kelas']
kehadiran_ws = None


ser = serial.Serial('COM7', 9600) # sesuaikan dengan port serial pada komputer Anda
last_scan = None


def get_current_kelas():
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    
    kelas_data = {}

    # Check if there is a class scheduled at the current time and date
    for row in kelas_ws.iter_rows(min_row=2, values_only=True):
        start_time_str = row[5].strftime('%H:%M:%S')
        start_time = datetime.datetime.strptime(start_time_str, '%H:%M:%S')
        end_time_str = row[6].strftime('%H:%M:%S')
        date_class_str = row[7].strftime('%d-%m-%Y')

        if date_class_str == current_date and start_time_str <= current_time <= end_time_str:
            kode_kelas = row[0]
            kode_mata_kuliah = row[1]
            lokasi = row[2]
            mata_kuliah = row[3]
            dosen = row[4]
            kelas_data = {
                'kode_kelas': kode_kelas,
                'kode_mata_kuliah': kode_mata_kuliah,
                'lokasi': lokasi,
                'mata_kuliah': mata_kuliah,
                'dosen': dosen
            }
            break

    return kelas_data


current_time = datetime.datetime.now().strftime('%H:%M:%S')
current_date = datetime.datetime.now().strftime('%d-%m-%Y')


if current_date in wb.sheetnames:
    kehadiran_ws = wb[current_date]
else:
    kehadiran_ws = wb.create_sheet(current_date)
    kehadiran_ws.append(['Waktu', 'Nama', 'NIM', 'Tag RFID', 'Kehadiran', 'Mata Kuliah', 'Kode Mata Kuliah', 'Kode Kelas', 'Lokasi', 'Dosen'])


mahasiswa_data = []
for row in mahasiswa_ws.iter_rows(min_row=2, values_only=True):
    mahasiswa_data.append(row)


def scan_card():
    global last_scan
    data = ser.readline().decode().strip()

    if data and data != last_scan:
        last_scan = data
        name = None
        nim = None
        kehadiran = None
        mata_kuliah = None
        kode_mata_kuliah = None
        kode_kelas = None
        lokasi = None
        dosen = None

        # Find student data from Mahasiswa sheet
        for row in mahasiswa_data:
            if row[2] == data:
                name = row[0]
                nim = row[1]
                break
        
        # Find class data from Kelas sheet
        if name is not None:
            current_kelas = get_current_kelas()

            if current_kelas is not None :
                kode_kelas = current_kelas.get('kode_kelas')
                lokasi = current_kelas.get('lokasi')
                mata_kuliah = current_kelas.get('mata_kuliah')
                kode_mata_kuliah = current_kelas.get('kode_mata_kuliah')
                dosen = current_kelas.get('dosen')
                kehadiran = 'Hadir'
        
        # Write data to Kehadiran sheet
        if name is not None:
            kehadiran_ws.append([f'{current_date} {current_time}', name, nim, data, kehadiran, mata_kuliah, kode_mata_kuliah, kode_kelas, lokasi, dosen])
            wb.save('data.xlsx')
            gedung.config(text=f"{lokasi}")
            nama.config(text=f"Nama                     :  {name}")
            # nim.config(text=f"NIM                        :     {nim}")
            status.config(text=f"Status Kehadiran :     {kehadiran}" )

        else:
            print(f'Data not found! {data}')
            
# gedung = None
# nama = None
# status = None


# def create_widget() :
#     global gedung
#     global nama
#     global status
#     global app

app = ttk.Window()
app.title("Mesin Absensi dan Rekap Kehadiran (MARK)")
background = ttk.PhotoImage(file=r"itboy.png")
canvas = ttk.Canvas(app, width=background.width(), height=background.height())
canvas.create_image(0, 0, image=background, anchor='nw')
canvas.pack()
gedung = ttk.Label(canvas, text="", font=("Helvetica", 40, "bold"))
gedung.pack()
matkul = ttk.Label(canvas, text="", font=("Helvetica", 40, "bold"))
matkul.pack()
kelas = ttk.Label(canvas, text="", font=("Helvetica", 40, "bold"))
kelas.pack()
nama = ttk.Label(canvas, text="", font=("Helvetica", 20, "bold"))
nama.pack()
# nim = ttk.Label(canvas, text="", font=("Helvetica", 20, "bold"))
# nim.pack()
status = ttk.Label(canvas, text="", font=("Helvetica", 20, "bold"))
status.pack()

canvas.create_window(720, 100, window = gedung)
canvas.create_window(720, 200, window = matkul)
canvas.create_window(720, 300, window = kelas)
canvas.create_window(350, 600, window = nama)
# canvas.create_window(350, 650, window = nim)
canvas.create_window(350, 700, window = status)


app.after(1000,scan_card())
# canvas.create_window(250, 650, window = tombol_jadwal)
# canvas.create_window(1110, 650, window = tombol_peserta_kelas)

app.mainloop()


    