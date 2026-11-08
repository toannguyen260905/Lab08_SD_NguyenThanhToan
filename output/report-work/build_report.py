from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from copy import deepcopy
import hashlib, json

ROOT=Path(__file__).parent
REF=Path(r'C:\Users\Windows\.codex\skills\artifact-template-bao-cao-nhom-sinh-vien\assets\reference.docx')
OUT=ROOT.parent/'Bao_cao_ca_nhan_bai_6_15_den_6_18.docx'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ns={'w':W}
def tag(x): return '{'+W+'}'+x
with ZipFile(REF) as z:
    parts={i.filename:z.read(i.filename) for i in z.infolist()}
    infos=z.infolist()
root=E.fromstring(parts['word/document.xml'])
body=root.find('w:body',ns)
ps=body.findall('w:p',ns)
inventory={k:{'size':len(v),'sha256':hashlib.sha256(v).hexdigest()} for k,v in parts.items()}
(ROOT/'package-inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
contract=f'''# Template contract
Reference: {REF}
SHA256: {hashlib.sha256(REF.read_bytes()).hexdigest()}
Reference rendered using native Word PDF export because packaged renderer failed: soffice.exe absent. Six pages visually inspected.
One section, portrait Letter 8.5 x 11 inches. Margins top/bottom 1 inch, left/right 0.75 inch. Preserve sectPr byte equivalent, all headers/footers, first page border, logo, ornament, styles and numbering.
Cover slots: word/document.xml body paragraphs 6 Title, 7 author, 9 subject, 10 exercise and report type, 17 location/year. Preserve pPr and first rPr while replacing text. Author and location blank because not supplied.
Body slot: paragraphs 22 onward replaced; retain source cover paragraphs 0 to 21 including page break. Two body pages using existing Heading1 and Normal paragraph properties, TNR 13 body, 14 bold heading, Consolas 10 code. Explicit page break before exercise 6.17.
All ZIP parts preserve-only except word/document.xml and docProps/core.xml (clear old personal metadata). Old body figure intentionally removed from flow; media parts retained untouched. No tables, new relationships or fields. Source footer PAGE field preserved.
Package inventory: package-inventory.json. Output final must retain all other parts byte-for-byte. All cover content unrelated to source example replaced. Content concise individual student voice, no invented test results.
'''
(ROOT/'artifact.md').write_text(contract,encoding='utf-8')
def replace(p,text):
    rp=p.find('w:r/w:rPr',ns)
    for c in list(p):
        if c.tag!=tag('pPr'): p.remove(c)
    r=E.SubElement(p,tag('r'))
    if rp is not None:r.append(deepcopy(rp))
    for i,line in enumerate(text.split('\n')):
        if i:E.SubElement(r,tag('br'))
        E.SubElement(r,tag('t')).text=line
replace(ps[6],'BÁO CÁO BÀI TẬP CHƯƠNG 6')
replace(ps[7],'Họ và tên: ..................................    MSSV: ....................')
replace(ps[9],'MẪU THIẾT KẾ COMMAND\nTHỰC HIỆN UNDO VÀ REDO')
replace(ps[10],'Bài 6.15 đến 6.18  |  Báo cáo cá nhân')
replace(ps[17],'...................., 2026')
normal=deepcopy(ps[23].find('w:pPr',ns))
heading=deepcopy(ps[22].find('w:pPr',ns))
for c in list(body)[list(body).index(ps[22]):]:
    if c.tag!=tag('sectPr'):body.remove(c)
def para(text,kind='body',page=False):
    p=E.Element(tag('p')); pp=deepcopy(heading if kind=='heading' else normal)
    if pp is None:pp=E.Element(tag('pPr'))
    for k in ['pageBreakBefore','keepNext']:
        for e in pp.findall('w:'+k,ns):pp.remove(e)
    if page:E.SubElement(pp,tag('pageBreakBefore'))
    if kind=='heading':E.SubElement(pp,tag('keepNext'))
    sp=pp.find('w:spacing',ns)
    if sp is None:sp=E.SubElement(pp,tag('spacing'))
    sp.set(tag('before'),'120' if kind=='heading' else '0');sp.set(tag('after'),'80')
    sp.set(tag('line'),'240');sp.set(tag('lineRule'),'auto')
    if kind=='code':
        ind=pp.find('w:ind',ns)
        if ind is not None:pp.remove(ind)
        jc=pp.find('w:jc',ns)
        if jc is None:jc=E.SubElement(pp,tag('jc'))
        jc.set(tag('val'),'left')
    p.append(pp)
    r=E.SubElement(p,tag('r'));rp=E.SubElement(r,tag('rPr'))
    f=E.SubElement(rp,tag('rFonts'))
    for x in ['ascii','hAnsi','eastAsia','cs']:f.set(tag(x),'Consolas' if kind=='code' else 'Times New Roman')
    E.SubElement(rp,tag('sz')).set(tag('val'),'20' if kind=='code' else ('28' if kind=='heading' else '26'))
    E.SubElement(rp,tag('color')).set(tag('val'),'000000')
    if kind=='heading':E.SubElement(rp,tag('b'))
    for i,line in enumerate(text.split('\n')):
        if i:E.SubElement(r,tag('br'))
        t=E.SubElement(r,tag('t'));t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=line
    body.insert(len(body)-1,p)

para('Phạm vi báo cáo','heading')
para('Trong các bài 6.15–6.18, em trình bày cách mở rộng chương trình quản lý lịch biểu diễn bằng mẫu Command. Hướng giải quyết là lưu trạng thái trước mỗi thao tác, quản lý lịch sử bằng stack và đưa chức năng undo, redo vào Program. Các ví dụ dưới đây minh họa phương pháp và kết quả dự kiến.')
para('1 Bài 6.15 Bổ sung undo cho command','heading')
para('Yêu cầu là hoàn tác các thao tác thêm show, xóa show và xóa toàn bộ lịch của bài 6.14. Em bổ sung undo() vào interface Command, giữ execute() và tạo các command bằng anonymous class trong Commands.')
para('Trước khi execute(), command add và remove lưu show cũ của ngày được chọn qua Program.get(). Command clear lưu đủ bảy ngày vào EnumMap<Day, Show>. Khi undo(), dữ liệu đã lưu được đưa trở lại lịch. Việc sao chép Show giúp trạng thái cũ không bị dùng chung ngoài ý muốn.')
para('add1.execute(); add2.execute();\nremove.execute(); clear.execute();\nclear.undo(); remove.undo();\nadd2.undo(); add1.undo();','code')
para('Ví dụ, thêm Movie 1 vào thứ Hai, thêm Movie 2 vào thứ Ba, xóa thứ Hai rồi xóa toàn bộ lịch. Undo clear dự kiến khôi phục Movie 2; undo remove khôi phục thêm Movie 1. Hai lần undo tiếp theo đưa lịch về trạng thái ban đầu. Cần lưu và so sánh lịch sau từng bước để phát hiện lỗi, thay vì chỉ kiểm tra chương trình không báo lỗi.')
para('Nếu chỉ xóa dữ liệu mà không lưu trạng thái trước đó, chương trình không biết show nào cần khôi phục. Với một vài thao tác, client có thể tự giữ dữ liệu cũ, nhưng cách này dễ lặp code khi bổ sung chức năng.')
para('2 Bài 6.16 Quản lý lịch sử bằng CommandProcessor','heading')
para('Em tạo CommandProcessor với một Deque<Command> dùng như stack. execute(command) gọi command.execute() rồi push command vào stack. undoLast() lấy command gần nhất, gọi undo() và chỉ bỏ nó khỏi lịch sử sau khi hoàn tác thành công. Nếu stack rỗng thì không thực hiện gì.')
para('processor.execute(Commands.add(program, movie, Day.MONDAY));\nprocessor.undoLast();','code')
para('Client chỉ yêu cầu processor thực thi hoặc hoàn tác, không lấy stack ra để tự xử lý. Cách này tuân thủ Law of Demeter vì client không cần biết cấu trúc lịch sử bên trong. Nếu chưa có processor, client phải tự nhớ các command và gọi undo theo đúng thứ tự ngược như bài 6.15.')

para('3 Bài 6.17 Bổ sung redo','heading',page=True)
para('Em thêm redoStack để chứa các command đã được hoàn tác. Khi undo thành công, command được chuyển từ undoStack sang redoStack. Khi redo, processor gọi lại execute() của command ở đầu redoStack rồi chuyển command về undoStack.')
para('processor.undoLast(); // Chuyen command sang redoStack\nprocessor.redoLast(); // Thuc hien lai command vua undo','code')
para('Ví dụ, sau khi thêm Movie 1 vào thứ Hai, undo dự kiến đưa ngày này về trạng thái cũ; redo thêm Movie 1 trở lại. Nếu người dùng undo rồi thêm Movie 3 vào thứ Tư, execute() phải xóa redoStack vì lịch đã chuyển sang một nhánh thao tác mới.')
para('Không gọi processor.execute() bên trong redoLast(), vì hàm đó xóa toàn bộ redoStack và làm mất các thao tác còn có thể redo. Với stack rỗng, redoLast() không thay đổi lịch. Nếu chỉ giữ undoStack, chương trình có thể hoàn tác nhưng không còn command để thực hiện lại.')
para('4 Bài 6.18 Đóng gói processor trong Program','heading')
para('Em đặt một CommandProcessor ở bên trong Program. Các hàm public add(), remove() và clear() tạo command rồi nhờ processor thực thi. Hai hàm undoLast() và redoLast() cũng ủy quyền cho processor. Nhờ đó, client thao tác trực tiếp với Program mà không phải tạo command.')
para('Program program = new Program();\nprogram.add(new Movie("Movie 1", 2017, 120), Day.MONDAY);\nprogram.remove(Day.MONDAY);\nprogram.undoLast(); // Du kien khoi phuc Movie 1\nprogram.redoLast(); // Du kien xoa Movie 1 lan nua','code')
para('Để tránh gọi lặp vô hạn, em tách addDirect(), removeDirect() và clearDirect() thành các hàm nội bộ không ghi lịch sử. Command gọi các hàm này trong execute() và undo(), không gọi lại các hàm public. Constructor cũng dùng clearDirect() để việc khởi tạo lịch không trở thành một thao tác có thể undo.')
para('Program chịu trách nhiệm quản lý lịch; CommandProcessor quản lý hai stack; mỗi command lưu trạng thái cần khôi phục. Việc chia trách nhiệm giúp Program không trở thành God class. Nếu Program tự quản lý cả dữ liệu lẫn hai stack, lớp sẽ khó đọc và khó sửa hơn khi lịch sử thao tác thay đổi.')
para('5 Nhận xét','heading')
para('Qua bốn bài, em hiểu rằng undo cần dữ liệu cũ, còn undo nhiều bước cần một nơi quản lý thứ tự thao tác. Hai stack giúp bổ sung redo và việc ủy quyền giữ cho Program gọn hơn. Khi kiểm tra, cần xét thêm lịch sử rỗng, ghi đè show đã có và thao tác mới sau undo. Cách này lưu lịch sử trong bộ nhớ nên chưa duy trì được lịch sử sau khi đóng chương trình.')
para('Tài liệu tham khảo: Martin P. Robillard, DesignBook, Chapter 6 Practice Exercises, bài 15–18.\nhttps://github.com/prmr/DesignBook/blob/master/exercises/e-chapter6.md')
parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
if 'docProps/core.xml' in parts:
    cr=E.fromstring(parts['docProps/core.xml'])
    for e in cr:
        if E.QName(e).localname in ['creator','lastModifiedBy','title','subject','description']:e.text=''
    parts['docProps/core.xml']=E.tostring(cr,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(OUT,'w') as z:
    for info in infos:z.writestr(info,parts[info.filename])
with ZipFile(OUT) as z:
    changed=[k for k,v in inventory.items() if hashlib.sha256(z.read(k)).hexdigest()!=v['sha256']]
assert set(changed)<= {'word/document.xml','docProps/core.xml'},changed
assert hashlib.sha256(REF.read_bytes()).hexdigest() in contract
print(OUT)
print('Changed parts:',changed)
