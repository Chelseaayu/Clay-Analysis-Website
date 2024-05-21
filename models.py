from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class index(db.Model):
    __tablename__ = 'index'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    opyhigh = db.Column(db.Integer)
    opylow = db.Column(db.Integer)
    lokasiprod = db.Column(db.Integer)
    opyhighcrusher = db.Column(db.Numeric)  
    opylowcrusher = db.Column(db.Numeric)   

    def __init__(self, date=None, opyhigh=None, opylow=None, lokasiprod=None, opyhighcrusher=None, opylowcrusher=None):
        self.date = date
        self.opyhigh = opyhigh
        self.opylow = opylow
        self.lokasiprod = lokasiprod
        self.opyhighcrusher = opyhighcrusher
        self.opylowcrusher = opylowcrusher
        
class tuban1(db.Model):
    __tablename__='tuban_1'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)  
    mining_date = db.Column(db.Date)
    permpro_high_al = db.Column(db.Integer)
    permpro_low_al = db.Column(db.Integer)
    stok_storage_hal = db.Column(db.Integer)
    stok_storage_lal = db.Column(db.Integer)
    tambang_hal = db.Column(db.Integer)
    tambang_lal = db.Column(db.Integer)
    hari_habis_hal = db.Column(db.Integer)
    hari_habis_lal = db.Column(db.Integer)
    warning_hal = db.Column(db.String)
    warning_lal = db.Column(db.String)
    target_lanjut_hal = db.Column(db.String)
    target_lanjut_lal = db.Column(db.String)

    def __init__(self, mining_date=None, permpro_high_al=None, permpro_low_al=None, stok_storage_hal=None, stok_storage_lal=None, tambang_hal=None, 
             tambang_lal=None, hari_habis_hal=None, hari_habis_lal=None, warning_hal=None, warning_lal=None, target_lanjut_hal=None, 
             target_lanjut_lal=None):
        self.mining_date = mining_date
        self.permpro_high_al = permpro_high_al
        self.permpro_low_al = permpro_low_al
        self.stok_storage_hal = stok_storage_hal
        self.stok_storage_lal = stok_storage_lal
        self.tambang_hal = tambang_hal
        self.tambang_lal = tambang_lal
        self.hari_habis_hal = hari_habis_hal
        self.hari_habis_lal = hari_habis_lal
        self.warning_hal = warning_hal
        self.warning_lal = warning_lal
        self.target_lanjut_hal = target_lanjut_hal
        self.target_lanjut_lal = target_lanjut_lal


class tuban2(db.Model):
    __tablename__='tuban_2'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)  # Menambahkan autoincrement=True di sini
    mining_date = db.Column(db.Date)
    permpro_high_al = db.Column(db.Integer)
    permpro_low_al = db.Column(db.Integer)
    stok_storage_hal = db.Column(db.Integer)
    stok_storage_lal = db.Column(db.Integer)
    tambang_hal = db.Column(db.Integer)
    tambang_lal = db.Column(db.Integer)
    hari_habis_hal = db.Column(db.Integer)
    hari_habis_lal = db.Column(db.Integer)
    warning_hal = db.Column(db.String)
    warning_lal = db.Column(db.String)
    target_lanjut_hal = db.Column(db.String)
    target_lanjut_lal = db.Column(db.String)

    def __init__(self, mining_date=None, permpro_high_al=None, permpro_low_al=None, stok_storage_hal=None, stok_storage_lal=None, tambang_hal=None, 
             tambang_lal=None, hari_habis_hal=None, hari_habis_lal=None, warning_hal=None, warning_lal=None, target_lanjut_hal=None, 
             target_lanjut_lal=None):
        self.mining_date=mining_date
        self.permpro_high_al=permpro_high_al
        self.permpro_low_al=permpro_low_al
        self.stok_storage_hal=stok_storage_hal
        self.stok_storage_lal=stok_storage_lal
        self.tambang_hal=tambang_hal
        self.tambang_lal=tambang_lal
        self.hari_habis_hal=hari_habis_hal
        self.hari_habis_lal=hari_habis_lal
        self.warning_hal= warning_hal
        self.warning_lal=warning_lal
        self.target_lanjut_hal=target_lanjut_hal
        self.target_lanjut_lal=target_lanjut_lal

