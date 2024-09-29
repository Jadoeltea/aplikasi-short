import streamlit as st
import random
import time
import multiprocessing as mp

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)

def parallel_sort(arr, method, num_processes):
    chunk_size = len(arr) // num_processes
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
    
    with mp.Pool(processes=num_processes) as pool:
        sorted_chunks = pool.map(method, chunks)
    
    # Menggabungkan hasil pengurutan
    if method == quick_sort:
        return quick_sort([item for chunk in sorted_chunks for item in chunk])
    else:
        result = []
        for chunk in sorted_chunks:
            result = merge(result, chunk)
        return result

def merge(left, right):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

st.set_page_config(page_title="APLIKASI SORTING", layout="wide")

st.title("APLIKASI SORTING")

with st.expander("Informasi Tambahan", expanded=True):
    st.write("Pilih jumlah data, metode pengurutan, dan jumlah proses paralel di bawah ini.")
    st.write("Setelah menekan tombol 'Proses', Anda akan melihat data sebelum dan sesudah diurutkan.")

with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        jumlah_data = st.number_input("Masukkan jumlah data:", min_value=1, max_value=1000000, value=10000)
    
    with col2:
        metode_sort = st.radio("Pilih metode pengurutan:", ("Bubble Sort", "Selection Sort", "Quick Sort"))
    
    with col3:
        num_processes = st.number_input("Jumlah proses komputasi:", min_value=1, max_value=mp.cpu_count(), value=mp.cpu_count())

if jumlah_data > 10000:
    st.warning("Peringatan: Memproses data dalam jumlah besar dapat memakan waktu lama.")

if metode_sort in ["Bubble Sort", "Selection Sort"] and jumlah_data > 10000:
    st.warning(f"Peringatan: {metode_sort} tidak efisien untuk data yang sangat besar. Pertimbangkan untuk menggunakan Quick Sort.")

status_placeholder = st.empty()
result_placeholder = st.empty()

if st.button("Proses", use_container_width=True):
    data = [random.randint(1, 1000) for _ in range(jumlah_data)]
    
    waktu_awal = time.time()
    
    status_placeholder.text("Memulai proses pengurutan ...")
    
    if metode_sort == "Bubble Sort":
        hasil = parallel_sort(data.copy(), bubble_sort, num_processes)
    elif metode_sort == "Selection Sort":
        hasil = parallel_sort(data.copy(), selection_sort, num_processes)
    else:
        hasil = parallel_sort(data.copy(), quick_sort, num_processes)
    
    waktu_akhir = time.time()
    waktu_proses = waktu_akhir - waktu_awal
    
    status_placeholder.text("Proses pengurutan selesai!")
    
    with result_placeholder.container():
        menit, detik = divmod(waktu_proses, 60)
        if menit > 0:
            st.success(f"Proses pengurutan paralel selesai dalam waktu {int(menit)} menit {detik:.2f} detik")
        else:
            st.success(f"Proses pengurutan paralel selesai dalam waktu {detik:.2f} detik")
        
        col_sebelum, col_sesudah = st.columns(2)
        
        with col_sebelum:
            st.subheader("Data Sebelum Diurutkan (10 pertama)")
            st.write(data[:10])
        
        with col_sesudah:
            st.subheader("Data Setelah Diurutkan (10 pertama)")
            st.write(hasil[:10])

        st.write(f"Metode pengurutan yang digunakan: {metode_sort}")
        st.write(f"Jumlah data yang diurutkan: {jumlah_data}")
        st.write(f"Jumlah proses paralel: {num_processes}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2023 Irfan Z Wastu. All rights reserved.</p>", unsafe_allow_html=True)
