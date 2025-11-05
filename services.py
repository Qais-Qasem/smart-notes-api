# services.py

from typing import List, Optional
from pydantic import BaseModel
# --- استيراد الأدوات الجديدة ---
from sentence_transformers import SentenceTransformer, util

# --- 1. تحديث هيكل البيانات ليحفظ البصمة الرقمية ---
class Note(BaseModel):
    id: int
    title: str
    content: str
    tags: Optional[List[str]] = None # the neww add on branch
    embedding: Optional[List[float]] = None # سيحتوي على بصمة المعنى

class NoteCreate(BaseModel):
    title: str
    content: str

# --- 2. تحديث الكلاس ليستخدم نموذج الذكاء الاصطناعي ---
class NoteService:
    def __init__(self):
        self.db: List[Note] = []
        self.next_note_id = 1
        # --- تحميل النموذج عند بدء التشغيل ---
        # سيتم تحميل النموذج مرة واحدة فقط، مما يحسن الأداء
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def create_note(self, note_in: NoteCreate) -> Note:
        new_note = Note(id=self.next_note_id, title=note_in.title, content=note_in.content)
        
        # --- حساب البصمة الرقمية للنص ---
        # ندمج العنوان والمحتوى للحصول على أفضل معنى
        text_to_embed = f"{new_note.title}: {new_note.content}"
        embedding = self.model.encode(text_to_embed, convert_to_tensor=False).tolist()
        new_note.embedding = embedding

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

    # --- إضافة وظيفة جديدة لإيجاد الملاحظات المتشابهة ---
    def find_related_notes(self, note_id: int, top_k=3) -> List[Note]:
        source_note = self.get_note_by_id(note_id)
        if not source_note or not source_note.embedding:
            return []

        scores = []
        for note in self.db:
            if note.id != source_note.id and note.embedding:
                # حساب مدى التشابه بين الملاحظة المصدر وكل ملاحظة أخرى
                score = util.cos_sim(source_note.embedding, note.embedding)
                scores.append((score.item(), note))
        
        # ترتيب النتائج من الأعلى إلى الأقل تشابهًا
        scores.sort(key=lambda x: x[0], reverse=True)
        
        # إرجاع أفضل النتائج (بدون درجة التشابه)
        return [note for score, note in scores[:top_k]]

    def update_note(self, note_id: int, note_update: NoteCreate) -> Note | None:
        # (الكود هنا لم يتغير)
        note_to_update = self.get_note_by_id(note_id)
        if note_to_update:
            note_to_update.title = note_update.title
            note_to_update.content = note_update.content
            # إعادة حساب البصمة عند التحديث
            text_to_embed = f"{note_to_update.title}: {note_to_update.content}"
            note_to_update.embedding = self.model.encode(text_to_embed).tolist()
            return note_to_update
        return None

    def delete_note(self, note_id: int) -> bool:
        # (الكود هنا لم يتغير)
        note_to_delete = self.get_note_by_id(note_id)
        if note_to_delete:
            self.db.remove(note_to_delete)
            return True
        return False