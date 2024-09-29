import streamlit as st
import random
import time
import threading

def bubble_sort(arr, status_placeholder):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        if i % 100 == 0:
            status_placeholder.text(f"Memproses... {i}/{n}")
    return arr

def selection_sort(arr, status_placeholder):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        if i % 100 == 0:
            status_placeholder.text(f"Memproses... {i}/{n}")
    return arr

def quick_sort(arr, status_placeholder):
    def partition(arr, low, high):
        i = low - 1
        pivot = arr[high]
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quick_sort_helper(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_helper(arr, low, pi - 1)
            quick_sort_helper(arr, pi + 1, high)
            status_placeholder.text(f"Memproses... {high}/{len(arr)}")

    quick_sort_helper(arr, 0, len(arr) - 1)
    return arr

st.set_page_config(page_title="APLIKASI SORTING", layout="wide")

st.title("APLIKASI SORTING")

with st.expander("Informasi Tambahan", expanded=True):
    st.write("Pilih jumlah data dan metode pengurutan di bawah ini.")
    st.write("Setelah menekan tombol 'Proses', Anda akan melihat data sebelum dan sesudah diurutkan.")

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        jumlah_data = st.number_input("Masukkan jumlah data:", min_value=1, max_value=1000000, value=10)
    
    with col2:
        metode_sort = st.radio("Pilih metode pengurutan:", ("Bubble Sort", "Selection Sort", "Quick Sort"))

if jumlah_data > 10000:
    st.warning("Peringatan: Memproses data dalam jumlah besar dapat memakan waktu lama dan mungkin membuat aplikasi tidak responsif.")

if metode_sort in ["Bubble Sort", "Selection Sort"] and jumlah_data > 10000:
    st.warning(f"Peringatan: {metode_sort} tidak efisien untuk data yang sangat besar. Pertimbangkan untuk menggunakan Quick Sort.")

status_placeholder = st.empty()
result_placeholder = st.empty()

if st.button("Proses", use_container_width=True):
    data = [random.randint(1, 1000) for _ in range(jumlah_data)]
    
    waktu_awal = time.time()
    
    status_placeholder.text("Memulai proses pengurutan...")
    
    if metode_sort == "Bubble Sort":
        hasil = bubble_sort(data.copy(), status_placeholder)
    elif metode_sort == "Selection Sort":
        hasil = selection_sort(data.copy(), status_placeholder)
    else:
        hasil = quick_sort(data.copy(), status_placeholder)
    
    waktu_akhir = time.time()
    waktu_proses = waktu_akhir - waktu_awal
    
    status_placeholder.text("Proses pengurutan selesai!")
    
    with result_placeholder.container():
        menit, detik = divmod(waktu_proses, 60)
        if menit > 0:
            st.success(f"Proses pengurutan selesai dalam waktu {int(menit)} menit {detik:.2f} detik")
        else:
            st.success(f"Proses pengurutan selesai dalam waktu {detik:.2f} detik")
        
        col_sebelum, col_sesudah = st.columns(2)
        
        with col_sebelum:
            st.subheader("Data Sebelum Diurutkan (10 pertama)")
            st.write(data[:10])
        
        with col_sesudah:
            st.subheader("Data Setelah Diurutkan (10 pertama)")
            st.write(hasil[:10])

        st.write(f"Metode pengurutan yang digunakan: {metode_sort}")
        st.write(f"Jumlah data yang diurutkan: {jumlah_data}")

# Menambahkan copyright di bagian bawah
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2024 Irfan Z Wastu. All rights reserved.</p>", unsafe_allow_html=True)