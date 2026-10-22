from pathlib import Path
import re
p=Path("RuangUsahaAndroid/app/src/main/assets/index.html")
s=p.read_text()
if "RuangUsaha feature upgrade v3" in s: raise SystemExit("Already applied")
s=s.replace("</style>", """
/* RuangUsaha feature upgrade v3 */
#page-dashboard .cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}
#page-dashboard .cards .card:nth-child(4){grid-column:1/-1;order:-1;background:linear-gradient(120deg,#133c43,#167c70);color:white;border:0}
#page-dashboard .cards .card:nth-child(4) .metric-label{color:#d0ece8}
#page-dashboard .cards .card:nth-child(4) .metric{font-size:clamp(28px,7vw,38px);color:white}
#page-dashboard .cards .card:nth-child(3){grid-column:1/-1;display:flex;justify-content:space-between;align-items:center}
#page-dashboard .cards .card:nth-child(3) .metric{margin:0}
.picker-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.picker-card{display:flex;align-items:center;gap:10px;text-align:left;background:#fff;border:1px solid #e9edf4;border-radius:15px;padding:13px;min-width:0}.picker-card strong{display:block;font-size:13px;overflow-wrap:anywhere}.picker-card small{display:block;color:var(--muted);font-size:11px;margin-top:3px}.picker-icon{width:38px;height:38px;display:grid;place-items:center;flex:0 0 38px;border-radius:12px;background:#e2f8f2;color:#147b69;font-size:20px}
.sale-row{display:grid;grid-template-columns:minmax(0,1fr) 60px 85px 28px;gap:6px;align-items:end;border:1px solid var(--line);border-radius:13px;padding:8px;margin-bottom:8px}.sale-row .field label{font-size:10px}.sale-row .field input,.sale-row .field select{padding:8px 5px;font-size:12px}
@media(max-width:700px){.picker-grid{grid-template-columns:1fr}.sale-row{grid-template-columns:minmax(0,1fr) 54px 76px 25px;gap:4px;padding:6px}.modal-backdrop{padding:0;align-items:flex-end}.modal{width:100%;max-height:94dvh;border-radius:20px 20px 0 0;padding:17px}.modal-head{position:sticky;top:-17px;background:white;padding:5px 0 12px;z-index:1}.form-actions{position:sticky;bottom:-17px;background:#fff;padding:12px 0 max(8px,env(safe-area-inset-bottom));z-index:1}}
</style>""",1)
anchor='<div class="account-list" id="businessesList" style="margin-top:14px"></div></div>'
rep='<div class="account-list" id="businessesList" style="margin-top:14px"></div><div class="panel-head" style="margin-top:22px"><div><h2>Produk tiap usaha</h2><div class="desc">Daftarkan foto, alarm, barang, atau jasa beserta harga jual.</div></div><button class="primary" onclick="openProduct()">＋ Tambah produk</button></div><div class="filters"><select id="productBusinessFilter"><option value="">Semua usaha</option></select></div><div class="account-list" id="productsList"></div></div>'
if anchor not in s: raise SystemExit("business list anchor missing")
s=s.replace(anchor,rep,1)
picker='<div class="modal-backdrop" id="businessPickerModal"><div class="modal"><div class="modal-head"><div><h2>Pilih usaha</h2><div class="desc">Pilih usaha sebelum mengisi data transaksi.</div></div><button onclick="closeModal(\'businessPickerModal\')">✕</button></div><div id="businessPickerCards" class="picker-grid"></div><button style="width:100%;margin-top:12px" onclick="chooseBusiness(\'__general__\')">Operasional umum / belum dipisah</button></div></div>'
productmodal='<div class="modal-backdrop" id="productModal"><div class="modal"><div class="modal-head"><h2 id="productModalTitle">Tambah produk</h2><button onclick="closeModal(\'productModal\')">✕</button></div><form id="productForm"><input type="hidden" id="productId"><div class="form-grid"><div class="field wide"><label>Usaha</label><select id="productBusiness" required></select></div><div class="field wide"><label>Nama produk / jasa</label><input id="productName" required maxlength="100" placeholder="Cetak foto 10R, Alarm wireless"></div><div class="field"><label>Harga jual/unit (Rp)</label><input id="productPrice" type="number" min="0" required value="0"></div><div class="field"><label>Satuan</label><input id="productUnit" maxlength="30" value="pcs"></div></div><div class="form-actions"><button type="button" onclick="closeModal(\'productModal\')">Batal</button><button class="primary" type="submit">Simpan produk</button></div></form></div></div>'
s=s.replace('<div class="modal-backdrop" id="txModal">',picker+productmodal+'<div class="modal-backdrop" id="txModal">',1)
amount='<div class="field"><label>Nominal (Rp)</label><input id="fAmount" type="number" min="1" step="1" placeholder="Contoh: 50000" required></div>'
s=s.replace(amount,amount+'<div class="field wide" id="saleItemsWrap" style="display:none"><div class="panel-head"><div><label>Produk terjual</label><div class="desc">Tambahkan beberapa produk dan jumlah terjual.</div></div><button type="button" class="small" onclick="addSaleItem()">＋ Tambah produk</button></div><div id="saleItems"></div></div>',1)
s=s.replace("if(!Array.isArray(d.businesses))d.businesses=defaultBusinesses();return d","if(!Array.isArray(d.businesses))d.businesses=defaultBusinesses();if(!Array.isArray(d.products))d.products=[];return d",1)
s=s.replace("businesses:Array.isArray(d.businesses)?d.businesses:defaultBusinesses()}","businesses:Array.isArray(d.businesses)?d.businesses:defaultBusinesses(),products:Array.isArray(d.products)?d.products:[]}",1)
s=s.replace("categories:DEFAULT_CATS.map(x=>({...x})),businesses:defaultBusinesses()}","categories:DEFAULT_CATS.map(x=>({...x})),businesses:defaultBusinesses(),products:[]}",1)
s=s.replace("function openTransaction(id=''){","function openTransactionForm(id='',presetBusiness=''){",1)
old="}updateTxForm();if(id){const t=state.transactions.find(x=>x.id===id);document.getElementById('fAccount').value=t.accountId;document.getElementById('fToAccount').value=t.toAccountId||'';document.getElementById('fCategory').value=t.categoryId||''}document.getElementById('txModal').style.display='flex'}"
new="}updateTxForm();if(id){const t=state.transactions.find(x=>x.id===id);document.getElementById('fAccount').value=t.accountId;document.getElementById('fToAccount').value=t.toAccountId||'';document.getElementById('fCategory').value=t.categoryId||'';document.getElementById('fBusiness').value=t.businessId||'';loadSaleItems(t.items||[])}else{document.getElementById('fBusiness').value=presetBusiness||'';clearSaleItems()}updateTxForm();document.getElementById('txModal').style.display='flex'}\nfunction openTransaction(id=''){if(id){const t=state.transactions.find(x=>x.id===id);openTransactionForm(id,t?t.businessId||'':'');return}renderBusinessPicker();document.getElementById('businessPickerModal').style.display='flex'}\nfunction renderBusinessPicker(){const host=document.getElementById('businessPickerCards');host.innerHTML=state.businesses.filter(b=>!b.archived).map(b=>'<button type=\"button\" class=\"picker-card\" onclick=\"chooseBusiness(&quot;'+esc(b.id)+'&quot;)\"><span class=\"picker-icon\">▣</span><span><strong>'+esc(b.name)+'</strong><small>'+esc(b.type)+'</small></span><span>›</span></button>').join('')||'<div class=\"empty\">Belum ada usaha. Tambahkan usaha dulu.</div>'}\nfunction chooseBusiness(id){closeModal('businessPickerModal');openTransactionForm('',id)}"
if old not in s: raise SystemExit("transaction opener anchor missing")
s=s.replace(old,new,1)
s=s.replace("function openTransactionForBusiness(type,id){openTransaction();document.getElementById('fType').value=type;","function openTransactionForBusiness(type,id){openTransactionForm('',id);document.getElementById('fType').value=type;",1)
salejs=r"""
function productOptions(bid,selected){return '<option value="">Pilih produk…</option>'+state.products.filter(p=>p.businessId===bid).map(p=>'<option value="'+esc(p.id)+'" '+(p.id===selected?'selected':'')+'>'+esc(p.name)+' · '+money(p.price)+'</option>').join('')}
function clearSaleItems(){const h=document.getElementById('saleItems');if(h)h.innerHTML=''}
function addSaleItem(item){item=item||{};const host=document.getElementById('saleItems'),bid=document.getElementById('fBusiness').value||'',row=document.createElement('div');row.className='sale-row';row.innerHTML='<div class="field"><label>Produk</label><select class="sale-p">'+productOptions(bid,item.productId||'')+'</select></div><div class="field"><label>Jumlah</label><input class="sale-q" type="number" min="1" step="1" value="'+Math.max(1,Number(item.qty)||1)+'"></div><div class="field"><label>Harga/unit</label><input class="sale-v" type="number" min="0" step="1" value="'+Math.max(0,Number(item.price)||0)+'"></div><button type="button" class="small danger sale-x">×</button>';host.appendChild(row);const sel=row.querySelector('.sale-p'),qty=row.querySelector('.sale-q'),price=row.querySelector('.sale-v');function calc(){row.dataset.subtotal=String((Number(qty.value)||0)*(Number(price.value)||0));recalcSaleTotal()}sel.addEventListener('change',()=>{const p=state.products.find(x=>x.id===sel.value);if(p)price.value=p.price;calc()});qty.addEventListener('input',calc);price.addEventListener('input',calc);row.querySelector('.sale-x').onclick=()=>{row.remove();recalcSaleTotal()};if(item.productId&&!item.price){const p=state.products.find(x=>x.id===item.productId);if(p)price.value=p.price}calc()}
function recalcSaleTotal(){const rows=[...document.querySelectorAll('#saleItems .sale-row')],sum=rows.reduce((n,r)=>n+(Number(r.dataset.subtotal)||0),0),amount=document.getElementById('fAmount');if(document.getElementById('fType').value==='income'&&rows.length){amount.value=Math.round(sum);amount.readOnly=true}else amount.readOnly=false}
function loadSaleItems(items){clearSaleItems();(items||[]).forEach(addSaleItem);recalcSaleTotal()}
function collectSaleItems(){return [...document.querySelectorAll('#saleItems .sale-row')].map(r=>{const id=r.querySelector('.sale-p').value,p=state.products.find(x=>x.id===id);return {productId:id,productName:p?p.name:'',qty:Math.max(0,Number(r.querySelector('.sale-q').value)||0),price:Math.max(0,Number(r.querySelector('.sale-v').value)||0),unit:p?p.unit||'pcs':'pcs'}}).filter(i=>i.productId&&i.qty>0)}
"""
s=s.replace("function openAccount(id=''){",salejs+"\nfunction openAccount(id=''){",1)
s=s.replace("function updateTxForm(){const type=document.getElementById('fType').value;","function updateTxForm(){const type=document.getElementById('fType').value;document.getElementById('saleItemsWrap').style.display=type==='income'?'block':'none';if(type!=='income')document.getElementById('fAmount').readOnly=false;",1)
s=s.replace("document.getElementById('fType').addEventListener('change',updateTxForm);","document.getElementById('fType').addEventListener('change',()=>{updateTxForm();recalcSaleTotal()});document.getElementById('fBusiness').addEventListener('change',()=>{clearSaleItems();updateTxForm()});",1)
s=s.replace("const t={id:id||uid(),type,businessId:document.getElementById('fBusiness').value||'',date:","const items=type==='income'?collectSaleItems():[];const t={id:id||uid(),type,businessId:document.getElementById('fBusiness').value||'',items,date:",1)
s=s.replace("amount:Math.round(amount),note:document.getElementById('fNote').value.trim()};","amount:Math.round(amount),note:document.getElementById('fNote').value.trim()};if(type==='income'&&items.length)t.amount=Math.round(items.reduce((n,i)=>n+i.qty*i.price,0));",1)
s=s.replace("if(!accountId||!Number.isFinite(amount)||amount<=0)return showToast('Pilih akun dan isi nominal yang valid.');","if(!accountId||!Number.isFinite(amount)||amount<=0)return showToast('Pilih dompet/rekening dan isi nominal yang valid.');if(type!=='transfer'&&!document.getElementById('fBusiness').value)return showToast('Pilih usaha untuk transaksi ini.');",1)
productjs=r"""
function openProduct(id){document.getElementById('productForm').reset();document.getElementById('productId').value='';document.getElementById('productPrice').value='0';document.getElementById('productUnit').value='pcs';const sel=document.getElementById('productBusiness');sel.innerHTML=state.businesses.filter(b=>!b.archived).map(b=>'<option value="'+esc(b.id)+'">'+esc(b.name)+'</option>').join('');document.getElementById('productModalTitle').textContent=id?'Edit produk':'Tambah produk';if(id){const p=state.products.find(x=>x.id===id);if(!p)return;document.getElementById('productId').value=p.id;sel.value=p.businessId;document.getElementById('productName').value=p.name;document.getElementById('productPrice').value=p.price;document.getElementById('productUnit').value=p.unit||'pcs'}document.getElementById('productModal').style.display='flex'}
document.getElementById('productForm').addEventListener('submit',e=>{e.preventDefault();const id=document.getElementById('productId').value,businessId=document.getElementById('productBusiness').value,name=document.getElementById('productName').value.trim(),price=Math.max(0,Math.round(Number(document.getElementById('productPrice').value)||0)),unit=document.getElementById('productUnit').value.trim()||'pcs';if(!businessId||!name)return showToast('Pilih usaha dan isi nama produk.');if(id){const p=state.products.find(x=>x.id===id);if(p)Object.assign(p,{businessId,name,price,unit})}else state.products.push({id:uid(),businessId,name,price,unit});closeModal('productModal');save();showToast('Produk disimpan.')});
function deleteProduct(id){if(state.transactions.some(t=>(t.items||[]).some(i=>i.productId===id)))return alert('Produk sudah dipakai dalam transaksi sehingga tidak dapat dihapus.');if(confirm('Hapus produk ini?')){state.products=state.products.filter(p=>p.id!==id);save()}}
function renderProducts(){const f=document.getElementById('productBusinessFilter');if(!f)return;const old=f.value;f.innerHTML='<option value="">Semua usaha</option>'+state.businesses.map(b=>'<option value="'+esc(b.id)+'">'+esc(b.name)+'</option>').join('');if([...f.options].some(o=>o.value===old))f.value=old;const rows=state.products.filter(p=>!f.value||p.businessId===f.value);document.getElementById('productsList').innerHTML=rows.map(p=>'<div class="account"><div style="min-width:0"><strong>'+esc(p.name)+'</strong><small>'+esc(businessName(p.businessId))+' · '+money(p.price)+' / '+esc(p.unit||'pcs')+'</small></div><div style="display:flex;gap:6px;flex-wrap:wrap"><button class="small" onclick="openProduct(\''+esc(p.id)+'\')">Edit</button><button class="small danger" onclick="deleteProduct(\''+esc(p.id)+'\')">Hapus</button></div></div>').join('')||'<div class="empty">Belum ada produk. Tekan Tambah produk untuk membuat daftar.</div>'}
document.getElementById('productBusinessFilter').addEventListener('change',renderProducts);
"""
s=s.replace("function renderBusinesses(){",productjs+"\nfunction renderBusinesses(){",1)
s=s.replace("renderCategories();renderBusinesses()}","renderCategories();renderBusinesses();renderProducts()}",1)
# Category editing uses a compact edit prompt while preserving the category's income/expense type.
s=s.replace("function deleteCategory(id){","function editCategory(id){const c=state.categories.find(x=>x.id===id);if(!c)return;const name=prompt('Ubah nama kategori:',c.name);if(!name||!name.trim())return;if(state.categories.some(x=>x.type===c.type&&x.id!==id&&x.name.toLowerCase()===name.trim().toLowerCase()))return showToast('Kategori sudah ada.');c.name=name.trim();save();showToast('Kategori diperbarui.')}\nfunction deleteCategory(id){",1)
# Replace category list renderer with buttons built by concatenation.
start=s.find("function renderCategories(){")
end=s.find("\nfunction editCategory",start)
if start<0 or end<0: raise SystemExit("category renderer missing")
renderer="""function renderCategories(){document.getElementById('categoriesList').innerHTML=['income','expense'].map(type=>'<h3 style="font-size:13px;color:var(--muted);margin:14px 0 8px">'+(type==='income'?'PEMASUKAN':'PENGELUARAN')+'</h3>'+state.categories.filter(c=>c.type===type).map(c=>'<div class="account"><div><strong>'+esc(c.name)+'</strong></div><div><button class="small" onclick="editCategory(&quot;'+esc(c.id)+'&quot;)">Edit</button> <button class="small danger" onclick="deleteCategory(&quot;'+esc(c.id)+'&quot;)">Hapus</button></div></div>').join('')).join('')}"""
s=s[:start]+renderer+s[end:]

