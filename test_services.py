# test_services.py

from services import NoteService, NoteCreate

# يجب أن يبدأ اسم كل دالة اختبار بكلمة "test_"
def test_create_and_get_note():
    # 1. الإعداد (Arrange)
    # نقوم بإنشاء نسخة جديدة وفارغة من خدمتنا
    service = NoteService()
    # نجهز بيانات الملاحظة التي نريد إنشاءها
    note_data = NoteCreate(title="Test Title", content="Test Content")

    # 2. التنفيذ (Act)
    # نقوم بتنفيذ الوظيفة التي نريد اختبارها: إنشاء ملاحظة
    created_note = service.create_note(note_data)

    # 3. التأكيد (Assert)
    # نتأكد من أن النتائج هي ما نتوقعه بالضبط
    
    # التأكد من أن الملاحظة التي تم إنشاؤها ليست فارغة
    assert created_note is not None
    # التأكد من أن الـ id الخاص بها هو 1 (لأنها أول ملاحظة)
    assert created_note.id == 1
    # التأكد من أن العنوان صحيح
    assert created_note.title == "Test Title"

    # الآن نختبر وظيفة القراءة (get_note_by_id)
    retrieved_note = service.get_note_by_id(1)
    
    # التأكد من أننا حصلنا على نفس الملاحظة
    assert retrieved_note is not None
    assert retrieved_note.id == 1
    assert retrieved_note.title == "Test Title"

def test_get_nonexistent_note():
    # 1. الإعداد (Arrange)
    service = NoteService()

    # 2. التنفيذ (Act)
    # نحاول الحصول على ملاحظة غير موجودة
    retrieved_note = service.get_note_by_id(999)

    # 3. التأكيد (Assert)
    # نتوقع أن تكون النتيجة None (لا شيء)
    assert retrieved_note is None