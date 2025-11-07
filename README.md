# Aoyama Supply Chain Backend

บริการ FastAPI ขนาดกะทัดรัดสำหรับเผยข้อมูล SPC (Statistical Process Control) Part Master จาก SQL Server โดยใช้ FastAPI + SQLAlchemy + Pydantic v2 และโหลดค่าคอนฟิกจากไฟล์ `.env`

## โครงสร้างโปรเจ็กต์
```
app/
├── core/            # การตั้งค่าและ helper สำหรับฐานข้อมูล/เซสชัน
├── models/          # โมเดล SQLAlchemy (เช่น SpcPartMasterModel)
├── routers/         # FastAPI router (ปัจจุบันมี /spc-part-master)
├── schemas/         # สคีมาคำตอบ/คำขอของ Pydantic
└── services/        # เลเยอร์ service สำหรับดึง/ประมวลผลข้อมูล
```

## สิ่งที่ต้องมี
- Python 3.11+ (ให้ตรงกับ virtualenv ในโปรเจ็กต์)
- SQL Server ที่เข้าถึงได้ด้วยข้อมูลใน `.env`
- [Microsoft ODBC Driver 17+ for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server) พร้อม build tools เพื่อให้ `pyodbc` ใช้งานได้

## การติดตั้ง
```powershell
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
pip install fastapi uvicorn[standard] sqlalchemy pydantic pydantic-settings pyodbc python-dotenv
```
ถ้าติดตั้ง dependency แล้ว แนะนำให้ freeze ไว้เพื่อให้ทีมใช้เวอร์ชันเดียวกัน:
```powershell
pip freeze > requirements.txt
```

## ตัวแปรสภาพแวดล้อม
ไฟล์ `app/core/config.py` จะโหลดค่าจาก `.env` ตัวอย่าง:
```
DB_SERVER=10.17.2.3
DB_PORT=1433
DB_USER=sa
DB_PASSWORD=sasql
DB_NAME=SLDB
DB_ENCRYPT=no
DB_DRIVER=ODBC Driver 17 for SQL Server
```
ปรับค่าเหล่านี้ให้ตรงกับระบบของคุณ โดยเฉพาะ `DB_DRIVER` ต้องตรงกับชื่อไดรเวอร์ ODBC ที่ติดตั้งไว้

## การรัน API
จากโฟลเดอร์รูทของโปรเจ็กต์:
```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```
หรือเมื่อ activate virtualenv แล้ว:
```powershell
uvicorn app.main:app --reload
```
เปิด `http://127.0.0.1:8000/docs` เพื่อทดลองเรียก API ผ่าน Swagger UI

## Endpoint ปัจจุบัน
- `GET /spc-part-master/` – ดึงรายการ SPC Part Master ทั้งหมด (อ่านจาก `SpcPartMasterModel` และ serialize ด้วย `SpcPartMasterResponse`)

## ทิปสำหรับการพัฒนา
- เพิ่ม response model ใหม่ให้ใช้ Pydantic v2 syntax: `model_config = ConfigDict(from_attributes=True)` (ไม่ใช้ `orm_mode`)
- ให้ชื่อ attribute ใน SQLAlchemy ตรงกับฟิลด์ใน schema หรือใช้ alias ของ Pydantic เพื่อเลี่ยง error “Field required”
- เมื่อระบบใหญ่ขึ้น พิจารณาเพิ่มชุดทดสอบ (เช่น `pytest`) และ workflow CI เพื่อป้องกัน regression
