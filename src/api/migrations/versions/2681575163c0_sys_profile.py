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
    # 预编译所有正则表达式
    patterns = {}
    for old, new in renames.items():
        patterns[old] = {
            "braces": re.compile(rf"\{{{old}\}}"),
            "parens": re.compile(rf"\({old}\)"),
            "json": re.compile(rf'\{{{{\"{old}\":\s*"([^"]*)"}}}}'),
            "brackets": re.compile(rf"\[{old}\]"),
            "new": new,
        }

    offset = 0
    while True:
        results = connection.execute(
            text(
                "SELECT id, script_check_prompt, script_ui_profile, script_prompt, script_profile "
                "FROM ai_lesson_script "
                "ORDER BY id ASC "
                "LIMIT :limit OFFSET :offset"
            ),
            {"limit": batch_size, "offset": offset},
        ).fetchall()
        if not results:
            break
        for row in results:
            # 初始化新值
            new_script_prompt = row[3]  # script_prompt 是第4个字段
            new_prompt = row[1]  # script_check_prompt 是第2个字段
            new_profile = row[2]  # script_ui_profile 是第3个字段
            new_script_profile = row[4]  # script_profile 是第5个字段

            # 对每个变量名进行替换
            for old, pattern_dict in patterns.items():
                new = pattern_dict["new"]

                # script_prompt 只替换 {old} 为 {new}
                if new_script_prompt and pattern_dict["braces"].search(
                    new_script_prompt
                ):
                    new_script_prompt = pattern_dict["braces"].sub(
                        f"{{{new}}}", new_script_prompt
                    )

                # script_check_prompt 替换 {old}、(old) 和 {{"old": "xxx"}}
                if new_prompt:
                    new_prompt = pattern_dict["braces"].sub(f"{{{new}}}", new_prompt)
                    new_prompt = pattern_dict["parens"].sub(f"({new})", new_prompt)
                    new_prompt = pattern_dict["json"].sub(
                        f'{{{{"{new}": "\\1"}}}}', new_prompt
                    )

                # script_ui_profile 替换 [old] 格式
                if new_profile:
                    new_profile = pattern_dict["brackets"].sub(f"[{new}]", new_profile)

                # script_profile 替换 [old] 格式
                if new_script_profile:
                    new_script_profile = pattern_dict["brackets"].sub(
                        f"[{new}]", new_script_profile
                    )

            # 如果有变化就更新
            if (
                new_prompt != row[1]
                or new_profile != row[2]
                or new_script_prompt != row[3]
                or new_script_profile != row[4]
            ):
                connection.execute(
                    text(
                        "UPDATE ai_lesson_script SET "
                        "script_check_prompt = :new_prompt, "
                        "script_ui_profile = :new_profile, "
                        "script_prompt = :new_script_prompt, "
                        "script_profile = :new_script_profile "
                        "WHERE id = :id"
                    ),
                    {
                        "new_prompt": new_prompt,
                        "new_profile": new_profile,
                        "new_script_prompt": new_script_prompt,
                        "new_script_profile": new_script_profile,
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
    # 预编译所有正则表达式
    patterns = {}
    for old, new in renames.items():
        patterns[old] = {
            "braces": re.compile(rf"\{{{old}\}}"),
            "parens": re.compile(rf"\({old}\)"),
            "json": re.compile(rf'\{{{{\"{old}\":\s*"([^"]*)"}}}}'),
            "brackets": re.compile(rf"\[{old}\]"),
            "new": new,
        }

    offset = 0
    while True:
        results = connection.execute(
            text(
                "SELECT id, script_check_prompt, script_ui_profile, script_prompt, script_profile "
                "FROM ai_lesson_script "
                "ORDER BY id ASC "
                "LIMIT :limit OFFSET :offset"
            ),
            {"limit": batch_size, "offset": offset},
        ).fetchall()
        if not results:
            break
        for row in results:
            # 初始化新值
            new_script_prompt = row[3]  # script_prompt 是第4个字段
            new_prompt = row[1]  # script_check_prompt 是第2个字段
            new_profile = row[2]  # script_ui_profile 是第3个字段
            new_script_profile = row[4]  # script_profile 是第5个字段

            # 对每个变量名进行替换
            for old, pattern_dict in patterns.items():
                new = pattern_dict["new"]

                # script_prompt 只替换 {old} 为 {new}
                if new_script_prompt and pattern_dict["braces"].search(
                    new_script_prompt
                ):
                    new_script_prompt = pattern_dict["braces"].sub(
                        f"{{{new}}}", new_script_prompt
                    )

                # script_check_prompt 替换 {old}、(old) 和 {{"old": "xxx"}}
                if new_prompt:
                    new_prompt = pattern_dict["braces"].sub(f"{{{new}}}", new_prompt)
                    new_prompt = pattern_dict["parens"].sub(f"({new})", new_prompt)
                    new_prompt = pattern_dict["json"].sub(
                        f'{{{{"{new}": "\\1"}}}}', new_prompt
                    )

                # script_ui_profile 替换 [old] 格式
                if new_profile:
                    new_profile = pattern_dict["brackets"].sub(f"[{new}]", new_profile)

                # script_profile 替换 [old] 格式
                if new_script_profile:
                    new_script_profile = pattern_dict["brackets"].sub(
                        f"[{new}]", new_script_profile
                    )

            # 如果有变化就更新
            if (
                new_prompt != row[1]
                or new_profile != row[2]
                or new_script_prompt != row[3]
                or new_script_profile != row[4]
            ):
                connection.execute(
                    text(
                        "UPDATE ai_lesson_script SET "
                        "script_check_prompt = :new_prompt, "
                        "script_ui_profile = :new_profile, "
                        "script_prompt = :new_script_prompt, "
                        "script_profile = :new_script_profile "
                        "WHERE id = :id"
                    ),
                    {
                        "new_prompt": new_prompt,
                        "new_profile": new_profile,
                        "new_script_prompt": new_script_prompt,
                        "new_script_profile": new_script_profile,
                        "id": row[0],  # id 是第1个字段
                    },
                )
        if len(results) < batch_size:
            break
        offset += batch_size
    # ### end Alembic commands ###
