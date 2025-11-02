from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# --- 1. تعريف هيكل البيانات (Data Model) ---
# هذا الكلاس يحدد كيف يجب أن تبدو "الملاحظة"
# أي ملاحظة يجب أن تحتوي على id, title, content
class Note(BaseModel):
    id: int
    title: str
    content: str

# هذا الكلاس سنستخدمه عند إنشاء ملاحظة جديدة، لأن الـ id سيتم إنشاؤه تلقائياً
class NoteCreate(BaseModel):
    title: str
    content: str

# --- 2. قاعدة بيانات مؤقتة في الذاكرة ---
# سنستخدم قائمة (list) عادية لتخزين الملاحظات
# كل مرة تعيد تشغيل الخادم، ستبدأ هذه القائمة فارغة
db: List[Note] = []
next_note_id = 1

# --- 3. إعداد تطبيق FastAPI ---
app = FastAPI()

# --- 4. برمجة نقاط الوصول (Endpoints) ---

# C = Create (إنشاء ملاحظة جديدة)
@app.post("/notes/", response_model=Note)
def create_note(note_in: NoteCreate):
    global next_note_id
    # إنشاء ملاحظة جديدة بالبيانات المستلمة وإعطائها id فريد
    new_note = Note(id=next_note_id, title=note_in.title, content=note_in.content)
    db.append(new_note)
    next_note_id += 1
    return new_note

# R = Read (قراءة كل الملاحظات)
@app.get("/notes/", response_model=List[Note])
def read_notes():
    return db

# R = Read (قراءة ملاحظة واحدة محددة)
@app.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int):
    # البحث عن الملاحظة في "قاعدة البيانات"
    for note in db:
        if note.id == note_id:
            return note
    # إذا لم يتم العثور على الملاحظة، أرجع خطأ 404
    raise HTTPException(status_code=404, detail="Note not found")

# U = Update (تحديث ملاحظة)
@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note_update: NoteCreate):
    for i, note in enumerate(db):
        if note.id == note_id:
            # تحديث بيانات الملاحظة
            db[i].title = note_update.title
            db[i].content = note_update.content
            return db[i]
    raise HTTPException(status_code=404, detail="Note not found")

# D = Delete (حذف ملاحظة)
@app.delete("/notes/{note_id}", response_model=dict)
def delete_note(note_id: int):
    for i, note in enumerate(db):
        if note.id == note_id:
            db.pop(i)
            return {"message": "Note deleted successfully"}
    raise HTTPException(status_code=404, detail="Note not found")