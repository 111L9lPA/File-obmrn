"""Seed from known conversation facts; does not modify NC or infer cut approval."""
from pathlib import Path
import json,hashlib,re,subprocess,shutil
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'docs'
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
raw=f'https://raw.githubusercontent.com/111L9lPA/File-obmrn/{commit}/'
projects=[]
def project(id,title,subtitle,stock,material,parts,description,color):
 p=dict(id=id,title=title,subtitle=subtitle,stock=stock,material=material,parts=parts,description=description,color=color,zero='XY — нижний левый угол листа; Z — верх материала',operations=[],images=[])
 projects.append(p);return p
def image(p,source,title):
 src=Path(source);dst=OUT/'assets'/src.name;shutil.copyfile(src,dst)
 p['images'].append(dict(url='assets/'+src.name,title=title,sha256=hashlib.sha256(dst.read_bytes()).hexdigest()))
def op(p,name,title,tool,depth,order,version='v1',archived=False,note='',cut='not_reported',requires=None):
 b=(ROOT/name).read_bytes();sha=hashlib.sha256(b).hexdigest()
 # Read facts only from explicit S/F codes, not safety assumptions.
 text=b.decode('ascii');code=re.sub(r'\([^)]*\)','',text)
 f=sorted(set(float(x) for x in re.findall(r'F([\d.]+)',code)));s=sorted(set(float(x) for x in re.findall(r'S([\d.]+)',code)))
 p['operations'].append(dict(id=name.rsplit('.',1)[0],title=title,filename=name,url=raw+name,sha256=sha,bytes=len(b),tool=tool,depth=depth,order=order,version=version,archived=archived,feeds=f,rpm=s,cutStatus=cut,checkStatus='geometry_checked' if p['id'] in ['panels','bubishki','tabletop'] else 'not_reviewed',note=note,requires=requires or [],source='Файл репозитория и переписка с Толиком',revision=commit))
p=project('panels','Панель и полоса','2 детали из комплекта · лист 1220 × 2440',[1220,2440,22],'Материал как у бобышек, 22 мм',[{'size':[1150,2150],'count':1},{'size':[1150,200],'count':1}], 'На других листах остаются 2110 × 200 — 2 шт. и 1150 × 200 — 1 шт. Отступы 35 мм по бокам, 40 мм на концах.', 'green')
base='/workspace/shared/downloads/'
image(p,base+'43_LAYOUT_PANEL_AND_STRIP.png','Что помещается на лист и что остаётся')
image(p,base+'44_TWO_LONG_STRIPS_STOCK_450x2160.png','Кусок для двух оставшихся длинных полос — не траектория файла 41')
op(p,'40_TOP_SCREW_MARKS_D4_Z4_v1.nc','Отметки под саморезы сверху','D4 · кукуруза',4,1,note='Три углубления примерно Ø6: X60 / 610 / 1160, Y2420. Шпиндель остановить до установки саморезов.')
op(p,'42_EXTRA_MARKS_LEFT_RIGHT_BOTTOM_D4_Z4_v1.nc','Отметки слева, справа и снизу','D4 · кукуруза',4,2,note='Дополнительные точки X12 Y1220; X1208 Y1220; X610 Y20. Верхние точки не повторяет.')
op(p,'41_PANEL_AND_STRIP_D4_Z22p7_v1.nc','Вырезать полосу и большую панель','D4 · кукуруза',22.7,3,note='Сначала полоса, потом панель. Нужны закрепление, вакуум и проверка нулей. Головки с шайбами — в радиусе до 10 мм от отметок.',requires=['40_TOP_SCREW_MARKS_D4_Z4_v1','42_EXTRA_MARKS_LEFT_RIGHT_BOTTOM_D4_Z4_v1'])
p=project('bubishki','Бобышки','Малые детали · актуальная раскладка 22 + 16',[650,1125,22],'Материал 22 мм, точный тип не подтверждён',[{'size':[47.001,23.8],'count':22},{'size':[63.8,27.001],'count':16}], 'По два ряда каждого размера. Между пропилами остаётся 2 мм. Один экземпляр предыдущей v2 отработал нормально со слов Толика; новая раскладка этим не подтверждена.', 'blue')
op(p,'32_BUBISHKI_22small_16long_D4_WEB2_650x1125_v3.nc','22 малых и 16 длинных бобышек','D4 · кукуруза',22.5,1,'v3',note='Лист 650 × 1125. Отступ от готовых деталей не меньше 16 мм. Между готовыми деталями 10 мм, остаток между пропилами 2 мм.')
op(p,'31_BUBISHKI_20plus20_D4_GAP22_Z22p5_v2.nc','Прежняя раскладка: 20 + 20','D4 · кукуруза',22.5,1,'v2',True,'Старый лист 670 × 1110; промежуток 22 мм. Подтверждена только первая деталь, не весь файл.','partial_reported')
op(p,'30_BUBISHKI_8small_2long_D4_Z22p5_v1.nc','Первая раскладка: 8 + 2','D4 · кукуруза',22.5,1,'v1',True,'Старая раскладка и боковые входы. Лист 670 × 1110.')
p=project('tabletop','Столешница под акрил','903 × 1703 · выборка 803 × 1603',[1220,2440,22],'Фанера',[{'size':[903,1703],'count':1}], 'Актуальные размеры из поздней версии проекта: 903 × 1703, выборка 803 × 1603 глубиной 11, углы снаружи R10. Старые 902 × 1702 не подставлять.', 'sand')
image(p,ROOT/'TABLETOP_903x1703_v1.png','Схема комплекта столешницы v1; файл 12 заменён на v2 без смены размеров')
op(p,'10_BIG_D4_SCORE_IN_OUT_Z3_v1.nc','Предварительно надрезать контуры','D4 · кукуруза',3,1)
op(p,'11_BIG_D32_POCKET_803x1603_Z11_v1.nc','Выбрать середину','D32 · выборочная',11,2,note='После выполнения измерить глубину в нескольких местах. Не обнулять Z на дне.',requires=['10_BIG_D4_SCORE_IN_OUT_Z3_v1'])
op(p,'12_BIG_D4_CORNERS_WALLS_Z11_v2.nc','Дочистить углы и стенки','D4 · кукуруза',11,3,'v2',note='Только после выборки D32 и замера. Заменяет файл 12 v1; не запускать обе версии.',requires=['11_BIG_D32_POCKET_803x1603_Z11_v1'])
op(p,'13_BIG_D4_OUTER_903x1703_R10_Z22p5_v1.nc','Отделить столешницу по контуру','D4 · кукуруза',22.5,4,requires=['12_BIG_D4_CORNERS_WALLS_Z11_v2'])
op(p,'12_BIG_D4_CORNERS_WALLS_Z11_v1.nc','Дочистка углов — старая версия','D4 · кукуруза',11,3,'v1',True,'Заменён на v2. Не запускать обе версии подряд.')
p=project('dobory','Доборы 475 мм','5 полос · лист вдоль Y',[1250,2500,6],'Листовой материал 6 мм',[{'size':[1250,475],'count':5}], 'Актуальная ширина 475 мм. Сначала оба прохода одной линии, затем следующая. Торцы длиной 1250 определяются исходным листом.', 'blue')
image(p,ROOT/'20_DOBORY_475x1250_LAYOUT_v3.png','Раскладка доборов шириной 475 мм — версия v3')
op(p,'20_DOBORY_475x1250_D3p9_2PASS_v3.nc','Пять доборов шириной 475 мм','D3,9',6.5,1,'v3')
for name in ['20_DOBORY_X1250_Y2500_D3p9_2PASS_v2.nc','20_DOBORY_5x450x1250_D3p9_Z6p5_v1.nc']:
 op(p,name,'Прежняя ширина 450 мм','D3,9',6.5,1,'v2' if 'v2' in name else 'v1',True,'Ширина 450 устарела. Геометрия и ориентация листа могли отличаться.')
