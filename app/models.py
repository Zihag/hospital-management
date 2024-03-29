from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from app import db, app
from datetime import datetime
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    PATIENT = 1
    ADMIN = 2
    NURSE = 3
    DOCTOR = 4
    CASHIER = 5

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.PATIENT)

    def __str__(self):
        return self.name


class GenderEnum(Enum):
    MALE = 'Male'
    FEMALE = 'Female'


class Patient(db.Model):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    gender = Column(String(10), nullable=True)
    date_appointment = Column(DateTime, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    address = Column(String(100), nullable=True)
    disease_history = Column(String(100), nullable=True)
    tel = Column(String(20), nullable=True)
    medicalreports = relationship('MedicalReport', backref='patient')
    # date_id = Column(Integer, ForeignKey('dateappointment.id'))
    # date_appointment = relationship('DateAppointment', back_populates='patients')

    def __str__(self):
        return self.name


# class DateAppointment(db.Model):
#     __tablename__ = 'dateappointment'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     date = Column(DateTime, nullable=True)
#     patients = relationship('Patient', back_populates='date_appointment')



class Medicine(BaseModel):
    __tablename__ = 'medicine'

    medicine_name = Column(String(50), nullable=False, unique=True)
    how_to_use = Column(String(255), nullable=False)
    price = Column(Integer, default=0)
    unit_name = Column(String(50), nullable=False)

    def __str__(self):
        return self.medicine_name


class MedicalReport(BaseModel):
    __tablename__ = 'medicalreport'

    date_examination = Column(DateTime, default=datetime.now())
    symptom = Column(String(255), nullable=True)
    disease_name = Column(String(50), nullable=True)
    price = Column(Float, default=100000)
    total_amount = Column(Float, nullable=True)
    receipt = relationship('Receipt', backref='medicalreport', lazy=True)
    prescription = relationship('Prescription',backref='medicalreport', lazy=True)
    patient_id = Column(Integer, ForeignKey('patient.id'))


class Prescription(db.Model):
    __tablename__ = 'prescription'

    # id = Column(Integer, primary_key=True, autoincrement=True)

    medical_report_id = Column(Integer, ForeignKey(MedicalReport.id), primary_key=True)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), primary_key=True)
    count = Column(Integer, nullable=False)

    medicine = relationship('Medicine', backref='prescriptions')

    created_date = Column(DateTime, default=datetime.now())



class Receipt(BaseModel):
    __tablename__ = 'receipt'

    user_id = Column(Integer, ForeignKey(User.id), nullable=True)
    medical_report_id = Column(Integer, ForeignKey(MedicalReport.id))
    price = Column(Integer, default=0, nullable=True)
    # paid = Column(Boolean, default=False)


class Rule(db.Model):
    __tablename__ = 'rule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_name = Column(String(20), nullable=True)
    value = Column(Integer, nullable=True)

    def __str__(self):
        return self.rule_name

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib
        #
        # u = User(name='Admin', username='admin',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.ADMIN)
        # p = User(name='Patient1', username='patient1',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.PATIENT)
        # n = User(name='Nurse1', username='nurse1',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.NURSE)
        # d = User(name='doctor1', username='doctor1',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.DOCTOR)
        # c = User(name='cashier1', username='cashier1',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.CASHIER)
        #
        #
        # db.session.add_all([u, p, n, d, c])
        # db.session.commit()
# ------THUỐC------
        # a1 = Medicine(medicine_name='Paramol', how_to_use='Trị các bệnh về đau đầu và hạ sốt',
        #          price=('20000'), unit_name='vĩ')
        # a2 = Medicine(medicine_name='Paracetamol 500mg', how_to_use='Thuốc giảm đau hạ sốt hiệu quả',
        #              price=('200000'), unit_name='vĩ')
        # a3 = Medicine(medicine_name='ZS Chondroitin', how_to_use='Thuốc bổ xương khớp cho người già',
        #              price=('60000'), unit_name='chai')
        # a4 = Medicine(medicine_name='Glucosamine Orihiro 1500 mg', how_to_use='Tăng cường sức khỏe xương khớp, cải thiện chức năng vận động',
        #              price=('100000'), unit_name='viên')
        # a5 = Medicine(medicine_name='Jpanwell Glucosamine', how_to_use='Viên bổ xương khớp cho người già',
        #              price=('20000'), unit_name='viên')
        #
        # a6 = Medicine(medicine_name='Jpanwell Glucosamine 3g', how_to_use='Viên bổ xương khớp cho người già',
        #               price=('20000'), unit_name='viên',created_date=('2024-01-10'))
        # a7 = Medicine(medicine_name='Jpanwell Glucosamine 1g', how_to_use='Viên bổ xương khớp cho người già',
        #               price=('20000'), unit_name='viên',created_date=('2024-01-10'))
        # a8 = Medicine(medicine_name='Jpanwell Glucosamine 2g', how_to_use='Viên bổ xương khớp cho người già',
        #               price=('20000'), unit_name='viên',created_date=('2024-01-11'))
        # a9 = Medicine(medicine_name='Jpanwell Glucosamine 4g', how_to_use='Viên bổ xương khớp cho người già',
        #               price=('20000'), unit_name='viên',created_date=('2024-01-11'))
        # a10 = Medicine(medicine_name='Jpanwell Glucosamine 5g', how_to_use='Viên bổ xương khớp cho người già',
        #               price=('20000'), unit_name='viên', created_date=('2024-01-11'))
        #
        # db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10])
        # db.session.commit()

