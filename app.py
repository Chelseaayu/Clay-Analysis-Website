from flask import Flask, render_template, request, redirect, url_for, session
from models import index, tuban1, tuban2, tuban3, tuban4, db
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bismillahlancar@localhost/tanah_liat'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db.init_app(app)

@app.route('/')
def success():
    return render_template('homepage.html')

@app.route('/index2', methods=['GET', 'POST'])
def index2():
    return render_template('lokasicrusher.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('openyard.html')

@app.route('/tuban1', methods=['GET', 'POST'])
def submit_tuban1():
    if request.method == 'POST':
        mining_date = request.form['miningDate']
        shift = float(request.form['shift'])
        clay_type = request.form['clayType']
        permpro_high_al = float(request.form['permproHighAl'])
        permpro_low_al = float(request.form['permproLowAl'])
        stok_storage_hal = float(request.form['stokStorageHal'])
        stok_storage_lal = float(request.form['stokStorageLal'])
        tambang_hal = float(request.form['tambangHal'])
        tambang_lal = float(request.form['tambangLal'])
        hari_habis_hal = int(request.form.get('hariHabisHal', 0) or 0)
        hari_habis_lal = int(request.form.get('hariHabisLal', 0) or 0)
        warning_hal = request.form.get('warningHal', '')
        warning_lal = request.form.get('warningLal', '')
        target_lanjut_hal = request.form.get('targetLanjutHal', '')
        target_lanjut_lal = request.form.get('targetLanjutLal', '')

        # Ambil nilai opyhighcrusher, opylowcrusher, dan target dengan tanggal dan shift yang sama dengan mining_date
        data = index.query.filter_by(date=mining_date, shift=shift).first()

        opyhighcrusher = float(data.opyhighcrusher)
        opylowcrusher = float(data.opylowcrusher)
        target = float(data.target)

        # Pembagian target
        if clay_type == 'both':
            target /= 2
        else:
            target = float(target)

        # Hitung stok tanah liat high dan low
        stok_tl_high = float(stok_storage_hal) + float(opyhighcrusher)
        stok_tl_low = float(stok_storage_lal) + float(opylowcrusher)

        # Hitung pengurangan produksi high dan low
        pengurangan_produksiT1_high = float(stok_tl_high) + tambang_hal - permpro_high_al
        pengurangan_produksiT1_low = float(stok_tl_low) + tambang_lal - permpro_low_al

        # Hitung selisih produksi dan target high dan low
        def selisih_produksiT1(target, tambang_hal, tambang_lal, permpro_high_al, permpro_low_al):
            if permpro_high_al ==0:
                selisih_prod_dan_targetT1_high = target
            else:
                selisih_prod_dan_targetT1_high = target - abs(tambang_hal - permpro_high_al)
            
            if permpro_low_al == 0:
                selisih_prod_dan_targetT1_low = target
            else:
                selisih_prod_dan_targetT1_low = target - abs(tambang_lal - permpro_low_al)

            return selisih_prod_dan_targetT1_high, selisih_prod_dan_targetT1_low

        selisih_highT1, selisih_lowT1 = selisih_produksiT1(target, tambang_hal, tambang_lal, permpro_high_al, permpro_low_al)

        # Hitung perkiraan habis terpisah
        def hitung_perkiraan_habis_terpisahT1(pengurangan_produksiT1_high, pengurangan_produksiT1_low, permpro_high_al, permpro_low_al):
            hari_habis_high_aluminaT1 = 0
            hari_habis_low_aluminaT1 = 0

            # Periksa apakah ada kekurangan produksi untuk high alumina
            if pengurangan_produksiT1_high > 0 and permpro_high_al != 0:

                if pengurangan_produksiT1_high > 0:
                    if pengurangan_produksiT1_high < permpro_high_al:
                        hari_habis_high_aluminaT1 += 1 
                        hari_habis_high_aluminaT1 -= 1
                    else:
                        while pengurangan_produksiT1_high >= permpro_high_al:
                            pengurangan_produksiT1_high -= permpro_high_al
                            pengurangan_produksiT1_high = max(0, pengurangan_produksiT1_high)
                            hari_habis_high_aluminaT1 += 1

            # Periksa apakah ada kekurangan produksi untuk low alumina
            if pengurangan_produksiT1_low > 0 and permpro_low_al != 0:

                if pengurangan_produksiT1_low > 0:
                    if pengurangan_produksiT1_low < permpro_low_al:
                        hari_habis_low_aluminaT1 += 1 
                        hari_habis_low_aluminaT1 -= 1
                    else:
                        while pengurangan_produksiT1_low >= permpro_low_al:
                            pengurangan_produksiT1_low -= permpro_low_al
                            pengurangan_produksiT1_low = max(0, pengurangan_produksiT1_low)
                            hari_habis_low_aluminaT1 += 1

            return hari_habis_high_aluminaT1, hari_habis_low_aluminaT1

        # Hitung perkiraan habis terpisah untuk high dan low alumina
        perkiraan_habis_high_aluminaT1, perkiraan_habis_low_aluminaT1 = hitung_perkiraan_habis_terpisahT1(pengurangan_produksiT1_high, pengurangan_produksiT1_low, permpro_high_al, permpro_low_al)

        # simpan dalam kolom baru bernama hari_habis
        hari_habis_hal = perkiraan_habis_high_aluminaT1 if perkiraan_habis_high_aluminaT1 <= 45 else 0
        hari_habis_lal = perkiraan_habis_low_aluminaT1 if perkiraan_habis_low_aluminaT1 <= 45 else 0

        # Simpan dalam kolom baru bernama peringatan
        if perkiraan_habis_high_aluminaT1 <= 14 and perkiraan_habis_high_aluminaT1 > 0:
            warning_hal = f' WARNING ! High Alumina Tuban 1 akan habis dalam {perkiraan_habis_high_aluminaT1} produksi ke depan'
        elif perkiraan_habis_high_aluminaT1 == 0 and permpro_high_al == 0:
            warning_hal = 'Tidak ada produksi'
        else:
            warning_hal = ''
        
        if perkiraan_habis_low_aluminaT1 <= 14 and perkiraan_habis_low_aluminaT1 > 0:
            warning_lal = f' WARNING ! Low Alumina Tuban 1 akan habis dalam {perkiraan_habis_low_aluminaT1} produksi ke depan'
        elif perkiraan_habis_low_aluminaT1 == 0 and permpro_low_al == 0:
            warning_lal = 'Tidak ada produksi'
        else:
            warning_lal = ''

        # simpan dalam kolom baru bernama target_lanjutnya
        target_lanjut_hal = f'Jumlah tonase minimal Tuban 1 shift berikutnya adalah {abs(selisih_highT1)} ton high alumina' 
        target_lanjut_lal = f'Jumlah tonase minimal Tuban 1 shift berikutnya adalah {abs(selisih_lowT1)} ton low alumina' 

        # simpan dalam database
        tuban_1 = tuban1(
            mining_date=mining_date,
            shift=shift,
            permpro_high_al=permpro_high_al,
            permpro_low_al=permpro_low_al,
            stok_storage_hal=stok_storage_hal,
            stok_storage_lal=stok_storage_lal,
            tambang_hal=tambang_hal,
            tambang_lal=tambang_lal,
            hari_habis_hal=hari_habis_hal,
            hari_habis_lal=hari_habis_lal,
            warning_hal=warning_hal,
            warning_lal=warning_lal,
            target_lanjut_hal=target_lanjut_hal,
            target_lanjut_lal=target_lanjut_lal
        )
        
        db.session.add(tuban_1)
        db.session.commit()
        return redirect(url_for('success'))
    else:
        return render_template('tuban1.html')

@app.route('/tuban2', methods=['GET', 'POST'])
def submit_tuban2():
    if request.method == 'POST':
        mining_date = request.form['miningDate']  
        shift = float(request.form['shift'])
        clay_type = request.form['clayType']
        permpro_high_al = float(request.form['permproHighAl'])  
        permpro_low_al = float(request.form['permproLowAl'])  
        stok_storage_hal = float(request.form['stokStorageHal'])  
        stok_storage_lal = float(request.form['stokStorageLal'])  
        tambang_hal = float(request.form['tambangHal'])  
        tambang_lal = float(request.form['tambangLal'])
        hari_habis_hal = int(request.form.get('hariHabisHal', 0) or 0)  
        hari_habis_lal = int(request.form.get('hariHabisLal', 0) or 0)  
        warning_hal = request.form.get('warningHal', '')  
        warning_lal = request.form.get('warningLal', '')  
        target_lanjut_hal = request.form.get('targetLanjutHal', '')  
        target_lanjut_lal = request.form.get('targetLanjutLal', '')

        # Ambil nilai opyhighcrusher, opylowcrusher, dan target dengan tanggal dan shift yang sama dengan mining_date
        data = index.query.filter_by(date=mining_date, shift=shift).first()

        opyhighcrusher = float(data.opyhighcrusher)
        opylowcrusher = float(data.opylowcrusher)
        target = float(data.target)

        # Pembagian target
        if clay_type == 'both':
            target /= 2
        else:
            target = float(target)

        # Hitung stok tanah liat high dan low
        stok_tl_high = float(stok_storage_hal) + float(opyhighcrusher)
        stok_tl_low = float(stok_storage_lal) + float(opylowcrusher)

        # Hitung pengurangan produksi high dan low
        pengurangan_produksiT2_high = float(stok_tl_high) + tambang_hal - permpro_high_al
        pengurangan_produksiT2_low = float(stok_tl_low) + tambang_lal - permpro_low_al

        # Hitung selisih produksi dan target high dan low
        def selisih_produksiT2(target, tambang_hal, tambang_lal, permpro_high_al, permpro_low_al):
            if permpro_high_al ==0:
                selisih_prod_dan_targetT2_high = target
            else:
                selisih_prod_dan_targetT2_high = target - abs(tambang_hal - permpro_high_al)
            
            if permpro_low_al == 0:
                selisih_prod_dan_targetT2_low = target
            else:
                selisih_prod_dan_targetT2_low = target - abs(tambang_lal - permpro_low_al)

            return selisih_prod_dan_targetT2_high, selisih_prod_dan_targetT2_low

        selisih_highT2, selisih_lowT2 = selisih_produksiT2(target, tambang_hal, tambang_lal, permpro_high_al, permpro_low_al)

        # Hitung perkiraan habis terpisah
        def hitung_perkiraan_habis_terpisahT2(pengurangan_produksiT2_high, pengurangan_produksiT2_low, permpro_high_al, permpro_low_al):
            hari_habis_high_aluminaT2= 0
            hari_habis_low_aluminaT2 = 0

            # Periksa apakah ada kekurangan produksi untuk high alumina
            if pengurangan_produksiT2_high > 0 and permpro_high_al != 0:

                if pengurangan_produksiT2_high > 0:
                    if pengurangan_produksiT2_high < permpro_high_al:
                        hari_habis_high_aluminaT2 += 1 
                        hari_habis_high_aluminaT2 -= 1
                    else:
                        while pengurangan_produksiT2_high >= permpro_high_al:
                            pengurangan_produksiT2_high -= permpro_high_al
                            pengurangan_produksiT2_high = max(0, pengurangan_produksiT2_high)
                            hari_habis_high_aluminaT2 += 1

            # Periksa apakah ada kekurangan produksi untuk low alumina
            if pengurangan_produksiT2_low > 0 and permpro_low_al != 0:

                if pengurangan_produksiT2_low > 0:
                    if pengurangan_produksiT2_low < permpro_low_al:
                        hari_habis_low_aluminaT2 += 1 
                        hari_habis_low_aluminaT2 -= 1
                    else:
                        while pengurangan_produksiT2_low >= permpro_low_al:
                            pengurangan_produksiT2_low -= permpro_low_al
                            pengurangan_produksiT2_low = max(0, pengurangan_produksiT2_low)
                            hari_habis_low_aluminaT2 += 1

            return hari_habis_high_aluminaT2, hari_habis_low_aluminaT2

        # Hitung perkiraan habis terpisah untuk high dan low alumina
        perkiraan_habis_high_aluminaT2, perkiraan_habis_low_aluminaT2 = hitung_perkiraan_habis_terpisahT2(pengurangan_produksiT2_high, pengurangan_produksiT2_low, permpro_high_al, permpro_low_al)

        # simpan dalam kolom baru bernama hari_habis
        hari_habis_hal = perkiraan_habis_high_aluminaT2 if perkiraan_habis_high_aluminaT2 <= 45 else 0
        hari_habis_lal = perkiraan_habis_low_aluminaT2 if perkiraan_habis_low_aluminaT2 <= 45 else 0

        # Simpan dalam kolom baru bernama peringatan
        if perkiraan_habis_high_aluminaT2 <= 14 and perkiraan_habis_high_aluminaT2 > 0:
            warning_hal = f' WARNING ! High Alumina Tuban 2 akan habis dalam {perkiraan_habis_high_aluminaT2} produksi ke depan'
        elif perkiraan_habis_high_aluminaT2 == 0 and permpro_high_al == 0:
            warning_hal = 'Tidak ada produksi'
        else:
            warning_hal = ''
        
        if perkiraan_habis_low_aluminaT2 <= 14 and perkiraan_habis_low_aluminaT2 > 0:
            warning_lal = f' WARNING ! Low Alumina Tuban 2 akan habis dalam {perkiraan_habis_low_aluminaT2} produksi ke depan'
        elif perkiraan_habis_low_aluminaT2 == 0 and permpro_low_al == 0:
            warning_lal = 'Tidak ada produksi'
        else:
            warning_lal = ''

        # simpan dalam kolom baru bernama target_lanjutnya
        target_lanjut_hal = f'Jumlah tonase minimal Tuban 2 shift berikutnya adalah {abs(selisih_highT2)} ton high alumina' 
        target_lanjut_lal = f'Jumlah tonase minimal Tuban 2 shift berikutnya adalah {abs(selisih_lowT2)} ton low alumina'

        # simpan dalam database
        tuban_2 = tuban2(
            mining_date=mining_date,
            shift=shift,
            permpro_high_al=permpro_high_al,
            permpro_low_al=permpro_low_al,
            stok_storage_hal=stok_storage_hal,
            stok_storage_lal=stok_storage_lal,
            tambang_hal=tambang_hal,
            tambang_lal=tambang_lal,
            hari_habis_hal=hari_habis_hal,
            hari_habis_lal=hari_habis_lal,
            warning_hal=warning_hal,
            warning_lal=warning_lal,
            target_lanjut_hal=target_lanjut_hal,
            target_lanjut_lal=target_lanjut_lal
        )
        
        db.session.add(tuban_2)
        db.session.commit()
        return redirect(url_for('success'))
    else:
        return render_template('tuban2.html')

@app.route('/tuban3', methods=['GET', 'POST'])
def submit_tuban3():
    if request.method == 'POST':
        mining_date = request.form['miningDate']  
        shift = float(request.form['shift'])
        clay_type = request.form['clayType']
        permpro_high_al = float(request.form['permproHighAl'])  
        permpro_low_al = float(request.form['permproLowAl'])  
        stok_storage_hal = float(request.form['stokStorageHal'])  
        stok_storage_lal = float(request.form['stokStorageLal'])  
        tambang_hal = float(request.form['tambangHal'])  
        tambang_lal = float(request.form['tambangLal'])
        hari_habis_hal = int(request.form.get('hariHabisHal', '') or 0)
        hari_habis_lal = int(request.form.get('hariHabisLal', '')  or 0) 
        warning_hal = request.form.get('warningHal', '')  
        warning_lal = request.form.get('warningLal', '')  
        target_lanjut_hal = request.form.get('targetLanjutHal', '')  
        target_lanjut_lal = request.form.get('targetLanjutLal', '')

        # Ambil nilai opyhighcrusher, opylowcrusher, dan target dengan tanggal dan shift yang sama dengan mining_date
        data = index.query.filter_by(date=mining_date, shift=shift).first()

        opyhighcrusher = float(data.opyhighcrusher)
        opylowcrusher = float(data.opylowcrusher)
        target = float(data.target)

        # Pembagian target
        if clay_type == 'both':
            target /= 2
        else:
            target = float(target)

        # Hitung stok tanah liat high dan low
        stok_tl_high = float(stok_storage_hal) + float(opyhighcrusher)
        stok_tl_low = float(stok_storage_lal) + float(opylowcrusher)

        # Hitung pengurangan produksi high dan low
        pengurangan_produksiT3_high = float(stok_tl_high) + tambang_hal - permpro_high_al
        pengurangan_produksiT3_low = float(stok_tl_low) + tambang_lal - permpro_low_al

        # Hitung selisih produksi dan target high dan low
        def selisih_produksiT3(target, tambang_hal, tambang_lal, permpro_high_al, permpro_low_al):
            if permpro_high_al ==0:
                selisih_prod_dan_targetT3_high = target
            else:
                selisih_prod_dan_targetT3_high = target - abs(tambang_hal - permpro_high_al)
            
            if permpro_low_al == 0:
                selisih_prod_dan_targetT3_low = target
            else:
                selisih_prod_dan_targetT3_low = target - abs(tambang_lal - permpro_low_al)

            return selisih_prod_dan_targetT3_high, selisih_prod_dan_targetT3_low

        selisih_highT3, selisih_lowT3 = selisih_produksiT3(target, tambang_hal, tambang_lal, permpro_high_al, permpro_low_al)

        # Hitung perkiraan habis terpisah
        def hitung_perkiraan_habis_terpisahT3(pengurangan_produksiT3_high, pengurangan_produksiT3_low, permpro_high_al, permpro_low_al):
            hari_habis_high_aluminaT3= 0
            hari_habis_low_aluminaT3 = 0

            # Periksa apakah ada kekurangan produksi untuk high alumina
            if pengurangan_produksiT3_high > 0 and permpro_high_al != 0:

                if pengurangan_produksiT3_high > 0:
                    if pengurangan_produksiT3_high < permpro_high_al:
                        hari_habis_high_aluminaT3 += 1 
                        hari_habis_high_aluminaT3 -= 1
                    else:
                        while pengurangan_produksiT3_high >= permpro_high_al:
                            pengurangan_produksiT3_high -= permpro_high_al
                            pengurangan_produksiT3_high = max(0, pengurangan_produksiT3_high)
                            hari_habis_high_aluminaT3 += 1

            # Periksa apakah ada kekurangan produksi untuk low alumina
            if pengurangan_produksiT3_low > 0 and permpro_low_al != 0:

                if pengurangan_produksiT3_low > 0:
                    if pengurangan_produksiT3_low < permpro_low_al:
                        hari_habis_low_aluminaT3 += 1 
                        hari_habis_low_aluminaT3 -= 1
                    else:
                        while pengurangan_produksiT3_low >= permpro_low_al:
                            pengurangan_produksiT3_low -= permpro_low_al
                            pengurangan_produksiT3_low = max(0, pengurangan_produksiT3_low)
                            hari_habis_low_aluminaT3 += 1

            return hari_habis_high_aluminaT3, hari_habis_low_aluminaT3

        # Hitung perkiraan habis terpisah untuk high dan low alumina
        perkiraan_habis_high_aluminaT3, perkiraan_habis_low_aluminaT3 = hitung_perkiraan_habis_terpisahT3(pengurangan_produksiT3_high, pengurangan_produksiT3_low, permpro_high_al, permpro_low_al)

        # simpan dalam kolom baru bernama hari_habis
        hari_habis_hal = perkiraan_habis_high_aluminaT3 if perkiraan_habis_high_aluminaT3 <= 45 else 0
        hari_habis_lal = perkiraan_habis_low_aluminaT3 if perkiraan_habis_low_aluminaT3 <= 45 else 0

        # Simpan dalam kolom baru bernama peringatan
        if perkiraan_habis_high_aluminaT3 <= 14 and perkiraan_habis_high_aluminaT3 > 0:
            warning_hal = f' WARNING ! High Alumina Tuban 3 akan habis dalam {perkiraan_habis_high_aluminaT3} produksi ke depan'
        elif perkiraan_habis_high_aluminaT3 == 0 and permpro_high_al == 0:
            warning_hal = 'Tidak ada produksi'
        else:
            warning_hal = ''
        
        if perkiraan_habis_low_aluminaT3 <= 14 and perkiraan_habis_low_aluminaT3 > 0:
            warning_lal = f' WARNING ! Low Alumina Tuban 3 akan habis dalam {perkiraan_habis_low_aluminaT3} produksi ke depan'
        elif perkiraan_habis_low_aluminaT3 == 0 and permpro_low_al == 0:
            warning_lal = 'Tidak ada produksi'
        else:
            warning_lal = ''

        # simpan dalam kolom baru bernama target_lanjutnya
        target_lanjut_hal = f'Jumlah tonase minimal Tuban 3 shift berikutnya adalah {abs(selisih_highT3)} ton high alumina' 
        target_lanjut_lal = f'Jumlah tonase minimal Tuban 3 shift berikutnya adalah {abs(selisih_lowT3)} ton low alumina' 

        # simpan dalam database
        tuban_3 = tuban3(
            mining_date=mining_date,
            shift=shift,
            permpro_high_al=permpro_high_al,
            permpro_low_al=permpro_low_al,
            stok_storage_hal=stok_storage_hal,
            stok_storage_lal=stok_storage_lal,
            tambang_hal=tambang_hal,
            tambang_lal=tambang_lal,
            hari_habis_hal=hari_habis_hal,
            hari_habis_lal=hari_habis_lal,
            warning_hal=warning_hal,
            warning_lal=warning_lal,
            target_lanjut_hal=target_lanjut_hal,
            target_lanjut_lal=target_lanjut_lal
        )
        
        db.session.add(tuban_3)
        db.session.commit()
        return redirect(url_for('success'))
    else:
        return render_template('tuban3.html')

@app.route('/tuban4', methods=['GET', 'POST'])
def submit_tuban4():
    if request.method == 'POST':
        mining_date = request.form['miningDate']
        shift = float(request.form['shift'])
        clay_type = request.form['clayType']
        permpro_high_al = float(request.form['permproHighAl'])
        permpro_low_al = float(request.form['permproLowAl'])
        stok_storage_hal = float(request.form['stokStorageHal'])
        stok_storage_lal = float(request.form['stokStorageLal'])
        tambang_hal = float(request.form['tambangHal'])
        tambang_lal = float(request.form['tambangLal'])
        hari_habis_hal = int(request.form.get('hariHabisHal', 0) or 0)
        hari_habis_lal = int(request.form.get('hariHabisLal', 0) or 0)
        warning_hal = request.form.get('warningHal', '')
        warning_lal = request.form.get('warningLal', '')
        target_lanjut_hal = request.form.get('targetLanjutHal', '')
        target_lanjut_lal = request.form.get('targetLanjutLal', '')

        # Ambil nilai opyhighcrusher, opylowcrusher, dan target dengan tanggal dan shift yang sama dengan mining_date
        data = index.query.filter_by(date=mining_date, shift=shift).first()

        opyhighcrusher = float(data.opyhighcrusher)
        opylowcrusher = float(data.opylowcrusher)
        target = float(data.target)

        # Pembagian target
        if clay_type == 'both':
            target /= 2
        else:
            target = float(target)

        # Hitung stok tanah liat high dan low
        stok_tl_high = stok_storage_hal + opyhighcrusher
        stok_tl_low = stok_storage_lal + opylowcrusher

        # Hitung pengurangan produksi high dan low
        pengurangan_produksiT4_high = stok_tl_high + tambang_hal - permpro_high_al
        pengurangan_produksiT4_low = stok_tl_low + tambang_lal - permpro_low_al

        # Hitung selisih produksi dan target high dan low
        def selisih_produksiT4(target, tambang_hal, tambang_lal, permpro_high_al, permpro_low_al):
            if permpro_high_al ==0:
                selisih_prod_dan_targetT4_high = target
            else:
                selisih_prod_dan_targetT4_high = target - abs(tambang_hal - permpro_high_al)
            
            if permpro_low_al == 0:
                selisih_prod_dan_targetT4_low = target
            else:
                selisih_prod_dan_targetT4_low = target - abs(tambang_lal - permpro_low_al)

            return selisih_prod_dan_targetT4_high, selisih_prod_dan_targetT4_low

        selisih_highT4, selisih_lowT4 = selisih_produksiT4(target, tambang_hal, tambang_lal, permpro_high_al, permpro_low_al)
        # Hitung perkiraan habis terpisah
        def hitung_perkiraan_habis_terpisahT4(pengurangan_produksiT4_high, pengurangan_produksiT4_low, permpro_high_al, permpro_low_al):
            hari_habis_high_aluminaT4= 0
            hari_habis_low_aluminaT4 = 0

            # Periksa apakah ada kekurangan produksi untuk high alumina
            if pengurangan_produksiT4_high > 0 and permpro_high_al != 0:

                if pengurangan_produksiT4_high > 0:
                    if pengurangan_produksiT4_high < permpro_high_al:
                        hari_habis_high_aluminaT4 += 1 
                        hari_habis_high_aluminaT4 -= 1
                    else:
                        while pengurangan_produksiT4_high >= permpro_high_al:
                            pengurangan_produksiT4_high -= permpro_high_al
                            pengurangan_produksiT4_high = max(0, pengurangan_produksiT4_high)
                            hari_habis_high_aluminaT4 += 1

            # Periksa apakah ada kekurangan produksi untuk low alumina
            if pengurangan_produksiT4_low > 0 and permpro_low_al != 0:

                if pengurangan_produksiT4_low > 0:
                    if pengurangan_produksiT4_low < permpro_low_al:
                        hari_habis_low_aluminaT4 += 1 
                        hari_habis_low_aluminaT4 -= 1
                    else:
                        while pengurangan_produksiT4_low >= permpro_low_al:
                            pengurangan_produksiT4_low -= permpro_low_al
                            pengurangan_produksiT4_low = max(0, pengurangan_produksiT4_low)
                            hari_habis_low_aluminaT4 += 1

            return hari_habis_high_aluminaT4, hari_habis_low_aluminaT4

        # Hitung perkiraan habis terpisah untuk high dan low alumina
        perkiraan_habis_high_aluminaT4, perkiraan_habis_low_aluminaT4 = hitung_perkiraan_habis_terpisahT4(pengurangan_produksiT4_high, pengurangan_produksiT4_low, permpro_high_al, permpro_low_al)

        # Simpan dalam kolom baru bernama hari_habis
        hari_habis_hal = perkiraan_habis_high_aluminaT4 if perkiraan_habis_high_aluminaT4 <= 45 else 0
        hari_habis_lal = perkiraan_habis_low_aluminaT4 if perkiraan_habis_low_aluminaT4 <= 45 else 0

        # Simpan dalam kolom baru bernama peringatan
        if perkiraan_habis_high_aluminaT4 <= 14 and perkiraan_habis_high_aluminaT4 > 0:
            warning_hal = f' WARNING ! High Alumina Tuban 4 akan habis dalam {perkiraan_habis_high_aluminaT4} produksi ke depan'
        elif perkiraan_habis_high_aluminaT4 == 0 and permpro_high_al == 0:
            warning_hal = 'Tidak ada produksi'
        else:
            warning_hal = ''
        
        if perkiraan_habis_low_aluminaT4 <= 14 and perkiraan_habis_low_aluminaT4 > 0:
            warning_lal = f' WARNING ! Low Alumina Tuban 4 akan habis dalam {perkiraan_habis_low_aluminaT4} produksi ke depan'
        elif perkiraan_habis_low_aluminaT4 == 0 and permpro_low_al == 0:
            warning_lal = 'Tidak ada produksi'
        else:
            warning_lal = ''

        # Simpan dalam kolom baru bernama target_lanjutnya
        target_lanjut_hal = f'Jumlah tonase minimal Tuban 4 shift berikutnya adalah {abs(selisih_highT4)} ton high alumina' 
        target_lanjut_lal = f'Jumlah tonase minimal Tuban 4 shift berikutnya adalah {abs(selisih_lowT4)} ton low alumina' 

        # Simpan dalam database
        tuban_4 = tuban4(
            mining_date=mining_date,
            shift=shift,
            permpro_high_al=permpro_high_al,
            permpro_low_al=permpro_low_al,
            stok_storage_hal=stok_storage_hal,
            stok_storage_lal=stok_storage_lal,
            tambang_hal=tambang_hal,
            tambang_lal=tambang_lal,
            hari_habis_hal=hari_habis_hal,
            hari_habis_lal=hari_habis_lal,
            warning_hal=warning_hal,
            warning_lal=warning_lal,
            target_lanjut_hal=target_lanjut_hal,
            target_lanjut_lal=target_lanjut_lal
        )
        
        db.session.add(tuban_4)
        db.session.commit()
        
        return redirect(url_for('success'))
    else:
        return render_template('tuban4.html')

@app.route('/visualisasi', methods = ['GET', 'POST'])
def visualisasi():
    return render_template('visualisasi.html')

@app.route('/submit_index', methods=['GET', 'POST'])
def submit_index():
    if request.method == 'POST':
        date = request.form['homeDate']
        shift = float(request.form['shift'])
        target = float(request.form['target'])
        opyhigh = float(request.form['opyhigh'])
        opylow = float(request.form['opylow'])
        lokasiprod = float(request.form['lokasiprod'])
    
        opyhighcrusher = opyhigh / lokasiprod
        opylowcrusher = opylow / lokasiprod

        session['opyhighcrusher'] = opyhighcrusher
        session['opylowcrusher'] = opylowcrusher
        session['target'] = target

        openyard = index(date=date, shift=shift, target=target, opyhigh=opyhigh, opylow=opylow, lokasiprod=lokasiprod, opyhighcrusher=opyhighcrusher, opylowcrusher=opylowcrusher)
        db.session.add(openyard)
        db.session.commit()
        return redirect(url_for('success'))
    else:
        return render_template('openyard.html')

if __name__ == '__main__':
    app.run(debug=True)