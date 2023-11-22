import os
import pdfplumber
from fpdf import FPDF
import tkinter as tk #tkinter kütüphanesi kullanıldı.
from tkinter import messagebox # Başarılı buton işlemlerinde mesaj box ile kullanıcıya bilgi gösterimi

class PdfManager:
    def __init__(self, pdf_folder="pdfler"):
        self.pdf_folder = pdf_folder
        self.pdf_files = [os.path.join(self.pdf_folder, f) for f in os.listdir(self.pdf_folder) if f.endswith(".pdf")]
        self.titles = []

    def extract_titles_from_pdf(self, pdf_path):
        titles = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                titles.extend(text.split('\n'))

        return titles

    def read_pdf_files(self):
        for pdf_file in self.pdf_files:
            self.titles.extend(self.extract_titles_from_pdf(pdf_file))

    def save_titles_to_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for title in self.titles:
            pdf.cell(200, 10, txt=title, ln=True)

        pdf.output("newfile.pdf")
        messagebox.showinfo("Başarı", "Başlıklar yeni PDF dosyasına başarıyla kaydedildi: newfile.pdf")

class PDFManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Manager")
        self.pdf_manager = PdfManager()

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        tk.Label(frame, text="Menü:", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(frame, text="PDF Dosya İçerik (Başlıklar) Oku", command=self.read_pdf).grid(row=1, column=0, pady=5)
        tk.Button(frame, text="PDF (Başlıkları) Kaydet", command=self.save_pdf).grid(row=1, column=1, pady=5)
        tk.Button(frame, text="Çıkış", command=self.root.destroy).grid(row=2, column=0, columnspan=2, pady=10)

    def read_pdf(self):
        self.pdf_manager.read_pdf_files()
        for title in self.pdf_manager.titles:
            print(title)

        messagebox.showinfo("Başarı", "PDF dosyalarından başlıklar başarıyla okundu.")

    def save_pdf(self):
        self.pdf_manager.read_pdf_files()
        self.pdf_manager.save_titles_to_pdf()