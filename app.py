from flask import Flask, request, render_template, redirect, url_for
import qrcode
import csv

app = Flask(__name__)

# PIN yang valid
VALID_PIN = "1234"

# Fungsi untuk memeriksa apakah NIK dan Nama terdaftar
def is_valid_employee(nik, name):
    try:
        with open('karyawan.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['NIK'] == nik and row['Nama'].lower() == name.lower():
                    return True
    except FileNotFoundError:
        print("File karyawan.csv tidak ditemukan.")
    return False

# Halaman pertama (QR Code)
@app.route("/")
def home():
    # URL yang ingin di-encode ke dalam QR Code
    url = "http://127.0.0.1:5000/verify"  # Sesuaikan URL lokal/hosting
    
    # Buat QR code dan simpan di folder static
    qr = qrcode.make(url)
    qr.save("static/qrcode.png")  # Menyimpan QR code sebagai qrcode.png di folder static
    
    # Tampilkan halaman index.html yang berisi QR code
    return render_template("index.html")

# Halaman untuk memasukkan PIN setelah memindai QR
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        pin = request.form["pin"]
        if pin == VALID_PIN:
            return redirect(url_for('submit_employee'))  # Arahkan ke halaman untuk memasukkan data karyawan
        else:
            return "PIN salah, coba lagi!"
    
    # Tampilkan form untuk memasukkan PIN
    return render_template("verify_pin.html")

# Halaman untuk memeriksa validitas data karyawan
@app.route("/submit_employee", methods=["GET", "POST"])
def submit_employee():
    if request.method == "POST":
        name = request.form["name"]
        nik = request.form["nik"]
        
        # Periksa apakah data karyawan valid
        if is_valid_employee(nik, name):
            return f"Selamat datang, {name} (NIK: {nik}). Anda berhasil mengakses QR!"
        else:
            return "Data Anda tidak valid. Hubungi HR untuk informasi lebih lanjut."
    
    # Tampilkan form untuk memasukkan data karyawan
@app.route("/submit_nik", methods=["GET", "POST"])
def submit_nik():
    error = None
    valid = False
    name = None
    nik = None

    if request.method == "POST":
        nik = request.form["nik"]
        name = request.form["name"]

        # Validasi NIK di file CSV
        with open("karyawan.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["NIK"] == nik:
                    valid = True
                    name = row["Nama"]
                    break

        if not valid:
            error = "NIK tidak terdaftar. Silakan coba lagi."

    return render_template("submit_nik.html", error=error, valid=valid, name=name, nik=nik)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