p=project('tests','Пробы и тесты','Маленькая выборка и пробный квадрат',None,'Разные заготовки',[], 'Архив отдельных проб. Это не последовательность запуска. Успех пробы не подтверждает новые большие программы.', 'sand')
p['sequence']=False;p['zero']='Проверить в описании конкретного файла; общий ноль для всех проб не задан'
op(p,'KVADRAT_TEST.nc','Пробный квадрат 50 × 50','D4 · кукуруза',.5,1,note='Отдельная проба. Проверь описание внутри NC и свободную зону.')
op(p,'02_TEST_POCKET_200x100_D32_Z11_v1.nc','Маленькая выборка D32','D32 · выборочная',11,2,note='Толик сообщил об удачной пробе. Точная связь запуска с байтами файла не подтверждена.',cut='partial_reported')
op(p,'03_TEST_POCKET_200x100_D4_Z11_v1.nc','Дочистка маленькой выборки D4','D4 · кукуруза',11,3,note='Только внутри уже выбранной середины. НЕ программа надреза цельной фанеры.')
catalog=dict(schemaVersion=1,revision=1,updatedAt='2026-11-07',repository='111L9lPA/File-obmrn',projects=projects)
(OUT/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
# Accurate current bubishki top-view illustration, not the obsolete v1 image.
rects=[]
for w,h,y,n in [(47.001,23.8,16,11),(63.8,27.001,83.6,8)]:
 for row in range(2):
  for col in range(n):rects.append(f'<rect x="{16+col*(w+10)}" y="{160-(y+row*(h+10)+h)}" width="{w}" height="{h}" rx="2"/>')
svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 220"><rect width="650" height="220" fill="#e1eafa"/><g fill="#90b4d8" stroke="#3c6286">'+''.join(rects)+'</g><text x="20" y="195" font-size="17" font-family="sans-serif" fill="#294b71">22 малых + 16 длинных • схема расположения</text></svg>'
(OUT/'assets/bubishki.svg').write_text(svg)
for p in projects:
 if p['id']=='bubishki':p['images']=[dict(url='assets/bubishki.svg',title='Текущая раскладка v3 — схема нижнего участка листа',sha256=hashlib.sha256(svg.encode()).hexdigest())]
(OUT/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
print(len(projects),'projects;',sum(len(p['operations']) for p in projects),'programs')