class tuban3(db.Model):
    __tablename__='tuban_3'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)  # Menambahkan autoincrement=True di sini
    mining_date = db.Column(db.Date)
    permpro_high_al = db.Column(db.Integer)
    permpro_low_al = db.Column(db.Integer)
    stok_storage_hal = db.Column(db.Integer)
    stok_storage_lal = db.Column(db.Integer)
    tambang_hal = db.Column(db.Integer)
    tambang_lal = db.Column(db.Integer)
    hari_habis_hal = db.Column(db.Integer)
    hari_habis_lal = db.Column(db.Integer)
    warning_hal = db.Column(db.String)
    warning_lal = db.Column(db.String)
    target_lanjut_hal = db.Column(db.String)
    target_lanjut_lal = db.Column(db.String)

    def __init__(self, mining_date=None, permpro_high_al=None, permpro_low_al=None, stok_storage_hal=None, stok_storage_lal=None, tambang_hal=None, 
             tambang_lal=None, hari_habis_hal=None, hari_habis_lal=None, warning_hal=None, warning_lal=None, target_lanjut_hal=None, 
             target_lanjut_lal=None):
        self.mining_date=mining_date
        self.permpro_high_al=permpro_high_al
        self.permpro_low_al=permpro_low_al
        self.stok_storage_hal=stok_storage_hal
        self.stok_storage_lal=stok_storage_lal
        self.tambang_hal=tambang_hal
        self.tambang_lal=tambang_lal
        self.hari_habis_hal=hari_habis_hal
        self.hari_habis_lal=hari_habis_lal
        self.warning_hal= warning_hal
        self.warning_lal=warning_lal
        self.target_lanjut_hal=target_lanjut_hal
        self.target_lanjut_lal=target_lanjut_lal

class tuban4(db.Model):
    __tablename__='tuban_4'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)  # Menambahkan autoincrement=True di sini
    mining_date = db.Column(db.Date)
    permpro_high_al = db.Column(db.Integer)
    permpro_low_al = db.Column(db.Integer)
    stok_storage_hal = db.Column(db.Integer)
    stok_storage_lal = db.Column(db.Integer)
    tambang_hal = db.Column(db.Integer)
    tambang_lal = db.Column(db.Integer)
    hari_habis_hal = db.Column(db.Integer)
    hari_habis_lal = db.Column(db.Integer)
    warning_hal = db.Column(db.String)
    warning_lal = db.Column(db.String)
    target_lanjut_hal = db.Column(db.String)
    target_lanjut_lal = db.Column(db.String)

    def __init__(self, mining_date=None, permpro_high_al=None, permpro_low_al=None, stok_storage_hal=None, stok_storage_lal=None, tambang_hal=None, 
             tambang_lal=None, hari_habis_hal=None, hari_habis_lal=None, warning_hal=None, warning_lal=None, target_lanjut_hal=None, 
             target_lanjut_lal=None):
        self.mining_date=mining_date
        self.permpro_high_al=permpro_high_al
        self.permpro_low_al=permpro_low_al
        self.stok_storage_hal=stok_storage_hal
        self.stok_storage_lal=stok_storage_lal
        self.tambang_hal=tambang_hal
        self.tambang_lal=tambang_lal
        self.hari_habis_hal=hari_habis_hal
        self.hari_habis_lal=hari_habis_lal
        self.warning_hal= warning_hal
        self.warning_lal=warning_lal
        self.target_lanjut_hal=target_lanjut_hal
        self.target_lanjut_lal=target_lanjut_lal