# UX and backup improvements requested after real-device testing.
extra_css = """
/* RuangUsaha modal and backup UX */
@media(max-width:700px){
 body.modal-open{overflow:hidden!important;position:fixed!important;width:100%;left:0;right:0}
 .modal-backdrop{overscroll-behavior:contain;touch-action:pan-y}
 .modal{display:flex;flex-direction:column;overflow:hidden;overscroll-behavior:contain}
 .modal form{min-height:0;overflow-y:auto;overscroll-behavior:contain;padding-bottom:8px}
 .modal .form-actions{position:sticky;bottom:0;flex-shrink:0;background:#fff;padding:12px 0 max(12px,env(safe-area-inset-bottom));box-shadow:0 -8px 14px #fff}
 .modal-head{flex-shrink:0}
 #page-dashboard .top .actions{display:none!important}
 #mobileBottomNav{grid-template-columns:repeat(5,minmax(0,1fr))}
 #mobileBottomNav button[data-action="record"]{grid-column:3;grid-row:1;align-self:center;transform:translateY(-13px);min-height:64px;border-radius:20px 20px 20px 8px;background:#5b65d8;color:white;box-shadow:0 7px 18px #5b65d84d;padding:9px 3px;font-size:11px}
 #mobileBottomNav button[data-action="record"] span:first-child{font-size:27px}
 #mobileBottomNav button[data-page="businesses"]{grid-column:2;grid-row:1}
 #mobileBottomNav button[data-page="reports"]{grid-column:4;grid-row:1}
 #mobileBottomNav button[data-page="transactions"]{grid-column:5;grid-row:1}
 #mobileBottomNav button[data-page="dashboard"]{grid-column:1;grid-row:1}
 #mobileBottomNav button[data-page="settings"]{display:none!important}
 /* Modal is layered above navigation on Android; only its form scrolls. */
 .modal-backdrop{position:fixed!important;inset:0!important;z-index:1000!important;align-items:flex-end;justify-content:center;padding:0!important;overflow:hidden}
 .modal{position:relative;z-index:1001;width:100%!important;max-height:calc(100dvh - env(safe-area-inset-top))!important;margin:0!important;border-radius:22px 22px 0 0!important;overflow:hidden!important;display:flex;flex-direction:column}
 .modal form{display:flex;flex:1 1 auto;flex-direction:column;min-height:0;overflow-y:auto;overscroll-behavior:contain;padding-bottom:0!important}
 .modal .form-actions{position:sticky!important;bottom:0!important;z-index:4!important;flex-shrink:0;background:#fff!important;padding:12px 0 max(14px,env(safe-area-inset-bottom))!important;box-shadow:0 -8px 14px #fff}
}
.backup-panel{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px;margin:12px 0}
.backup-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}.backup-actions button{flex:1;min-width:130px}
"""
s=s.replace("</style>",extra_css+"\\n</style>",1)
# Add a Settings section if this source version does not already provide one.
if 'id="page-settings"' not in s:
 settings_html = '<section class="section" id="page-settings"><div class="top"><div><div class="eyebrow">DATA APLIKASI</div><h1 class="heading">Pengaturan</h1><div class="desc">Cadangkan dan pulihkan data pembukuan.</div></div></div><div class="backup-panel"><h2>Cadangan data</h2><p class="desc">Ekspor semua usaha, akun, kategori, produk, dan transaksi ke file JSON. Simpan file ini di folder Download atau Google Drive sebelum memperbarui aplikasi.</p><div class="backup-actions"><button class="primary" onclick="exportBackup()">⬇ Ekspor data</button><button onclick="document.getElementById(\'backupFile\').click()">⬆ Impor data</button></div><input id="backupFile" type="file" accept=".json,application/json" style="display:none" onchange="importBackupFile(event)"><p class="desc" style="margin-top:12px">Data tersimpan di penyimpanan privat aplikasi dan biasanya tetap ada saat aplikasi diperbarui dengan paket yang sama. Data dapat hilang jika aplikasi dihapus, data aplikasi dibersihkan, atau perangkat direset. Simpan cadangan secara berkala.</p></div></section>'
 s=s.replace('<section class="section" id="page-transactions">',settings_html+'<section class="section" id="page-transactions">',1)
