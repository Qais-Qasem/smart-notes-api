# services.py

from typing import List
from pydantic import BaseModel

# --- 1. تعريف هياكل البيانات ---
# سنحتاج إلى تعريفها هنا أيضًا
class Note(BaseModel):
    id: int
    title: str
    content: str

class NoteCreate(BaseModel):
    title: str
    content: str

# --- 2. إنشاء كلاس لإدارة الملاحظات ---
# هذا الكلاس هو المسؤول الوحيد عن التعامل مع البيانات
class NoteService:
    def __init__(self):
        self.db: List[Note] = []
        self.next_note_id = 1

    def create_note(self, note_in: NoteCreate) -> Note:
        new_note = Note(id=self.next_note_id, title=note_in.title, content=note_in.content)
        self.db.append(new_note)
        self.next_note_id += 1
        return new_note

    def get_all_notes(self) -> List[Note]:
        return self.db

    def get_note_by_id(self, note_id: int) -> Note | None:
        for note in self.db:
            if note.id == note_id:
                return note
        return None

    def update_note(self, note_id: int, note_update: NoteCreate) -> Note | None:
        note_to_update = self.get_note_by_id(note_id)
        if note_to_update:
            note_to_update.title = note_update.title
            note_to_update.content = note_update.content
            return note_to_update
        return None

    def delete_note(self, note_id: int) -> bool:
        note_to_delete = self.get_note_by_id(note_id)
        if note_to_delete:
            self.db.remove(note_to_delete)
            return True
        return False