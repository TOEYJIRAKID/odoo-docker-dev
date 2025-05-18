# Todo List Module for Odoo 17

โมดูลสำหรับจัดการรายการสิ่งที่ต้องทำ (Todo List) บน Odoo 17

## คุณสมบัติหลัก

- สร้างและจัดการรายการ Todo List พร้อมกำหนดวันเริ่มต้นและวันสิ้นสุด
- จัดการงานย่อย (Tasks) ภายใน Todo List
- ระบบติดตามสถานะ (Draft, In Progress, Complete)
- ระบบแท็ก (Tags) พร้อมสีที่กำหนดเอง
- เพิ่มผู้เข้าร่วม (Attendees) ในแต่ละ Todo List

## วิดีโอสาธิตการใช้งาน

[![Todo List Module Demo](https://img.youtube.com/vi/1ySwNWxXKX0/0.jpg)](https://www.youtube.com/watch?v=1ySwNWxXKX0)

## การติดตั้งผ่าน Docker

1. **Clone โปรเจกต์**

\`\`\`bash
git clone https://github.com/TOEYJIRAKID/odoo-docker-dev.git
cd odoo-docker-dev
\`\`\`

2. **สร้างไฟล์ docker-compose.yml**

\`\`\`yaml
version: '3'
services:
  web:
    image: odoo:17
    depends_on:
      - db
    ports:
      - "8069:8069"
    volumes:
      - ./addons:/mnt/extra-addons
      - ./etc:/etc/odoo
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
    volumes:
      - odoo-db-data:/var/lib/postgresql/data

volumes:
  odoo-db-data:
\`\`\`

3. **คัดลอกโมดูล Todo List ไปยังโฟลเดอร์ addons**

\`\`\`bash
mkdir -p addons
cp -r todo_list_module addons/todo_list
\`\`\`

4. **เริ่มต้นใช้งาน Docker**

\`\`\`bash
docker-compose up -d
\`\`\`

5. **เข้าถึง Odoo และติดตั้งโมดูล**
   - เปิดเบราว์เซอร์ไปที่ http://localhost:8069
   - สร้างฐานข้อมูลใหม่
   - เข้าสู่โหมด Developer
   - ไปที่ Apps > Update Apps List
   - ค้นหา "Todo List" และกดติดตั้ง

## วิธีการใช้งาน

1. ไปที่เมนู Todo List > All
2. คลิกปุ่ม "Create" เพื่อสร้าง Todo List ใหม่
3. กรอกชื่อ, เลือกแท็ก, กำหนดวันที่เริ่มต้นและสิ้นสุด
4. เพิ่มงานย่อย (Tasks) ในแท็บ "List"
5. คลิกปุ่ม "PROGRESS" เพื่อเริ่มดำเนินการ
6. ทำเครื่องหมายงานย่อยเป็น "เสร็จสิ้น" โดยเลือกช่อง "Is Complete"
7. เมื่องานย่อยทั้งหมดเสร็จสิ้น คลิกปุ่ม "DONE"

## ข้อกำหนดระบบ

- Odoo 17
- PostgreSQL 16
- Docker และ Docker Compose

## ผู้พัฒนา

- TOEYJIRA - [GitHub](https://github.com/TOEYJIRAKID)
