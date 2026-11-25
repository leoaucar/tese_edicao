r"""Exporta itens da biblioteca PESSOAL do Zotero para BibTeX a partir de uma copia do zotero.sqlite.
Uso: cp ~/Zotero/zotero.sqlite /tmp/z.sqlite; python3 zotero_bib_export.py /tmp/z.sqlite CHAVE1 CHAVE2 ... > novo.bib
Chave de citacao no padrao nativo do Zotero (sobrenome_primeirapalavra_ano, sem stopwords inglesas).
Nao escapa & nos campos: rodar  sed -i "/url = /!s/\([^\\\\]\)&/\1\\\\\&/g" novo.bib  depois. Criado em 2026-11-25 (cap. 2)."""
import sqlite3, sys, re, unicodedata
c = sqlite3.connect(sys.argv[1]); keys = sys.argv[2:]
STOP = {'a','an','the','some','from','on','in','of','and','or','to','for','with','by','at'}
TYPES = {'book':'book','bookSection':'incollection','journalArticle':'article','thesis':'phdthesis','report':'techreport'}
FMAP = [('title','title'),('publicationTitle','journal'),('bookTitle','booktitle'),('volume','volume'),('issue','number'),
        ('pages','pages'),('edition','edition'),('publisher','publisher'),('place','address'),('DOI','doi'),('ISBN','isbn'),
        ('ISSN','issn'),('url','url'),('language','language'),('series','series')]
def ascii(s): return unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower()
def fields(iid):
    return dict(c.execute("""select f.fieldName, v.value from itemData d join fields f using(fieldID)
        join itemDataValues v using(valueID) where d.itemID=?""",(iid,)))
for k in keys:
    iid, typ = c.execute("select itemID, t.typeName from items i join itemTypes t using(itemTypeID) where key=? and libraryID=1",(k,)).fetchone()
    f = fields(iid)
    cr = c.execute("""select cr.lastName, cr.firstName, ct.creatorType from itemCreators ic join creators cr using(creatorID)
        join creatorTypes ct using(creatorTypeID) where ic.itemID=? order by orderIndex""",(iid,)).fetchall()
    au = [(l,fn) for l,fn,t in cr if t=='author']; ed = [(l,fn) for l,fn,t in cr if t=='editor']
    year = f.get('date','')[:4]
    words = [w for w in re.findall(r"[\w'-]+", ascii(f.get('title',''))) if w not in STOP]
    key = f"{re.sub(r'[^a-z]','',ascii((au or ed)[0][0]))}_{re.sub(r'[^a-z0-9]','',words[0]) if words else ''}_{year}"
    out = [f"@{TYPES.get(typ,'misc')}{{{key},"]
    for zf,bf in FMAP:
        if f.get(zf): out.append(f"\t{bf} = {{{f[zf]}}},")
    if au: out.append("\tauthor = {" + " and ".join(f"{l}, {fn}".strip(', ') for l,fn in au) + "},")
    if ed: out.append("\teditor = {" + " and ".join(f"{l}, {fn}".strip(', ') for l,fn in ed) + "},")
    out.append(f"\tyear = {{{year}}},\n\tnote = {{Zotero {k}}},\n}}\n")
    print("\n".join(out))