# Add settings entry in the mobile navigation and make Record the center button.
nav_old='<button onclick="openTransaction()"><span>⊕</span><span>Catat</span></button>'
nav_new='<button data-action="record" onclick="openTransaction()"><span>＋</span><span>Catat</span></button>'
s=s.replace(nav_old,nav_new,1)
# Insert backup and modal behavior functions into the app script before it closes.
backup_js = r"""
function setModalBodyLock(){const open=[...document.querySelectorAll('.modal-backdrop')].some(el=>getComputedStyle(el).display!=='none');if(open){if(!document.body.classList.contains('modal-open')){document.body.dataset.scrollY=String(window.scrollY);document.body.classList.add('modal-open');document.body.style.top='-'+(window.scrollY||0)+'px'}}else if(document.body.classList.contains('modal-open')){const y=Number(document.body.dataset.scrollY)||0;document.body.classList.remove('modal-open');document.body.style.top='';window.scrollTo(0,y)}}
const _ruCloseModal=window.closeModal;
window.closeModal=function(id){if(typeof _ruCloseModal==='function')_ruCloseModal(id);else{const el=document.getElementById(id);if(el)el.style.display='none'}setTimeout(setModalBodyLock,0)};
const _ruOpenTransaction=window.openTransaction;
window.openTransaction=function(id){if(typeof _ruOpenTransaction==='function')_ruOpenTransaction(id);setTimeout(setModalBodyLock,0)};
document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;if(b.closest('.modal-backdrop'))setTimeout(setModalBodyLock,0);if(b.dataset.page==='settings'){e.preventDefault();if(typeof go==='function')go('settings');document.querySelectorAll('#mobileBottomNav button').forEach(x=>x.classList.toggle('active',x===b));}});
document.querySelectorAll('.modal-backdrop').forEach(el=>new MutationObserver(setModalBodyLock).observe(el,{attributes:true,attributeFilter:['style','class']}));
/* Keep five bottom-nav slots; move the existing Excel export control into Settings. */
(function arrangeHeaderActions(){
 const top=document.querySelector('.top');
 if(top&&!document.getElementById('settingsShortcut')){
   const b=document.createElement('button');b.type='button';b.id='settingsShortcut';b.className='small settings-shortcut';b.textContent='⚙ Pengaturan';b.setAttribute('aria-label','Buka pengaturan');b.addEventListener('click',()=>{if(typeof go==='function')go('settings')});top.appendChild(b);
 }
 const all=[...document.querySelectorAll('button,a,[role="button"]')];
 const exportBtn=all.find(el=>/\b(ekspor|export)\s+excel\b/i.test((el.innerText||el.textContent||'').replace(/[⬇⬆⇩↓↑📊]/g,' ').trim()));
 const settingsActions=document.querySelector('#page-settings .backup-actions');
 if(exportBtn&&settingsActions){
   exportBtn.removeAttribute('id');exportBtn.textContent='📊 Ekspor Excel';exportBtn.setAttribute('type','button');exportBtn.classList.add('excel-export-settings');settingsActions.insertBefore(exportBtn,settingsActions.firstChild);
 }
 document.querySelectorAll('button,a,[role="button"]').forEach(el=>{
   const label=(el.innerText||el.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
   if(/catat transaksi/.test(label)){el.remove();return}
   if(/\b(ekspor|export)\s+excel\b/.test(label)&&!el.classList.contains('excel-export-settings'))el.remove();
 });
 document.querySelectorAll('.top .actions').forEach(box=>{if(!box.querySelector('button,a,[role="button"]'))box.remove()});
})();
function exportBackup(){try{const payload={app:'RuangUsaha',formatVersion:1,exportedAt:new Date().toISOString(),data:state};const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='RuangUsaha-backup-'+new Date().toISOString().slice(0,10)+'.json';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),3000);showToast('Cadangan disiapkan. Pastikan file tersimpan di perangkat.')}catch(err){alert('Ekspor gagal: '+err.message)}}
function importBackupFile(event){const file=event.target.files&&event.target.files[0];if(!file)return;const reader=new FileReader();reader.onload=()=>{try{const parsed=JSON.parse(String(reader.result||'')),d=parsed.data||parsed;if(!d||!Array.isArray(d.transactions)||!Array.isArray(d.accounts)||!Array.isArray(d.categories))throw new Error('Format file cadangan tidak dikenali');if(!confirm('Impor akan mengganti data saat ini. Pastikan Anda sudah mengekspor cadangan data terbaru. Lanjutkan?'))return;state={...state,...d,accounts:d.accounts,transactions:d.transactions,categories:d.categories,businesses:Array.isArray(d.businesses)?d.businesses:[],products:Array.isArray(d.products)?d.products:[]};save();if(typeof render==='function')render();showToast('Data berhasil dipulihkan.')}catch(err){alert('File cadangan tidak valid atau rusak: '+err.message)}finally{event.target.value=''}};reader.onerror=()=>alert('File tidak dapat dibaca.');reader.readAsText(file)}
"""
# Add just before the final script closing tag; preserve other script tags.
idx=s.lower().rfind('</script>')
if idx<0: raise SystemExit("No script closing tag found")
s=s[:idx]+backup_js+s[idx:]
# Ensure navigation action handler knows settings page and scroll lock after every modal open.
s=s.replace("p.write_text(s)","p.write_text(s)",1)