# -------ĐƠN THUỐC--------
        # a11 = Prescription(medical_report_id='1', medicine_id='2',
        #               count=('33'),created_date=('2024-03-09'))
        # a12 = Prescription(medical_report_id='1', medicine_id='5',
        #                count=('11'), created_date=('2024-03-09'))
        # a13 = Prescription(medical_report_id='1', medicine_id='7',
        #                count=('2'), created_date=('2024-03-09'))
        # a14 = Prescription(medical_report_id='2', medicine_id='3',
        #                count=('22'), created_date=('2024-03-11'))
        # a15 = Prescription(medical_report_id='2', medicine_id='8',
        #                count=('6'), created_date=('2024-03-10'))
        # a16 = Prescription(medical_report_id='2', medicine_id='10',
        #                count=('5'), created_date=('2024-03-9'))
        #
        # db.session.add_all([a11, a12, a13, a14, a15, a16])
        # db.session.commit()


        u = User(name='Admin', username='admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.ADMIN)
        p = User(name='Patient1', username='patient1',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.PATIENT)
        n = User(name='Nurse1', username='nurse1',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.NURSE)
        d = User(name='doctor1', username='doctor1',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.DOCTOR)
        c = User(name='cashier1', username='cashier1',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRoleEnum.CASHIER)
        patients = [Patient(name='Lê Thị Thanh An',gender='Nữ',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-01-07 00:00:00',address='Hà Nội',disease_history='',tel='0987-345-123'),
                    Patient(name='Nguyễn Phương Anh',gender='Nữ',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-08-05 00:00:00',address='Nam Định',disease_history='',tel='2454-454-345'),
                    Patient(name='Phạm Giang Linh',gender='Nữ',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-10-05 00:00:00',address='Phú Thọ',disease_history='',tel='3452-324-453'),
                    Patient(name='Bùi Thị Khánh Linh',gender='Nữ',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-12-05 00:00:00',address='Huế',disease_history='',tel='5323-456-424'),
                    Patient(name='Phạm Nhật Tiến',gender='Nam',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-01-06 00:00:00',address='Tây Ninh',disease_history='',tel='4345-653-221'),
                    Patient(name='Phạm Quốc Đại',gender='Nam',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-01-05 00:00:00',address='Đăk Lăk',disease_history='',tel='4356-432-894'),
                    Patient(name='Đỗ Công Vinh',gender='Nam',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-01-05 00:00:00',address='Nghệ An',disease_history='',tel='2345-231-345'),
                    Patient(name='Đoàn Phan An Khánh',gender='Nam',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-01-05 00:00:00',address='Quảng Nam',disease_history='',tel='4354-768-876'),
                    Patient(name='Nguyễn Thị Tú Anh',gender='Nữ',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-01-05 00:00:00',address='Đà Nẵng',disease_history='',tel='2431-324-067'),
                    Patient(name='Vũ Thế Quang',gender='Nam',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-01-05 00:00:00',address='Lào Cai',disease_history='',tel='9567-097-456'),
                    Patient(name='Tạ Xuân Nam',gender='Nam',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-01-05 00:00:00',address='Cao Bằng',disease_history='',tel='0985-456-342'),
                    Patient(name='Đinh Thị Bích Ngọc',gender='Nữ',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-01-05 00:00:00',address='Bình Định',disease_history='',tel='4595-456-432'),
                    Patient(name='Vũ Thành Nhân',gender='Nam',date_appointment='2024-01-05 00:00:00',date_of_birth='2002-01-05 00:00:00',address='Vinh',disease_history='',tel='4356-968-438'),
                    ]
        rule = Rule(rule_name='Patient per day', value='10')
        rule1 = Rule(rule_name='Examination price', value='100000')
        db.session.add_all([u, p, n, d, c,rule,rule1])
        db.session.add_all(patients)
        db.session.commit()


