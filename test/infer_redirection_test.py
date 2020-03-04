# coding: utf-8
# =============================================================================
# Ural Infer Redirection Unit Tests
# =============================================================================
from ural import infer_redirection

TESTS = [
    (
        'https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=2ahUKEwjp8Lih_LnmAhWQlxQKHVTmCJYQFjADegQIARAB&url=http%3A%2F%2Fwww.mon-ip.com%2F&usg=AOvVaw0sfeZJyVtUS2smoyMlJmes',
        'http://www.mon-ip.com/'
    )
]


class TestInferRedirection(object):
    def test_basics(self):
        for url, redirected in TESTS:
            assert infer_redirection(url) == redirected