# Per-business categories and transaction-type-first flow (v4).
v4 = r"""
<style>
#txTypePicker .modal{max-width:520px}#txTypePicker .type-choice{width:100%;display:flex;align-items:center;gap:14px;padding:16px;margin:8px 0;text-align:left;border:1px solid var(--line);border-radius:16px;background:#fff}
#txTypePicker .type-icon{display:grid;place-items:center;width:44px;height:44px;border-radius:13px;background:#eaf0ff;color:#4655ca;font-size:23px;flex-shrink:0}
.biz-settings-panel{background:#fff;border:1px solid var(--line);border-radius:16px;padding:15px;margin:16px 0}
.biz-cat-row{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:10px 0;border-bottom:1px solid var(--line)}
</style>
<div class="modal-backdrop" id="txTypePicker" style="display:none"><div class="modal"><div class="modal-head"><div><h2>Catat transaksi</h2><div class="desc">Pilih jenis transaksi terlebih dahulu.</div></div><button type="button" onclick="closeModal('txTypePicker')">✕</button></div>
<button type="button" class="type-choice" onclick="startTypedTransaction('income')"><span class="type-icon">↙</span><span><strong>Pemasukan</strong><small class="desc">Pilih usaha, lalu isi pemasukan.</small></span></button>
<button type="button" class="type-choice" onclick="startTypedTransaction('expense')"><span class="type-icon">↗</span><span><strong>Pengeluaran</strong><small class="desc">Pilih usaha, lalu isi pengeluaran.</small></span></button>
<button type="button" class="type-choice" onclick="startTypedTransaction('transfer')"><span class="type-icon">⇄</span><span><strong>Transfer antar dompet</strong><small class="desc">Pilih dompet asal dan tujuan.</small></span></button>
</div>
<div class="biz-settings-panel" id="businessCategorySettings">
<div class="panel-head"><div><h2>Pengaturan per usaha</h2><div class="desc">Kategori dan produk dikelola terpisah untuk setiap usaha.</div></div></div>
<div class="field"><label>Pilih usaha</label><select id="bizSettingsBusiness"></select></div>
<div class="panel-head" style="margin-top:15px"><div><h3>Kategori usaha</h3><div class="desc">Kategori pemasukan dan pengeluaran khusus usaha terpilih.</div></div><button type="button" class="primary" onclick="openBusinessCategory()">＋ Kategori</button></div>
<div id="bizSettingsCategories"></div>
</div>
<div class="modal-backdrop" id="bizCategoryModal" style="display:none"><div class="modal"><div class="modal-head"><h2 id="bizCategoryTitle">Kategori usaha</h2><button type="button" onclick="closeModal('bizCategoryModal')">✕</button></div>
<form id="bizCategoryForm"><input type="hidden" id="bizCategoryId"><div class="field"><label>Usaha</label><select id="bizCategoryBusiness" required></select></div><div class="field"><label>Jenis kategori</label><select id="bizCategoryType"><option value="income">Pemasukan</option><option value="expense">Pengeluaran</option></select></div><div class="field"><label>Nama kategori</label><input id="bizCategoryName" required maxlength="70" placeholder="Contoh: Cetak foto"></div><div class="form-actions"><button type="button" onclick="closeModal('bizCategoryModal')">Batal</button><button type="submit" class="primary">Simpan kategori</button></div></form>
</div></div>
<script>
(function(){
 const oldOpen=window.openTransaction;
 let nextType='income';
 window.openTransaction=function(id){if(id){oldOpen(id);return}document.getElementById('txTypePicker').style.display='flex'};
 window.startTypedTransaction=function(type){
   nextType=type;
   closeModal('txTypePicker');
   if(type==='transfer'){
     openTransactionForm('', '');
     document.getElementById('fType').value='transfer';
     updateTxForm();
     document.getElementById('fBusiness').value='';
     document.getElementById('txModal').style.display='flex';
     setTimeout(()=>{if(window.setModalBodyLock) setModalBodyLock()},0);
   }else{
     renderBusinessPicker();
     const host=document.getElementById('businessPickerCards');
     host.querySelectorAll('button').forEach(b=>{if(!b.textContent.includes('Operasional umum'))b.setAttribute('onclick',b.getAttribute('onclick').replace('chooseBusiness(','chooseBusinessTyped('))});
     const general=host.parentElement.querySelector('button[onclick*="__general__"]');
     if(general)general.setAttribute('onclick',"chooseBusinessTyped('__general__')");
     document.getElementById('businessPickerModal').style.display='flex';
   }
 };
 window.chooseBusinessTyped=function(id){
   closeModal('businessPickerModal');
   openTransactionForm('',id==='__general__'?'':id);
   document.getElementById('fType').value=nextType;
   updateTxForm();
   if(window.setModalBodyLock)setModalBodyLock();
 };
 // Transfer does not require an enterprise; both source and destination wallets are selected in the form.
 const oldUpdate=window.updateTxForm;
 window.updateTxForm=function(){
   oldUpdate();
   const type=document.getElementById('fType').value,bid=document.getElementById('fBusiness').value,cat=document.getElementById('fCategory');
   if(!cat)return;
   const previous=cat.value;
   const eligible=(state.categories||[]).filter(c=>c.type===type && (type==='transfer' || !c.businessId || c.businessId===bid));
   cat.innerHTML=eligible.map(c=>'<option value="'+esc(c.id)+'">'+esc(c.name)+'</option>').join('');
   if(eligible.some(c=>c.id===previous))cat.value=previous;
 };
 function businessSelectOptions(selected){return (state.businesses||[]).filter(b=>!b.archived).map(b=>'<option value="'+esc(b.id)+'" '+(b.id===selected?'selected':'')+'>'+esc(b.name)+'</option>').join('')}
 function selectedBiz(){return document.getElementById('bizSettingsBusiness').value}
 window.renderBusinessCategorySettings=function(){
   const sel=document.getElementById('bizSettingsBusiness'),old=sel.value;
   sel.innerHTML=businessSelectOptions(old);
   if(!sel.value&&sel.options.length)sel.selectedIndex=0;
   const bid=sel.value;
   document.getElementById('bizCategoryBusiness').innerHTML=businessSelectOptions(bid);
   const cats=(state.categories||[]).filter(c=>c.businessId===bid);
   document.getElementById('bizSettingsCategories').innerHTML=['income','expense'].map(type=>'<h4 style="margin:12px 0 4px">'+(type==='income'?'PEMASUKAN':'PENGELUARAN')+'</h4>'+cats.filter(c=>c.type===type).map(c=>'<div class="biz-cat-row"><span>'+esc(c.name)+'</span><span><button type="button" class="small" onclick="openBusinessCategory(&quot;'+esc(c.id)+'&quot;)">Edit</button> <button type="button" class="small danger" onclick="deleteBusinessCategory(&quot;'+esc(c.id)+'&quot;)">Hapus</button></span></div>').join('')||'<div class="desc">Belum ada kategori untuk usaha ini.</div>').join('');
   const pf=document.getElementById('productBusinessFilter');if(pf&&bid){pf.value=bid;if(window.renderProducts)renderProducts()}
 };
 window.openBusinessCategory=function(id){
   const sel=document.getElementById('bizCategoryBusiness');sel.innerHTML=businessSelectOptions(selectedBiz());
   document.getElementById('bizCategoryForm').reset();document.getElementById('bizCategoryId').value='';
   document.getElementById('bizCategoryTitle').textContent=id?'Edit kategori':'Tambah kategori';
   if(id){const c=state.categories.find(x=>x.id===id);if(!c)return;document.getElementById('bizCategoryId').value=c.id;sel.value=c.businessId;document.getElementById('bizCategoryType').value=c.type;document.getElementById('bizCategoryName').value=c.name}
   document.getElementById('bizCategoryModal').style.display='flex';
 };
 window.deleteBusinessCategory=function(id){
   if(state.transactions.some(t=>t.categoryId===id))return alert('Kategori sudah digunakan transaksi. Edit nama kategori jika ingin mempertahankannya.');
   if(confirm('Hapus kategori dari usaha ini?')){state.categories=state.categories.filter(c=>c.id!==id);save();renderBusinessCategorySettings();updateTxForm()}
 };
 document.getElementById('bizCategoryForm').addEventListener('submit',e=>{
   e.preventDefault();const id=document.getElementById('bizCategoryId').value,businessId=document.getElementById('bizCategoryBusiness').value,type=document.getElementById('bizCategoryType').value,name=document.getElementById('bizCategoryName').value.trim();
   if(!businessId||!name)return alert('Pilih usaha dan nama kategori.');
   if(state.categories.some(c=>c.id!==id&&c.businessId===businessId&&c.type===type&&c.name.toLowerCase()===name.toLowerCase()))return alert('Kategori dengan nama tersebut sudah ada di usaha ini.');
   if(id){const c=state.categories.find(x=>x.id===id);if(c)Object.assign(c,{businessId,type,name})}
   else state.categories.push({id:uid(),businessId,type,name});
   save();closeModal('bizCategoryModal');renderBusinessCategorySettings();updateTxForm();showToast('Kategori usaha disimpan.');
 });
 document.getElementById('bizSettingsBusiness').addEventListener('change',renderBusinessCategorySettings);
 const oldRender=window.renderBusinesses;
 if(typeof oldRender==='function')window.renderBusinesses=function(){oldRender();renderBusinessCategorySettings()};
 document.addEventListener('DOMContentLoaded',renderBusinessCategorySettings);
 setTimeout(renderBusinessCategorySettings,100);
})();
</script>
"""
if (!s.includes("</body>")) throw new Error("body closing tag not found");
s=s.replace("</body>",v4+"</body>");

p.write_text(s)
print("Feature upgrade applied",len(s))
