# -*- coding: utf-8 -*-
# =============================================================================
# Ural Shortened Url Testing Function
# =============================================================================
#
# Function testing whether the given url is probably a shortened url or not.
#
from ural.tries import HostnameTrieSet
from ural.is_homepage import is_homepage

# Some domains taken from: https://github.com/timleland/url-shorteners
SHORTENER_DOMAINS = ['0rz.tw', '1-url.net', '126.am', '1link.in', '1tk.us', '1un.fr', '1url.com', '1url.cz', '1wb2.net', '2.gp', '2.ht', '23o.net', '2ad.in', '2big.at', '2doc.net', '2fear.com', '2long.cc', '2no.co', '2pl.us', '2tu.us', '2ty.in', '2u.xf.cz', '2ya.com', '3.ly', '307.to', '3ra.be', '3x.si', '4i.ae', '4ms.me', '4sq.com', '4url.cc', '4view.me', '5em.cz', '5url.net', '5z8.info', '6fr.ru', '6g6.eu', '6url.com', '7.ly', '76.gd', '77.ai', '7fth.cc', '7li.in', '7vd.cn', '8u.cz', '944.la', '98.to', 'app.link', 'AltURL.com', 'BudURL.com', 'Buff.ly', 'BurnURL.com', 'C-O.IN', 'ClickMeter.com', 'DecentURL.com', 'DigBig.com', 'Digg.com', 'DwarfURL.com', 'EasyURI.com', 'EasyURL.net', 'EasyURL.com', 'Fhurl.com', 'Fly2.ws', 'GoWat.ch', 'Hurl.it', 'IsCool.net', 'Just.as', 'L9.fr', 'Lvvk.com', 'MyURL.in', 'PiURL.com', 'Profile.to', 'QLNK.net', 'Quip-Art.com', 'RedirX.com', 'Sharein.com', 'ShortLinks.co.uk', 'Shrinkify.com', 'SimURL.com', 'StartURL.com', 'TightURL.com', 'Tnij.org', 'To8.cc', 'TraceURL.com', 'URL.ie', 'URLHawk.com', 'WapURL.co.uk', 'XeeURL.com', 'Yep.it', 'a.co', 'a.gg', 'a.nf', 'a0.fr', 'a2a.me', 'aa.cx', 'abbr.sk', 'abbrr.com', 'abcurl.net', 'abnb.me', 'ad-med.cz', 'ad.vu', 'ad5.eu', 'ad7.biz', 'adb.ug', 'adec.co', 'adf.ly', 'adfa.st', 'adfly.fr', 'adfoc.us', 'adjix.com', 'adli.pw', 'admy.link', 'adv.li', 'afx.cc', 'ajn.me', 'aka.gr', 'al.ly', 'alil.in', 'amn.st', 'any.gs', 'apne.ws', 'aqva.pl', 'ar.gy', 'ares.tl', 'arst.ch', 'asso.in', 'atu.ca', 'au.ms', 'ayt.fr', 'azali.fr', 'azc.cc', 'b00.fr', 'b23.ru', 'b2l.me', 'b54.in', 'bacn.me', 'baid.us', 'bc.vc', 'bcool.bz', 'bddy.me', 'bee4.biz', 'bim.im', 'binged.it', 'bit.do', 'bit.ly', 'bitly.com', 'bitly.ws', 'bitw.in', 'bizj.us', 'bkite.com', 'blap.net', 'ble.pl', 'blip.tv', 'bloat.me', 'bnc.lt', 'boi.re', 'bote.me', 'bougn.at', 'br4.in', 'bravo.ly', 'bre.is', 'brk.to', 'brzu.net', 'bsa.ly', 'buff.ly', 'buk.me', 'bul.lu', 'bxl.me', 'bzh.me', 'cachor.ro', 'canurl.com', 'captur.in', 'catchylink.com', 'cbs.so', 'cbug.cc', 'cc.cc', 'ccj.im', 'cf.ly', 'cf2.me', 'cf6.co', 'chilp.it', 'chl.li,', 'chzb.gr', 'cjb.net', 'cl.lk', 'cl.ly', 'clck.ru', 'cleanuri.com', 'cli.gs', 'cliccami.info', 'clickmetertracking.com', 'clickthru.ca', 'clikk.in', 'clop.in', 'cmpdnt.cc', 'cn86.org', 'cnhv.co', 'coinurl.com', 'conta.cc', 'cort.as', 'cot.ag', 'couic.fr', 'cr.tl', 'crks.me', 'crwd.fr', 'ctvr.us', 'cudder.it', 'cur.lv', 'curl.im', 'cut.ci', 'cut.pe', 'cut.sk', 'cutt.eu', 'cutt.ly', 'cutt.us', 'cutu.me', 'cuturl.com', 'cybr.fr', 'cyonix.to', 'd75.eu', 'daa.pl', 'dai.ly', 'dd.ma', 'ddp.net', 'dfl8.me', 'dft.ba', 'disq.us', 'dld.bz', 'dlvr.it', 'do.my', 'doiop.com', 'dolp.cc', 'dopen.us', 'dopice.sk', 'droid.ws', 'dv.gd', 'dy.fi', 'dyo.gs', 'e37.eu', 'ebx.sh', 'ecra.se', 'ed.gr', 'eepurl.com', 'ely.re', 'erax.cz', 'erw.cz', 'eweri.com', 'ewerl.com', 'ex9.co', 'ezurl.cc', 'fa.b', 'fa.by', 'fal.cn', 'fav.me', 'fb.me', 'fbshare.me', 'fcld.ly', 'feedproxy.google.com', 'ff.im', 'fff.re', 'fff.to', 'fff.wf', 'filz.fr', 'fire.to', 'firsturl.de', 'firsturl.net', 'flic.kr', 'flip.it', 'flq.us', 'fnk.es', 'foe.hn', 'folu.me', 'fon.gs', 'frama.link', 'freak.to', 'freze.it', 'from.ubs', 'fur.ly', 'fuseurl.com', 'fuzzy.to', 'fw.to', 'fwd4.me', 'fwib.net', 'g.ro.lt', 'g00.me', 'g2g.to', 'gerd.fm', 'gg.gg', 'git.io', 'gizmo.do', 'gl.am', 'go.9nl.com', 'go.ign.com', 'go.shr.lc', 'go.usa.gov', 'go2.me', 'go2cut.com', 'goo.gl', 'goo.lu', 'good.ly', 'goog.le', 'goshrink.com', 'gotrim.me', 'grabify.link', 'grem.io', 'gri.ms', 'guiama.is', 'gurl.es', 'hadej.co', 'hec.su', 'hellotxt.com', 'hex.io', 'hide.my', 'hiderefer.com', 'hjkl.fr', 'hmm.ph', 'hops.me', 'hover.com', 'href.in', 'href.li', 'hsblinks.com', 'ht.ly', 'httpslink.com', 'htxt.it', 'hubs.li', 'hubs.ly', 'huff.to', 'hugeurl.com', 'hulu.com', 'hurl.me', 'hurl.ws', 'i-2.co', 'i99.cz', 'ibit.ly', 'icanhaz.com', 'icit.fr', 'ick.li', 'icks.ro', 'idek.net', 'ift.tt', 'iiiii.in', 'iky.fr', 'ilix.in', 'info.ms', 'ino.to', 'inreply.to', 'io.webhelp.com', 'is.gd', 'isra.li', 'isra.liiterasi.net', 'itm.im', 'its.my', 'ity.im', 'ix.lt', 'ix.sk', 'j.gs', 'j.mp', 'jdem.cz', 'jieb.be', 'jijr.com', 'jmp2.net', 'jp22.net', 'jpeg.ly', 'jqw.de', 'kask.us', 'kd2.org', 'kfd.pl', 'kissa.be', 'kl.am', 'klck.me', 'korta.nu', 'kr3w.de', 'krat.si', 'kratsi.cz', 'krod.cz', 'krunchd.com', 'kuc.cz', 'kxb.me', 'l-k.be', 'l.gg', 'l9k.net', 'lat.ms', 'lc-s.co', 'lc.cx', 'lcut.in', 'letop10.', 'lety.io', 'libero.it', 'lick.my', 'lien.li', 'lien.pl', 'lifehac.kr', 'liip.to', 'liltext.com', 'lin.cr', 'lin.io', 'linkbee.com', 'linkbun.ch', 'linkn.co', 'liurl.cn', 'llu.ch', 'lmde.fr', 'ln-s.net', 'ln-s.ru', 'lnk.co', 'lnk.gd', 'lnk.in', 'lnk.ly', 'lnk.ms', 'lnk.sk', 'lnkd.in', 'lnked.in', 'lnki.nl', 'lnkiy.com,', 'lnks.fr', 'lnkurl.com', 'lnky.fr', 'lnp.sn', 'loom.ly', 'loopt.us', 'lp25.fr', 'lru.jp', 'lt.tl', 'lurl.no', 'lynk.my', 'm1p.fr', 'm3mi.com', 'macte.ch', 'make.my', 'mash.to', 'mcaf.ee', 'mdl29.net', 'merky.de', 'metamark.net', 'mic.fr', 'migre.me', 'minilien.com', 'miniurl.be', 'miniurl.com', 'minu.me', 'minurl.fr', 'mke.me', 'moby.to', 'mon.actu.io', 'moourl.com', 'more.sh', 'mrte.ch', 'msft.social', 'mtr.cool', 'mut.lu', 'myloc.me', 'my.sociabble.com', 'myurl.in', 'n.pr', 'n9.cl', 'nbc.co', 'nblo.gs', 'ne1.net', 'net.ms', 'net46.net', 'nicou.ch', 'nig.gr', 'njx.me', 'nn.nf', 'non.li', 'not.my', 'notlong.com', 'nov.io', 'nq.st', 'nsfw.in', 'nutshellurl.com', 'nxy.in', 'nyti.ms', 'o-x.fr', 'oc1.us', 'okok.fr', 'om.ly', 'omf.gd', 'omoikane.net', 'on.cnn.com', 'on.mktw.net', 'onforb.es', 'orz.se', 'ou.af', 'ou.gd', 'oua.be', 'ouo.io', 'ow.ly', 'owl.li', 'p.pw', 'para.pt', 'parky.tv', 'past.is', 'pd.am', 'pdh.co', 'ph.dog', 'ph.ly', 'pic.gd', 'pich.in', 'pin.st', 'ping.fm', 'pli.gs', 'plots.fr', 'pnt.me', 'po.st', 'politi.co', 'poprl.com', 'post.ly', 'posted.at', 'pp.gg', 'ppfr.it', 'ppst.me', 'ppt.cc', 'ppt.li', 'prejit.cz', 'ptab.it', 'ptiturl.com', 'ptm.ro', 'pub.vitrue.com', 'pw2.ro', 'py6.ru', 'q.gs', 'qbn.ru', 'qicute.com', 'qqc.co', 'qr.net', 'qrtag.fr', 'qte.me', 'qu.tc', 'qxp.cz', 'qxp.sk', 'qy.fi', 'r.im', 'rb.gy', 'rb6.co', 'rb6.me', 'rcknr.io', 'rdz.me', 'read.bi', 'readthis.ca', 'reallytinyurl.com', 'rebrand.ly', 'rebrandlydomain.com', 'redir.ec', 'redir.fr', 'redirects.ca', 'redu.it', 'ref.so', 'reise.lc', 'rel.ink', 'relink.fr', 'retwt.me', 'reut.rs', 'ri.ms', 'rickroll.it', 'riz.cz', 'riz.gd', 'rod.gs', 'roflc.at', 'rsmonkey.com', 'rt.nu', 'rt.se', 'rt.tc', 'ru.ly', 'rubyurl.com', 'rurl.org', 'rww.tw', 's-url.fr', 's.id', 's4c.in', 's7y.us', 'safe.mn', 'sagyap.tk', 'sameurl.com', 'sco.lt', 'sdu.sk', 'sdut.us', 'seeme.at', 'segue.se', 'sh.st', 'shar.as', 'shar.es', 'sharetabs.com', 'shink.de', 'shorl.com', 'short.cc', 'short.ie', 'short.nr', 'short.pk', 'short.to', 'shorte.st', 'shortna.me', 'shorturl.at', 'shorturl.com', 'shoturl.us', 'shout.to', 'show.my', 'shrinkee.com', 'shrinkr.com', 'shrinkster.com', 'shrinkurl.in', 'shrt.fr', 'shrt.in', 'shrt.st', 'shrtco.de', 'shrten.com', 'shrunkin.com', 'shw.me', 'shy.si', 'sicax.net', 'sina.lt', 'sk.gy', 'skr.sk', 'skroc.pl', 'slate.me', 'smallr.com', 'smll.co', 'smsh.me', 'smurl.name', 'sn.im', 'sn.vc', 'snipr.com', 'snipurl.com', 'snsw.us', 'snurl.com', 'soc.fm', 'soo.gd', 'sp2.ro', 'spedr.com', 'spn.sr', 'spr.ly', 'sptfy.com', 'sq6.ru', 'sqrl.it', 'srnk.net', 'srs.li', 'ssl.gs', 'sturly.com', 'su.pr', 'surl.co.uk', 'surl.hu', 'surl.me', 'sux.cz', 'swll.to', 'sy.pe', 't.cn', 't.co', 't.lh.com', 't.ly', 't2m.io', 'ta.gd', 'tabzi.com', 'tau.pe', 'tbd.ly', 'tcrn.ch', 'tdjt.cz', 'tgr.me', 'tgr.ph', 'thesa.us', 'thinfi.com', 'thrdl.es', 'tin.li', 'tini.cc', 'tiniuri.com', 'tiny.cc', 'tiny.lt', 'tiny.ly', 'tiny.ms', 'tiny.one', 'tiny.pl', 'tiny123.com', 'tinyarro.ws', 'tinylink.in', 'tinytw.it', 'tinyuri.ca', 'tinyurl.com', 'tinyurl.hu', 'tinyvid.io', 'tixsu.com', 'tk.', 'tl.gd', 'tldr.sk', 'tldrify.com', 'tllg.net', 'tmblr.co', 'tmi.me', 'tnij.org', 'tnw.to', 'tny.com', 'tny.cz', 'tny.im', 'to.ly', 'togoto.us', 'tohle.de', 'totc.us', 'toysr.us', 'tpm.ly', 'tpmr.com', 'tr.im', 'tr.my', 'tr5.in', 'tra.kz', 'trck.me', 'trib.al', 'trick.ly', 'trkr.ws', 'trunc.it', 'turo.us', 'tweetburner.com', 'twet.fr', 'twhub.com', 'twi.im', 'twib.in', 'twirl.at', 'twit.ac', 'twitclicks.com', 'twitterpan.com', 'twitterurl.net', 'twitterurl.org', 'twitthis.com', 'twiturl.de', 'twlr.me', 'twurl.cc', 'twurl.nl', 'u.afp.com', 'u.mavrev.com', 'u.nu', 'u.to', 'u6e.de', 'u76.org', 'ub0.cc', 'uby.es', 'ucam.me', 'ug.cz', 'ulmt.in', 'ulu.lu', 'unlc.us', 'updating.me', 'upzat.com', 'ur1.ca', 'url.az', 'url.co.uk', 'url2.fr', 'url360.me', 'url4.eu', 'url5.org', 'urlao.com', 'urlborg.com', 'urlbrief.com', 'urlcover.com', 'urlcut.com', 'urlenco.de', 'urli.nl', 'urlin.it', 'urlkiss.com', 'urlkr.com', 'urlot.com', 'urlpire.com', 'urlr.me', 'urls.fr', 'urls.im', 'urlshorteningservicefortwitter.com', 'urlx.ie', 'urlx.org', 'urlz.fr', 'urlz.host', 'urlzen.com', 'urub.us', 'usat.ly', 'use.my', 'utfg.sk', 'v.gd', 'v.ht', 'v5.gd', 'vaaa.fr', 'valv.im', 'vaza.me', 'vb.ly', 'vbly.us', 'vd55.com', 'verd.in', 'vgn.am', 'vgn.me', 'viid.me', 'virl.com', 'vl.am', 'vm.lc', 'vov.li', 'vsll.eu', 'vt802.us', 'vu.fr', 'vur.me', 'vv.vg', 'w1p.fr', 'w3t.org', 'w55.de', 'waa.ai', 'wapo.st', 'wb1.eu', 'wclink.co', 'web99.eu', 'wed.li', 'wideo.fr', 'wipi.es', 'wow.link', 'wp.me', 'wrld.bg', 'wtc.la', 'wu.cz', 'ww7.fr', 'wwy.me', 'x.co', 'x.nu', 'x.se', 'x.vu', 'x10.mx', 'x2c.eu', 'x2c.eumx', 'xaddr.com', 'xav.cc', 'xfru.it', 'xgd.in', 'xib.me', 'xl8.eu', 'xoe.cz', 'xq.ms', 'xr.com', 'xrl.in', 'xrl.us', 'xt3.me', 'xua.me', 'xub.me', 'xurl.es', 'xurl.jp', 'xurls.co', 'xzb.cc', 'y.ahoo.it', 'y2u.be', 'yagoa.fr', 'yagoa.me', 'yatuc.com', 'yau.sh', 'ye.pe', 'yeca.eu', 'yect.com', 'yep.it', 'yfrog.com', 'yhoo.it', 'yiyd.com', 'yogh.me', 'yon.ir', 'youfap.me', 'youtu.be', 'ysear.ch', 'yuarel.com', 'yweb.com', 'yyv.co', 'z0p.de', 'z9.fr', 'zSMS.net', 'zapit.nu', 'zcu.io', 'zeek.ir', 'zi.ma', 'zi.mu', 'zi.pe', 'zip.net', 'zipmyurl.com', 'zkr.cz', 'zkrat.me', 'zkrt.cz', 'zoodl.com', 'zpag.es', 'zpr.io', 'zti.me', 'zubb.it', 'zud.me', 'zurl.io', 'zurl.ws', 'zws.im', 'zxq.net', 'zyva.org', 'zz.gd', 'zzang.kr', 'zzb.bz', '›.ws', '✩.ws', '✿.ws', '❥.ws', '➔.ws', '➞.ws', '➡.ws', '➨.ws', '➯.ws', '➹.ws', '➽.ws']

# NOTE: we use a trie to perform efficient queries and so we don't
# need to test every domain/subdomain linearly
TRIE = HostnameTrieSet()

for domain in SHORTENER_DOMAINS:
    TRIE.add(domain)


def is_shortened_url(url):
    if is_homepage(url) is True:
        return False
    return TRIE.match(url)

DOMAINS_TO_RESOLVE = ['doi.org', 'list-manage.com']

TRIE2 = HostnameTrieSet()

for domain in DOMAINS_TO_RESOLVE:
    TRIE2.add(domain)


def should_resolve(url):
    if is_homepage(url) is True:
        return False
    return TRIE2.match(url)
