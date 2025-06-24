from flaskr.service.shifu.funcs import get_shifu_summary

# from .test_utils import dump, dump_detailed


# aitest tests/test_shifu_funcs.py::test_get_shifu_abstract
def test_get_shifu_abstract(app):
    with app.app_context():
        get_shifu_summary(app, "ba91abb2b57e4edfb5855144dc780220")
        # for i in data:
        #     dump_detailed(i.outline, include_methods=False)
        # for j in i.children:
        #     dump_detailed(j.outline, include_methods=False)
