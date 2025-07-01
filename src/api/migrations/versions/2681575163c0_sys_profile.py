"""sys_profile

Revision ID: 2681575163c0
Revises: 7cee4b561f30
Create Date: 2025-07-01 13:56:40.217637

"""
from alembic import op
# import sqlalchemy as sa
# from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2681575163c0'
down_revision = '7cee4b561f30'
branch_labels = None
depends_on = None


def upgrade():
    # 数据清洗：修正系统变量 profile_key 命名
    op.execute("""
        UPDATE profile_item SET profile_key = 'sys_user_nickname' WHERE parent_id = '' AND profile_key = 'nick_name';
    """)
    op.execute("""
        UPDATE profile_item SET profile_key = 'sys_user_style' WHERE parent_id = '' AND profile_key = 'style';
    """)
    op.execute("""
        UPDATE profile_item SET profile_key = 'sys_user_background' WHERE parent_id = '' AND profile_key = 'userbackground';
    """)
    op.execute("""
        UPDATE profile_item SET profile_key = 'sys_user_input' WHERE parent_id = '' AND profile_key = 'input';
    """)
    # 同步 user_profile 表中的系统变量 profile_key
    op.execute("""
        UPDATE user_profile SET profile_key = 'sys_user_nickname' WHERE profile_type = 1 AND profile_key = 'nick_name';
    """)
    op.execute("""
        UPDATE user_profile SET profile_key = 'sys_user_style' WHERE profile_type = 1 AND profile_key = 'style';
    """)
    op.execute("""
        UPDATE user_profile SET profile_key = 'sys_user_background' WHERE profile_type = 1 AND profile_key = 'userbackground';
    """)
    op.execute("""
        UPDATE user_profile SET profile_key = 'sys_user_input' WHERE profile_type = 1 AND profile_key = 'input';
    """)
    # 课程/师傅自定义变量（引用系统变量）也需要同步 profile_key
    op.execute("""
        UPDATE profile_item SET profile_key = 'sys_user_nickname' WHERE parent_id != '' AND profile_key = 'nick_name';
    """)
    op.execute("""
        UPDATE profile_item SET profile_key = 'sys_user_style' WHERE parent_id != '' AND profile_key = 'style';
    """)
    op.execute("""
        UPDATE profile_item SET profile_key = 'sys_user_background' WHERE parent_id != '' AND profile_key = 'userbackground';
    """)
    op.execute("""
        UPDATE profile_item SET profile_key = 'sys_user_input' WHERE parent_id != '' AND profile_key = 'input';
    """)
    # 遍历 ai_lesson_script 表，替换 script_check_prompt 和 script_ui_profile 字段中的变量名
    # 替换 script_check_prompt 里的变量
    op.execute("""
        UPDATE ai_lesson_script SET script_check_prompt = REPLACE(script_check_prompt, 'nick_name', 'sys_user_nickname') WHERE script_check_prompt LIKE '%nick_name%';
    """)
    op.execute("""
        UPDATE ai_lesson_script SET script_check_prompt = REPLACE(script_check_prompt, 'style', 'sys_user_style') WHERE script_check_prompt LIKE '%style%';
    """)
    op.execute("""
        UPDATE ai_lesson_script SET script_check_prompt = REPLACE(script_check_prompt, 'userbackground', 'sys_user_background') WHERE script_check_prompt LIKE '%userbackground%';
    """)
    op.execute("""
        UPDATE ai_lesson_script SET script_check_prompt = REPLACE(script_check_prompt, 'input', 'sys_user_input') WHERE script_check_prompt LIKE '%input%';
    """)
    # 替换 script_ui_profile 里的变量
    op.execute("""
        UPDATE ai_lesson_script SET script_ui_profile = REPLACE(script_ui_profile, 'nick_name', 'sys_user_nickname') WHERE script_ui_profile LIKE '%nick_name%';
    """)
    op.execute("""
        UPDATE ai_lesson_script SET script_ui_profile = REPLACE(script_ui_profile, 'style', 'sys_user_style') WHERE script_ui_profile LIKE '%style%';
    """)
    op.execute("""
        UPDATE ai_lesson_script SET script_ui_profile = REPLACE(script_ui_profile, 'userbackground', 'sys_user_background') WHERE script_ui_profile LIKE '%userbackground%';
    """)
    op.execute("""
        UPDATE ai_lesson_script SET script_ui_profile = REPLACE(script_ui_profile, 'input', 'sys_user_input') WHERE script_ui_profile LIKE '%input%';
    """)
    # ### end Alembic commands ###


def downgrade():
       pass

    # ### end Alembic commands ###
