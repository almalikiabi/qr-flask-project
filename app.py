from flask import Flask, request, render_template, redirect, url_for
import csv

app = Flask(__name__)

# PIN yang valid
VALID_PIN = "1234"

# URL ke file (misalnya link Google Drive atau URL file lain)
FILE_LINK = "https://docs.google.com/spreadsheets/d/1InhCZCr26RqOKR9l45PRXEPpFWmT29P5/edit?usp=sharing&ouid=113193728529755822035&rtpof=true&sd=true"  # Gantilah dengan link Anda

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

@app.route("/")
def home():
    url = "https://qr-flask-project-production.up.railway.app"  # Sesuaikan dengan URL aplikasi Anda
    return render_template("index.html", url=url)

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        pin = request.form["pin"]
        if pin == VALID_PIN:
            return redirect(url_for('submit_nik'))  # Arahkan ke halaman untuk memasukkan NIK
        else:
            return "PIN salah, coba lagi!"

    return render_template("verify_pin.html")

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

    if valid:
        # Arahkan pengguna ke link setelah NIK dan PIN valid
        return redirect(FILE_LINK)  # Arahkan ke file/link setelah verifikasi

    return render_template("submit_nik.html", error=error, valid=valid, name=name, nik=nik)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
