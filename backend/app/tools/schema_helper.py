from pathlib import Path
import sys

# Ensure the repo root is on sys.path so absolute imports work
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from sqlalchemy import inspect
from backend.app.db.database import engine 

def get_database_schema():
    """
    نسخة محسنة تعطي الـ LLM فقط ما يحتاجه: الأسماء والعلاقات.
    """
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    # جداول يجب تجاهلها تماماً لتوفير التوكنز ومنع التشتت
    blacklisted_tables = ["access_logs", "alembic_version", "chat_history"]
    
    schema_description = "### DATABASE SCHEMA (Optimized) ###\n"
    relationships = []

    for table_name in table_names:
        if table_name in blacklisted_tables:
            continue
            
        # إضافة اسم الجدول فقط
        schema_description += f"- {table_name} ("
        
        # جلب الأعمدة (الأسماء فقط بدون الأنواع)
        columns = inspector.get_columns(table_name)
        col_names = [col['name'] for col in columns]
        schema_description += ", ".join(col_names) + ")\n"
        
        # جلب المفاتيح الخارجية (Foreign Keys) لفهم الـ JOIN
        fks = inspector.get_foreign_keys(table_name)
        for fk in fks:
            target_table = fk['referred_table']
            target_col = fk['referred_columns'][0]
            source_col = fk['constrained_columns'][0]
            relationships.append(f"  * {table_name}.{source_col} -> {target_table}.{target_col}")

    # إضافة قسم العلاقات في النهاية
    if relationships:
        schema_description += "\nRELEATIONSHIPS (For JOINs):\n"
        schema_description += "\n".join(relationships)
    
    return schema_description

# Simple test to see what the AI will see
if __name__ == "__main__":
    # print schema in text file in same dir
    with open("schema.txt", "w") as f:
        f.write(get_database_schema())
    
    print("done")