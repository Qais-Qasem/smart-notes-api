# main.py

from fastapi import FastAPI, HTTPException
from typing import List
# استيراد الكلاسات من ملف services
from services import NoteService, Note, NoteCreate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart Notes API! Please visit /docs for the documentation."}

# إنشاء نسخة واحدة من خدمة الملاحظات لاستخدامها في كل التطبيق
note_service = NoteService()

# --- نقاط الوصول (Endpoints) الآن أصبحت أنظف بكثير ---

@app.post("/notes/", response_model=Note)
def create_note_endpoint(note_in: NoteCreate):
    return note_service.create_note(note_in)

@app.get("/notes/", response_model=List[Note])
def read_notes_endpoint():
    return note_service.get_all_notes()

@app.get("/notes/{note_id}", response_model=Note)
def read_note_endpoint(note_id: int):
    note = note_service.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=Note)
def update_note_endpoint(note_id: int, note_update: NoteCreate):
    updated_note = note_service.update_note(note_id, note_update)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note

@app.delete("/notes/{note_id}", response_model=dict)
def delete_note_endpoint(note_id: int):
    was_deleted = note_service.delete_note(note_id)
    if not was_deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}

# أضف هذا الكود في نهاية ملف main.py

@app.get("/notes/{note_id}/related", response_model=List[Note])
def get_related_notes_endpoint(note_id: int):
    related_notes = note_service.find_related_notes(note_id)
    if not related_notes:
        # لا يعتبر خطأ إذا لم توجد ملاحظات مشابهة، نرجع قائمة فارغة
        return []
    return related_notes