"""sys_profile

Revision ID: 2681575163c0
Revises: 7cee4b561f30
Create Date: 2025-07-01 13:56:40.217637

"""

from alembic import op
from sqlalchemy.sql import text
import re

# revision identifiers, used by Alembic.
revision = "2681575163c0"
down_revision = "7cee4b561f30"
branch_labels = None
depends_on = None


def upgrade():
    renames = {
        "nick_name": "sys_user_nickname",
        "nickname": "sys_user_nickname",
        "style": "sys_user_style",
        "userbackground": "sys_user_background",
        "user_background": "sys_user_background",
        "input": "sys_user_input",
    }
    # profile_item parent_id = ''
    for old, new in renames.items():
        op.execute(
            f"UPDATE profile_item SET profile_key = '{new}' WHERE parent_id = '' AND profile_key = '{old}';"
        )
    # user_profile - 处理所有 profile_type 的记录
    for old, new in renames.items():
        op.execute(
            f"UPDATE user_profile SET profile_key = '{new}' WHERE profile_key = '{old}';"
        )
    # profile_item parent_id != ''
    for old, new in renames.items():
        op.execute(
            f"UPDATE profile_item SET profile_key = '{new}' WHERE parent_id != '' AND profile_key = '{old}';"
        )
    # ai_lesson_script
    connection = op.get_bind()
    batch_size = 5000
    # ai_lesson_script 分批处理（优化：全表遍历，内存判断，script_prompt 用正则）
    for old, new in renames.items():
        pattern = re.compile(rf"\{{{old}\}}")
        pattern_parens = re.compile(rf"\({old}\)")
        pattern_json = re.compile(rf'\{{{{\"{old}\":\s*"([^"]*)"}}}}')
        pattern_brackets = re.compile(rf"\[{old}\]")
        offset = 0
        while True:
            results = connection.execute(
                text(
                    "SELECT id, script_check_prompt, script_ui_profile, script_prompt "
                    "FROM ai_lesson_script "
                    "ORDER BY id ASC "
                    "LIMIT :limit OFFSET :offset"
                ),
                {"limit": batch_size, "offset": offset},
            ).fetchall()
            if not results:
                break
            for row in results:
                # script_prompt 只替换 {old} 为 {new}
                new_script_prompt = (
                    pattern.sub(f"{{{new}}}", row[3])  # script_prompt 是第4个字段
                    if row[3] and pattern.search(row[3])
                    else row[3]
                )
                # script_check_prompt 替换 {old}、(old) 和 {{"old": "xxx"}}
                new_prompt = row[1]  # script_check_prompt 是第2个字段
                if new_prompt:
                    new_prompt = pattern.sub(f"{{{new}}}", new_prompt)
                    new_prompt = pattern_parens.sub(f"({new})", new_prompt)
                    new_prompt = pattern_json.sub(f'{{{{"{new}": "\\1"}}}}', new_prompt)
                # script_ui_profile 替换 [old] 格式
                new_profile = row[2]  # script_ui_profile 是第3个字段
                if new_profile:
                    new_profile = pattern_brackets.sub(f"[{new}]", new_profile)
                if (
                    new_prompt != row[1]
                    or new_profile != row[2]
                    or new_script_prompt != row[3]
                ):
                    connection.execute(
                        text(
                            "UPDATE ai_lesson_script SET script_check_prompt = :new_prompt, script_ui_profile = :new_profile, script_prompt = :new_script_prompt WHERE id = :id"
                        ),
                        {
                            "new_prompt": new_prompt,
                            "new_profile": new_profile,
                            "new_script_prompt": new_script_prompt,
                            "id": row[0],  # id 是第1个字段
                        },
                    )
            if len(results) < batch_size:
                break
            offset += batch_size
    # ### end Alembic commands ###


def downgrade():
    renames = {
        "sys_user_nickname": "nick_name",
        "sys_user_style": "style",
        "sys_user_background": "user_background",
        "sys_user_input": "input",

    }
    # profile_item parent_id = ''
    for old, new in renames.items():
        op.execute(
            f"UPDATE profile_item SET profile_key = '{new}' WHERE parent_id = '' AND profile_key = '{old}';"
        )
    # user_profile - 处理所有 profile_type 的记录
    for old, new in renames.items():
        op.execute(
            f"UPDATE user_profile SET profile_key = '{new}' WHERE profile_key = '{old}';"
        )
    # profile_item parent_id != ''
    for old, new in renames.items():
        op.execute(
            f"UPDATE profile_item SET profile_key = '{new}' WHERE parent_id != '' AND profile_key = '{old}';"
        )
    # ai_lesson_script
    connection = op.get_bind()
    batch_size = 5000
    # ai_lesson_script 分批处理（回滚）
    for old, new in renames.items():
        pattern = re.compile(rf"\{{{old}\}}")
        pattern_parens = re.compile(rf"\({old}\)")
        pattern_json = re.compile(rf'\{{{{\"{old}\":\s*"([^"]*)"}}}}')
        pattern_brackets = re.compile(rf"\[{old}\]")
        offset = 0
        while True:
            results = connection.execute(
                text(
                    "SELECT id, script_check_prompt, script_ui_profile, script_prompt "
                    "FROM ai_lesson_script "
                    "ORDER BY id ASC "
                    "LIMIT :limit OFFSET :offset"
                ),
                {"limit": batch_size, "offset": offset},
            ).fetchall()
            if not results:
                break
            for row in results:
                # script_prompt 只替换 {old} 为 {new}
                new_script_prompt = (
                    pattern.sub(f"{{{new}}}", row[3])  # script_prompt 是第4个字段
                    if row[3] and pattern.search(row[3])
                    else row[3]
                )
                # script_check_prompt 替换 {old}、(old) 和 {{"old": "xxx"}}
                new_prompt = row[1]  # script_check_prompt 是第2个字段
                if new_prompt:
                    new_prompt = pattern.sub(f"{{{new}}}", new_prompt)
                    new_prompt = pattern_parens.sub(f"({new})", new_prompt)
                    new_prompt = pattern_json.sub(f'{{{{"{new}": "\\1"}}}}', new_prompt)
                # script_ui_profile 替换 [old] 格式
                new_profile = row[2]  # script_ui_profile 是第3个字段
                if new_profile:
                    new_profile = pattern_brackets.sub(f"[{new}]", new_profile)
                if (
                    new_prompt != row[1]
                    or new_profile != row[2]
                    or new_script_prompt != row[3]
                ):
                    connection.execute(
                        text(
                            "UPDATE ai_lesson_script SET script_check_prompt = :new_prompt, script_ui_profile = :new_profile, script_prompt = :new_script_prompt WHERE id = :id"
                        ),
                        {
                            "new_prompt": new_prompt,
                            "new_profile": new_profile,
                            "new_script_prompt": new_script_prompt,
                            "id": row[0],  # id 是第1个字段
                        },
                    )
            if len(results) < batch_size:
                break
            offset += batch_size
    # ### end Alembic commands ###
