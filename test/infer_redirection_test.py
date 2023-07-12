# coding: utf-8
# =============================================================================
# Ural Infer Redirection Unit Tests
# =============================================================================
from ural import infer_redirection

TESTS = [
    (
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=2ahUKEwjp8Lih_LnmAhWQlxQKHVTmCJYQFjADegQIARAB&url=http%3A%2F%2Fwww.mon-ip.com%2F&usg=AOvVaw0sfeZJyVtUS2smoyMlJmes",
        "http://www.mon-ip.com/",
    ),
    (
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=2ahUKEwicu4K-rZzmAhWOEBQKHRNWA08QFjAAegQIARAB&url=https%3A%2F%2Fwww.facebook.com%2Fiygeff.ogbeide&usg=AOvVaw0vrBVCiIHUr5pncjeLpPUp",
        "https://www.facebook.com/iygeff.ogbeide",
    ),
    ("http://lemonde.fr", "http://lemonde.fr"),
    (
        "http://lemonde.fr?url=yizfèzfftzfzgfzèzfgçç",
        "http://lemonde.fr?url=yizfèzfftzfzgfzèzfgçç",
    ),
    (
        "https://l.facebook.com/l.php?u=http%3A%2F%2Fwww.chaos-controle.com%2Farchives%2F2013%2F10%2F14%2F28176300.html&amp;h=AT0iUqJpUTMzHAH8HAXwZ11p8P3Z-SrY90wIXZhcjMnxBTHMiau8Fv1hvz00ZezRegqmF86SczyUXx3Gzdt_MdFH-I4CwHIXKKU9L6w522xwOqkOvLAylxojGEwrp341uC-GlVyGE2N7XwTPK9cpP0mQ8PIrWh8Qj2gHIIR08Js0mUr7G8Qe9fx66uYcfnNfTTF1xi0Us8gTo4fOZxAgidGWXsdgtU_OdvQqyEm97oHzKbWfXjkhsrzbtb8ZNMDwCP5099IMcKRD8Hi5H7W3vwh9hd_JlRgm5Z074epD_mGAeoEATE_QUVNTxO0SHO4XNn2Z7LgBamvevu1ENBcuyuSOYA0BsY2cx8mPWJ9t44tQcnmyQhBlYm_YmszDaQx9IfVP26PRqhsTLz-kZzv0DGMiJFU78LVWVPc9QSw2f9mA5JYWr29w12xJJ5XGQ6DhJxDMWRnLdG8Tnd7gZKCaRdqDER1jkO72u75-o4YuV3CLh4j-_4u0fnHSzHdVD8mxr9pNEgu8rvJF1E2H3-XbzA6F2wMQtFCejH8MBakzYtTGNvHSexSiKphE04Ci1Z23nBjCZFsgNXwL3wbIXWfHjh2LCKyihQauYsnvxp6fyioStJSGgyA9GGEswizHa20lucQF0S0F8H9-",
        "http://www.chaos-controle.com/archives/2013/10/14/28176300.html",
    ),
    (
        "https://lm.facebook.com/l.php?u=https%3A%2F%2Fwww.santeplusmag.com%2Fvoici-homme-ideal-selon-signe-zodiaque%2F%3Ffbclid%3DIwAR0y7QtbwjHkA5xGt-JpiINpi5sx9bBdqPgVZlLoY4QXGr7eyHum1wA1tgw&h=AT0JS8tV0L4V23RGMkKsnQNfkt2k9ncZ39JltGuSXqro1LpLQw-kUxgTo2QJprUxH9WS3HpZvb5XRsv3pKJyo6yRF5Zpw6qZRorVGSwiKlD8L5LOmUstIPrGrdboG-OMBDzrGQOU5yONWyjEGlNIZDEpcGSzz4ZZi8IRq6FU-fX385WrAbToCn8AahZXz1_fPFz7bzaDEiHhgM0PHd4iHtF5T-h0lqLlVoqVOMAKU9X2Of2Ief9xWBqlaszvlo816PgMDDhYBkM1TUfevQDa1seXKHdYHKLaHz1LQEIlUlbZnINwWHq9qdgO0KR6Zml2jSsts8ttdxwn8-YYmiRuGy14DWb_-h8WU-_j4O6dWo-9oEfXP_V4RS9ZCkB1aTiaTy1-d92EtVaii24vDuxF_k7VzjZmlA3IToH0weg269bRO_4adejJuYRlaCQFsEhtwom9BqWriXYfdYznFd0po5vHTE9h7ZDRN7jvYSiACSShPnD_xfDiIsQOkE11J4qft7J5ZsHhYk0i2e3WwOqUsK_-kb7aEdeLO3Na7tOfO1UkxlAkCcpANn3ZBBFfjTu4yBQDmuQ7eBMQHUmvRDp96p2EuYPGjsCYP_sXH5dwZ6wKB5GzunmtexIMwiVaIHdOeM42e435pSk0nD3XZhU15qday5GelcMfwHsbN8kzAdvJSRK5EmbVX0dPWsIk5GEVEhqNOOT0ANFz85bXB8nSbLkNk1NLkWd6cwGHVOmmW6Vgl15FzUJKwfoya-owBE9aQhItB_MANmkajA98vAuuAwe1Wfw1MGDuOKUzBNp6ercFpO1diFR-N9SvTxfKc-ZCu0lQKXOcgT3qpe5usMmxcXg6TUCC7ox0pu_j8ees4fF-JQIddh5DDQm5sXOajqKKDEj1-hDL15oW_z_NRuRkXAxhLXN1s5vWt_cDuxHuqwlKI3wst9fK31Z1ovRk0HJa_deZ47E81QxPGlcWFUp3If2tPqE5qiiX6yfRD3QriMMH04wDnSN-R8gYjQKydKQpF_B9tn1BfEvIiOK21kgtzvgnu6iJRTfrNS9qRD1HJcMkf_W5fWPPk1HMc6VtEgf-uU7xxZ1heqj52nVUoMJl3pWV2dlv44KOIPM9afoRddeRH3RDl7B8nbabEER0zsVjGgkre6qLRgKz5P2M8BJJJtCo",
        "https://www.santeplusmag.com/voici-homme-ideal-selon-signe-zodiaque/?fbclid=IwAR0y7QtbwjHkA5xGt-JpiINpi5sx9bBdqPgVZlLoY4QXGr7eyHum1wA1tgw",
    ),
    (
        "https://digital.sustainablebrands.com/wp-login.php?redirect_to=https%3A%2F%2Fdigital.sustainablebrands.com%2Fresources-report-learning-from-leaders-5.html%3Futm_source%3DTwitter%26utm_medium%3Dcards%26utm_campaign%3DLfL5",
        "https://digital.sustainablebrands.com/resources-report-learning-from-leaders-5.html?utm_source=Twitter&utm_medium=cards&utm_campaign=LfL5",
    ),
    (
        "http://www.wiki-rennes.fr/index.php?title=CampOSV_Makers&redirect=no",
        "http://www.wiki-rennes.fr/index.php?title=CampOSV_Makers&redirect=no",
    ),
    (
        "http://www.themavision.fr/jcms/OP_8008/login?portal=OP_8008&redirect=http%3A%2F%2Fwww.themavision.fr%2Fwork%2FdisplayWork.jsp%3Fcid%3Drw_262625%26amp%3Bportal%3Dc_166385%26amp%3Bid%3Drw_502538&jsp=front%2Flogin.jsp",
        "http://www.themavision.fr/work/displayWork.jsp?cid=rw_262625&amp;portal=c_166385&amp;id=rw_502538",
    ),
    (
        "http://www.portailrh.org/_Externe.aspx?l=http%3a%2f%2fwww.ledevoir.com%2fsociete%2feducation%2f497900%2fune-reflexion-sur-l-employabilite-des-doctorants%3fp%3d668624&utm_source=Sociallymap&utm_medium=Sociallymap&utm_campaign=Sociallymap",
        "http://www.ledevoir.com/societe/education/497900/une-reflexion-sur-l-employabilite-des-doctorants?p=668624",
    ),
    (
        "http://mashable-com.cdn.ampproject.org/c/s/mashable.com/2018/08/10/deep-web-challenge-youtube-unboxing.amp",
        "https://mashable.com/2018/08/10/deep-web-challenge-youtube-unboxing.amp",
    ),
    (
        "http://mashable-com.cdn.ampproject.org/c/s/mashable.com/2018/08/10/deep-web-challenge-youtube-unboxing.amp?test#test",
        "https://mashable.com/2018/08/10/deep-web-challenge-youtube-unboxing.amp?test#test",
    ),
    (
        "https://www.google.com/url?sa=t&source=web&rct=j&url=https%3A%2F%2Fm.youtube.com%2Fwatch%3Fv%3D4iJBsjHMviQ&ved=2ahUKEwiBm-TO3OvkAhUnA2MBHQRPAR4QwqsBMAB6BAgDEAQ&usg=AOvVaw0i7y2_fEy3nwwdIZyo_qug",
        "https://m.youtube.com/watch?v=4iJBsjHMviQ",
    ),
    (
        "https://www.youtube.com/attribution_link?a=bWdZjuszr4I&u=%2Fwatch%3Fv%3Df5ZJLklAIQc%26feature%3Dshare",
        "https://www.youtube.com/watch?v=f5ZJLklAIQc&feature=share",
    ),
    (
        "http://cdn.ampproject.org/c/s/bc.marfeel.com/www.capital.fr/carriere-management/actualites/l-ecole-42-de-xavier-niel-classee-meilleure-ecole-de-code-au-monde-1199824?marfeeltn=amp",
        "https://www.capital.fr/carriere-management/actualites/l-ecole-42-de-xavier-niel-classee-meilleure-ecole-de-code-au-monde-1199824?marfeeltn=amp",
    ),
    (
        "http://bc-marfeelcache-com.cdn.ampproject.org/c/s/bc.marfeelcache.com/amp/positivr.fr/grenoble-interdit-panneaux-publicitaires/",
        "https://positivr.fr/grenoble-interdit-panneaux-publicitaires/",
    ),
    # Recursive case
    (
        "https://test.com?url=http%3A%2F%2Flemonde.fr%3Fnext%3Dhttp%253A%252F%252Ftarget.fr",
        "http://target.fr",
    ),
    # Degenerate loop case
    ("http://lemonde.fr?url=http%3A%2F%2Flemonde.fr", "http://lemonde.fr"),
    # google.com/url case
    (
        "http://www.google.com/url?q=http://www.unwomen.org/es/digital-library/publications/2014/8/modelo-de-protocolo-latinoamericano&sa=D&sntz=1&usg=AFQjCNHAbpLxShgtUW-gsJa0TCxfK8GZ_g",
        "http://www.unwomen.org/es/digital-library/publications/2014/8/modelo-de-protocolo-latinoamericano",
    ),
    (
        "https://www.google.com/url?q=https%3A%2F%2Fwww.facebook.com%2Fgroups%2F58383368963%2F&sa=D&sntz=1&usg=AFQjCNFEV50Fn9Peac6rDCzX4qbcpWdrrA",
        "https://www.facebook.com/groups/58383368963/",
    ),
    (
        "https://www.google.fr/url?q=https://www.medisite.fr/coronavirus-vaccin-pfizer-un-americain-de-13-ans-meurt-dans-son-sommeil-apres-la-seconde-dose.5620367.806703.html%253fv=amp",
        "https://www.medisite.fr/coronavirus-vaccin-pfizer-un-americain-de-13-ans-meurt-dans-son-sommeil-apres-la-seconde-dose.5620367.806703.html%3fv=amp",
    ),
    (
        "https://www.google.es/url?q=https://www.lavanguardia.com/politica/elecciones-catalanas/20121024/54353836096/elecciones-catalanas-53-catalanes-a-favor-independencia-referendum.html%253ffacet=amp",
        "https://www.lavanguardia.com/politica/elecciones-catalanas/20121024/54353836096/elecciones-catalanas-53-catalanes-a-favor-independencia-referendum.html%3ffacet=amp",
    ),
    # Empty redirections
    (
        "https://www-lesechos-fr.cdn.ampproject.org/v/",
        "https://www-lesechos-fr.cdn.ampproject.org/v/",
    ),
    (
        "https://www-bbc-com.cdn.ampproject.org/v/s/",
        "https://www-bbc-com.cdn.ampproject.org/v/s/",
    ),
    (
        "https://www.dpbolvw.net/click-8187505-15219391?url=https://",
        "https://www.dpbolvw.net/click-8187505-15219391?url=https://",
    ),
]


class TestInferRedirection(object):
    def test_basics(self):
        for url, redirected in TESTS:
            assert infer_redirection(url) == redirected

    def test_nonrecursive(self):
        target = infer_redirection(
            "https://test.com?url=http%3A%2F%2Flemonde.fr%3Fnext%3Dhttp%253A%252F%252Ftarget.fr",
            recursive=False,
        )

        assert target == "http://lemonde.fr?next=http%3A%2F%2Ftarget.fr"
