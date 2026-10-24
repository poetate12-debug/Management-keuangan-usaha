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
rep='<div class="account-list" id="businessesList" style="margin-top:14px"></div><div id="globalProductsBlock" style="display:none"><div class="panel-head" style="margin-top:22px"><div><h2>Produk tiap usaha</h2><div class="desc">Daftarkan foto, alarm, barang, atau jasa beserta harga jual.</div></div><button class="primary" onclick="openProduct()">＋ Tambah produk</button></div><div class="filters"><select id="productBusinessFilter"><option value="">Semua usaha</option></select></div><div class="account-list" id="productsList"></div></div></div>'
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
function openProduct(id){document.getElementById('productBusiness').disabled=false;document.getElementById('productForm').reset();document.getElementById('productId').value='';document.getElementById('productPrice').value='0';document.getElementById('productUnit').value='pcs';const sel=document.getElementById('productBusiness');sel.innerHTML=state.businesses.filter(b=>!b.archived).map(b=>'<option value="'+esc(b.id)+'">'+esc(b.name)+'</option>').join('');document.getElementById('productModalTitle').textContent=id?'Edit produk':'Tambah produk';if(id){const p=state.products.find(x=>x.id===id);if(!p)return;document.getElementById('productId').value=p.id;sel.value=p.businessId;document.getElementById('productName').value=p.name;document.getElementById('productPrice').value=p.price;document.getElementById('productUnit').value=p.unit||'pcs'}document.getElementById('productModal').style.display='flex'}
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
 let exportBtn=all.find(el=>/\b(ekspor|export)\s+excel\b/i.test((el.innerText||el.textContent||'').replace(/[⬇⬆⇩↓↑📊]/g,' ').trim()));
 const backupButton=all.find(el=>/unduh cadangan json|ekspor data|unduh.*json|cadangan.*json/i.test((el.innerText||el.textContent||'').replace(/\\s+/g,' ').trim()));
 const settingsActions=document.querySelector('#page-settings .backup-actions')||(backupButton&&backupButton.parentElement&&backupButton.parentElement.parentElement);
 if(!exportBtn&&settingsActions){
   exportBtn=document.createElement('button');exportBtn.type='button';exportBtn.className='primary excel-export-settings';exportBtn.textContent='📊 Ekspor Excel';
   settingsActions.insertBefore(exportBtn,settingsActions.firstChild);
 }
 if(exportBtn&&settingsActions){
   exportBtn.removeAttribute('id');exportBtn.textContent='📊 Ekspor Excel';exportBtn.setAttribute('type','button');exportBtn.classList.add('excel-export-settings');exportBtn.onclick=()=>exportExcel();
   if(exportBtn.parentElement!==settingsActions)settingsActions.insertBefore(exportBtn,settingsActions.firstChild);
 }
 // Explicitly bind the JSON backup button for Android WebView.
 const jsonButton=[...document.querySelectorAll('#page-settings button')].find(el=>/unduh cadangan json|ekspor data|unduh.*json|cadangan.*json/i.test((el.innerText||el.textContent||'').replace(/\\s+/g,' ').trim()));
 if(jsonButton){jsonButton.type='button';jsonButton.onclick=function(ev){if(ev){ev.preventDefault();ev.stopPropagation()}exportBackup()}}
 document.querySelectorAll('button,a,[role="button"]').forEach(el=>{
   const label=(el.innerText||el.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
   if(/catat transaksi/.test(label)){el.remove();return}
   if(/\b(ekspor|export)\s+excel\b/.test(label)&&!el.classList.contains('excel-export-settings'))el.remove();
 });
 document.querySelectorAll('.top .actions').forEach(box=>{if(!box.querySelector('button,a,[role="button"]'))box.remove()});
})();
function exportExcel(){
 try{
  const clean=v=>String(v===null||v===undefined?'':v);
  const csv=v=>'"'+clean(v).replace(/"/g,'""')+'"';
  const row=values=>values.map(csv).join(',');
  const businesses=state.businesses||[],accounts=state.accounts||[],categories=state.categories||[],products=state.products||[],transactions=state.transactions||[],hpp=state.hppRecords||[];
  const lines=[row(['LAPORAN KASUSAHA','Tanggal ekspor',new Date().toLocaleDateString('id-ID')]),'',row(['TRANSAKSI']),row(['Tanggal','Jenis','Usaha','Kategori','Akun asal','Akun tujuan','Nominal (Rp)','Catatan','Rincian produk'])];
  transactions.slice().sort((a,b)=>String(a.date||'').localeCompare(String(b.date||''))).forEach(t=>lines.push(row([t.date||'',t.type==='income'?'Pemasukan':t.type==='expense'?'Pengeluaran':'Transfer',t.businessId?businessName(t.businessId):'',t.categoryId?categoryName(t.categoryId):'',t.accountId?accountName(t.accountId):'',t.toAccountId?accountName(t.toAccountId):'',Number(t.amount)||0,t.note||'',(t.items||[]).map(it=>(it.productName||(products.find(p=>p.id===it.productId)||{}).name||'Produk')+' x '+(Number(it.qty)||0)+' @ '+(Number(it.price)||0)).join('; ')])));
  lines.push('',row(['DAFTAR USAHA']),row(['ID usaha','Nama usaha','Jenis usaha','Status']));
  businesses.forEach(b=>lines.push(row([b.id||'',b.name||'',b.type||'',b.archived?'Diarsipkan':'Aktif'])));
  lines.push('',row(['AKUN']),row(['Nama akun','Jenis akun','Saldo awal (Rp)']));
  accounts.forEach(a=>lines.push(row([a.name||'',a.type||'',Number(a.opening)||0])));
  lines.push('',row(['KATEGORI']),row(['Usaha','Jenis','Nama kategori']));
  categories.forEach(c=>lines.push(row([c.businessId?businessName(c.businessId):'Umum',c.type==='income'?'Pemasukan':'Pengeluaran',c.name||''])));
  lines.push('',row(['PRODUK']),row(['Usaha','Nama produk','Harga jual (Rp)','Satuan']));
  products.forEach(p=>lines.push(row([businessName(p.businessId),p.name||'',Number(p.price)||0,p.unit||'pcs'])));
  lines.push('',row(['HPP']),row(['Tanggal','Usaha','Nama produk','Jumlah unit','Biaya bahan baku (Rp)','Tenaga kerja (Rp)','Overhead (Rp)','Total biaya (Rp)','HPP per unit (Rp)']));
  hpp.forEach(h=>lines.push(row([h.date||'',businessName(h.businessId),h.productName||'',Number(h.quantity)||0,Number(h.materialCost)||0,Number(h.laborCost)||0,Number(h.overheadCost)||0,Number(h.totalCost)||0,Number(h.unitCost)||0])));
  const csvText='\\uFEFF'+lines.join('\\r\\n');
  const filename='KasUsaha-Laporan-'+new Date().toISOString().slice(0,10)+'.csv',mime='text/csv';
  if(window.AndroidDownloads&&typeof window.AndroidDownloads.saveFile==='function'){
   const bytes=new TextEncoder().encode(csvText),parts=[];for(let k=0;k<bytes.length;k+=8192)parts.push(String.fromCharCode(...bytes.subarray(k,k+8192)));
   window.AndroidDownloads.saveFile(filename,mime,btoa(parts.join('')));
  }else{
   const blob=new Blob([csvText],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');
   a.href=url;a.download=filename;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),3000);
  }
  showToast('Laporan CSV untuk Excel disiapkan. Periksa folder Unduhan.');
 }catch(err){alert('Ekspor Excel gagal: '+(err&&err.message?err.message:String(err)))}
}
function exportBackup(){
 try{
  const payload=JSON.stringify({app:'RuangUsaha',formatVersion:1,exportedAt:new Date().toISOString(),data:state},null,2);
  const filename='KasUsaha-backup-'+new Date().toISOString().slice(0,10)+'.json';
  if(window.AndroidDownloads&&typeof window.AndroidDownloads.saveFile==='function'){
   const bytes=new TextEncoder().encode(payload),parts=[];
   for(let i=0;i<bytes.length;i+=8192)parts.push(String.fromCharCode(...bytes.subarray(i,i+8192)));
   window.AndroidDownloads.saveFile(filename,'application/json',btoa(parts.join('')));
   showToast('Membuat cadangan JSON… Periksa folder Unduhan.');
  }else{
   const blob=new Blob([payload],{type:'application/json;charset=utf-8'});
   const url=URL.createObjectURL(blob),a=document.createElement('a');
   a.href=url;a.download=filename;a.style.display='none';document.body.appendChild(a);a.click();
   setTimeout(()=>{a.remove();URL.revokeObjectURL(url)},1000);
   showToast('Unduhan cadangan JSON dimulai.');
  }
 }catch(err){alert('Unduh cadangan JSON gagal: '+(err&&err.message?err.message:String(err)))}
}
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
<div id="bizSettingsCategories"></div><div class="panel-head" style="margin-top:18px"><div><h3>Produk usaha</h3><div class="desc">Produk hanya milik usaha yang dipilih.</div></div><button type="button" class="primary" onclick="openBusinessProduct()">＋ Produk</button></div><div id="bizSettingsProducts"></div>
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
   const businessField=document.getElementById('fBusiness')?.closest('.field');if(businessField)businessField.style.display=type==='transfer'?'none':'';const catField=cat?.closest('.field');if(catField)catField.style.display=type==='transfer'?'none':'';const eligibleAll=(state.categories||[]).filter(c=>c.type===type && (type==='transfer' || !c.businessId || c.businessId===bid));const ownNames=new Set(eligibleAll.filter(c=>c.businessId===bid).map(c=>c.name.toLowerCase()));const eligible=eligibleAll.filter(c=>c.businessId===bid||!ownNames.has(c.name.toLowerCase()));
   cat.innerHTML=eligible.map(c=>'<option value="'+esc(c.id)+'">'+esc(c.name)+'</option>').join('');
   if(eligible.some(c=>c.id===previous))cat.value=previous;
 };
 function businessSelectOptions(selected){return (state.businesses||[]).filter(b=>!b.archived).map(b=>'<option value="'+esc(b.id)+'" '+(b.id===selected?'selected':'')+'>'+esc(b.name)+'</option>').join('')}
 function selectedBiz(){return document.getElementById('bizSettingsBusiness').value}
 window.renderBusinessCategorySettings=function(){
   const panel=document.getElementById('businessCategorySettings'),section=document.getElementById('page-businesses');if(panel&&section&&panel.parentElement!==section)section.appendChild(panel);const sel=document.getElementById('bizSettingsBusiness'),old=sel.value;
   sel.innerHTML=businessSelectOptions(old);
   if(!sel.value&&sel.options.length)sel.selectedIndex=0;
   const bid=sel.value;
   document.getElementById('bizCategoryBusiness').innerHTML=businessSelectOptions(bid);
   const cats=(state.categories||[]).filter(c=>c.businessId===bid||!c.businessId);
   document.getElementById('bizSettingsCategories').innerHTML=['income','expense'].map(type=>'<h4 style="margin:12px 0 4px">'+(type==='income'?'PEMASUKAN':'PENGELUARAN')+'</h4>'+cats.filter(c=>c.type===type).map(c=>'<div class="biz-cat-row"><span>'+esc(c.name)+'</span><span><button type="button" class="small" onclick="openBusinessCategory(&quot;'+esc(c.id)+'&quot;)">Edit</button> <button type="button" class="small danger" onclick="deleteBusinessCategory(&quot;'+esc(c.id)+'&quot;)">Hapus</button></span></div>').join('')||'<div class="desc">Belum ada kategori untuk usaha ini.</div>').join('');
   const pf=document.getElementById('productBusinessFilter');if(pf&&bid){pf.value=bid;if(window.renderProducts)renderProducts()}if(window.renderBusinessProducts)renderBusinessProducts()
 };
 window.openBusinessCategory=function(id){
   const sel=document.getElementById('bizCategoryBusiness');sel.innerHTML=businessSelectOptions(selectedBiz());
   document.getElementById('bizCategoryForm').reset();document.getElementById('bizCategoryId').value='';
   document.getElementById('bizCategoryTitle').textContent=id?'Edit kategori':'Tambah kategori';
   if(id){const c=state.categories.find(x=>x.id===id);if(!c)return;const scoped=c.businessId===selectedBiz();document.getElementById('bizCategoryId').value=scoped?c.id:'';sel.value=selectedBiz();document.getElementById('bizCategoryTitle').textContent=scoped?'Edit kategori':'Salin kategori ke usaha';document.getElementById('bizCategoryType').value=c.type;document.getElementById('bizCategoryName').value=c.name}
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
 window.openBusinessProduct=function(id){if(typeof openProduct!=='function')return;openProduct(id);const sel=document.getElementById('productBusiness');sel.value=selectedBiz();sel.disabled=true;};
  window.renderBusinessProducts=function(){const bid=selectedBiz(),host=document.getElementById('bizSettingsProducts');if(!host)return;const list=(state.products||[]).filter(p=>p.businessId===bid);host.innerHTML=list.map(p=>'<div class="biz-cat-row"><span><strong>'+esc(p.name)+'</strong><small class="desc" style="display:block">'+money(p.price)+' / '+esc(p.unit||'pcs')+'</small></span><span><button type="button" class="small" onclick="openBusinessProduct(&quot;'+esc(p.id)+'&quot;)">Edit</button> <button type="button" class="small danger" onclick="deleteProduct(&quot;'+esc(p.id)+'&quot;)">Hapus</button></span></div>').join('')||'<div class="desc">Belum ada produk untuk usaha ini.</div>'};
 document.getElementById('bizSettingsBusiness').addEventListener('change',renderBusinessCategorySettings);
 const oldRender=window.renderBusinesses;
 if(typeof oldRender==='function')window.renderBusinesses=function(){oldRender();renderBusinessCategorySettings()};
 document.addEventListener('DOMContentLoaded',renderBusinessCategorySettings);
 setTimeout(renderBusinessCategorySettings,100);
})();
</script>
"""
if "</body>" not in s: raise SystemExit("body closing tag not found")

s=s.replace("</body>",v4+"</body>",1)
# Visual layout and a separate details view for each business.
v5 = r"""
<style>
/* Business selector: icon above label; compact visual choices */
#txTypePicker .modal{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;padding:18px!important}
#txTypePicker .modal-head{grid-column:1/-1}
#txTypePicker .type-choice{width:100%;min-width:0;min-height:104px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:8px;margin:0;padding:12px 4px;border-radius:15px;text-align:center}
#txTypePicker .type-icon{width:43px;height:43px;font-size:23px}
#txTypePicker .type-choice>span:nth-child(2){display:block;text-align:center}
#txTypePicker .type-choice strong{font-size:12px;line-height:1.2;display:block}
#txTypePicker .type-choice small{display:none!important}
#businessPickerCards.picker-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:10px}
#businessPickerCards .picker-card{width:100%;min-height:104px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:8px;text-align:center;padding:12px 6px}
#businessPickerCards .picker-icon{width:46px;height:46px;font-size:25px;display:grid;place-items:center}
#businessPickerCards .picker-card strong{font-size:13px;line-height:1.2}
#businessPickerCards .picker-card small,#businessPickerCards .picker-card>span:last-child{display:none!important}
#businessCategorySettings{display:none}
#businessDetailView{padding-bottom:24px}
.business-detail-top{display:flex;align-items:center;gap:10px;margin-bottom:16px}
.business-detail-back{flex:0 0 auto}
.business-detail-logo{width:54px;height:54px;border-radius:16px;display:grid;place-items:center;background:#e5efff;color:#4655c9;font-size:28px}
.business-detail-title{font-size:23px;font-weight:800;line-height:1.15;margin:0}
.business-detail-kind{font-size:12px;color:var(--muted);margin-top:5px}
.business-stat-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin:12px 0 18px}
.business-stat{padding:14px;background:#fff;border:1px solid var(--line);border-radius:15px}
.business-stat small{display:block;font-size:11px;color:var(--muted)}
.business-stat strong{display:block;font-size:17px;margin-top:7px;overflow-wrap:anywhere}
.business-detail-actions{display:flex;gap:8px;margin:12px 0 18px}
.business-detail-actions button{flex:1;min-height:43px}
.business-section-heading{font-size:17px;font-weight:800;margin:20px 0 10px}
#businessDetailRecent{display:grid;gap:8px}
.business-detail-transaction{display:flex;align-items:center;justify-content:space-between;gap:10px;background:#fff;padding:11px 12px;border:1px solid var(--line);border-radius:12px}
.business-detail-transaction small{display:block;color:var(--muted);font-size:11px;margin-top:3px}
#businessDetailSettings .biz-settings-panel{margin:0 0 16px}
#businessDetailSettings #bizSettingsBusiness{pointer-events:none}
@media(max-width:700px){
 #txTypePicker .modal{grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;padding:16px!important}
 #txTypePicker .type-choice{min-height:100px;padding:10px 3px}
 #txTypePicker .type-icon{width:39px;height:39px;font-size:21px}
 #businessPickerCards.picker-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}
 #businessPickerCards .picker-card{min-height:100px}
 .business-detail-title{font-size:20px}
}
</style>
<div id="businessSettingsParking" style="display:none!important"></div>
<script>
(function(){
 const section=document.getElementById('page-businesses');
 if(!section)return;
 const detail=document.createElement('div');detail.id='businessDetailView';detail.style.display='none';section.appendChild(detail);
 const parking=document.getElementById('businessSettingsParking');
 const stateOriginalDisplay=new WeakMap();
 let selectedBusinessId=null;
 function norm(v){return String(v||'').trim().toLowerCase()}
 function logoForBusiness(b){
   const n=norm(b&&b.name);
   if(/studio|foto|fotografi|cetak/.test(n))return '📷';
   if(/wifi|internet|net/.test(n))return '📡';
   if(/cctv|alarm|security|sentinel|keamanan/.test(n))return '🛡️';
   if(/delivery|gelis|antar|kurir/.test(n))return '🛵';
   return '🏪';
 }
 function hideBusinessList(){
   [...section.children].forEach(el=>{
     if(el===detail)return;
     if(!el.hasAttribute('data-ru-old-display'))el.setAttribute('data-ru-old-display',el.style.display||'');
     el.style.display='none';
   });
   detail.style.display='block';
 }
 function showBusinessList(){
   [...section.children].forEach(el=>{
     if(el===detail)return;
     if(el.hasAttribute('data-ru-old-display')){
       el.style.display=el.getAttribute('data-ru-old-display');
       el.removeAttribute('data-ru-old-display');
     }
   });
   detail.style.display='none';
   selectedBusinessId=null;
   const panel=document.getElementById('businessCategorySettings');
   if(panel){parking.appendChild(panel);panel.style.display='none'}
 }
 function detailStats(id){
   const b=(state.businesses||[]).find(x=>x.id===id);if(!b)return;
   const month=typeof monthNow==='function'?monthNow():new Date().toISOString().slice(0,7);
   const txs=(state.transactions||[]).filter(t=>t.businessId===id);
   const monthTx=txs.filter(t=>String(t.date||'').startsWith(month));
   const sm=typeof totals==='function'?totals(monthTx):{inc:0,out:0,net:0};
   const balance=sm.net;
   const stats=document.getElementById('businessDetailStats');
   if(stats)stats.innerHTML='<div class="business-stat"><small>Pemasukan bulan ini</small><strong style="color:var(--green)">'+money(sm.inc)+'</strong></div><div class="business-stat"><small>Pengeluaran bulan ini</small><strong style="color:var(--red)">'+money(sm.out)+'</strong></div><div class="business-stat"><small>Arus kas bersih</small><strong style="color:var(--blue)">'+money(balance)+'</strong></div><div class="business-stat"><small>Jumlah transaksi</small><strong>'+txs.length+'</strong></div>';
   const recent=document.getElementById('businessDetailRecent');
   if(recent){
     const items=txs.slice().sort((a,b)=>String(b.date||'').localeCompare(String(a.date||''))).slice(0,6);
     recent.innerHTML=items.map(t=>'<div class="business-detail-transaction"><div><strong>'+esc(t.note||(t.type==='income'?'Pemasukan':t.type==='expense'?'Pengeluaran':'Transfer'))+'</strong><small>'+esc(t.date||'')+' · '+esc(t.type==='transfer'?'Transfer':(typeof categoryName==='function'?categoryName(t.categoryId):''))+'</small></div><strong style="white-space:nowrap">'+(t.type==='expense'?'−':t.type==='income'?'+':'')+money(t.amount)+'</strong></div>').join('')||'<div class="desc">Belum ada transaksi untuk usaha ini.</div>';
   }
 }
 function mountSettings(){
   const panel=document.getElementById('businessCategorySettings'),mount=document.getElementById('businessDetailSettings');
   if(!panel)return;
   if(selectedBusinessId){
     const chooser=document.getElementById('bizSettingsBusiness');if(chooser)chooser.value=selectedBusinessId;
     panel.style.display='block';
     if(mount)mount.appendChild(panel);
   }else{
     parking.appendChild(panel);panel.style.display='none';
   }
 }
 window.openBusinessDetail=function(id){
   const b=(state.businesses||[]).find(x=>x.id===id);if(!b)return;
   selectedBusinessId=id;
   detail.innerHTML='<div class="business-detail-top"><button type="button" class="small business-detail-back" onclick="closeBusinessDetail()">← Kembali</button><div class="business-detail-logo">'+logoForBusiness(b)+'</div><div style="min-width:0"><h1 class="business-detail-title">'+esc(b.name)+'</h1><div class="business-detail-kind">'+esc(b.type||'Usaha')+'</div></div></div><div class="desc">Ringkasan kinerja usaha untuk bulan berjalan.</div><div class="business-stat-grid" id="businessDetailStats"></div><div class="business-detail-actions"><button type="button" class="primary" id="businessDetailIncome">＋ Pemasukan</button><button type="button" id="businessDetailExpense">－ Pengeluaran</button></div><h2 class="business-section-heading">Transaksi terbaru</h2><div id="businessDetailRecent"></div><h2 class="business-section-heading">Pengaturan usaha</h2><div id="businessDetailSettings"></div>';
   hideBusinessList();
   document.getElementById('businessDetailIncome').onclick=()=>openTransactionForBusiness('income',id);
   document.getElementById('businessDetailExpense').onclick=()=>openTransactionForBusiness('expense',id);
   if(typeof renderBusinessCategorySettings==='function')renderBusinessCategorySettings();
   mountSettings();detailStats(id);
   window.scrollTo(0,0);
 };
 window.closeBusinessDetail=function(){showBusinessList();if(typeof renderBusinesses==='function')renderBusinesses();window.scrollTo(0,0)};
 const oldPicker=window.renderBusinessPicker;
 window.renderBusinessPicker=function(){
   if(typeof oldPicker==='function')oldPicker();
   const host=document.getElementById('businessPickerCards');if(!host)return;
   [...host.querySelectorAll('button.picker-card')].forEach(btn=>{
     const strong=btn.querySelector('strong'),name=strong?strong.textContent:'';
     const b=(state.businesses||[]).find(x=>norm(x.name)===norm(name));
     if(!b)return;
     btn.innerHTML='<span class="picker-icon">'+logoForBusiness(b)+'</span><strong>'+esc(b.name)+'</strong>';
   });
   const general=host.parentElement.querySelector('button[onclick*="__general__"]');
   if(general){host.appendChild(general);general.classList.add('picker-card');general.innerHTML='<span class="picker-icon">🏪</span><strong>Umum</strong>'}
 };
 function decorateBusinesses(){
   const list=document.getElementById('businessesList');if(!list)return;
   list.querySelectorAll('.account,.business-card,.biz-card').forEach(row=>{
     const strong=row.querySelector('strong');if(!strong)return;
     const b=(state.businesses||[]).find(x=>norm(x.name)===norm(strong.textContent));if(!b)return;
     if(!row.querySelector('.business-detail-trigger')){
       const dest=row.querySelector(':scope > div:last-child')||row;
       const button=document.createElement('button');button.type='button';button.className='small business-detail-trigger';button.textContent='Detail ›';
       button.addEventListener('click',e=>{e.stopPropagation();openBusinessDetail(b.id)});
       dest.appendChild(button);
     }
   });
 }
 const oldSettings=window.renderBusinessCategorySettings;
 window.renderBusinessCategorySettings=function(){
   if(typeof oldSettings==='function')oldSettings();
   mountSettings();
   if(selectedBusinessId)detailStats(selectedBusinessId);
 };
 const oldRenderBusinesses=window.renderBusinesses;
 if(typeof oldRenderBusinesses==='function')window.renderBusinesses=function(){
   oldRenderBusinesses();decorateBusinesses();mountSettings();
   if(selectedBusinessId)detailStats(selectedBusinessId);
 };
 section.addEventListener('click',e=>{
   if(selectedBusinessId||e.target.closest('button,a,input,select,textarea'))return;
   const row=e.target.closest('#businessesList .account,#businessesList .business-card,#businessesList .biz-card');
   if(!row)return;
   const strong=row.querySelector('strong');if(!strong)return;
   const b=(state.businesses||[]).find(x=>norm(x.name)===norm(strong.textContent));if(b)openBusinessDetail(b.id);
 });
 const categoryChooser=document.getElementById('bizSettingsBusiness');
 if(categoryChooser)categoryChooser.addEventListener('change',()=>{
   if(selectedBusinessId)categoryChooser.value=selectedBusinessId;
 });
 setTimeout(()=>{const panel=document.getElementById('businessCategorySettings');if(panel&&!selectedBusinessId){parking.appendChild(panel);panel.style.display='none'}decorateBusinesses()},180);
})();
</script>
"""
if "</body>" not in s: raise SystemExit("body closing tag not found before v5")
s=s.replace("</body>",v5+"</body>",1)
# Transaction form cards, nested business settings pages, and HPP calculator.
v6 = r"""
<style>
/* Transaction context cards */
#txModal #ruTxContext{display:grid;gap:9px;margin:0 0 12px;flex-shrink:0}
#ruTxContext .ru-tx-business{display:flex;align-items:center;gap:14px;padding:17px;border-radius:18px;background:linear-gradient(120deg,#172c64,#5368d7);color:white;box-shadow:0 7px 18px #5264ce28}
#ruTxContext .ru-tx-business-icon{height:58px;width:58px;display:grid;place-items:center;flex:0 0 58px;border-radius:17px;background:#ffffff24;font-size:32px}
#ruTxContext .ru-tx-eyebrow{font-size:10px;text-transform:uppercase;letter-spacing:1px;opacity:.8}
#ruTxContext .ru-tx-business-name{font-size:20px;font-weight:850;line-height:1.2;margin-top:4px;overflow-wrap:anywhere}
#ruTxContext .ru-tx-type{display:flex;align-items:center;gap:12px;padding:13px 15px;border-radius:15px;border:1px solid transparent}
#ruTxContext .ru-tx-type-icon{height:40px;width:40px;display:grid;place-items:center;border-radius:12px;font-size:22px;font-weight:850}
#ruTxContext .ru-tx-type strong{font-size:15px;display:block}
#ruTxContext .ru-tx-type small{font-size:11px;display:block;margin-top:3px;opacity:.78}
#ruTxContext .ru-tx-income{background:#e4f8ee;border-color:#c6edd8;color:#087647}
#ruTxContext .ru-tx-income .ru-tx-type-icon{background:#c6efd9}
#ruTxContext .ru-tx-expense{background:#fff0ef;border-color:#f4d1cf;color:#b72f38}
#ruTxContext .ru-tx-expense .ru-tx-type-icon{background:#ffd9d7}
#ruTxContext .ru-tx-transfer{background:#edf1ff;border-color:#d5dcff;color:#4655be}
#ruTxContext .ru-tx-transfer .ru-tx-type-icon{background:#dbe2ff}
#businessDetailLanding .business-menu-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:14px 0}
#businessDetailLanding .business-menu-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:15px 12px;text-align:left;min-height:106px;display:flex;flex-direction:column;gap:9px}
#businessDetailLanding .business-menu-card .menu-symbol{width:40px;height:40px;display:grid;place-items:center;background:#eef1ff;color:#4f5dc4;border-radius:13px;font-size:21px}
#businessDetailLanding .business-menu-card strong{font-size:14px}
#businessSubPage .business-sub-head{display:flex;align-items:center;gap:10px;margin-bottom:14px}
#businessSubPage .business-sub-head h2{font-size:19px;margin:0}
#businessSubPage #businessDetailSettings{padding:0}
#businessSubPage .biz-settings-panel{margin:0;background:transparent;border:0;padding:0}
#businessSubPage .hpp-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:15px;margin:12px 0}
#businessSubPage .hpp-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
#businessSubPage .hpp-result{background:#eff3ff;color:#3446ac;border-radius:14px;padding:14px;margin-top:12px}
#businessSubPage .hpp-result strong{font-size:21px;display:block;margin-top:6px}
#businessSubPage .hpp-history-row{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 0;border-bottom:1px solid var(--line)}
#businessSubPage .hpp-history-row small{display:block;color:var(--muted);font-size:11px;margin-top:4px}
@media(max-width:700px){
 #txModal #ruTxContext .ru-tx-business{padding:15px;border-radius:17px}
 #ruTxContext .ru-tx-business-icon{width:52px;height:52px;flex-basis:52px;font-size:28px}
 #ruTxContext .ru-tx-business-name{font-size:18px}
 #businessDetailLanding .business-menu-card{min-height:100px;padding:12px}
 #businessSubPage .hpp-grid{grid-template-columns:1fr}
}
</style>
<script>
(function(){
 const normName=v=>String(v||'').trim().toLowerCase();
 function iconBusiness(b){
   const n=normName(b&&b.name);
   if(/studio|foto|fotografi|cetak/.test(n))return '📷';
   if(/wifi|internet|net/.test(n))return '📡';
   if(/cctv|alarm|security|sentinel|keamanan/.test(n))return '🛡️';
   if(/delivery|gelis|antar|kurir/.test(n))return '🛵';
   return '🏪';
 }
 function txTypeMeta(type){
   if(type==='income')return {title:'Pemasukan',sub:'Uang masuk ke usaha',icon:'↙',cls:'income'};
   if(type==='expense')return {title:'Pengeluaran',sub:'Biaya yang dikeluarkan usaha',icon:'↗',cls:'expense'};
   return {title:'Transfer antar dompet',sub:'Pindahkan saldo dari satu dompet ke dompet lain',icon:'⇄',cls:'transfer'};
 }
 function drawTxContext(){
   const modal=document.getElementById('txModal'),typeEl=document.getElementById('fType'),bizEl=document.getElementById('fBusiness');
   if(!modal||!typeEl||!bizEl)return;
   const form=typeEl.closest('form');if(!form)return;
   const type=typeEl.value,meta=txTypeMeta(type),biz=(state.businesses||[]).find(b=>b.id===bizEl.value);
   const typeField=typeEl.closest('.field'),bizField=bizEl.closest('.field');
   if(typeField)typeField.style.display='none';
   if(bizField)bizField.style.display='none';
   let box=document.getElementById('ruTxContext');
   if(!box){box=document.createElement('div');box.id='ruTxContext';form.insertBefore(box,form.firstChild)}
   const businessCard=type==='transfer'?'':'<div class="ru-tx-business"><div class="ru-tx-business-icon">'+iconBusiness(biz)+'</div><div style="min-width:0"><div class="ru-tx-eyebrow">Usaha yang digunakan</div><div class="ru-tx-business-name">'+esc(biz?biz.name:'Usaha belum dipilih')+'</div></div></div>';
   box.innerHTML=businessCard+'<div class="ru-tx-type ru-tx-'+meta.cls+'"><div class="ru-tx-type-icon">'+meta.icon+'</div><div><strong>'+meta.title+'</strong><small>'+meta.sub+'</small></div></div>';
 }
 const origOpenForm=window.openTransactionForm;
 if(typeof origOpenForm==='function')window.openTransactionForm=function(id,presetBusiness){origOpenForm(id,presetBusiness);setTimeout(drawTxContext,0)};
 const origTyped=window.startTypedTransaction;
 if(typeof origTyped==='function')window.startTypedTransaction=function(type){origTyped(type);setTimeout(drawTxContext,80)};
 const origChoose=window.chooseBusinessTyped;
 if(typeof origChoose==='function')window.chooseBusinessTyped=function(id){origChoose(id);setTimeout(drawTxContext,80)};
 window.openTransactionForBusiness=function(type,id){
   if(typeof window.openTransactionForm!=='function')return;
   window.openTransactionForm('',id);
   const typeEl=document.getElementById('fType'),bizEl=document.getElementById('fBusiness');
   if(typeEl)typeEl.value=type;
   if(bizEl)bizEl.value=id||'';
   if(typeof window.updateTxForm==='function')window.updateTxForm();
   const title=document.getElementById('txModalTitle'),b=(state.businesses||[]).find(x=>x.id===id);
   if(title)title.textContent=(type==='income'?'Catat pemasukan — ':'Catat pengeluaran — ')+(b?b.name:'Usaha');
   drawTxContext();
 };
 document.getElementById('txModal')&&new MutationObserver(()=>setTimeout(drawTxContext,0)).observe(document.getElementById('txModal'),{attributes:true,attributeFilter:['style','class']});
 document.getElementById('fType')&&document.getElementById('fType').addEventListener('change',drawTxContext);
 document.getElementById('fBusiness')&&document.getElementById('fBusiness').addEventListener('change',drawTxContext);

 // Business pages: the business landing page shows statistics and links only.
 const origOpenBusiness=window.openBusinessDetail;
 const origCloseBusiness=window.closeBusinessDetail;
 let activeBizId=null,activeSub='overview';
 function businessById(id){return (state.businesses||[]).find(b=>b.id===id)}
 function fmtDate(v){return String(v||'').slice(0,10)}
 function bizTx(id){return (state.transactions||[]).filter(t=>t.businessId===id)}
 function recentRows(id){
   return bizTx(id).slice().sort((a,b)=>String(b.date||'').localeCompare(String(a.date||''))).slice(0,6).map(t=>'<div class="business-detail-transaction"><div><strong>'+esc(t.note||(t.type==='income'?'Pemasukan':t.type==='expense'?'Pengeluaran':'Transfer'))+'</strong><small>'+esc(fmtDate(t.date))+' · '+esc(t.type==='transfer'?'Transfer':(typeof categoryName==='function'?categoryName(t.categoryId):''))+'</small></div><strong style="white-space:nowrap;color:'+(t.type==='income'?'var(--green)':t.type==='expense'?'var(--red)':'var(--blue)')+'">'+(t.type==='expense'?'−':t.type==='income'?'+':'')+money(t.amount)+'</strong></div>').join('')||'<div class="desc">Belum ada transaksi untuk usaha ini.</div>'
 }
 function refreshBusinessOverview(){
   const b=businessById(activeBizId);if(!b)return;
   const month=typeof monthNow==='function'?monthNow():new Date().toISOString().slice(0,7);
   const monthTx=bizTx(activeBizId).filter(t=>String(t.date||'').startsWith(month));
   const st=totals(monthTx);
   const target=document.getElementById('businessCustomStats');
   if(target)target.innerHTML='<div class="business-stat"><small>Pemasukan bulan ini</small><strong style="color:var(--green)">'+money(st.inc)+'</strong></div><div class="business-stat"><small>Pengeluaran bulan ini</small><strong style="color:var(--red)">'+money(st.out)+'</strong></div><div class="business-stat"><small>Arus kas bersih</small><strong style="color:var(--blue)">'+money(st.net)+'</strong></div><div class="business-stat"><small>Total transaksi</small><strong>'+bizTx(activeBizId).length+'</strong></div>';
   const rt=document.getElementById('businessCustomRecent');if(rt)rt.innerHTML=recentRows(activeBizId);
 }
 function closeBusinessSub(){
   activeSub='overview';
   const detail=document.getElementById('businessDetailView');
   if(detail){
     const oldPanel=document.getElementById('businessCategorySettings'),parking=document.getElementById('businessSettingsParking');
     if(oldPanel&&parking)parking.appendChild(oldPanel);
     oldPanel&&(oldPanel.style.display='none');
     detail.innerHTML=detailLandingHtml();
   }
   refreshBusinessOverview();
   window.scrollTo(0,0);
 }
 function detailLandingHtml(){
   const b=businessById(activeBizId);if(!b)return '<button class="small" onclick="closeBusinessDetail()">← Kembali</button>';
   return '<div class="business-detail-top"><button type="button" class="small business-detail-back" onclick="closeBusinessDetail()">← Kembali</button><div class="business-detail-logo">'+iconBusiness(b)+'</div><div style="min-width:0"><h1 class="business-detail-title">'+esc(b.name)+'</h1><div class="business-detail-kind">'+esc(b.type||'Usaha')+'</div></div></div><div class="desc">Ringkasan kinerja usaha untuk bulan berjalan.</div><div class="business-stat-grid" id="businessCustomStats"></div><div class="business-detail-actions"><button type="button" class="primary" id="businessDetailIncome">＋ Pemasukan</button><button type="button" id="businessDetailExpense">－ Pengeluaran</button></div><h2 class="business-section-heading">Pengaturan dan alat usaha</h2><div class="business-menu-grid"><button type="button" class="business-menu-card" onclick="openBusinessSubPage(\'categories\')"><span class="menu-symbol">▤</span><strong>Kategori usaha</strong></button><button type="button" class="business-menu-card" onclick="openBusinessSubPage(\'products\')"><span class="menu-symbol">▣</span><strong>Produk usaha</strong></button><button type="button" class="business-menu-card" onclick="openBusinessSubPage(\'hpp\')"><span class="menu-symbol">∑</span><strong>Perhitungan HPP</strong></button></div><h2 class="business-section-heading">Transaksi terbaru</h2><div id="businessCustomRecent"></div>';
 }
 window.openBusinessDetail=function(id){
   if(typeof origOpenBusiness==='function')origOpenBusiness(id);
   activeBizId=id;activeSub='overview';
   const detail=document.getElementById('businessDetailView'),parking=document.getElementById('businessSettingsParking'),panel=document.getElementById('businessCategorySettings');
   if(panel&&parking)parking.appendChild(panel);
   if(detail)detail.innerHTML=detailLandingHtml();
   const inc=document.getElementById('businessDetailIncome'),out=document.getElementById('businessDetailExpense');
   if(inc)inc.onclick=()=>openTransactionForBusiness('income',id);
   if(out)out.onclick=()=>openTransactionForBusiness('expense',id);
   refreshBusinessOverview();window.scrollTo(0,0);
 };
 window.closeBusinessDetail=function(){
   if(typeof origCloseBusiness==='function')origCloseBusiness();
   activeBizId=null;activeSub='overview';
   const panel=document.getElementById('businessCategorySettings'),parking=document.getElementById('businessSettingsParking');
   if(panel&&parking)parking.appendChild(panel);
   if(panel)panel.style.display='none';
   const detail=document.getElementById('businessDetailView');if(detail)detail.style.display='none';
 };
 window.openBusinessSubPage=function(kind){
   if(!businessById(activeBizId))return;
   activeSub=kind;
   const detail=document.getElementById('businessDetailView');
   if(!detail)return;
   if(kind==='categories'||kind==='products'){
     detail.innerHTML='<div class="business-sub-head"><button type="button" class="small" onclick="closeBusinessSub()">← Kembali</button><div><h2>'+(kind==='categories'?'Kategori usaha':'Produk usaha')+'</h2><div class="desc">'+esc(businessById(activeBizId).name)+'</div></div></div><div id="businessDetailSettings"></div>';
     const panel=document.getElementById('businessCategorySettings'),parking=document.getElementById('businessSettingsParking');
     if(panel&&parking)parking.appendChild(panel);
     if(typeof renderBusinessCategorySettings==='function')renderBusinessCategorySettings();
     const p=document.getElementById('businessCategorySettings');
     if(p){
       p.style.display='block';
       const heads=[...p.querySelectorAll('.panel-head')],chooser=p.querySelector('.field');
       if(heads[0])heads[0].style.display='none';
       if(chooser)chooser.style.display='none';
       const cat=document.getElementById('bizSettingsCategories'),prod=document.getElementById('bizSettingsProducts');
       if(cat)cat.style.display=kind==='categories'?'block':'none';
       if(prod)prod.style.display=kind==='products'?'block':'none';
       if(heads[1])heads[1].style.display=kind==='categories'?'flex':'none';
       if(heads[2])heads[2].style.display=kind==='products'?'flex':'none';
     }
     window.scrollTo(0,0);return;
   }
   if(kind==='hpp'){renderHppPage();return}
 };
 function renderHppPage(){
   const detail=document.getElementById('businessDetailView'),b=businessById(activeBizId);if(!detail||!b)return;
   if(!Array.isArray(state.hppRecords))state.hppRecords=[];
   detail.innerHTML='<div class="business-sub-head"><button type="button" class="small" onclick="closeBusinessSub()">← Kembali</button><div><h2>Perhitungan HPP</h2><div class="desc">'+esc(b.name)+'</div></div></div><div class="hpp-card"><div class="desc">Harga Pokok Produksi per unit = (bahan baku + tenaga kerja + overhead) ÷ jumlah unit yang dihasilkan.</div><form id="hppForm"><div class="field"><label>Nama produk</label><input id="hppName" required maxlength="100" placeholder="Contoh: Cetak foto 10R"></div><div class="field"><label>Jumlah unit yang dihasilkan</label><input id="hppQty" required type="number" min="0.001" step="any" value="1"></div><div class="hpp-grid"><div class="field"><label>Total bahan baku (Rp)</label><input id="hppMaterial" required type="number" min="0" step="1" value="0"></div><div class="field"><label>Total tenaga kerja (Rp)</label><input id="hppLabor" required type="number" min="0" step="1" value="0"></div><div class="field" style="grid-column:1/-1"><label>Overhead / biaya produksi lain (Rp)</label><input id="hppOverhead" required type="number" min="0" step="1" value="0"></div></div><div class="hpp-result"><small>Total biaya produksi</small><strong id="hppTotal">Rp0</strong><small style="display:block;margin-top:10px">HPP per unit</small><strong id="hppUnit">Rp0</strong></div><div class="form-actions" style="margin-top:14px"><button type="button" onclick="closeBusinessSub()">Batal</button><button type="submit" class="primary">Simpan perhitungan</button></div></form></div><h2 class="business-section-heading">Riwayat HPP usaha ini</h2><div id="hppHistory"></div>';
   const calc=()=>{const q=Number(document.getElementById('hppQty').value)||0,m=Number(document.getElementById('hppMaterial').value)||0,l=Number(document.getElementById('hppLabor').value)||0,o=Number(document.getElementById('hppOverhead').value)||0,total=m+l+o,unit=q>0?total/q:0;document.getElementById('hppTotal').textContent=money(total);document.getElementById('hppUnit').textContent=money(unit);return {q,m,l,o,total,unit}};
   document.getElementById('hppForm').querySelectorAll('input').forEach(el=>el.addEventListener('input',calc));
   const hppRender=()=>{const list=(state.hppRecords||[]).filter(x=>x.businessId===activeBizId).slice().reverse();document.getElementById('hppHistory').innerHTML=list.map(x=>'<div class="hpp-history-row"><div><strong>'+esc(x.productName)+'</strong><small>'+esc(x.date)+' · '+x.quantity+' unit · Total '+money(x.totalCost)+'</small></div><strong>'+money(x.unitCost)+'/unit</strong></div>').join('')||'<div class="desc">Belum ada perhitungan HPP disimpan.</div>'};
   document.getElementById('hppForm').addEventListener('submit',e=>{e.preventDefault();const v=calc(),name=document.getElementById('hppName').value.trim();if(!name||v.q<=0)return alert('Isi nama produk dan jumlah unit lebih dari nol.');if(!Array.isArray(state.hppRecords))state.hppRecords=[];state.hppRecords.push({id:uid(),businessId:activeBizId,productName:name,quantity:v.q,materialCost:v.m,laborCost:v.l,overheadCost:v.o,totalCost:v.total,unitCost:v.unit,date:new Date().toISOString().slice(0,10)});save();showToast('Perhitungan HPP disimpan.');renderHppPage()});
   calc();hppRender();
 }
 // Keep product/category settings inside the dedicated subpage rather than the business list.
 const oldSettingsRenderer=window.renderBusinessCategorySettings;
 if(typeof oldSettingsRenderer==='function')window.renderBusinessCategorySettings=function(){oldSettingsRenderer();if(activeBizId&&activeSub!=='overview')setTimeout(()=>{const p=document.getElementById('businessCategorySettings');if(p)p.style.display='block'},0)};
})();
</script>
"""
if "</body>" not in s: raise SystemExit("body closing tag not found before v6")

s=s.replace("</body>",v6+"</body>",1)
# Photo-enabled business cards, reliable Android Back behavior, and itemized raw-material HPP.
v7 = r"""
<style>
/* Elegant business cards with individual photos */
#businessesList.ru-business-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.ru-business-card{min-width:0;overflow:hidden;position:relative;background:#fff;border:1px solid #e9eaf1;border-radius:19px;box-shadow:0 5px 18px #2024470a;cursor:pointer;transition:transform .15s,box-shadow .15s}
.ru-business-card:active,.ru-dashboard-business:active{transform:scale(.985)}
.ru-business-cover{height:124px;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#e7edff,#dff7f2 58%,#f4efff)}
.ru-business-cover img{width:100%;height:100%;object-fit:cover;display:block}
.ru-business-cover-fallback{display:flex;align-items:center;justify-content:center;width:68px;height:68px;border-radius:22px;background:#ffffffb8;box-shadow:0 7px 20px #282b4e12;font-size:36px}
.ru-business-photo-btn{position:absolute;right:9px;top:9px;width:34px;height:34px;border:0;border-radius:12px;background:#11182a99;color:#fff;display:grid;place-items:center;font-size:16px;backdrop-filter:blur(8px)}
.ru-business-info{padding:12px 12px 8px}
.ru-business-name{font-size:14px;font-weight:800;line-height:1.25;overflow-wrap:anywhere}
.ru-business-type{font-size:11px;color:var(--muted);margin-top:5px;min-height:28px;line-height:1.35;overflow-wrap:anywhere}
.ru-business-status{display:inline-flex;font-size:10px;font-weight:700;border-radius:20px;padding:4px 8px;background:#edf7f4;color:#187a66;margin-top:8px}
.ru-business-status.archived{background:#f4f1f1;color:#7e6262}
.ru-business-actions{display:flex;border-top:1px solid #f0f0f5;padding:8px;gap:7px}
.ru-business-actions button{flex:1;font-size:11px;min-width:0;padding:7px 3px;border-radius:9px;background:#f5f6fb;color:#424861}
.ru-business-actions button.archive{color:#8d5d5d}
#businessesList .empty{grid-column:1/-1}
.ru-photo-picker{display:none!important}
#businessDetailView .business-detail-logo{overflow:hidden}
#businessDetailView .business-detail-logo img{width:100%;height:100%;object-fit:cover;display:block}
.ru-detail-photo{display:inline-flex;align-items:center;gap:6px;margin:8px 0 0;padding:7px 10px!important;border-radius:10px!important;background:#eef1ff!important;color:#4a57b8!important;font-size:11px!important}
#businessPerformance{display:grid;gap:12px}
.ru-dashboard-business{position:relative;cursor:pointer;background:#fff!important;border:1px solid #e9eaf2!important;border-radius:19px!important;padding:15px!important;box-shadow:0 6px 20px #2024470a!important;transition:transform .15s;min-width:0}
.ru-dashboard-business .biz-head{align-items:center;gap:11px}
.ru-dashboard-business .biz-icon{width:53px!important;height:53px!important;flex:0 0 53px!important;border-radius:16px!important;background:linear-gradient(135deg,#e6edff,#e1f7f0)!important;color:#4d5bc5!important;font-size:26px!important;overflow:hidden}
.ru-dashboard-business .biz-icon img{height:100%;width:100%;object-fit:cover;display:block}
.ru-dashboard-business .biz-name{font-size:15px!important;font-weight:850!important}
.ru-dashboard-business .biz-type{font-size:11px!important;line-height:1.3;margin-top:3px}
.ru-dashboard-business .biz-open{font-size:10px;padding:5px 8px}
.ru-dashboard-business .biz-actions{display:none!important}
.ru-dashboard-business .biz-stats{margin-top:13px;padding-top:12px;gap:8px}
.ru-dashboard-business .biz-stats>div{min-width:0}
.ru-dashboard-business .biz-stats small{font-size:10px}
.ru-dashboard-business .biz-stats strong{font-size:clamp(11px,3.5vw,15px);overflow-wrap:anywhere}
.ru-dashboard-business::after{content:"›";position:absolute;right:14px;top:16px;font-size:23px;line-height:1;color:#9ba2b7;pointer-events:none}
#businessSubPage .hpp-material-row{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(52px,.55fr) minmax(82px,.85fr) 32px;gap:7px;align-items:end;background:#f8f9fc;border:1px solid var(--line);padding:9px;border-radius:13px;margin:8px 0}
#businessSubPage .hpp-material-row .field{min-width:0}
#businessSubPage .hpp-material-row label{font-size:10px}
#businessSubPage .hpp-material-row input{min-width:0;width:100%;padding:9px 6px;font-size:13px}
#businessSubPage .hpp-material-row button{padding:8px 6px;min-height:39px}
#businessSubPage .hpp-material-total{display:flex;justify-content:space-between;align-items:center;background:#f0f4ff;padding:12px;border-radius:12px;margin-top:9px}
#businessSubPage .hpp-material-total strong{color:#4657bf}
@media(max-width:700px){
 #businessesList.ru-business-grid{gap:9px}
 .ru-business-cover{height:104px}
 .ru-business-info{padding:10px 9px 7px}
 .ru-business-name{font-size:13px}
 .ru-business-type{font-size:10px;min-height:27px}
 .ru-business-actions{padding:7px 6px;gap:5px}
 .ru-business-actions button{font-size:10px}
 .ru-dashboard-business{padding:13px!important}
 .ru-dashboard-business .biz-open{margin-right:16px}
 #businessSubPage .hpp-material-row{grid-template-columns:minmax(0,1fr) 55px minmax(76px,.8fr) 30px;gap:4px;padding:6px}
 #businessSubPage .hpp-material-row input{font-size:12px;padding:8px 4px}
}
</style>
<script>
(function(){
 const normal=v=>String(v||'').trim().toLowerCase();
 const iconFor=b=>{
   const n=normal(b&&b.name);
   if(/studio|foto|fotografi|cetak|print/.test(n))return '📷';
   if(/wifi|internet|net/.test(n))return '📡';
   if(/cctv|alarm|security|sentinel|keamanan/.test(n))return '🛡️';
   if(/delivery|gelis|antar|kurir/.test(n))return '🛵';
   if(/kuliner|makan|warung|cafe/.test(n))return '🍜';
   return '🏪';
 };
 function addPhotoView(id){
   const b=(state.businesses||[]).find(x=>x.id===id),detail=document.getElementById('businessDetailView');
   if(!b||!detail)return;
   let logo=detail.querySelector('.business-detail-logo');
   if(logo)logo.innerHTML=b.photoData?'<img alt="Foto usaha" src="'+b.photoData+'">':iconFor(b);
   const title=detail.querySelector('.business-detail-title');
   if(title){
     let holder=detail.querySelector('.ru-photo-control');
     if(!holder){
       holder=document.createElement('div');holder.className='ru-photo-control';
       holder.innerHTML='<button type="button" class="ru-detail-photo">📷 Ganti foto usaha</button><input class="ru-photo-picker" type="file" accept="image/*">';
       title.parentElement.appendChild(holder);
       const btn=holder.querySelector('button'),input=holder.querySelector('input');
       btn.addEventListener('click',e=>{e.stopPropagation();input.click()});
       input.addEventListener('change',e=>savePhotoFile(id,e.target.files&&e.target.files[0],()=>addPhotoView(id)));
     }
   }
 }
 function savePhotoFile(id,file,done){
   if(!file)return;
   if(!/^image\//.test(file.type||''))return alert('Pilih file gambar untuk foto usaha.');
   const reader=new FileReader();
   reader.onerror=()=>alert('Foto tidak dapat dibaca.');
   reader.onload=()=>{
     const img=new Image();
     img.onerror=()=>alert('File gambar tidak valid.');
     img.onload=()=>{
       try{
         const maxW=800,maxH=600,scale=Math.min(1,maxW/img.width,maxH/img.height),w=Math.max(1,Math.round(img.width*scale)),h=Math.max(1,Math.round(img.height*scale)),canvas=document.createElement('canvas');
         canvas.width=w;canvas.height=h;canvas.getContext('2d').drawImage(img,0,0,w,h);
         const data=canvas.toDataURL('image/jpeg',.74),b=(state.businesses||[]).find(x=>x.id===id);if(!b)return;
         b.photoData=data;save();
         if(typeof done==='function')done();
         showToast('Foto usaha berhasil disimpan.');
       }catch(err){alert('Foto tidak dapat disimpan. Pilih gambar yang lebih kecil.')}
     };
     img.src=String(reader.result||'');
   };
   reader.readAsDataURL(file);
 }
 function renderBusinessCards(){
   const list=document.getElementById('businessesList');if(!list)return;
   list.classList.add('ru-business-grid');
   list.innerHTML='';
   const items=state.businesses||[];
   if(!items.length){list.innerHTML='<div class="empty">Belum ada usaha. Tekan Tambah usaha untuk memulai.</div>';return;}
   items.forEach(b=>{
     const card=document.createElement('article');card.className='ru-business-card';card.tabIndex=0;card.setAttribute('role','button');card.setAttribute('aria-label','Buka detail '+b.name);
     const cover=document.createElement('div');cover.className='ru-business-cover';
     if(b.photoData){const img=document.createElement('img');img.src=b.photoData;img.alt='Foto '+b.name;cover.appendChild(img)}
     else{const mark=document.createElement('div');mark.className='ru-business-cover-fallback';mark.textContent=iconFor(b);cover.appendChild(mark)}
     const choose=document.createElement('button');choose.type='button';choose.className='ru-business-photo-btn';choose.title='Pilih foto usaha';choose.textContent='📷';
     const input=document.createElement('input');input.type='file';input.accept='image/*';input.className='ru-photo-picker';
     choose.addEventListener('click',e=>{e.stopPropagation();input.click()});
     input.addEventListener('click',e=>e.stopPropagation());
     input.addEventListener('change',e=>savePhotoFile(b.id,e.target.files&&e.target.files[0],()=>renderBusinessCards()));
     cover.append(choose,input);
     const info=document.createElement('div');info.className='ru-business-info';
     const name=document.createElement('div');name.className='ru-business-name';name.textContent=b.name;
     const type=document.createElement('div');type.className='ru-business-type';type.textContent=b.type||'Usaha';
     const status=document.createElement('span');status.className='ru-business-status'+(b.archived?' archived':'');status.textContent=b.archived?'Diarsipkan':'Aktif';
     info.append(name,type,status);
     const nowMonth=typeof monthNow==='function'?monthNow():new Date().toISOString().slice(0,7);
     const txs=(state.transactions||[]).filter(t=>t.businessId===b.id),monthTx=txs.filter(t=>String(t.date||'').startsWith(nowMonth));
     const sum=typeof totals==='function'?totals(monthTx):{inc:0,out:0,net:0};
     const statGrid=document.createElement('div');statGrid.className='ru-business-stat-grid';
     statGrid.innerHTML='<div class="ru-business-stat"><small>Pemasukan bulan ini</small><strong style="color:var(--green)">'+money(sum.inc)+'</strong></div><div class="ru-business-stat"><small>Pengeluaran bulan ini</small><strong style="color:var(--red)">'+money(sum.out)+'</strong></div><div class="ru-business-stat"><small>Arus kas bersih</small><strong style="color:var(--blue)">'+money(sum.net)+'</strong></div><div class="ru-business-stat"><small>Total transaksi</small><strong>'+txs.length+'</strong></div>';
     const actions=document.createElement('div');actions.className='ru-business-actions';
     const edit=document.createElement('button');edit.type='button';edit.textContent='Edit';edit.addEventListener('click',e=>{e.stopPropagation();openBusiness(b.id)});
     const archive=document.createElement('button');archive.type='button';archive.className='archive';archive.textContent=b.archived?'Aktifkan':'Arsipkan';archive.addEventListener('click',e=>{e.stopPropagation();toggleBusinessArchive(b.id);});
     actions.append(edit,archive);
     card.append(cover,info,statGrid,actions);
     card.addEventListener('click',()=>window.openBusinessDetail(b.id));
     card.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();window.openBusinessDetail(b.id)}});
     list.appendChild(card);
   });
 }
 const baseRenderBusinesses=window.renderBusinesses;
 if(typeof baseRenderBusinesses==='function')window.renderBusinesses=function(){baseRenderBusinesses();renderBusinessCards()};
 const baseRenderDashboard=window.renderBusinessDashboard;
 function decorateDashboardCards(){
   const host=document.getElementById('businessPerformance');if(!host)return;
   host.querySelectorAll('.biz-card').forEach(card=>{
     const title=card.querySelector('.biz-name'),name=title?title.textContent:'',b=(state.businesses||[]).find(x=>normal(x.name)===normal(name));
     if(!b)return;
     card.classList.add('ru-dashboard-business');card.setAttribute('role','button');card.setAttribute('tabindex','0');card.setAttribute('aria-label','Lihat detail usaha '+b.name);
     card.querySelector('.biz-actions')?.remove();
     const icon=card.querySelector('.biz-icon');
     if(icon)icon.innerHTML=b.photoData?'<img alt="" src="'+b.photoData+'">':iconFor(b);
     card.onclick=()=>window.openBusinessDetail(b.id);
     card.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();window.openBusinessDetail(b.id)}};
   });
 }
 if(typeof baseRenderDashboard==='function')window.renderBusinessDashboard=function(){baseRenderDashboard();decorateDashboardCards()};
 const baseOpenBusiness=window.openBusinessDetail;
 let currentBusiness=null;
 window.openBusinessDetail=function(id){
   const result=baseOpenBusiness&&baseOpenBusiness(id);
   currentBusiness=id;window.ruCurrentBusinessId=id;
   addPhotoView(id);
   if(!window.ruUseSingleNavigationStack&&!window.ruSuppressLegacyHistory&&!window.ruSuppressBusinessHistory)pushUi('business',id);
   return result;
 };
 const baseCloseBusiness=window.closeBusinessDetail;
 function restoreDetail(id){
   currentBusiness=id||currentBusiness;
   if(currentBusiness&&baseOpenBusiness){
     window.ruSuppressBusinessHistory=true;baseOpenBusiness(currentBusiness);window.ruSuppressBusinessHistory=false;
     addPhotoView(currentBusiness);
   }
 }
 window.closeBusinessDetail=function(){
   const id=currentBusiness;
   if(baseCloseBusiness)baseCloseBusiness();
   currentBusiness=null;window.ruCurrentBusinessId=null;
   if(!window.ruUseSingleNavigationStack&&!window.ruSuppressLegacyHistory)if(!window.ruUseSingleNavigationStack&&!window.ruSuppressLegacyHistory)finishUiBack('business',id);
 };
 // Browser history also drives Android's native Back button via WebView.goBack().
 const uiStack=[];let uiSeq=0,pendingUiBack=false,suppressPageHistory=false;
 function pushUi(kind,id,from){
   const top=uiStack[uiStack.length-1];
   if(top&&top.kind===kind&&top.id===id)return;
   uiSeq++;const item={kind,id,from,seq:uiSeq};uiStack.push(item);
   try{history.pushState({ruApp:true,seq:uiSeq},'','#ru-'+kind+'-'+uiSeq)}catch(e){}
 }
 function finishUiBack(kind,id){
   const top=uiStack[uiStack.length-1];
   if(top&&top.kind===kind&&(id==null||top.id===id)&&history.state&&history.state.ruApp){
     pendingUiBack=true;history.back();
   }
 }
 const baseGo=window.go;
 let pageBeforeNav=null;
 window.go=function(page){
   const active=document.querySelector('.section.active'),from=active?active.id.replace('page-',''):'dashboard';
   if(!window.ruUseSingleNavigationStack&&!window.ruSuppressLegacyHistory&&!suppressPageHistory&&from!==page)pushUi('page',from);
   if(typeof baseGo==='function')baseGo(page);
 };
 const originalCloseModal=window.closeModal;
 window.closeModal=function(id){
   if(typeof originalCloseModal==='function')originalCloseModal(id);
   else{const el=document.getElementById(id);if(el)el.style.display='none'}
   const top=uiStack[uiStack.length-1];
   if(!window.ruUseSingleNavigationStack&&!window.ruSuppressLegacyHistory)if(!window.ruUseSingleNavigationStack&&!window.ruSuppressLegacyHistory)finishUiBack('modal',id);
   updateBodyLock();
 };
 function updateBodyLock(){
   const visible=[...document.querySelectorAll('.modal-backdrop')].some(el=>getComputedStyle(el).display!=='none');
   if(visible){document.body.style.overflow='hidden';document.body.style.overscrollBehavior='none'}
   else{document.body.style.overflow='';document.body.style.overscrollBehavior=''}
 }
 function topVisibleModal(){
   return [...document.querySelectorAll('.modal-backdrop')].reverse().find(el=>getComputedStyle(el).display!=='none');
 }
 function observeModalOpen(){
   if(window.ruUseSingleNavigationStack){updateBodyLock();return}
   const visible=topVisibleModal();
   if(visible){
     const top=uiStack[uiStack.length-1];
     if(!top||top.kind!=='modal'||top.id!==visible.id)pushUi('modal',visible.id);
   }
   updateBodyLock();
 }
 document.querySelectorAll('.modal-backdrop').forEach(el=>{
   new MutationObserver(()=>setTimeout(observeModalOpen,40)).observe(el,{attributes:true,attributeFilter:['style','class']});
 });
 window.addEventListener('popstate',()=>{
   const entry=uiStack.pop();
   if(pendingUiBack){pendingUiBack=false;updateBodyLock();return}
   if(entry){
     if(entry.kind==='modal'){const el=document.getElementById(entry.id);if(el)el.style.display='none';updateBodyLock();return}
     if(entry.kind==='subpage'){restoreDetail(entry.id);return}
     if(entry.kind==='business'){if(baseCloseBusiness)baseCloseBusiness();currentBusiness=null;window.ruCurrentBusinessId=null;return}
     if(entry.kind==='page'){suppressPageHistory=true;if(typeof baseGo==='function')baseGo(entry.id||'dashboard');suppressPageHistory=false;return}
   }
   const active=document.querySelector('.section.active');
   if(active&&active.id!=='page-dashboard'){suppressPageHistory=true;if(typeof baseGo==='function')baseGo('dashboard');suppressPageHistory=false}
 });
 // Both visible back buttons and Android hardware Back use this global function.
 window.closeBusinessSub=function(){
   const top=uiStack[uiStack.length-1];
   if(top&&top.kind==='subpage'&&history.state&&history.state.ruApp){pendingUiBack=true;history.back()}
   else if(currentBusiness)restoreDetail(currentBusiness);
 };
 const baseOpenSub=window.openBusinessSubPage;
 window.openBusinessSubPage=function(kind){
   const id=currentBusiness||window.ruCurrentBusinessId;if(!id)return;
   if(!window.ruUseSingleNavigationStack&&!window.ruSuppressLegacyHistory)if(!window.ruUseSingleNavigationStack&&!window.ruSuppressLegacyHistory)pushUi('subpage',id);
   if(kind==='categories'||kind==='products'){
     if(typeof baseOpenSub==='function')baseOpenSub(kind);
     setTimeout(()=>{
       const panel=document.getElementById('businessCategorySettings');
       if(panel)panel.style.display='block';
       const heads=panel?[...panel.querySelectorAll('.panel-head')]:[];
       if(heads[0])heads[0].style.display='none';
       const chooser=panel&&panel.querySelector('.field');if(chooser)chooser.style.display='none';
       const cats=document.getElementById('bizSettingsCategories'),products=document.getElementById('bizSettingsProducts');
       if(cats)cats.style.display=kind==='categories'?'block':'none';
       if(products)products.style.display=kind==='products'?'block':'none';
       if(heads[1])heads[1].style.display=kind==='categories'?'flex':'none';
       if(heads[2])heads[2].style.display=kind==='products'?'flex':'none';
     },0);
   }else if(kind==='hpp')renderHppWithMaterials(id);
 };
 function restoreCategoryProductVisibility(){
   const panel=document.getElementById('businessCategorySettings');if(panel)panel.style.display='none';
   restoreDetail(currentBusiness);
 }
 function renderHppWithMaterials(id){
   const detail=document.getElementById('businessDetailView'),b=(state.businesses||[]).find(x=>x.id===id);if(!detail||!b)return;
   if(!Array.isArray(state.hppRecords))state.hppRecords=[];
   detail.innerHTML='<div id="businessSubPage"><div class="business-sub-head"><button type="button" class="small" onclick="closeBusinessSub()">← Kembali</button><div><h2>Perhitungan HPP</h2><div class="desc">'+esc(b.name)+'</div></div></div><div class="hpp-card"><p class="desc">Masukkan bahan baku satu per satu. Total bahan baku dihitung dari jumlah × harga per unit, lalu ditambah tenaga kerja dan overhead.</p><form id="hppForm"><div class="field"><label>Nama produk yang dibuat</label><input id="hppName" required maxlength="100" placeholder="Contoh: Cetak foto 10R"></div><div class="field"><label>Jumlah produk yang dihasilkan (unit)</label><input id="hppQty" required type="number" min="0.001" step="any" value="1"></div><div class="panel-head" style="margin-top:16px"><div><h3>Bahan baku</h3><div class="desc">Contoh: kertas foto, tinta, laminasi, lem.</div></div><button type="button" class="small" id="hppAddMaterial">＋ Bahan baku</button></div><div id="hppMaterials"></div><div class="hpp-material-total"><span>Total bahan baku</span><strong id="hppMaterialTotal">Rp0</strong></div><div class="hpp-grid" style="margin-top:14px"><div class="field"><label>Total tenaga kerja (Rp)</label><input id="hppLabor" required type="number" min="0" step="1" value="0"></div><div class="field"><label>Overhead lain (Rp)</label><input id="hppOverhead" required type="number" min="0" step="1" value="0"></div></div><div class="hpp-result"><small>Total biaya produksi</small><strong id="hppTotal">Rp0</strong><small style="display:block;margin-top:10px">HPP per unit</small><strong id="hppUnit">Rp0</strong></div><div class="form-actions" style="margin-top:14px"><button type="button" onclick="closeBusinessSub()">Batal</button><button type="submit" class="primary">Simpan HPP</button></div></form></div><h2 class="business-section-heading">Riwayat HPP usaha ini</h2><div id="hppHistory"></div></div>';
   const materialsHost=document.getElementById('hppMaterials');
   function addMaterial(v){
     v=v||{};const row=document.createElement('div');row.className='hpp-material-row';
     const name=document.createElement('div');name.className='field';name.innerHTML='<label>Nama bahan</label>';
     const nameInput=document.createElement('input');nameInput.type='text';nameInput.className='hpp-m-name';nameInput.maxLength=80;nameInput.placeholder='Kertas foto, tinta…';nameInput.value=v.name||'';name.appendChild(nameInput);
     const qty=document.createElement('div');qty.className='field';qty.innerHTML='<label>Jumlah</label>';
     const qtyInput=document.createElement('input');qtyInput.type='number';qtyInput.className='hpp-m-qty';qtyInput.min='0';qtyInput.step='any';qtyInput.value=v.qty==null?'1':String(v.qty);qty.appendChild(qtyInput);
     const cost=document.createElement('div');cost.className='field';cost.innerHTML='<label>Harga/unit Rp</label>';
     const costInput=document.createElement('input');costInput.type='number';costInput.className='hpp-m-cost';costInput.min='0';costInput.step='1';costInput.placeholder='3000';costInput.value=v.unitCost==null?'':String(v.unitCost);cost.appendChild(costInput);
     const del=document.createElement('button');del.type='button';del.className='small danger';del.textContent='×';del.title='Hapus bahan';del.addEventListener('click',()=>{row.remove();calc()});
     [nameInput,qtyInput,costInput].forEach(el=>el.addEventListener('input',calc));
     row.append(name,qty,cost,del);materialsHost.appendChild(row);
   }
   function calc(){
     const materials=[...materialsHost.querySelectorAll('.hpp-material-row')].map(row=>({name:row.querySelector('.hpp-m-name').value.trim(),qty:Math.max(0,Number(row.querySelector('.hpp-m-qty').value)||0),unitCost:Math.max(0,Number(row.querySelector('.hpp-m-cost').value)||0)})).filter(x=>x.name);
     const materialCost=materials.reduce((n,m)=>n+m.qty*m.unitCost,0),labor=Number(document.getElementById('hppLabor').value)||0,overhead=Number(document.getElementById('hppOverhead').value)||0,qty=Number(document.getElementById('hppQty').value)||0,total=materialCost+labor+overhead,unit=qty>0?total/qty:0;
     document.getElementById('hppMaterialTotal').textContent=money(materialCost);document.getElementById('hppTotal').textContent=money(total);document.getElementById('hppUnit').textContent=money(unit);
     return {materials,materialCost,labor,overhead,qty,total,unit};
   }
   document.getElementById('hppAddMaterial').addEventListener('click',()=>{addMaterial();calc()});
   [document.getElementById('hppQty'),document.getElementById('hppLabor'),document.getElementById('hppOverhead')].forEach(el=>el.addEventListener('input',calc));
   document.getElementById('hppForm').addEventListener('submit',e=>{
     e.preventDefault();const v=calc(),name=document.getElementById('hppName').value.trim();
     if(!name||v.qty<=0)return alert('Isi nama produk dan jumlah unit yang valid.');
     if(!Array.isArray(state.hppRecords))state.hppRecords=[];
     state.hppRecords.push({id:uid(),businessId:id,productName:name,quantity:v.qty,materials:v.materials,materialCost:v.materialCost,laborCost:v.labor,overheadCost:v.overhead,totalCost:v.total,unitCost:v.unit,date:new Date().toISOString().slice(0,10)});
     save();showToast('HPP tersimpan.');renderHppWithMaterials(id);
   });
   addMaterial();calc();
   const history=(state.hppRecords||[]).filter(x=>x.businessId===id).slice().reverse();
   document.getElementById('hppHistory').innerHTML=history.map(x=>{
     const materialDesc=(x.materials||[]).map(m=>esc(m.name)+' ('+m.qty+' × '+money(m.unitCost)+')').join(', ');
     return '<div class="hpp-history-row"><div><strong>'+esc(x.productName)+'</strong><small>'+esc(x.date)+' · '+x.quantity+' unit'+(materialDesc?' · '+materialDesc:'')+'</small></div><strong>'+money(x.unitCost)+'/unit</strong></div>';
   }).join('')||'<div class="desc">Belum ada perhitungan HPP untuk usaha ini.</div>';
 }
 // Coordinated history stack: Android WebView's Back button closes overlays/subpages first, then returns between tabs.
  const ruUiStack=[];let ruUiSeq=0,ruPendingUiBack=false,ruSuppressGoHistory=false;
  function pushUi(kind,id,from){
    const top=ruUiStack[ruUiStack.length-1];
    if(top&&top.kind===kind&&top.id===id)return;
    const seq=++ruUiSeq;ruUiStack.push({kind,id,from,seq});
    try{history.pushState({ruApp:true,ruSeq:seq},'','#ru-'+kind+'-'+seq)}catch(err){}
  }
  function finishUiBack(kind,id){
    const top=ruUiStack[ruUiStack.length-1];
    if(top&&top.kind===kind&&(id==null||top.id===id)&&history.state&&history.state.ruApp){ruPendingUiBack=true;history.back()}
    else if(top&&top.kind===kind&&(id==null||top.id===id))ruUiStack.pop();
  }
  const ruBaseGo=window.go;
  window.go=function(page){
    const active=document.querySelector('.section.active'),from=active?active.id.replace('page-',''):'dashboard';
    if(!window.ruUseSingleNavigationStack&&!window.ruSuppressLegacyHistory&&!ruSuppressGoHistory&&from!==page)pushUi('page',from,page);
    if(typeof ruBaseGo==='function')ruBaseGo(page);
  };
  const ruBaseCloseModal=window.closeModal;
  window.closeModal=function(id){
    if(typeof ruBaseCloseModal==='function')ruBaseCloseModal(id);
    else{const el=document.getElementById(id);if(el)el.style.display='none'}
    if(!window.ruUseSingleNavigationStack&&!window.ruSuppressLegacyHistory)finishUiBack('modal',id);ruUpdateBodyLock();
  };
  function ruUpdateBodyLock(){
    const visible=[...document.querySelectorAll('.modal-backdrop')].some(el=>getComputedStyle(el).display!=='none');
    document.body.style.overflow=visible?'hidden':'';
    document.body.style.overscrollBehavior=visible?'none':'';
  }
  function ruTopModal(){return [...document.querySelectorAll('.modal-backdrop')].reverse().find(el=>getComputedStyle(el).display!=='none')}
  function ruObserveModal(){
    if(window.ruUseSingleNavigationStack){ruUpdateBodyLock();return}
    const visible=ruTopModal(),top=ruUiStack[ruUiStack.length-1];
    if(visible&&(!top||top.kind!=='modal'||top.id!==visible.id))pushUi('modal',visible.id);
    ruUpdateBodyLock();
  }
  document.querySelectorAll('.modal-backdrop').forEach(el=>{
    new MutationObserver(()=>setTimeout(ruObserveModal,45)).observe(el,{attributes:true,attributeFilter:['style','class']});
  });
  const ruBaseOpenBusiness=baseOpenBusiness,ruBaseCloseBusiness=baseCloseBusiness;
  window.openBusinessDetail=function(id){
    const result=ruBaseOpenBusiness&&ruBaseOpenBusiness(id);
    currentBusiness=id;window.ruCurrentBusinessId=id;addPhotoView(id);
    if(!window.ruUseSingleNavigationStack&&!window.ruSuppressLegacyHistory&&!window.ruSuppressBusinessHistory)pushUi('business',id);
    return result;
  };
  window.closeBusinessDetail=function(){
    const id=currentBusiness;
    if(ruBaseCloseBusiness)ruBaseCloseBusiness();
    currentBusiness=null;window.ruCurrentBusinessId=null;
    if(!window.ruUseSingleNavigationStack&&!window.ruSuppressLegacyHistory)finishUiBack('business',id);
  };
  const ruBaseOpenBusinessSub=window.openBusinessSubPage;
  window.openBusinessSubPage=function(kind){
    const id=currentBusiness||window.ruCurrentBusinessId;if(!id)return;
    pushUi('subpage',id,kind);
    if(kind==='hpp'){renderHppWithMaterials(id);return}
    if(typeof ruBaseOpenBusinessSub==='function')ruBaseOpenBusinessSub(kind);
    setTimeout(()=>{
      const panel=document.getElementById('businessCategorySettings');
      if(panel)panel.style.display='block';
      const heads=panel?[...panel.querySelectorAll('.panel-head')]:[];
      if(heads[0])heads[0].style.display='none';
      const chooser=panel&&panel.querySelector('.field');if(chooser)chooser.style.display='none';
      const cats=document.getElementById('bizSettingsCategories'),products=document.getElementById('bizSettingsProducts');
      if(cats)cats.style.display=kind==='categories'?'block':'none';
      if(products)products.style.display=kind==='products'?'block':'none';
      if(heads[1])heads[1].style.display=kind==='categories'?'flex':'none';
      if(heads[2])heads[2].style.display=kind==='products'?'flex':'none';
    },0);
  };
  function ruRestoreDetail(id){
    const target=id||currentBusiness;if(!target)return;
    if(ruBaseOpenBusiness){window.ruSuppressBusinessHistory=true;ruBaseOpenBusiness(target);window.ruSuppressBusinessHistory=false}
    currentBusiness=target;window.ruCurrentBusinessId=target;addPhotoView(target);
  }
  window.closeBusinessSub=function(){
    const top=ruUiStack[ruUiStack.length-1];
    if(top&&top.kind==='subpage'&&history.state&&history.state.ruApp){
      ruRestoreDetail(top.id);
      ruPendingUiBack=true;history.back();
    }else ruRestoreDetail(currentBusiness);
  };
  window.addEventListener('popstate',()=>{
    const entry=ruUiStack.pop();
    if(ruPendingUiBack){ruPendingUiBack=false;ruUpdateBodyLock();return}
    if(entry){
      if(entry.kind==='modal'){const el=document.getElementById(entry.id);if(el)el.style.display='none';ruUpdateBodyLock();return}
      if(entry.kind==='subpage'){ruRestoreDetail(entry.id);return}
      if(entry.kind==='business'){
        if(ruBaseCloseBusiness)ruBaseCloseBusiness();currentBusiness=null;window.ruCurrentBusinessId=null;return;
      }
      if(entry.kind==='page'){
        ruSuppressGoHistory=true;if(typeof ruBaseGo==='function')ruBaseGo(entry.id||'dashboard');ruSuppressGoHistory=false;return;
      }
    }
    const active=document.querySelector('.section.active');
    if(active&&active.id!=='page-dashboard'){ruSuppressGoHistory=true;if(typeof ruBaseGo==='function')ruBaseGo('dashboard');ruSuppressGoHistory=false}
  }
  );
  // Both visible back buttons and Android hardware Back now use the same stack.
})();
</script>
"""
v8 = r"""
<style>
/* Keep the fixed mobile navigation visible while transaction sheets are open. */
@media(max-width:700px){
 .modal-backdrop{z-index:29!important;bottom:calc(76px + env(safe-area-inset-bottom,0px))!important;align-items:flex-end!important;padding:0!important}
 .modal-backdrop>.modal{max-height:calc(100% - 8px)!important;width:100%!important;border-radius:20px 20px 0 0!important;overflow-y:auto!important}
 .mobile-bottom-nav{z-index:30!important}
 #txTypePicker .type-choice{min-height:100px;flex:1;flex-direction:column;justify-content:center;text-align:center;gap:8px;padding:12px 7px!important;margin:0!important}
 #txTypePicker .modal{padding-bottom:16px!important}
 #txTypePicker .type-choice:first-of-type{border-color:#b9e7cc;background:#edfaf2;color:#117747}
 #txTypePicker .type-choice:first-of-type .type-icon{background:#ccefd9;color:#087643}
 #txTypePicker .type-choice:nth-of-type(2){border-color:#f1c7c7;background:#fff0f0;color:#b42332}
 #txTypePicker .type-choice:nth-of-type(2) .type-icon{background:#ffd9d9;color:#b42332}
 #txTypePicker .type-choice:nth-of-type(3){border-color:#d8def8;background:#f3f5ff;color:#4655be}
 #businessesList.ru-business-grid{grid-template-columns:minmax(0,1fr)!important;gap:14px!important}
 .ru-business-card{display:grid;grid-template-columns:112px minmax(0,1fr);grid-template-rows:auto auto;border-radius:20px!important}
 .ru-business-cover{grid-column:1;grid-row:1/3;height:100%;min-height:160px}
 .ru-business-cover img{position:absolute;inset:0}
 .ru-business-photo-btn{right:7px;top:7px;width:30px;height:30px}
 .ru-business-info{grid-column:2;grid-row:1;padding:14px 12px 8px!important}
 .ru-business-name{font-size:15px;line-height:1.3}
 .ru-business-type{min-height:0;font-size:12px;margin-top:5px}
 .ru-business-status{margin-top:9px}
 .ru-business-stat-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;padding:0 12px 10px;grid-column:2;grid-row:2}
 .ru-business-stat{background:#f7f8fc;border-radius:10px;padding:7px 8px;min-width:0}
 .ru-business-stat small{display:block;color:var(--muted);font-size:10px;line-height:1.2}
 .ru-business-stat strong{display:block;font-size:12px;line-height:1.3;margin-top:3px;overflow-wrap:anywhere}
 .ru-business-actions{grid-column:1/-1;grid-row:3;padding:8px 10px!important;gap:8px}
 .ru-business-actions button{padding:9px!important;font-size:12px!important}
}
@media(max-width:390px){.ru-business-card{grid-template-columns:96px minmax(0,1fr)}.ru-business-cover{min-height:170px}}
</style>
<script>
(function(){
  window.ruUseSingleNavigationStack=true;
  window.ruSuppressLegacyHistory=false;
  let ruStack=[],ruSeq=0,ruActiveBusiness=null,ruActiveSub=null;
  const legacyGo=window.go,legacyOpenBusiness=window.openBusinessDetail,legacyCloseBusiness=window.closeBusinessDetail;
  const legacyOpenSub=window.openBusinessSubPage,legacyCloseModal=window.closeModal;
  let modalHandoff=null;
  function currentPage(){const n=document.querySelector('.section.active');return n?n.id.replace(/^page-/,''):'dashboard'}
  function pushEntry(entry){ruStack.push(entry);const seq=++ruSeq;try{history.pushState({ruUnified:true,seq},'','#ru-state-'+seq)}catch(e){}}
  function callLegacy(fn){window.ruSuppressLegacyHistory=true;window.ruSuppressBusinessHistory=true;try{return typeof fn==='function'?fn():undefined}finally{window.ruSuppressLegacyHistory=false;window.ruSuppressBusinessHistory=false}}
  function rawGo(page){return callLegacy(()=>legacyGo&&legacyGo(page))}
  function ensureModernBusinessDetail(id){
    const host=document.getElementById('businessDetailView'),b=business(id);
    if(!host||!b||host.querySelector('.business-menu-grid'))return;
    host.innerHTML='<div class="business-detail-top"><button type="button" class="small business-detail-back" onclick="closeBusinessDetail()">← Kembali</button><div class="business-detail-logo" style="overflow:hidden">'+photoIcon(b)+'</div><div style="min-width:0"><h1 class="business-detail-title">'+esc(b.name)+'</h1><div class="business-detail-kind">'+esc(b.type||'Usaha')+'</div></div></div><div class="desc">Ringkasan kinerja usaha untuk bulan berjalan.</div><div class="business-stat-grid" id="businessCustomStats"></div><div class="business-detail-actions"><button type="button" class="primary" id="businessDetailIncome">＋ Pemasukan</button><button type="button" id="businessDetailExpense">－ Pengeluaran</button></div><h2 class="business-section-heading">Pengaturan dan alat usaha</h2><div class="business-menu-grid"><button type="button" class="business-menu-card" onclick="openBusinessSubPage(\'categories\')"><span class="menu-symbol">▤</span><strong>Kategori usaha</strong></button><button type="button" class="business-menu-card" onclick="openBusinessSubPage(\'products\')"><span class="menu-symbol">▣</span><strong>Produk usaha</strong></button><button type="button" class="business-menu-card" onclick="openBusinessSubPage(\'hpp\')"><span class="menu-symbol">∑</span><strong>Perhitungan HPP</strong></button></div><h2 class="business-section-heading">Transaksi terbaru</h2><div id="businessCustomRecent"></div>';
    const inc=document.getElementById('businessDetailIncome'),out=document.getElementById('businessDetailExpense');
    if(inc)inc.onclick=()=>window.openTransactionForBusiness('income',id);
    if(out)out.onclick=()=>window.openTransactionForBusiness('expense',id);
    refreshPhoto(id);
    const month=typeof monthNow==='function'?monthNow():new Date().toISOString().slice(0,7),txs=(state.transactions||[]).filter(t=>t.businessId===id),mt=txs.filter(t=>String(t.date||'').startsWith(month)),st=typeof totals==='function'?totals(mt):{inc:0,out:0,net:0};
    const stats=document.getElementById('businessCustomStats');
    if(stats)stats.innerHTML='<div class="business-stat"><small>Pemasukan bulan ini</small><strong>'+money(st.inc)+'</strong></div><div class="business-stat"><small>Pengeluaran bulan ini</small><strong>'+money(st.out)+'</strong></div><div class="business-stat"><small>Arus kas bersih</small><strong>'+money(st.net)+'</strong></div><div class="business-stat"><small>Total transaksi</small><strong>'+txs.length+'</strong></div>';
    const recent=document.getElementById('businessCustomRecent');
    if(recent)recent.innerHTML=txs.slice().sort((a,b)=>String(b.date||'').localeCompare(String(a.date||''))).slice(0,6).map(t=>'<div class="business-detail-transaction"><div><strong>'+esc(t.note||(t.type==='income'?'Pemasukan':t.type==='expense'?'Pengeluaran':'Transfer'))+'</strong><small>'+esc(t.date||'')+' · '+esc(t.type==='transfer'?'Transfer':(typeof categoryName==='function'?categoryName(t.categoryId):''))+'</small></div><strong>'+(t.type==='expense'?'−':t.type==='income'?'+':'')+money(t.amount)+'</strong></div>').join('')||'<div class="desc">Belum ada transaksi untuk usaha ini.</div>';
  }
  function rawOpenBusiness(id){callLegacy(()=>legacyOpenBusiness&&legacyOpenBusiness(id));ensureModernBusinessDetail(id)}
  function rawCloseBusiness(){return callLegacy(()=>legacyCloseBusiness&&legacyCloseBusiness())}
  function rawOpenSub(kind){return callLegacy(()=>legacyOpenSub&&legacyOpenSub(kind))}
  function business(id){return (state.businesses||[]).find(b=>b.id===id)}
  function photoIcon(b){const n=String(b&&b.name||'').toLowerCase();if(b&&b.photoData)return '<img alt="Foto usaha" src="'+b.photoData+'">';if(/foto|studio|cetak|print/.test(n))return '📷';if(/wifi|internet/.test(n))return '📡';if(/cctv|alarm|security/.test(n))return '🛡️';if(/delivery|antar|kurir/.test(n))return '🛵';return '🏪'}
  function refreshPhoto(id){const b=business(id),logo=document.querySelector('#businessDetailView .business-detail-logo');if(b&&logo)logo.innerHTML=photoIcon(b)}
  function isVisibleModal(el){return !!(el&&getComputedStyle(el).display!=='none')}
  function topVisibleModal(){return [...document.querySelectorAll('.modal-backdrop')].reverse().find(isVisibleModal)}
  function lockScroll(){const yes=!!topVisibleModal();document.body.style.overflow=yes?'hidden':'';document.body.style.overscrollBehavior=yes?'none':''}
  function currentEntry(){return ruStack[ruStack.length-1]}
  function swapModalEntry(from,to){
    const top=currentEntry(),fromEl=document.getElementById(from);
    if(fromEl)fromEl.style.display='none';
    if(top&&top.kind==='modal'&&top.id===from){
      top.id=to;
      const st=history.state||{};
      try{history.replaceState({ruUnified:true,seq:st.seq||ruSeq},'','#ru-state-'+(st.seq||ruSeq)+'-'+to)}catch(e){}
    }else{
      pushEntry({kind:'modal',id:to});
    }
    lockScroll();
  }
  function startModalHandoff(from,to,invoke){modalHandoff={from,to};swapModalEntry(from,to);try{invoke()}finally{modalHandoff=null}}
  window.go=function(page){
    const from=currentPage();
    if(from!==page)pushEntry({kind:'page',page:from});
    rawGo(page);
  };
  window.openBusinessDetail=function(id){
    const b=business(id);if(!b)return;
    const from=currentPage();
    if(from!=='businesses'){
      pushEntry({kind:'page',page:from});
      rawGo('businesses');
    }
    pushEntry({kind:'business',id,page:'businesses'});
    ruActiveBusiness=id;ruActiveSub=null;window.ruCurrentBusinessId=id;
    rawOpenBusiness(id);ensureModernBusinessDetail(id);refreshPhoto(id);window.scrollTo(0,0);
  };
  window.closeBusinessDetail=function(){
    const top=currentEntry();
    if(top&&top.kind==='business'){history.back();return}
    const id=ruActiveBusiness;ruActiveBusiness=null;ruActiveSub=null;window.ruCurrentBusinessId=null;rawCloseBusiness();
  };
  window.openBusinessSubPage=function(kind){
    const id=ruActiveBusiness||window.ruCurrentBusinessId;if(!id)return;
    pushEntry({kind:'subpage',id,subpage:kind});ruActiveSub=kind;
    rawOpenSub(kind);
  };
  window.closeBusinessSub=function(){
    const top=currentEntry();
    if(top&&top.kind==='subpage'){history.back();return}
    if(ruActiveBusiness){rawOpenBusiness(ruActiveBusiness);refreshPhoto(ruActiveBusiness);ruActiveSub=null}
  };
  const ruLegacyStartTyped=window.startTypedTransaction;
  const ruLegacyChooseBusiness=window.chooseBusinessTyped;
  window.startTypedTransaction=function(type){
    if(type!=='income'&&type!=='expense'&&type!=='transfer')return;
    window.ruNextTransactionType=type;
    const action=()=>{
      // The legacy function fills its private selected-type state; close/open are handed off as one modal history entry.
      const fn=ruLegacyStartTyped;
      if(typeof fn==='function')fn(type);
      else{
        const tp=document.getElementById('txTypePicker');if(tp)tp.style.display='none';
        if(type==='transfer'){
          if(typeof window.openTransactionForm==='function')window.openTransactionForm('','');
          const t=document.getElementById('fType');if(t)t.value='transfer';
          if(typeof window.updateTxForm==='function')window.updateTxForm();
          const m=document.getElementById('txModal');if(m)m.style.display='flex';
        }else{
          if(typeof window.renderBusinessPicker==='function')renderBusinessPicker();
          const m=document.getElementById('businessPickerModal');if(m)m.style.display='flex';
        }
      }
    };
    startModalHandoff('txTypePicker',type==='transfer'?'txModal':'businessPickerModal',action);
  };
  window.chooseBusinessTyped=function(id){
    window.ruChosenBusinessId=id;
    startModalHandoff('businessPickerModal','txModal',()=>{
      if(typeof ruLegacyChooseBusiness==='function')ruLegacyChooseBusiness(id);
      else{
        if(typeof window.openTransactionForm==='function')window.openTransactionForm('',id==='__general__'?'':id);
        const t=document.getElementById('fType');if(t&&window.ruNextTransactionType)t.value=window.ruNextTransactionType;
        const b=document.getElementById('fBusiness');if(b)b.value=id==='__general__'?'':id;
        if(typeof window.updateTxForm==='function')window.updateTxForm();
        const m=document.getElementById('txModal');if(m)m.style.display='flex';
      }
    });
  };
  window.closeModal=function(id){
    const top=currentEntry();
    if(modalHandoff&&modalHandoff.from===id){const el=document.getElementById(id);if(el)el.style.display='none';return}
    if(top&&top.kind==='modal'&&top.id===id){history.back();return}
    if(typeof legacyCloseModal==='function')callLegacy(()=>legacyCloseModal(id));
    else{const el=document.getElementById(id);if(el)el.style.display='none'}
    lockScroll();
  };
  function returnToBusinessDetail(id){
    if(!id)return;
    ruActiveBusiness=id;ruActiveSub=null;window.ruCurrentBusinessId=id;
    rawOpenBusiness(id);refreshPhoto(id);window.scrollTo(0,0);
  }
  window.addEventListener('popstate',function(event){
    if(!window.ruUseSingleNavigationStack)return;
    event.stopImmediatePropagation();
    const entry=ruStack.pop();
    if(entry){
      if(entry.kind==='modal'){
        const el=document.getElementById(entry.id);if(el)el.style.display='none';
        lockScroll();return;
      }
      if(entry.kind==='subpage'){returnToBusinessDetail(entry.id);return}
      if(entry.kind==='business'){
        ruActiveBusiness=null;ruActiveSub=null;window.ruCurrentBusinessId=null;rawCloseBusiness();lockScroll();return;
      }
      if(entry.kind==='page'){rawGo(entry.page||'dashboard');lockScroll();return}
    }
    const modal=topVisibleModal();
    if(modal){modal.style.display='none';lockScroll();return}
    if(ruActiveSub&&ruActiveBusiness){returnToBusinessDetail(ruActiveBusiness);return}
    if(ruActiveBusiness){ruActiveBusiness=null;window.ruCurrentBusinessId=null;rawCloseBusiness();return}
    if(currentPage()!=='dashboard')rawGo('dashboard');
  },true);
  document.querySelectorAll('.modal-backdrop').forEach(el=>{
    new MutationObserver(()=>{
      setTimeout(()=>{
        const visible=topVisibleModal(),top=currentEntry();
        if(visible){
          if(modalHandoff&&modalHandoff.to===visible.id){lockScroll();return}
          if(!top||top.kind!=='modal'||top.id!==visible.id)pushEntry({kind:'modal',id:visible.id});
        }
        lockScroll();
      },20);
    }).observe(el,{attributes:true,attributeFilter:['style','class']});
  });
})();
</script>
"""
s=s.replace("</body>",v7+v8+"</body>",1)
p.write_text(s)
print("Feature upgrade applied",len(s))



# KasUsaha fix pack v1: resilient categories, monthly reports per business, import normalization
s = p.read_text()
if "RuangUsaha finance fixes v1" not in s:
    finance_css = r"""
/* RuangUsaha finance fixes v1 */
#ruMonthlyBusinessReport{margin:0 0 16px}
#ruMonthlyBusinessReport .ru-report-controls{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0}
#ruMonthlyBusinessReport .ru-report-controls label{display:block;font-size:12px;color:var(--muted);margin-bottom:5px}
#ruMonthlyBusinessReport .ru-report-controls input,#ruMonthlyBusinessReport .ru-report-controls select{width:100%;min-width:0;padding:10px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink);font:inherit}
#ruMonthlyBusinessReport .ru-report-total{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin:12px 0}
#ruMonthlyBusinessReport .ru-report-metric{border:1px solid var(--line);border-radius:13px;padding:10px;min-width:0;background:#fff}
#ruMonthlyBusinessReport .ru-report-metric small{display:block;color:var(--muted);font-size:11px;margin-bottom:5px}
#ruMonthlyBusinessReport .ru-report-metric strong{display:block;font-size:clamp(12px,3.6vw,18px);overflow-wrap:anywhere}
#ruMonthlyBusinessReport .ru-business-month-card{background:#fff;border:1px solid var(--line);border-radius:15px;padding:13px;margin:10px 0;min-width:0}
#ruMonthlyBusinessReport .ru-business-month-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px}
#ruMonthlyBusinessReport .ru-business-month-head h3{margin:0;font-size:15px;overflow-wrap:anywhere}
#ruMonthlyBusinessReport .ru-month-tx{display:flex;justify-content:space-between;gap:10px;padding:9px 0;border-top:1px solid var(--line);font-size:12px}
#ruMonthlyBusinessReport .ru-month-tx > div:first-child{min-width:0;overflow-wrap:anywhere}
#ruMonthlyBusinessReport .ru-month-tx small{display:block;color:var(--muted);margin-top:3px}
#ruMonthlyBusinessReport .ru-month-tx strong{white-space:nowrap;font-size:12px}
#bizCategoryModal{z-index:10000!important}
#bizCategoryModal .modal{z-index:10001!important}
@media(max-width:700px){#ruMonthlyBusinessReport .ru-report-controls{grid-template-columns:1fr}#ruMonthlyBusinessReport .ru-report-total{grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}#ruMonthlyBusinessReport .ru-report-metric{padding:8px}}
"""
    if "</style>" not in s:
        raise SystemExit("Tidak menemukan penutup style untuk patch laporan")
    s = s.replace("</style>", finance_css + "\n</style>", 1)
    reports_marker = '<section class="section" id="page-reports">'
    if reports_marker not in s:
        import re
        m = re.search("<section[^>]*id=[\\\"']page-reports[\\\"'][^>]*>", s, re.I)
        if not m:
            raise SystemExit("Bagian halaman Laporan tidak ditemukan")
        reports_marker = m.group(0)
    report_html = r"""
<div class="panel" id="ruMonthlyBusinessReport">
  <div class="panel-head"><div><h2>Laporan bulanan per usaha</h2><div class="desc">Pemasukan, pengeluaran, dan saldo bersih tiap usaha dipisahkan.</div></div></div>
  <div class="ru-report-controls">
    <div><label for="ruReportMonth">Bulan laporan</label><input id="ruReportMonth" type="month"></div>
    <div><label for="ruReportBusiness">Usaha</label><select id="ruReportBusiness"><option value="">Semua usaha (ditampilkan terpisah)</option></select></div>
  </div>
  <div id="ruReportSummary"></div>
  <div id="ruReportBusinessCards"></div>
  <div class="desc" id="ruReportDateNote" style="margin-top:10px">Transaksi tanpa tanggal hanya masuk laporan bulanan jika memiliki penanda bulan pada data transaksi.</div>
</div>
"""
    s = s.replace(reports_marker, reports_marker + report_html, 1)
    finance_js = r"""
<script>
(function(){
  var reportRoot = document.getElementById('ruMonthlyBusinessReport');
  if (!reportRoot) return;
  function allState(){ return (typeof state !== 'undefined' && state) ? state : {}; }
  function escReport(v){
    return String(v === undefined || v === null ? '' : v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }
  function rupiah(v){ return 'Rp' + (Number(v)||0).toLocaleString('id-ID'); }
  function monthKey(t){
    var d = String(t && t.date || '');
    if (/^\d{4}-\d{2}/.test(d)) return d.slice(0,7);
    var m = String(t && (t.reportMonth || t.monthKey || t.month) || '');
    return /^\d{4}-\d{2}/.test(m) ? m.slice(0,7) : '';
  }
  function typeText(t){ return t==='income'?'Pemasukan':t==='expense'?'Pengeluaran':'Transfer'; }
  function categoryText(id){
    var cats = allState().categories || [], c = cats.find(function(x){return x.id===id;});
    return c ? c.name : '';
  }
  function dateText(t){
    var d=String(t && t.date || '');
    if (/^\d{4}-\d{2}-\d{2}$/.test(d)) return d;
    if (monthKey(t)) return 'Bulan '+monthKey(t);
    return 'Tanggal tidak tercantum';
  }
  function businesses(){
    return (allState().businesses || []).filter(function(b){return !b.archived;});
  }
  function transactions(){ return allState().transactions || []; }
  function fillBusinessFilter(){
    var select=document.getElementById('ruReportBusiness'),old=select.value;
    var html='<option value="">Semua usaha (ditampilkan terpisah)</option>';
    businesses().forEach(function(b){html+='<option value="'+escReport(b.id)+'">'+escReport(b.name)+'</option>';});
    select.innerHTML=html;
    if ([].some.call(select.options,function(o){return o.value===old;})) select.value=old;
  }
  function renderBusinessCards(){
    var month=document.getElementById('ruReportMonth').value;
    var selected=document.getElementById('ruReportBusiness').value;
    var txs=transactions().filter(function(t){return month && monthKey(t)===month;});
    var biz=businesses().filter(function(b){return !selected || b.id===selected;});
    var totals={inc:0,out:0,bon:0};
    var reportTxs=selected?txs.filter(function(t){return t.businessId===selected;}):txs;
    reportTxs.forEach(function(t){if(t.type==='income')totals.inc+=Number(t.amount)||0;else if(t.type==='expense'&&categoryText(t.categoryId).toLowerCase()==='bon')totals.bon+=Number(t.amount)||0;else if(t.type==='expense')totals.out+=Number(t.amount)||0;});
    var summary=document.getElementById('ruReportSummary');
    summary.innerHTML='<div class="ru-report-total"><div class="ru-report-metric"><small>Total pemasukan</small><strong style="color:var(--green)">'+rupiah(totals.inc)+'</strong></div><div class="ru-report-metric"><small>Pengeluaran</small><strong style="color:var(--red)">'+rupiah(totals.out)+'</strong></div><div class="ru-report-metric"><small>BON</small><strong>'+rupiah(totals.bon)+'</strong></div><div class="ru-report-metric"><small>Saldo bersih</small><strong>'+rupiah(totals.inc-totals.out-totals.bon)+'</strong></div></div>';
    var cards='';
    biz.forEach(function(b){
      var items=txs.filter(function(t){return t.businessId===b.id && (t.type==='income'||t.type==='expense');})
        .sort(function(a,b){return String(a.date||'').localeCompare(String(b.date||''));});
      var inc=0,out=0,bon=0;
      items.forEach(function(t){if(t.type==='income')inc+=Number(t.amount)||0;else if(categoryText(t.categoryId).toLowerCase()==='bon')bon+=Number(t.amount)||0;else out+=Number(t.amount)||0;});
      cards+='<div class="ru-business-month-card"><div class="ru-business-month-head"><h3>'+escReport(b.name)+'</h3><strong>'+rupiah(inc-out-bon)+'</strong></div><div class="ru-report-total"><div class="ru-report-metric"><small>Pemasukan</small><strong style="color:var(--green)">'+rupiah(inc)+'</strong></div><div class="ru-report-metric"><small>Pengeluaran</small><strong style="color:var(--red)">'+rupiah(out)+'</strong></div><div class="ru-report-metric"><small>BON</small><strong>'+rupiah(bon)+'</strong></div><div class="ru-report-metric"><small>Transaksi</small><strong>'+items.length+'</strong></div></div>';
      if(items.length){
        items.forEach(function(t){
          cards+='<div class="ru-month-tx"><div><strong>'+escReport(t.note || typeText(t.type))+'</strong><small>'+escReport(dateText(t))+' · '+escReport(categoryText(t.categoryId)||typeText(t.type))+'</small></div><strong style="color:'+(t.type==='expense'?'var(--red)':'var(--green)')+'">'+(t.type==='expense'?'−':'+')+rupiah(t.amount)+'</strong></div>';
        });
      }else cards+='<div class="desc">Belum ada transaksi bertanggal/bulan untuk usaha ini.</div>';
      cards+='</div>';
    });
    var general=txs.filter(function(t){return !t.businessId && (t.type==='income'||t.type==='expense');});
    if(!selected && general.length){
      var gi=0,go=0,gb=0;general.forEach(function(t){if(t.type==='income')gi+=Number(t.amount)||0;else if(categoryText(t.categoryId).toLowerCase()==='bon')gb+=Number(t.amount)||0;else go+=Number(t.amount)||0;});
      cards+='<div class="ru-business-month-card"><div class="ru-business-month-head"><h3>Operasional umum</h3><strong>'+rupiah(gi-go-gb)+'</strong></div><div class="ru-report-total"><div class="ru-report-metric"><small>Pemasukan</small><strong>'+rupiah(gi)+'</strong></div><div class="ru-report-metric"><small>Pengeluaran</small><strong>'+rupiah(go)+'</strong></div><div class="ru-report-metric"><small>BON</small><strong>'+rupiah(gb)+'</strong></div><div class="ru-report-metric"><small>Transaksi</small><strong>'+general.length+'</strong></div></div></div>';
    }
    document.getElementById('ruReportBusinessCards').innerHTML=cards || '<div class="desc">Belum ada usaha. Tambahkan usaha terlebih dahulu.</div>';
  }
  window.renderRuMonthlyBusinessReport=function(){
    if(!reportRoot) return;
    fillBusinessFilter();
    var input=document.getElementById('ruReportMonth');
    if(!input.value){
      var months=transactions().map(monthKey).filter(Boolean).sort();
      input.value=months.length?months[months.length-1]:new Date().toISOString().slice(0,7);
    }
    renderBusinessCards();
  };
  document.getElementById('ruReportMonth').addEventListener('change',renderBusinessCards);
  document.getElementById('ruReportBusiness').addEventListener('change',renderBusinessCards);
  document.addEventListener('click',function(e){
    var button=e.target && e.target.closest ? e.target.closest('[data-page="reports"],[onclick*="reports"]') : null;
    if(button) setTimeout(window.renderRuMonthlyBusinessReport,80);
  },true);
  if(typeof window.render==='function'){
    var oldRender=window.render;
    window.render=function(){oldRender.apply(this,arguments);window.renderRuMonthlyBusinessReport();};
  }
  window.addEventListener('storage',window.renderRuMonthlyBusinessReport);
  setTimeout(window.renderRuMonthlyBusinessReport,100);
  setTimeout(window.renderRuMonthlyBusinessReport,500);

  // Reliable category modal/form path, independent of page-level navigation wrappers.
  function currentBusinessId(){
    var sel=document.getElementById('bizSettingsBusiness');
    if(sel && sel.value) return sel.value;
    if(window.ruCurrentBusinessId) return window.ruCurrentBusinessId;
    var active=(allState().businesses||[]).filter(function(b){return !b.archived;});
    return active.length?active[0].id:'';
  }
  function businessOptions(selected){
    return (allState().businesses||[]).filter(function(b){return !b.archived;}).map(function(b){
      return '<option value="'+escReport(b.id)+'"'+(b.id===selected?' selected':'')+'>'+escReport(b.name)+'</option>';
    }).join('');
  }
  window.openBusinessCategory=function(id){
    var st=allState(), bid=currentBusinessId(), form=document.getElementById('bizCategoryForm');
    var modal=document.getElementById('bizCategoryModal'),sel=document.getElementById('bizCategoryBusiness');
    if(!form||!modal||!sel){alert('Form kategori tidak ditemukan. Silakan buka kembali halaman Usaha.');return;}
    if(!bid){alert('Tambahkan usaha terlebih dahulu.');return;}
    sel.innerHTML=businessOptions(bid);sel.value=bid;
    form.reset();
    document.getElementById('bizCategoryId').value='';
    document.getElementById('bizCategoryTitle').textContent=id?'Edit kategori':'Tambah kategori';
    if(id){
      var c=(st.categories||[]).find(function(x){return x.id===id;});
      if(!c){alert('Kategori tidak ditemukan.');return;}
      document.getElementById('bizCategoryId').value=c.id;
      sel.value=c.businessId||bid;
      document.getElementById('bizCategoryType').value=c.type||'expense';
      document.getElementById('bizCategoryName').value=c.name||'';
    }
    modal.style.setProperty('display','flex','important');
    modal.style.setProperty('z-index','10000','important');
    var inner=modal.querySelector('.modal');if(inner)inner.style.setProperty('z-index','10001','important');
    if(typeof window.setModalBodyLock==='function')window.setModalBodyLock();
    setTimeout(function(){var name=document.getElementById('bizCategoryName');if(name)name.focus();},50);
  };
  var form=document.getElementById('bizCategoryForm');
  if(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();e.stopImmediatePropagation();
      try{
        var st=allState(),id=document.getElementById('bizCategoryId').value;
        var businessId=document.getElementById('bizCategoryBusiness').value;
        var type=document.getElementById('bizCategoryType').value;
        var name=document.getElementById('bizCategoryName').value.trim();
        if(!businessId||!name){alert('Pilih usaha dan isi nama kategori.');return;}
        st.categories=st.categories||[];
        var duplicate=st.categories.some(function(c){return c.id!==id&&c.businessId===businessId&&c.type===type&&String(c.name||'').toLowerCase()===name.toLowerCase();});
        if(duplicate){alert('Kategori dengan nama tersebut sudah ada di usaha ini.');return;}
        if(id){
          var existing=st.categories.find(function(c){return c.id===id;});
          if(!existing){alert('Kategori yang akan diedit tidak ditemukan.');return;}
          Object.assign(existing,{businessId:businessId,type:type,name:name});
        }else{
          var newId='cat-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,8);
          st.categories.push({id:newId,businessId:businessId,type:type,name:name});
        }
        if(typeof save==='function')save();
        if(typeof window.renderBusinessCategorySettings==='function')window.renderBusinessCategorySettings();
        if(typeof window.updateTxForm==='function')window.updateTxForm();
        if(typeof window.closeModal==='function')window.closeModal('bizCategoryModal');
        else modal.style.display='none';
        if(typeof window.showToast==='function')window.showToast('Kategori usaha berhasil disimpan.');
      }catch(err){alert('Gagal menyimpan kategori: '+(err&&err.message?err.message:String(err)));}
    },true);
  }

  // Accept both native backups (data:{...}) and top-level JSON transaction exports.
  window.importBackupFile=function(event){
    var file=event.target.files&&event.target.files[0];if(!file)return;
    var reader=new FileReader();
    reader.onload=function(){
      try{
        var parsed=JSON.parse(String(reader.result||'')), d=parsed&&parsed.data?parsed.data:parsed;
        if(!d||!Array.isArray(d.transactions)||!Array.isArray(d.accounts)||!Array.isArray(d.categories))throw new Error('JSON harus memiliki transactions, accounts, dan categories berupa array.');
        if(!confirm('Impor akan mengganti data usaha, akun, kategori, produk, HPP, dan transaksi saat ini. Ekspor cadangan dahulu bila data masih diperlukan. Lanjutkan?'))return;
        var accounts=d.accounts.map(function(a){var x=Object.assign({},a);x.opening=Number(x.opening!==undefined?x.opening:(x.balance!==undefined?x.balance:0))||0;delete x.balance;return x;});
        var businesses=Array.isArray(d.businesses)?d.businesses:[];
        var categories=d.categories.map(function(c){return Object.assign({},c,{type:c.type==='income'?'income':'expense',businessId:c.businessId||''});});
        var transactions=d.transactions.map(function(t,i){
          var x=Object.assign({},t);
          x.id=x.id||('import-tx-'+Date.now()+'-'+i);
          x.amount=Number(x.amount)||0;
          x.date=String(x.date||'');
          if(!x.reportMonth)x.reportMonth=x.monthKey||x.month||'';
          x.type=['income','expense','transfer'].indexOf(x.type)>=0?x.type:'expense';
          x.businessId=x.businessId||'';
          x.categoryId=x.categoryId||'';
          x.accountId=x.accountId||(accounts[0]&&accounts[0].id)||'';
          return x;
        });
        state=Object.assign({},state,d,{businesses:businesses,accounts:accounts,categories:categories,transactions:transactions,products:Array.isArray(d.products)?d.products:[],hppRecords:Array.isArray(d.hppRecords)?d.hppRecords:[]});
        if(typeof save==='function')save();
        if(typeof render==='function')render();
        if(typeof window.renderRuMonthlyBusinessReport==='function')window.renderRuMonthlyBusinessReport();
        if(typeof window.showToast==='function')window.showToast('Data berhasil dipulihkan.');
        else alert('Data berhasil dipulihkan.');
      }catch(err){alert('File cadangan tidak valid atau rusak: '+(err&&err.message?err.message:String(err)));}
      finally{event.target.value='';}
    };
    reader.onerror=function(){alert('File tidak dapat dibaca.');};
    reader.readAsText(file);
  };
  document.addEventListener('DOMContentLoaded',function(){
    window.renderRuMonthlyBusinessReport();
  });
})();
</script>
"""
    s = s.replace("</body>", finance_js + "\n</body>", 1)
    p.write_text(s)

 
# KasUsaha category modal guard v2: capture the add button and save form reliably.
# This block is intentionally outside the report-feature guard so it is applied on every build.
s = p.read_text()
if "KasUsaha category modal guard v2" not in s:
    category_guard_js = r"""
<script>
/* KasUsaha category modal guard v2 */
(function(){
  if(window.__ruCategoryModalGuardV2) return;
  window.__ruCategoryModalGuardV2 = true;

  document.addEventListener('click', function(e){
    var button = e.target && e.target.closest ? e.target.closest('#businessCategorySettings button') : null;
    if(!button) return;
    var label = String(button.innerText || button.textContent || '').replace(/\s+/g,' ').trim();
    if(!/kategori/i.test(label) || !/[＋+]/.test(label)) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    try {
      var modal = document.getElementById('bizCategoryModal');
      if(!modal) throw new Error('Jendela kategori tidak ditemukan di halaman. Silakan tutup lalu buka kembali halaman Usaha.');
      /* The category editor is originally inside the businesses page. On mobile, the detail subpage hides that parent, so move the modal to body before opening it. */
      if(modal.parentElement !== document.body) document.body.appendChild(modal);
      if(typeof window.openBusinessCategory !== 'function') throw new Error('Fungsi tambah kategori belum siap. Tutup lalu buka kembali halaman Usaha.');
      window.openBusinessCategory();
      modal = document.getElementById('bizCategoryModal');
      if(modal){
        modal.style.setProperty('display','flex','important');
        modal.style.setProperty('position','fixed','important');
        modal.style.setProperty('inset','0','important');
        modal.style.setProperty('z-index','10000','important');
        modal.style.setProperty('align-items','center','important');
        modal.style.setProperty('justify-content','center','important');
        var inner = modal.querySelector('.modal');
        if(inner){
          inner.style.setProperty('position','relative','important');
          inner.style.setProperty('z-index','10001','important');
          inner.style.setProperty('max-height','85vh','important');
          inner.style.setProperty('overflow-y','auto','important');
        }
      }
    } catch(err) {
      alert('Tidak dapat membuka form kategori: ' + (err && err.message ? err.message : String(err)));
    }
  }, true);

  /* Saving is handled by the existing bizCategoryForm submit listener in the finance patch. */
})();
</script>
"""
    if "</body>" not in s:
        raise SystemExit("Tidak menemukan penutup body untuk perbaikan kategori")
    s = s.replace("</body>", category_guard_js + "\n</body>", 1)
    p.write_text(s)


# KasUsaha multi-wallet manager v1.
# Expose wallet/account CRUD in Settings and guarantee transfer semantics are wallet-to-wallet.
s = p.read_text()
if "KasUsaha multi-wallet manager v1" not in s:
    s = re.sub(r"Transfer\s+antar\s+usaha", "Transfer antar dompet", s, flags=re.I)

    wallet_js = r"""
<style>
/* KasUsaha multi-wallet manager v1 */
#ruWalletManager{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px;margin:12px 0}
#ruWalletManager .ru-wallet-head{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
#ruWalletManager .ru-wallet-head h2{margin:0}
#ruWalletManager .ru-wallet-row{display:flex;justify-content:space-between;align-items:center;gap:10px;border-top:1px solid var(--line);padding:13px 0}
#ruWalletManager .ru-wallet-row:first-child{border-top:0}
#ruWalletManager .ru-wallet-meta{font-size:12px;color:var(--muted);margin-top:4px}
#ruWalletManager .ru-wallet-balance{font-size:14px;font-weight:800;margin-top:5px}
#ruWalletManager .ru-wallet-actions{display:flex;gap:6px;flex-wrap:wrap;flex-shrink:0}
#ruWalletModal{display:none;position:fixed!important;inset:0!important;z-index:15000!important;align-items:center!important;justify-content:center!important;background:rgba(20,25,45,.52);padding:18px}
#ruWalletModal .ru-wallet-dialog{background:#fff;color:var(--ink);border-radius:18px;padding:18px;width:min(100%,480px);max-height:85dvh;overflow:auto;box-shadow:0 18px 60px #0003}
#ruWalletModal .ru-wallet-dialog h2{margin-top:0}
#ruWalletModal .ru-wallet-dialog .field{margin:12px 0}
#ruWalletModal .ru-wallet-dialog input,#ruWalletModal .ru-wallet-dialog select{width:100%;box-sizing:border-box;padding:12px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink);font:inherit}
#ruWalletModal .ru-wallet-form-actions{display:flex;gap:9px;position:sticky;bottom:-18px;background:#fff;padding:14px 0 2px}
#ruWalletModal .ru-wallet-form-actions button{flex:1}
@media(max-width:420px){#ruWalletManager .ru-wallet-row{align-items:flex-start;flex-direction:column}#ruWalletManager .ru-wallet-actions{width:100%}#ruWalletManager .ru-wallet-actions button{flex:1}}
</style>
<script>
/* KasUsaha multi-wallet manager v1 */
(function(){
  if(window.__ruMultiWalletManagerV1) return;
  window.__ruMultiWalletManagerV1 = true;
  function appState(){ return (typeof state !== 'undefined' && state) ? state : (window.state || {}); }
  function escWallet(v){return String(v==null?'':v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
  function rupiah(v){
    var n=Number(v)||0;
    if(typeof window.money==='function') return window.money(n);
    return 'Rp'+n.toLocaleString('id-ID');
  }
  function accounts(){var st=appState();return Array.isArray(st.accounts)?st.accounts:[];}
  function transactions(){var st=appState();return Array.isArray(st.transactions)?st.transactions:[];}
  function typeLabel(type){
    return ({cash:'Tunai',bank:'Bank',ewallet:'E-wallet',other:'Lainnya'})[type] || String(type||'Dompet');
  }
  function walletBalance(account){
    var balance=Number(account.opening!==undefined?account.opening:(account.balance!==undefined?account.balance:0))||0;
    transactions().forEach(function(t){
      var amount=Number(t.amount)||0;
      if(t.accountId===account.id){
        if(t.type==='income') balance+=amount;
        else if(t.type==='expense'||t.type==='transfer') balance-=amount;
      }
      if(t.type==='transfer'&&t.toAccountId===account.id) balance+=amount;
    });
    return balance;
  }
  function accountUsed(id){
    return transactions().some(function(t){return t.accountId===id||t.toAccountId===id;});
  }
  function ensureUI(){
    var settings=document.getElementById('page-settings');
    if(!settings) return false;
    var panel=document.getElementById('ruWalletManager');
    if(!panel){
      panel=document.createElement('section');
      panel.id='ruWalletManager';
      panel.innerHTML='<div class="ru-wallet-head"><div><h2>Dompet &amp; Rekening</h2><div class="desc">Kelola beberapa dompet, rekening bank, dan e-wallet. Pilih dompet saat mencatat transaksi atau transfer.</div></div><button type="button" class="primary" id="ruWalletAdd">＋ Tambah dompet</button></div><div id="ruWalletList" style="margin-top:10px"></div>';
      var top=settings.querySelector('.top');
      if(top&&top.parentElement===settings) top.insertAdjacentElement('afterend',panel);
      else settings.insertBefore(panel,settings.firstChild);
    }
    var modal=document.getElementById('ruWalletModal');
    if(!modal){
      modal=document.createElement('div');
      modal.id='ruWalletModal';
      modal.innerHTML='<div class="ru-wallet-dialog"><div style="display:flex;justify-content:space-between;align-items:center;gap:12px"><h2 id="ruWalletModalTitle">Tambah dompet</h2><button type="button" id="ruWalletClose" aria-label="Tutup">✕</button></div><form id="ruWalletForm"><input type="hidden" id="ruWalletId"><div class="field"><label for="ruWalletName">Nama dompet</label><input id="ruWalletName" required maxlength="70" placeholder="Contoh: Kas Tunai, BCA, DANA"></div><div class="field"><label for="ruWalletType">Jenis dompet</label><select id="ruWalletType"><option value="cash">Tunai / Kas</option><option value="bank">Rekening bank</option><option value="ewallet">E-wallet</option><option value="other">Lainnya</option></select></div><div class="field"><label for="ruWalletOpening">Saldo awal (Rp)</label><input id="ruWalletOpening" type="number" step="1" required value="0" placeholder="0"></div><div class="desc">Saldo awal adalah saldo sebelum transaksi yang tercatat di aplikasi.</div><div class="ru-wallet-form-actions"><button type="button" id="ruWalletCancel">Batal</button><button type="submit" class="primary">Simpan dompet</button></div></form></div>';
      document.body.appendChild(modal);
    }
    return true;
  }
  function renderWallets(){
    if(!ensureUI()) return;
    var host=document.getElementById('ruWalletList');
    var list=accounts();
    if(!list.length){
      host.innerHTML='<div class="desc" style="padding:14px 0">Belum ada dompet. Tambahkan dompet untuk mulai mencatat transaksi.</div>';
      return;
    }
    host.innerHTML=list.map(function(a){
      var used=accountUsed(a.id);
      return '<div class="ru-wallet-row"><div style="min-width:0;flex:1"><strong>'+escWallet(a.name||'Dompet')+'</strong><div class="ru-wallet-meta">'+typeLabel(a.type)+' · Saldo awal '+rupiah(a.opening!==undefined?a.opening:a.balance)+'</div><div class="ru-wallet-balance">Saldo saat ini: '+rupiah(walletBalance(a))+'</div></div><div class="ru-wallet-actions"><button type="button" class="small" data-wallet-edit="'+escWallet(a.id)+'">Edit</button><button type="button" class="small danger" data-wallet-delete="'+escWallet(a.id)+'" '+(used?'disabled title="Dompet sudah dipakai transaksi"':'')+'>Hapus</button></div></div>';
    }).join('');
  }
  function openWallet(id){
    if(!ensureUI()) return;
    var form=document.getElementById('ruWalletForm');
    var account=id?accounts().find(function(a){return a.id===id;}):null;
    form.reset();
    document.getElementById('ruWalletId').value=account?account.id:'';
    document.getElementById('ruWalletName').value=account?account.name||'':'';
    document.getElementById('ruWalletType').value=account?account.type||'cash':'cash';
    document.getElementById('ruWalletOpening').value=account?Number(account.opening!==undefined?account.opening:account.balance)||0:0;
    document.getElementById('ruWalletModalTitle').textContent=account?'Edit dompet':'Tambah dompet';
    document.getElementById('ruWalletModal').style.display='flex';
    setTimeout(function(){var input=document.getElementById('ruWalletName');if(input)input.focus();},50);
  }
  function refreshApp(){
    try{if(typeof save==='function')save();else if(typeof window.save==='function')window.save();}
    catch(e){alert('Dompet disimpan sementara, tetapi gagal menyimpan data: '+e.message);return;}
    try{if(typeof window.updateTxForm==='function')window.updateTxForm();}catch(e){}
    try{if(typeof window.render==='function')window.render();}catch(e){}
    try{if(typeof window.renderBusinessCategorySettings==='function')window.renderBusinessCategorySettings();}catch(e){}
    renderWallets();
  }
  document.addEventListener('click',function(e){
    var add=e.target&&e.target.closest?e.target.closest('#ruWalletAdd'):null;
    var close=e.target&&e.target.closest?e.target.closest('#ruWalletClose,#ruWalletCancel'):null;
    var edit=e.target&&e.target.closest?e.target.closest('[data-wallet-edit]'):null;
    var del=e.target&&e.target.closest?e.target.closest('[data-wallet-delete]'):null;
    if(add){e.preventDefault();openWallet('');return;}
    if(close){e.preventDefault();document.getElementById('ruWalletModal').style.display='none';return;}
    if(edit){e.preventDefault();openWallet(edit.getAttribute('data-wallet-edit'));return;}
    if(del){
      e.preventDefault();
      var id=del.getAttribute('data-wallet-delete'),account=accounts().find(function(a){return a.id===id;});
      if(!account)return;
      if(accountUsed(id)){alert('Dompet ini sudah digunakan dalam transaksi. Jangan hapus agar riwayat dan saldo tetap benar.');return;}
      if(accounts().length<=1){alert('Minimal harus ada satu dompet.');return;}
      if(confirm('Hapus dompet "'+(account.name||'Dompet')+'"?')){
        var st=appState();st.accounts=accounts().filter(function(a){return a.id!==id;});
        refreshApp();
      }
    }
  },true);
  document.addEventListener('submit',function(e){
    if(!e.target||e.target.id!=='ruWalletForm')return;
    e.preventDefault();e.stopImmediatePropagation();
    var st=appState(),id=document.getElementById('ruWalletId').value;
    var name=document.getElementById('ruWalletName').value.trim();
    var type=document.getElementById('ruWalletType').value;
    var opening=Number(document.getElementById('ruWalletOpening').value);
    if(!name){alert('Masukkan nama dompet.');return;}
    if(!Number.isFinite(opening)){alert('Saldo awal tidak valid.');return;}
    st.accounts=Array.isArray(st.accounts)?st.accounts:[];
    if(st.accounts.some(function(a){return a.id!==id&&String(a.name||'').trim().toLowerCase()===name.toLowerCase();})){
      alert('Nama dompet sudah digunakan. Gunakan nama yang berbeda.');return;
    }
    if(id){
      var existing=st.accounts.find(function(a){return a.id===id;});
      if(!existing){alert('Dompet tidak ditemukan.');return;}
      existing.name=name;existing.type=type;existing.opening=Math.round(opening);delete existing.balance;
    }else{
      st.accounts.push({id:'wallet-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,8),name:name,type:type,opening:Math.round(opening)});
    }
    document.getElementById('ruWalletModal').style.display='none';
    refreshApp();
  },true);
  document.addEventListener('submit',function(e){
    var form=e.target;
    if(!form||!form.querySelector||!form.querySelector('#fType'))return;
    var type=document.getElementById('fType').value;
    if(type!=='transfer')return;
    var from=document.getElementById('fAccount'),to=document.getElementById('fToAccount'),business=document.getElementById('fBusiness');
    if(business)business.value='';
    if(!from||!from.value||!to||!to.value){
      e.preventDefault();e.stopImmediatePropagation();alert('Pilih dompet asal dan dompet tujuan untuk transfer.');return;
    }
    if(from.value===to.value){
      e.preventDefault();e.stopImmediatePropagation();alert('Dompet asal dan tujuan harus berbeda.');return;
    }
  },true);
  function renameTransferLabels(){
    document.querySelectorAll('button,option,label,h1,h2,h3,small,strong,span,div').forEach(function(el){
      if(el.children.length>4)return;
      var txt=(el.textContent||'').trim();
      if(/^transfer\s+antar\s+usaha$/i.test(txt))el.textContent='Transfer antar dompet';
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){renderWallets();renameTransferLabels();});
  else {renderWallets();renameTransferLabels();}
  document.addEventListener('click',function(e){
    var settings=e.target&&e.target.closest?e.target.closest('[data-page="settings"],#settingsShortcut'):null;
    if(settings)setTimeout(renderWallets,80);
  },true);
  if(typeof window.render==='function'){
    var originalRender=window.render;
    window.render=function(){originalRender.apply(this,arguments);renderWallets();};
  }
})();
</script>
"""
    if "</body>" not in s:
        raise SystemExit("Tidak menemukan penutup body untuk multi-wallet manager")
    s = s.replace("</body>", wallet_js + "\n</body>", 1)
    p.write_text(s)


# KasUsaha transaction wallet-first flow v1.
# For income/expense/transfer, choose transaction type -> wallet -> (business if applicable) -> transaction form.
s = p.read_text()
if "KasUsaha transaction wallet-first flow v1" not in s:
    wallet_first_js = r"""
<script>
/* KasUsaha transaction wallet-first flow v1 */
(function(){
  if(window.__ruWalletFirstFlowV1)return;
  window.__ruWalletFirstFlowV1=true;
  var pendingType='income', pendingWallet='';
  function st(){return (typeof state!=='undefined'&&state)?state:(window.state||{});}
  function esc(v){return String(v==null?'':v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
  function money(v){return typeof window.money==='function'?window.money(Number(v)||0):'Rp'+(Number(v)||0).toLocaleString('id-ID');}
  function accounts(){return Array.isArray(st().accounts)?st().accounts:[];}
  function transactions(){return Array.isArray(st().transactions)?st().transactions:[];}
  function balance(a){
    var n=Number(a.opening!==undefined?a.opening:(a.balance||0))||0;
    transactions().forEach(function(t){
      var v=Number(t.amount)||0;
      if(t.accountId===a.id){if(t.type==='income')n+=v;else if(t.type==='expense'||t.type==='transfer')n-=v;}
      if(t.type==='transfer'&&t.toAccountId===a.id)n+=v;
    });
    return n;
  }
  function ensurePicker(){
    var el=document.getElementById('ruTxWalletPicker');
    if(el)return el;
    el=document.createElement('div');el.id='ruTxWalletPicker';
    el.style.cssText='display:none;position:fixed;inset:0;z-index:16000;background:rgba(15,23,42,.55);align-items:flex-end;justify-content:center;padding:0';
    el.innerHTML='<div style="background:#fff;color:#172033;width:100%;max-width:560px;max-height:88dvh;overflow:auto;border-radius:22px 22px 0 0;padding:18px 16px calc(18px + env(safe-area-inset-bottom));box-sizing:border-box"><div style="display:flex;justify-content:space-between;align-items:center;gap:10px"><div><h2 id="ruTxWalletTitle" style="margin:0 0 5px;font-size:21px">Pilih dompet</h2><div id="ruTxWalletSubtitle" style="font-size:13px;color:#687386">Pilih dompet yang digunakan.</div></div><button type="button" id="ruTxWalletClose">✕</button></div><div id="ruTxWalletOptions" style="display:grid;gap:9px;margin-top:16px"></div><button type="button" id="ruTxWalletManage" style="width:100%;margin-top:12px">＋ Kelola dompet</button></div>';
    document.body.appendChild(el);
    document.getElementById('ruTxWalletClose').onclick=function(){el.style.display='none';};
    document.getElementById('ruTxWalletManage').onclick=function(){
      el.style.display='none';
      var settings=document.querySelector('[data-page="settings"]');
      if(settings)settings.click();
      setTimeout(function(){var add=document.getElementById('ruWalletAdd');if(add)add.click();else alert('Buka Pengaturan untuk mengelola dompet.');},100);
    };
    return el;
  }
  function openWalletPicker(type){
    pendingType=type;
    pendingWallet='';
    var el=ensurePicker(),opts=document.getElementById('ruTxWalletOptions');
    var names={income:'Pemasukan',expense:'Pengeluaran',transfer:'Transfer antar dompet'};
    document.getElementById('ruTxWalletTitle').textContent='Pilih dompet';
    document.getElementById('ruTxWalletSubtitle').textContent=type==='transfer'?'Pilih dompet asal transfer.':'Pilih dompet untuk transaksi '+names[type].toLowerCase()+'.';
    var list=accounts();
    opts.innerHTML=list.map(function(a){
      var kind=({cash:'Tunai / Kas',bank:'Rekening bank',ewallet:'E-wallet',other:'Lainnya'})[a.type]||'Dompet';
      return '<button type="button" data-ru-wallet="'+esc(a.id)+'" style="display:flex;justify-content:space-between;align-items:center;gap:12px;text-align:left;background:#fff;border:1px solid #dfe5ee;border-radius:14px;padding:14px;color:#172033"><span style="min-width:0"><strong style="display:block">'+esc(a.name||'Dompet')+'</strong><small style="display:block;color:#687386;margin-top:4px">'+kind+'</small></span><strong style="white-space:nowrap">'+money(balance(a))+'</strong></button>';
    }).join('')||'<div style="padding:14px;color:#687386">Belum ada dompet. Tambahkan dompet terlebih dahulu.</div>';
    el.style.display='flex';
  }
  function showBusinessPicker(type,walletId){
    pendingType=type;pendingWallet=walletId;
    if(typeof window.renderBusinessPicker==='function')window.renderBusinessPicker();
    var modal=document.getElementById('businessPickerModal');
    if(modal){
      var heading=modal.querySelector('h2');
      if(heading)heading.textContent='Pilih usaha';
      var desc=modal.querySelector('.desc');
      if(desc)desc.textContent='Pilih usaha untuk transaksi '+(type==='income'?'pemasukan':'pengeluaran')+'.';
      modal.style.display='flex';
    }else openForm(type,walletId,'');
  }
  function openForm(type,walletId,businessId){
    if(typeof window.openTransactionForm==='function')window.openTransactionForm('',businessId||'');
    var typeEl=document.getElementById('fType'),accountEl=document.getElementById('fAccount');
    if(typeEl){typeEl.value=type;if(typeof window.updateTxForm==='function')window.updateTxForm();}
    if(accountEl)accountEl.value=walletId||'';
    var businessEl=document.getElementById('fBusiness');
    if(businessEl)businessEl.value=businessId||'';
    var toAccount=document.getElementById('fToAccount');
    if(type==='transfer'&&toAccount)toAccount.value='';
    if(typeof window.updateTxForm==='function')window.updateTxForm();
    var modal=document.getElementById('txModal');
    if(modal)modal.style.display='flex';
  }
  document.addEventListener('click',function(e){
    var btn=e.target&&e.target.closest?e.target.closest('[data-ru-wallet]'):null;
    if(!btn)return;
    e.preventDefault();
    var id=btn.getAttribute('data-ru-wallet'),type=pendingType;
    document.getElementById('ruTxWalletPicker').style.display='none';
    if(type==='transfer'){openForm(type,id,'');return;}
    showBusinessPicker(type,id);
  },true);
  var originalStart=window.startTypedTransaction;
  window.startTypedTransaction=function(type){
    if(['income','expense','transfer'].indexOf(type)<0){if(typeof originalStart==='function')originalStart(type);return;}
    var typeModal=document.getElementById('txTypePicker');
    if(typeModal)typeModal.style.display='none';
    openWalletPicker(type);
  };
  var originalChoose=window.chooseBusiness;
  window.chooseBusiness=function(id){
    var modal=document.getElementById('businessPickerModal');
    if(modal)modal.style.display='none';
    var type=pendingType,walletId=pendingWallet;
    if(type==='income'||type==='expense'){
      openForm(type,walletId,id==='__general__'?'':id);
      return;
    }
    if(typeof originalChoose==='function')originalChoose(id);
  };
  var originalOpenForBusiness=window.openTransactionForBusiness;
  window.openTransactionForBusiness=function(type,id){
    openWalletPicker(type);
    pendingBusiness=id||'';
  };
  var originalOpen=window.openTransaction;
  window.openTransaction=function(id){
    if(id&&typeof window.openTransactionForm==='function'){
      var t=(st().transactions||[]).find(function(x){return x.id===id;});
      window.openTransactionForm(id,t?t.businessId||'':'');
      return;
    }
    var picker=document.getElementById('txTypePicker');
    if(picker)picker.style.display='flex';
    else if(typeof originalOpen==='function')originalOpen(id);
  };
  var originalRender=window.render;
  if(typeof originalRender==='function'){
    window.render=function(){originalRender.apply(this,arguments);};
  }
})();
</script>
"""
    if "</body>" not in s:
        raise SystemExit("Tidak menemukan penutup body untuk alur pilih dompet")
    s=s.replace("</body>",wallet_first_js+"\n</body>",1)
    p.write_text(s)


# KasUsaha financial dashboard and reconciliation v1.
# Additive enhancement: preserve existing navigation/pages and all existing transaction data.
s = p.read_text()
if "KasUsaha financial dashboard and reconciliation v1" not in s:
    old_wallet_balance = """    transactions().forEach(function(t){
      var amount=Number(t.amount)||0;
      if(t.accountId===account.id){
        if(t.type==='income') balance+=amount;
        else if(t.type==='expense'||t.type==='transfer') balance-=amount;
      }
      if(t.type==='transfer'&&t.toAccountId===account.id) balance+=amount;
    });
    return balance;
  }
  function accountUsed(id){"""
    new_wallet_balance = """    transactions().forEach(function(t){
      var amount=Number(t.amount)||0;
      if(t.accountId===account.id){
        if(t.type==='income') balance+=amount;
        else if(t.type==='expense'||t.type==='transfer') balance-=amount;
      }
      if(t.type==='transfer'&&t.toAccountId===account.id) balance+=amount;
    });
    ((appState().walletAdjustments)||[]).forEach(function(a){if(a.accountId===account.id)balance+=Number(a.delta)||0;});
    return balance;
  }
  function accountUsed(id){"""
    if old_wallet_balance not in s:
        raise SystemExit("Tidak menemukan fungsi saldo dompet untuk memperluas penyesuaian")
    s = s.replace(old_wallet_balance, new_wallet_balance, 1)
    old_account_used = """  function accountUsed(id){
    return transactions().some(function(t){return t.accountId===id||t.toAccountId===id;});
  }"""
    new_account_used = """  function accountUsed(id){
    return transactions().some(function(t){return t.accountId===id||t.toAccountId===id;}) ||
      ((appState().walletAdjustments)||[]).some(function(a){return a.accountId===id;});
  }"""
    if old_account_used not in s:
        raise SystemExit("Tidak menemukan pemeriksaan penggunaan dompet")
    s = s.replace(old_account_used, new_account_used, 1)
    balance_match = re.search(r"(function balance\(a\)\{[\s\S]*?)(\n\s*return n;\s*\})", s)
    if not balance_match:
        raise SystemExit("Tidak menemukan fungsi saldo pada pemilih dompet")
    s = s[:balance_match.start(2)] + "\n     (((st().walletAdjustments)||[])).forEach(function(x){if(x.accountId===a.id)n+=Number(x.delta)||0;});" + s[balance_match.start(2):]

    finance_ui_js = r"""
<script>
/* KasUsaha financial dashboard and reconciliation v1 */
(function(){
  if(window.__ruFinancialDashboardV1)return;
  window.__ruFinancialDashboardV1=true;
  function app(){return (typeof state!=='undefined'&&state)?state:(window.state||{});}
  function txs(){return Array.isArray(app().transactions)?app().transactions:[];}
  function wallets(){return Array.isArray(app().accounts)?app().accounts:[];}
  function businesses(){return (Array.isArray(app().businesses)?app().businesses:[]).filter(function(b){return !b.archived;});}
  function adjustments(){return Array.isArray(app().walletAdjustments)?app().walletAdjustments:[];}
  function ensureAdjustments(){if(!Array.isArray(app().walletAdjustments))app().walletAdjustments=[];return app().walletAdjustments;}
  function esc(v){return String(v==null?'':v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
  function rupiah(v){return 'Rp'+(Number(v)||0).toLocaleString('id-ID');}
  function walletName(id){var a=wallets().find(function(x){return x.id===id;});return a?a.name||'Dompet':'Dompet dihapus';}
  function businessName(id){var b=businesses().find(function(x){return x.id===id;});return b?b.name:(id?'Usaha diarsipkan':'Operasional umum');}
  function categoryName(id){var c=(app().categories||[]).find(function(x){return x.id===id;});return c?c.name:'';}
  function typeName(t){return t==='income'?'Pemasukan':t==='expense'?'Pengeluaran':t==='transfer'?'Transfer antar dompet':'Penyesuaian saldo';}
  function walletBalance(a){
    var n=Number(a.opening!==undefined?a.opening:(a.balance!==undefined?a.balance:0))||0;
    txs().forEach(function(t){
      var v=Number(t.amount)||0;
      if(t.accountId===a.id){if(t.type==='income')n+=v;else if(t.type==='expense'||t.type==='transfer')n-=v;}
      if(t.type==='transfer'&&t.toAccountId===a.id)n+=v;
    });
    adjustments().forEach(function(x){if(x.accountId===a.id)n+=Number(x.delta)||0;});
    return n;
  }
  function totalBalance(){return wallets().reduce(function(n,a){return n+walletBalance(a);},0);}
  function currentDate(){var d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
  function monthKey(t){var d=String(t&&t.date||'');if(/^\d{4}-\d{2}-\d{2}$/.test(d))return d.slice(0,7);var m=String(t&&(t.reportMonth||t.monthKey||t.month)||'');return /^\d{4}-\d{2}/.test(m)?m.slice(0,7):'';}
  function dateKey(t){var d=String(t&&t.date||'');return /^\d{4}-\d{2}-\d{2}$/.test(d)?d:'';}
  function saveApp(){
    try{if(typeof save==='function')save();else if(typeof window.save==='function')window.save();}
    catch(e){alert('Gagal menyimpan data. Ekspor cadangan JSON dan coba kembali. '+(e&&e.message||''));return false;}
    try{if(typeof window.render==='function')window.render();}catch(e){}
    try{if(typeof window.renderRuMonthlyBusinessReport==='function')window.renderRuMonthlyBusinessReport();}catch(e){}
    refreshDashboard();renderWalletView();renderFinanceReport();
    return true;
  }
  var css = '<style id="ruFinancialDashboardCss">'
    + '#ruFinanceDash{background:#fff;border:1px solid var(--line);border-radius:18px;padding:15px;margin:14px 0 18px;box-shadow:0 8px 24px rgba(25,40,70,.045)}'
    + '#ruFinanceDash .ru-fd-head,#ruAllWallets .ru-fd-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap}'
    + '#ruFinanceDash h2,#ruAllWallets h2,#ruAdvancedReport h2{font-size:17px;margin:0 0 4px}'
    + '.ru-fd-sub{font-size:12px;color:var(--muted);line-height:1.5}'
    + '.ru-fd-kpis{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:13px}'
    + '.ru-fd-kpi{border:1px solid var(--line);border-radius:13px;padding:11px;min-width:0;background:#fff}'
    + '.ru-fd-kpi small{display:block;font-size:11px;color:var(--muted);margin-bottom:6px}'
    + '.ru-fd-kpi strong{display:block;font-size:clamp(12px,3.5vw,18px);overflow-wrap:anywhere}'
    + '.ru-fd-chart{margin-top:15px;display:grid;gap:12px}'
    + '.ru-fd-month{display:grid;grid-template-columns:47px minmax(0,1fr);gap:9px;align-items:center}'
    + '.ru-fd-month-label{font-size:11px;color:var(--muted)}.ru-fd-bars{display:grid;gap:5px;min-width:0}'
    + '.ru-fd-barline{display:flex;align-items:center;gap:6px;min-width:0}.ru-fd-bar{height:9px;border-radius:99px;min-width:2px;max-width:100%}'
    + '.ru-fd-bar.in{background:#0c9b77}.ru-fd-bar.out{background:#ef7b68}.ru-fd-barline small{font-size:10px;color:var(--muted);white-space:nowrap}'
    + '#ruFinanceDash .ru-fd-legend{display:flex;gap:13px;font-size:11px;color:var(--muted);margin-top:9px;flex-wrap:wrap}'
    + '.ru-fd-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px}.ru-fd-link{cursor:pointer}'
    + '#ruAdvancedReport{background:#fff;border:1px solid var(--line);border-radius:18px;padding:15px;margin:0 0 16px}'
    + '#ruAdvancedReport .ru-fr-controls{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:13px 0}'
    + '#ruAdvancedReport label{display:block;font-size:12px;color:var(--muted);margin-bottom:5px}'
    + '#ruAdvancedReport input,#ruAdvancedReport select{width:100%;min-width:0;box-sizing:border-box;border:1px solid var(--line);border-radius:10px;padding:10px;background:#fff;color:var(--ink)}'
    + '#ruAdvancedReport .ru-fr-actions{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 13px}#ruAdvancedReport .ru-fr-actions button{flex:1;min-width:125px}'
    + '#ruAdvancedReport .ru-fr-results{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin:12px 0}'
    + '#ruAdvancedReport .ru-fr-metric{border:1px solid var(--line);border-radius:12px;padding:10px;min-width:0}'
    + '#ruAdvancedReport .ru-fr-metric small{display:block;color:var(--muted);font-size:11px;margin-bottom:5px}'
    + '#ruAdvancedReport .ru-fr-metric strong{display:block;font-size:clamp(11px,3.3vw,16px);overflow-wrap:anywhere}'
    + '#ruAdvancedReport .ru-fr-business{border:1px solid var(--line);border-radius:13px;padding:12px;margin:9px 0}'
    + '#ruAdvancedReport .ru-fr-business-head{display:flex;justify-content:space-between;gap:8px;align-items:center}'
    + '#ruAdvancedReport .ru-fr-business-head strong{overflow-wrap:anywhere}#ruAdvancedReport .ru-fr-business-head span{font-weight:800;white-space:nowrap}'
    + '#ruAdvancedReport .ru-fr-tx{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;border-top:1px solid var(--line);padding:9px 0;font-size:12px}'
    + '#ruAdvancedReport .ru-fr-tx small{display:block;color:var(--muted);margin-top:3px}#ruAdvancedReport .ru-fr-tx strong{white-space:nowrap}'
    + '#ruAdvancedReport .ru-fr-chart{display:grid;gap:10px;margin:12px 0}.ru-fr-chart-row{display:grid;grid-template-columns:54px minmax(0,1fr);gap:8px;align-items:center}.ru-fr-chart-label{font-size:11px;color:var(--muted)}'
    + '.ru-fr-chart-bars{display:grid;gap:4px}.ru-fr-chart-bar{height:8px;border-radius:20px}.ru-fr-chart-bar.in{background:#0c9b77}.ru-fr-chart-bar.out{background:#ef7b68}'
    + '#ruAllWallets{display:none;position:fixed;inset:0;z-index:20000;background:#f5f7fb;color:var(--ink);overflow-y:auto;padding:calc(14px + env(safe-area-inset-top)) 14px calc(24px + env(safe-area-inset-bottom));box-sizing:border-box}'
    + '#ruAllWallets .ru-fd-sheet{max-width:650px;margin:0 auto}#ruAllWallets .ru-fd-panel{background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px;margin-top:12px}'
    + '.ru-aw-card{border:1px solid var(--line);border-radius:13px;padding:13px;display:flex;justify-content:space-between;gap:10px;align-items:center;margin-top:8px;background:#fff;cursor:pointer}'
    + '.ru-aw-card small{display:block;color:var(--muted);margin-top:4px}.ru-aw-card strong{overflow-wrap:anywhere}.ru-aw-history{border-top:1px solid var(--line);padding:10px 0;font-size:12px;display:flex;justify-content:space-between;gap:10px}'
    + '.ru-fd-btn{border:1px solid var(--line);background:#fff;border-radius:10px;padding:10px 12px;color:var(--ink);font-size:13px}.ru-fd-primary{background:#176d62;color:#fff;border-color:#176d62}'
    + '#ruReconcileModal{display:none;position:fixed;inset:0;z-index:21000;background:rgba(15,23,42,.55);padding:14px;align-items:flex-end;justify-content:center;box-sizing:border-box}'
    + '#ruReconcileModal .ru-rec-dialog{width:100%;max-width:520px;max-height:92dvh;overflow:auto;border-radius:20px;background:#fff;padding:17px;box-sizing:border-box;color:#172033}'
    + '#ruReconcileModal input,#ruReconcileModal select,#ruReconcileModal textarea{width:100%;box-sizing:border-box;border:1px solid #dce2eb;border-radius:10px;padding:11px;background:#fff;color:#172033}'
    + '#ruReconcileModal .ru-rec-field{margin:12px 0}#ruReconcileModal label{display:block;margin-bottom:5px;font-size:12px;color:#586579}'
    + '@media(max-width:540px){.ru-fd-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}#ruAdvancedReport .ru-fr-controls{grid-template-columns:1fr}#ruAdvancedReport .ru-fr-results{grid-template-columns:repeat(2,minmax(0,1fr))}.ru-fd-month{grid-template-columns:39px minmax(0,1fr)}}'
    + '</style>';
  if(!document.getElementById('ruFinancialDashboardCss'))document.head.insertAdjacentHTML('beforeend',css);

  function ensureDashboard(){
    var page=document.getElementById('page-dashboard');if(!page)return;
    if(!document.getElementById('ruFinanceDash')){
      var html='<section id="ruFinanceDash"><div class="ru-fd-head"><div><h2>Ringkasan keuangan</h2><div class="ru-fd-sub">Pemasukan dan pengeluaran enam bulan terakhir.</div></div><button type="button" class="ru-fd-btn" id="ruOpenAllWallets">Lihat semua saldo ›</button></div><div id="ruFdKpis" class="ru-fd-kpis"></div><div id="ruFdChart" class="ru-fd-chart"></div><div class="ru-fd-legend"><span><i class="ru-fd-dot" style="background:#0c9b77"></i>Pemasukan</span><span><i class="ru-fd-dot" style="background:#ef7b68"></i>Pengeluaran</span></div></section>';
      var cards=page.querySelector('.cards');if(cards)cards.insertAdjacentHTML('afterend',html);else page.insertAdjacentHTML('beforeend',html);
    }
  }
  function lastMonths(){
    var out=[],d=new Date();d.setDate(1);d.setHours(12,0,0,0);
    for(var i=5;i>=0;i--){var x=new Date(d.getFullYear(),d.getMonth()-i,1,12),key=x.getFullYear()+'-'+String(x.getMonth()+1).padStart(2,'0');out.push({key:key,label:x.toLocaleDateString('id-ID',{month:'short'}),inc:0,out:0});}
    out.forEach(function(m){txs().forEach(function(t){if(monthKey(t)!==m.key)return;var v=Number(t.amount)||0;if(t.type==='income')m.inc+=v;else if(t.type==='expense')m.out+=v;});});
    return out;
  }
  function bindTotalBalance(){
    var page=document.getElementById('page-dashboard');if(!page)return;
    var cards=[].slice.call(page.querySelectorAll('.cards .card'));
    var chosen=cards.find(function(c){return /total\s+saldo|saldo\s+total|total\s+balance|total\s+seluruh\s+saldo/i.test(c.textContent||'');})||cards[3];
    if(chosen){chosen.classList.add('ru-fd-link');chosen.setAttribute('role','button');chosen.setAttribute('tabindex','0');chosen.setAttribute('aria-label','Lihat saldo semua dompet');}
  }
  function refreshDashboard(){
    ensureDashboard();bindTotalBalance();
    var k=document.getElementById('ruFdKpis'),chart=document.getElementById('ruFdChart');if(!k||!chart)return;
    var key=currentDate().slice(0,7),inc=0,out=0,count=0;
    txs().forEach(function(t){if(monthKey(t)===key){if(t.type==='income')inc+=Number(t.amount)||0;else if(t.type==='expense')out+=Number(t.amount)||0;if(t.type==='income'||t.type==='expense')count++;}});
    k.innerHTML='<div class="ru-fd-kpi"><small>Total seluruh saldo</small><strong>'+rupiah(totalBalance())+'</strong></div><div class="ru-fd-kpi"><small>Pemasukan bulan ini</small><strong style="color:#0c9b77">'+rupiah(inc)+'</strong></div><div class="ru-fd-kpi"><small>Pengeluaran bulan ini</small><strong style="color:#d65c4b">'+rupiah(out)+'</strong></div><div class="ru-fd-kpi"><small>Arus kas bulan ini</small><strong style="color:'+(inc-out<0?'#d65c4b':'#0c8069')+'">'+rupiah(inc-out)+'</strong></div><div class="ru-fd-kpi"><small>Transaksi bulan ini</small><strong>'+count+'</strong></div><div class="ru-fd-kpi"><small>Jumlah dompet</small><strong>'+wallets().length+'</strong></div>';
    var months=lastMonths(),max=1;months.forEach(function(m){max=Math.max(max,m.inc,m.out);});
    chart.innerHTML=months.map(function(m){return '<div class="ru-fd-month"><div class="ru-fd-month-label">'+esc(m.label)+'</div><div class="ru-fd-bars"><div class="ru-fd-barline"><div class="ru-fd-bar in" style="width:'+Math.max(m.inc?1:0,m.inc/max*100)+'%"></div><small>'+rupiah(m.inc)+'</small></div><div class="ru-fd-barline"><div class="ru-fd-bar out" style="width:'+Math.max(m.out?1:0,m.out/max*100)+'%"></div><small>'+rupiah(m.out)+'</small></div></div></div>';}).join('');
  }

  var walletViewId=null;
  function ensureWalletView(){
    if(document.getElementById('ruAllWallets'))return;
    var html='<div id="ruAllWallets"><div class="ru-fd-sheet"><div class="ru-fd-head"><div><div class="ru-fd-sub">DOMPET & REKENING</div><h2>Semua saldo</h2><div class="ru-fd-sub">Saldo dihitung dari saldo awal, transaksi, transfer, dan penyesuaian.</div></div><button type="button" class="ru-fd-btn" id="ruCloseAllWallets">← Kembali</button></div><div class="ru-fd-panel"><div class="ru-fd-sub">TOTAL SELURUH SALDO</div><div id="ruAllWalletTotal" style="font-size:25px;font-weight:850;margin-top:5px;overflow-wrap:anywhere"></div><div id="ruWalletCards"></div><div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:14px"><button type="button" class="ru-fd-btn ru-fd-primary" id="ruOpenReconcile">＋ Rekonsiliasi / penyesuaian</button></div></div><div class="ru-fd-panel"><h2 style="font-size:15px">Riwayat penyesuaian saldo</h2><div class="ru-fd-sub">Catatan ini terpisah dari pemasukan dan pengeluaran transaksi.</div><div id="ruAdjustHistory"></div></div><div class="ru-fd-panel" id="ruWalletTransactionsPanel" style="display:none"><div class="ru-fd-head"><h2 id="ruWalletTxTitle">Riwayat dompet</h2><button type="button" class="ru-fd-btn" id="ruCloseWalletTx">Tutup riwayat</button></div><div id="ruWalletTxHistory"></div></div></div></div>';
    document.body.insertAdjacentHTML('beforeend',html);
  }
  function dateTimeText(s){if(!s)return '-';var d=new Date(s);return isNaN(d.getTime())?String(s):d.toLocaleString('id-ID');}
  function renderWalletView(){
    ensureWalletView();
    var total=document.getElementById('ruAllWalletTotal'),host=document.getElementById('ruWalletCards'),hist=document.getElementById('ruAdjustHistory');
    if(!total||!host||!hist)return;
    total.textContent=rupiah(totalBalance());
    host.innerHTML=wallets().map(function(a){
      return '<div class="ru-aw-card" data-ru-wallet-detail="'+esc(a.id)+'"><div style="min-width:0"><strong>'+esc(a.name||'Dompet')+'</strong><small>'+esc(({cash:'Tunai / Kas',bank:'Rekening bank',ewallet:'E-wallet',other:'Lainnya'})[a.type]||'Dompet')+' · Saldo awal '+rupiah(a.opening!==undefined?a.opening:a.balance)+'</small></div><div style="text-align:right;min-width:0"><strong>'+rupiah(walletBalance(a))+'</strong><small>Lihat riwayat ›</small></div></div>';
    }).join('')||'<div class="ru-fd-sub" style="padding:12px 0">Belum ada dompet.</div>';
    var arr=adjustments().slice().sort(function(a,b){return String(b.createdAt||b.date||'').localeCompare(String(a.createdAt||a.date||''));});
    hist.innerHTML=arr.map(function(a){return '<div class="ru-aw-history"><div><strong>'+esc(walletName(a.accountId))+'</strong><small style="display:block;color:var(--muted);margin-top:3px">'+esc(dateTimeText(a.createdAt||a.date))+' · '+esc(a.note||'Penyesuaian saldo')+'</small></div><strong style="white-space:nowrap;color:'+(Number(a.delta)<0?'#d65c4b':'#0c8069')+'">'+(Number(a.delta)>0?'+':'')+rupiah(a.delta)+'</strong></div>';}).join('')||'<div class="ru-fd-sub" style="padding:12px 0">Belum ada penyesuaian saldo.</div>';
    if(walletViewId)renderWalletTransactions(walletViewId);
  }
  function renderWalletTransactions(id){
    walletViewId=id;var panel=document.getElementById('ruWalletTransactionsPanel');if(!panel)return;
    var a=wallets().find(function(x){return x.id===id;});if(!a){panel.style.display='none';return;}
    document.getElementById('ruWalletTxTitle').textContent='Riwayat: '+(a.name||'Dompet');
    var rows=[];
    txs().forEach(function(t){
      var amount=Number(t.amount)||0;
      if(t.accountId===id){
        var incoming=t.type==='income',label=t.type==='transfer'?'Transfer keluar':typeName(t.type);
        rows.push({date:t.date||'',label:label,note:t.note||categoryName(t.categoryId),amount:(incoming?1:-1)*amount});
      }
      if(t.type==='transfer'&&t.toAccountId===id)rows.push({date:t.date||'',label:'Transfer masuk',note:'Dari '+walletName(t.accountId),amount:amount});
    });
    adjustments().filter(function(x){return x.accountId===id;}).forEach(function(x){rows.push({date:x.createdAt||x.date||'',label:'Penyesuaian saldo',note:x.note||'',amount:Number(x.delta)||0,sortDate:x.createdAt||x.date||''});});
    rows.sort(function(x,y){return String(y.sortDate||y.date||'').localeCompare(String(x.sortDate||x.date||''));});
    document.getElementById('ruWalletTxHistory').innerHTML=rows.map(function(x){return '<div class="ru-aw-history"><div><strong>'+esc(x.label)+'</strong><small style="display:block;color:var(--muted);margin-top:3px">'+esc(x.date)+' · '+esc(x.note||'')+'</small></div><strong style="white-space:nowrap;color:'+(x.amount<0?'#d65c4b':'#0c8069')+'">'+(x.amount>0?'+':'')+rupiah(x.amount)+'</strong></div>';}).join('')||'<div class="ru-fd-sub" style="padding:12px 0">Belum ada riwayat untuk dompet ini.</div>';
    panel.style.display='block';
  }

  function ensureReconcileModal(){
    if(document.getElementById('ruReconcileModal'))return;
    var html='<div id="ruReconcileModal"><div class="ru-rec-dialog"><div style="display:flex;justify-content:space-between;gap:10px;align-items:center"><div><h2 style="margin:0;font-size:19px">Rekonsiliasi saldo</h2><div style="font-size:12px;color:#667085;margin-top:4px">Bandingkan saldo catatan dengan saldo sebenarnya.</div></div><button type="button" class="ru-fd-btn" id="ruRecClose">✕</button></div><form id="ruReconcileForm"><div class="ru-rec-field"><label for="ruRecWallet">Dompet / rekening</label><select id="ruRecWallet" required></select></div><div class="ru-rec-field"><label for="ruRecActual">Saldo aktual yang dihitung (Rp)</label><input id="ruRecActual" type="number" step="1" required placeholder="Masukkan saldo aktual"></div><div class="ru-fd-panel" style="margin:10px 0;padding:12px"><div style="font-size:12px;color:#667085">Saldo sistem saat ini</div><strong id="ruRecSystem" style="display:block;font-size:19px;margin:4px 0"></strong><div style="font-size:12px;color:#667085">Selisih penyesuaian</div><strong id="ruRecDifference" style="display:block;font-size:18px;margin-top:4px">-</strong></div><div class="ru-rec-field"><label for="ruRecNote">Catatan / alasan (opsional)</label><textarea id="ruRecNote" rows="2" maxlength="200" placeholder="Contoh: saldo awal dikoreksi setelah cek kas"></textarea></div><div style="display:flex;gap:8px;margin-top:16px"><button type="button" id="ruRecCancel" class="ru-fd-btn" style="flex:1">Batal</button><button type="submit" class="ru-fd-btn ru-fd-primary" style="flex:1">Simpan penyesuaian</button></div></form></div></div>';
    document.body.insertAdjacentHTML('beforeend',html);
  }
  function openReconcile(){
    ensureReconcileModal();var sel=document.getElementById('ruRecWallet');
    sel.innerHTML=wallets().map(function(a){return '<option value="'+esc(a.id)+'">'+esc(a.name||'Dompet')+'</option>';}).join('');
    if(!wallets().length){alert('Tambahkan dompet terlebih dahulu.');return;}
    document.getElementById('ruRecActual').value='';
    document.getElementById('ruRecNote').value='';
    updateReconcile();document.getElementById('ruReconcileModal').style.display='flex';
  }
  function updateReconcile(){
    var id=document.getElementById('ruRecWallet');if(!id)return;
    var a=wallets().find(function(x){return x.id===id.value;});if(!a)return;
    var sys=walletBalance(a),raw=document.getElementById('ruRecActual').value,valid=raw!==''&&Number.isFinite(Number(raw)),diff=valid?Math.round(Number(raw)-sys):null;
    document.getElementById('ruRecSystem').textContent=rupiah(sys);
    document.getElementById('ruRecDifference').textContent=diff===null?'Masukkan saldo aktual':(diff>0?'+':'')+rupiah(diff);
    document.getElementById('ruRecDifference').style.color=diff===null?'#667085':diff<0?'#c24133':'#087f5b';
  }

  function ensureReport(){
    var page=document.getElementById('page-reports');if(!page)return;
    if(document.getElementById('ruAdvancedReport'))return;
    var html='<div id="ruAdvancedReport"><div class="ru-fd-head"><div><h2>Laporan keuangan</h2><div class="ru-fd-sub">Filter periode dan usaha. Transfer tidak dihitung sebagai pemasukan atau pengeluaran.</div></div></div><div class="ru-fr-controls"><div><label for="ruFrPeriod">Periode laporan</label><select id="ruFrPeriod"><option value="daily">Harian</option><option value="weekly">Mingguan</option><option value="monthly" selected>Bulanan</option><option value="yearly">Tahunan</option><option value="custom">Rentang tanggal khusus</option></select></div><div id="ruFrDateWrap"><label for="ruFrDate">Tanggal acuan</label><input id="ruFrDate" type="date"></div><div id="ruFrMonthWrap" style="display:none"><label for="ruFrMonth">Bulan laporan</label><input id="ruFrMonth" type="month"></div><div id="ruFrYearWrap" style="display:none"><label for="ruFrYear">Tahun laporan</label><input id="ruFrYear" type="number" min="2000" max="2100"></div><div id="ruFrStartWrap" style="display:none"><label for="ruFrStart">Tanggal mulai</label><input id="ruFrStart" type="date"></div><div id="ruFrEndWrap" style="display:none"><label for="ruFrEnd">Tanggal akhir</label><input id="ruFrEnd" type="date"></div><div><label for="ruFrBusiness">Usaha</label><select id="ruFrBusiness"><option value="">Semua usaha</option></select></div></div><div id="ruFrRangeText" class="ru-fd-sub"></div><div id="ruFrResults" class="ru-fr-results"></div><h3 style="font-size:14px;margin:16px 0 8px">Grafik pemasukan vs pengeluaran</h3><div id="ruFrChart" class="ru-fr-chart"></div><h3 style="font-size:14px;margin:16px 0 8px">Laba / rugi kas per usaha</h3><div class="ru-fd-sub">Perhitungan = pemasukan transaksi dikurangi pengeluaran transaksi yang tercatat. Biaya HPP tersendiri tidak ditambahkan lagi agar tidak berisiko dihitung ganda.</div><div id="ruFrBusinesses"></div><h3 style="font-size:14px;margin:16px 0 8px">Rincian transaksi</h3><div id="ruFrTransactions"></div><div class="ru-fr-actions"><button type="button" class="ru-fd-btn ru-fd-primary" id="ruFrExportExcel">Ekspor laporan Excel (CSV)</button><button type="button" class="ru-fd-btn" id="ruFrExportPdf">Ekspor laporan PDF</button></div><div class="ru-fd-sub">Laporan Excel disimpan sebagai CSV yang dapat dibuka di Excel. Ekspor cadangan JSON tetap terpisah di Pengaturan.</div></div>';
    var monthly=document.getElementById('ruMonthlyBusinessReport');
    if(monthly)monthly.insertAdjacentHTML('beforebegin',html);else page.insertAdjacentHTML('afterbegin',html);
    document.getElementById('ruFrDate').value=currentDate();
    document.getElementById('ruFrMonth').value=currentDate().slice(0,7);
    document.getElementById('ruFrYear').value=String(new Date().getFullYear());
    document.getElementById('ruFrStart').value=currentDate().slice(0,7)+'-01';
    document.getElementById('ruFrEnd').value=currentDate();
  }
  function periodRange(){
    var mode=document.getElementById('ruFrPeriod').value,ref=document.getElementById('ruFrDate').value||currentDate(),start='',end='',label='';
    if(mode==='daily'){start=end=ref;label='Harian: '+start;}
    else if(mode==='weekly'){
      var d=new Date(ref+'T12:00:00');var day=(d.getDay()+6)%7;d.setDate(d.getDate()-day);
      start=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
      d.setDate(d.getDate()+6);end=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');label='Mingguan: '+start+' s.d. '+end;
    }else if(mode==='monthly'){
      var m=document.getElementById('ruFrMonth').value||ref.slice(0,7);start=m+'-01';
      var d2=new Date(Number(m.slice(0,4)),Number(m.slice(5,7)),0,12);end=d2.getFullYear()+'-'+String(d2.getMonth()+1).padStart(2,'0')+'-'+String(d2.getDate()).padStart(2,'0');label='Bulanan: '+m;
    }else if(mode==='yearly'){
      var y=String(document.getElementById('ruFrYear').value||new Date().getFullYear());start=y+'-01-01';end=y+'-12-31';label='Tahunan: '+y;
    }else{
      start=document.getElementById('ruFrStart').value||currentDate();end=document.getElementById('ruFrEnd').value||currentDate();
      if(start>end){var tmp=start;start=end;end=tmp;}label='Rentang khusus: '+start+' s.d. '+end;
    }
    return {mode:mode,start:start,end:end,label:label};
  }
  function showReportControls(){
    var mode=document.getElementById('ruFrPeriod').value;
    document.getElementById('ruFrDateWrap').style.display=(mode==='daily'||mode==='weekly')?'block':'none';
    document.getElementById('ruFrMonthWrap').style.display=mode==='monthly'?'block':'none';
    document.getElementById('ruFrYearWrap').style.display=mode==='yearly'?'block':'none';
    document.getElementById('ruFrStartWrap').style.display=mode==='custom'?'block':'none';
    document.getElementById('ruFrEndWrap').style.display=mode==='custom'?'block':'none';
  }
  function txInRange(t,r){
    var d=dateKey(t);
    if(d)return d>=r.start&&d<=r.end;
    var m=monthKey(t);
    if(!m)return false;
    if(r.mode==='monthly')return m===r.start.slice(0,7);
    if(r.mode==='yearly')return m.slice(0,4)===r.start.slice(0,4);
    return false;
  }
  function getReportData(){
    var r=periodRange(),biz=document.getElementById('ruFrBusiness').value;
    var list=txs().filter(function(t){return txInRange(t,r)&&(!biz||t.businessId===biz);}).sort(function(a,b){return String(a.date||'').localeCompare(String(b.date||''));});
    var inc=0,out=0,count=0;
    list.forEach(function(t){if(t.type==='income'){inc+=Number(t.amount)||0;count++;}else if(t.type==='expense'){out+=Number(t.amount)||0;count++;}});
    var adj=adjustments().filter(function(a){var d=String(a.date||a.createdAt||'').slice(0,10);return d>=r.start&&d<=r.end&&(!biz||!a.businessId||a.businessId===biz);});
    return {range:r,business:biz,transactions:list,inc:inc,out:out,net:inc-out,count:count,adjustments:adj};
  }
  function summaryHtml(d){
    return '<div class="ru-fr-metric"><small>Pemasukan</small><strong style="color:#0c9b77">'+rupiah(d.inc)+'</strong></div><div class="ru-fr-metric"><small>Pengeluaran</small><strong style="color:#d65c4b">'+rupiah(d.out)+'</strong></div><div class="ru-fr-metric"><small>Arus kas bersih</small><strong style="color:'+(d.net<0?'#d65c4b':'#087f5b')+'">'+rupiah(d.net)+'</strong></div><div class="ru-fr-metric"><small>Jumlah transaksi</small><strong>'+d.count+'</strong></div>';
  }
  function periodSeries(d){
    var days=[],start=new Date(d.range.start+'T12:00:00'),end=new Date(d.range.end+'T12:00:00'),span=Math.round((end-start)/86400000)+1;
    var unit=(d.range.mode==='yearly'||span>62)?'month':(span>14?'week':'day');
    var map={};
    for(var i=0;i<span;i++){
      var dt=new Date(start);dt.setDate(start.getDate()+i);
      var key=unit==='month'?dt.getFullYear()+'-'+String(dt.getMonth()+1).padStart(2,'0'):unit==='week'?String(Math.floor(i/7)):dt.getFullYear()+'-'+String(dt.getMonth()+1).padStart(2,'0')+'-'+String(dt.getDate()).padStart(2,'0');
      if(!map[key])map[key]={key:key,label:unit==='month'?dt.toLocaleDateString('id-ID',{month:'short'}):unit==='week'?'M'+(Math.floor(i/7)+1):String(dt.getDate()),inc:0,out:0};
    }
    d.transactions.forEach(function(t){var date=dateKey(t);if(!date)return;var dt=new Date(date+'T12:00:00'),key=unit==='month'?dt.getFullYear()+'-'+String(dt.getMonth()+1).padStart(2,'0'):unit==='week'?String(Math.floor((dt-start)/86400000/7)):dt.getFullYear()+'-'+String(dt.getMonth()+1).padStart(2,'0')+'-'+String(dt.getDate()).padStart(2,'0');var b=map[key];if(!b)return;if(t.type==='income')b.inc+=Number(t.amount)||0;else if(t.type==='expense')b.out+=Number(t.amount)||0;});
    return Object.keys(map).map(function(k){return map[k];}).slice(0,unit==='day'?31:12);
  }
  function renderReportChart(d){
    var host=document.getElementById('ruFrChart'),series=periodSeries(d),max=1;series.forEach(function(x){max=Math.max(max,x.inc,x.out);});
    host.innerHTML=series.map(function(x){return '<div class="ru-fr-chart-row"><div class="ru-fr-chart-label">'+esc(x.label)+'</div><div class="ru-fr-chart-bars"><div class="ru-fd-barline"><div class="ru-fr-chart-bar in" style="width:'+Math.max(x.inc?1:0,x.inc/max*100)+'%"></div><small>'+rupiah(x.inc)+'</small></div><div class="ru-fd-barline"><div class="ru-fr-chart-bar out" style="width:'+Math.max(x.out?1:0,x.out/max*100)+'%"></div><small>'+rupiah(x.out)+'</small></div></div></div>';}).join('')||'<div class="ru-fd-sub">Belum ada data untuk grafik.</div>';
  }
  function renderReportBusinesses(d){
    var all=businesses().filter(function(b){return !d.business||b.id===d.business;}),out='';
    all.forEach(function(b){
      var list=d.transactions.filter(function(t){return t.businessId===b.id&&(t.type==='income'||t.type==='expense');}),inc=0,exp=0;
      list.forEach(function(t){if(t.type==='income')inc+=Number(t.amount)||0;else exp+=Number(t.amount)||0;});
      out+='<div class="ru-fr-business"><div class="ru-fr-business-head"><strong>'+esc(b.name)+'</strong><span style="color:'+(inc-exp<0?'#d65c4b':'#087f5b')+'">'+rupiah(inc-exp)+'</span></div><div class="ru-fd-sub" style="margin-top:6px">Pemasukan '+rupiah(inc)+' · Pengeluaran '+rupiah(exp)+' · '+list.length+' transaksi</div></div>';
    });
    if(!d.business){
      var general=d.transactions.filter(function(t){return !t.businessId&&(t.type==='income'||t.type==='expense');}),gi=0,go=0;
      general.forEach(function(t){if(t.type==='income')gi+=Number(t.amount)||0;else go+=Number(t.amount)||0;});
      if(general.length)out+='<div class="ru-fr-business"><div class="ru-fr-business-head"><strong>Operasional umum</strong><span>'+rupiah(gi-go)+'</span></div><div class="ru-fd-sub" style="margin-top:6px">Pemasukan '+rupiah(gi)+' · Pengeluaran '+rupiah(go)+' · '+general.length+' transaksi</div></div>';
    }
    document.getElementById('ruFrBusinesses').innerHTML=out||'<div class="ru-fd-sub">Belum ada data usaha untuk periode ini.</div>';
  }
  function renderReportTransactions(d){
    var arr=d.transactions.slice().reverse().slice(0,50),host=document.getElementById('ruFrTransactions');
    host.innerHTML=arr.map(function(t){var v=Number(t.amount)||0,sign=t.type==='income'?'+':t.type==='expense'?'−':'',color=t.type==='income'?'#087f5b':t.type==='expense'?'#c24133':'var(--muted)';return '<div class="ru-fr-tx"><div style="min-width:0"><strong>'+esc(t.note||typeName(t.type))+'</strong><small>'+esc(t.date||monthKey(t)||'Tanggal tidak tercantum')+' · '+esc(typeName(t.type))+' · '+esc(businessName(t.businessId))+' · '+esc(walletName(t.accountId))+'</small></div><strong style="color:'+color+'">'+sign+rupiah(v)+'</strong></div>';}).join('')||'<div class="ru-fd-sub">Tidak ada transaksi pada periode ini.</div>';
    if(d.transactions.length>50)host.insertAdjacentHTML('beforeend','<div class="ru-fd-sub">Menampilkan 50 transaksi terakhir dari '+d.transactions.length+' transaksi. Ekspor berisi seluruh transaksi yang terfilter.</div>');
  }
  function fillBusinessSelect(){
    var sel=document.getElementById('ruFrBusiness');if(!sel)return;var old=sel.value;
    sel.innerHTML='<option value="">Semua usaha</option>'+businesses().map(function(b){return '<option value="'+esc(b.id)+'">'+esc(b.name)+'</option>';}).join('');
    if([].some.call(sel.options,function(o){return o.value===old;}))sel.value=old;
  }
  function renderFinanceReport(){
    if(!document.getElementById('ruAdvancedReport'))ensureReport();
    var period=document.getElementById('ruFrPeriod');if(!period)return;
    showReportControls();fillBusinessSelect();
    var d=getReportData();
    document.getElementById('ruFrRangeText').textContent=d.range.label;
    document.getElementById('ruFrResults').innerHTML=summaryHtml(d);
    renderReportChart(d);renderReportBusinesses(d);renderReportTransactions(d);
  }
  function csvEscape(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"';}
  function csvExport(){
    var d=getReportData(),rows=[];
    rows.push(['LAPORAN KEUANGAN KASUSAHA',d.range.label],['Usaha',d.business?businessName(d.business):'Semua usaha'],[],['RINGKASAN'],['Pemasukan',d.inc],['Pengeluaran',d.out],['Arus kas bersih',d.net],['Jumlah transaksi',d.count],[],['LABA/RUGI KAS PER USAHA'],['Nama usaha','Pemasukan','Pengeluaran','Laba/rugi kas','Jumlah transaksi']);
    businesses().filter(function(b){return !d.business||b.id===d.business;}).forEach(function(b){var ts=d.transactions.filter(function(t){return t.businessId===b.id&&(t.type==='income'||t.type==='expense');}),i=0,o=0;ts.forEach(function(t){if(t.type==='income')i+=Number(t.amount)||0;else o+=Number(t.amount)||0;});rows.push([b.name,i,o,i-o,ts.length]);});
    rows.push([],['RINCIAN TRANSAKSI'],['Tanggal','Jenis','Usaha','Kategori','Dompet asal','Dompet tujuan','Nominal','Catatan']);
    d.transactions.forEach(function(t){rows.push([t.date||monthKey(t),typeName(t.type),businessName(t.businessId),categoryName(t.categoryId),walletName(t.accountId),walletName(t.toAccountId),Number(t.amount)||0,t.note||'']);});
    rows.push([],['PENYESUAIAN SALDO'],['Tanggal','Dompet','Selisih','Catatan']);
    d.adjustments.forEach(function(a){rows.push([a.date||a.createdAt,walletName(a.accountId),Number(a.delta)||0,a.note||'']);});
    return '\uFEFF'+rows.map(function(r){return r.map(csvEscape).join(',');}).join('\r\n');
  }
  function downloadFile(filename,mime,textData){
    var bytes=new TextEncoder().encode(textData),binary='';
    for(var i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode.apply(null,bytes.subarray(i,i+8192));
    var base64=btoa(binary);
    if(window.AndroidDownloads&&typeof window.AndroidDownloads.saveFile==='function'){window.AndroidDownloads.saveFile(filename,mime,base64);return;}
    var blob=new Blob([bytes],{type:mime}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=filename;document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(url);},3000);
  }
  function exportReportCsv(){
    try{var d=getReportData();downloadFile('KasUsaha-Laporan-'+d.range.start+'-sd-'+d.range.end+'.csv','text/csv;charset=utf-8',csvExport());if(typeof showToast==='function')showToast('Laporan untuk Excel disiapkan. Periksa folder Unduhan.');}
    catch(e){alert('Ekspor Excel gagal: '+(e&&e.message||e));}
  }
  function ascii(v){return String(v==null?'':v).normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/Rp/g,'Rp').replace(/[^\x20-\x7E]/g,' ');}
  function pdfEscape(v){return ascii(v).replace(/\\/g,'\\\\').replace(/\(/g,'\\(').replace(/\)/g,'\\)');}
  function makePdf(lines){
    var pages=[];for(var i=0;i<lines.length;i+=48)pages.push(lines.slice(i,i+48));if(!pages.length)pages=[['Laporan KasUsaha']];
    var objs=[];
    objs[1]='<< /Type /Catalog /Pages 2 0 R >>';
    var pageIds=[],next=4;
    objs[3]='<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>';
    pages.forEach(function(linesPage){
      var pageId=next++,contentId=next++;pageIds.push(pageId);
      var commands=['BT','/F1 9 Tf','50 790 Td','12 TL'];
      linesPage.forEach(function(line){commands.push('('+pdfEscape(line)+') Tj','T*');});
      commands.push('ET');
      var stream=commands.join('\n');
      objs[contentId]='<< /Length '+stream.length+' >>\nstream\n'+stream+'\nendstream';
      objs[pageId]='<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents '+contentId+' 0 R >>';
    });
    objs[2]='<< /Type /Pages /Count '+pageIds.length+' /Kids ['+pageIds.map(function(id){return id+' 0 R';}).join(' ')+'] >>';
    var pdf='%PDF-1.4\n',offsets=[0];
    for(var j=1;j<objs.length;j++){if(!objs[j])continue;offsets[j]=pdf.length;pdf+=j+' 0 obj\n'+objs[j]+'\nendobj\n';}
    var xref=pdf.length;pdf+='xref\n0 '+objs.length+'\n0000000000 65535 f \n';
    for(var k=1;k<objs.length;k++)pdf+=(offsets[k]||0).toString().padStart(10,'0')+' 00000 n \n';
    pdf+='trailer\n<< /Size '+objs.length+' /Root 1 0 R >>\nstartxref\n'+xref+'\n%%EOF';
    return pdf;
  }
  function exportReportPdf(){
    try{
      var d=getReportData(),lines=['LAPORAN KEUANGAN KASUSAHA',d.range.label,'Usaha: '+(d.business?businessName(d.business):'Semua usaha'),'','RINGKASAN','Pemasukan: '+rupiah(d.inc),'Pengeluaran: '+rupiah(d.out),'Arus kas bersih: '+rupiah(d.net),'Jumlah transaksi: '+d.count,'','LABA/RUGI KAS PER USAHA'];
      businesses().filter(function(b){return !d.business||b.id===d.business;}).forEach(function(b){var ts=d.transactions.filter(function(t){return t.businessId===b.id&&(t.type==='income'||t.type==='expense');}),i=0,o=0;ts.forEach(function(t){if(t.type==='income')i+=Number(t.amount)||0;else o+=Number(t.amount)||0;});lines.push(b.name+' | masuk '+rupiah(i)+' | keluar '+rupiah(o)+' | net '+rupiah(i-o));});
      lines.push('','RINCIAN TRANSAKSI (semua yang terfilter)');
      d.transactions.forEach(function(t){lines.push((t.date||monthKey(t)||'-')+' | '+typeName(t.type)+' | '+businessName(t.businessId)+' | '+walletName(t.accountId)+' | '+rupiah(t.amount)+' | '+(t.note||''));});
      lines.push('','PENYESUAIAN SALDO');d.adjustments.forEach(function(a){lines.push((a.date||a.createdAt||'-')+' | '+walletName(a.accountId)+' | '+rupiah(a.delta)+' | '+(a.note||''));});
      lines.push('','Catatan: laba/rugi kas dihitung dari transaksi pemasukan dikurangi pengeluaran. Transfer antar dompet tidak dihitung.');
      downloadFile('KasUsaha-Laporan-'+d.range.start+'-sd-'+d.range.end+'.pdf','application/pdf',makePdf(lines));
      if(typeof showToast==='function')showToast('Laporan PDF disiapkan. Periksa folder Unduhan.');
    }catch(e){alert('Ekspor PDF gagal: '+(e&&e.message||e));}
  }

  document.addEventListener('click',function(e){
    var open=e.target&&e.target.closest?e.target.closest('#ruOpenAllWallets'):null;
    var totalCard=e.target&&e.target.closest?e.target.closest('#page-dashboard .cards .card'):null;
    if(open){e.preventDefault();document.getElementById('ruAllWallets').style.display='block';renderWalletView();return;}
    if(totalCard&&document.getElementById('page-dashboard')&&document.getElementById('page-dashboard').contains(totalCard)){
      var label=totalCard.textContent||'';
      var allCards=[].slice.call(document.querySelectorAll('#page-dashboard .cards .card'));
      var likely=allCards.find(function(c){return /total\s+saldo|saldo\s+total|total\s+balance|total\s+seluruh\s+saldo/i.test(c.textContent||'');})||allCards[3];
      if(likely===totalCard){e.preventDefault();e.stopImmediatePropagation();document.getElementById('ruAllWallets').style.display='block';renderWalletView();return;}
    }
    if(e.target&&e.target.closest&&e.target.closest('#ruCloseAllWallets')){document.getElementById('ruAllWallets').style.display='none';return;}
    var detail=e.target&&e.target.closest?e.target.closest('[data-ru-wallet-detail]'):null;if(detail){renderWalletTransactions(detail.getAttribute('data-ru-wallet-detail'));return;}
    if(e.target&&e.target.closest&&e.target.closest('#ruCloseWalletTx')){var p=document.getElementById('ruWalletTransactionsPanel');if(p)p.style.display='none';walletViewId=null;return;}
    if(e.target&&e.target.closest&&e.target.closest('#ruOpenReconcile')){openReconcile();return;}
    if(e.target&&e.target.closest&&e.target.closest('#ruRecClose,#ruRecCancel')){document.getElementById('ruReconcileModal').style.display='none';return;}
    if(e.target&&e.target.closest&&e.target.closest('#ruFrExportExcel')){exportReportCsv();return;}
    if(e.target&&e.target.closest&&e.target.closest('#ruFrExportPdf')){exportReportPdf();return;}
  },true);
  document.addEventListener('change',function(e){
    if(e.target&&e.target.id==='ruFrPeriod'){showReportControls();renderFinanceReport();}
    if(e.target&&['ruFrDate','ruFrMonth','ruFrYear','ruFrStart','ruFrEnd','ruFrBusiness'].indexOf(e.target.id)>=0)renderFinanceReport();
    if(e.target&&e.target.id==='ruRecWallet')updateReconcile();
  });
  document.addEventListener('input',function(e){if(e.target&&e.target.id==='ruRecActual')updateReconcile();});
  document.addEventListener('submit',function(e){
    if(!e.target||e.target.id!=='ruReconcileForm')return;
    e.preventDefault();e.stopImmediatePropagation();
    var id=document.getElementById('ruRecWallet').value,actual=Number(document.getElementById('ruRecActual').value),a=wallets().find(function(x){return x.id===id;});
    if(!a||document.getElementById('ruRecActual').value===''||!Number.isFinite(actual)){alert('Pilih dompet dan isi saldo aktual yang valid.');return;}
    var system=walletBalance(a),delta=Math.round(actual)-Math.round(system),note=document.getElementById('ruRecNote').value.trim();
    if(!confirm('Saldo sistem '+rupiah(system)+'\nSaldo aktual '+rupiah(Math.round(actual))+'\nSelisih '+(delta>0?'+':'')+rupiah(delta)+'\n\nSimpan penyesuaian saldo ini?'))return;
    ensureAdjustments().push({id:'adj-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,7),accountId:id,delta:delta,date:currentDate(),createdAt:new Date().toISOString(),note:note||'Rekonsiliasi saldo'});
    document.getElementById('ruReconcileModal').style.display='none';
    saveApp();
    alert('Penyesuaian saldo tersimpan. Riwayat tersedia pada halaman Semua Saldo.');
  },true);
  function init(){
    ensureDashboard();ensureWalletView();ensureReconcileModal();ensureReport();
    var btn=document.getElementById('ruOpenAllWallets');if(btn)btn.onclick=function(){document.getElementById('ruAllWallets').style.display='block';renderWalletView();};
    document.getElementById('ruFrExportExcel').onclick=exportReportCsv;
    document.getElementById('ruFrExportPdf').onclick=exportReportPdf;
    document.getElementById('ruRecActual').addEventListener('input',updateReconcile);
    document.getElementById('ruRecWallet').addEventListener('change',updateReconcile);
    refreshDashboard();renderWalletView();renderFinanceReport();
  }
  var priorRender=window.render;
  if(typeof priorRender==='function'){
    window.render=function(){var result=priorRender.apply(this,arguments);try{refreshDashboard();renderWalletView();renderFinanceReport();}catch(e){}return result;};
  }
  document.addEventListener('click',function(e){
    var nav=e.target&&e.target.closest?e.target.closest('[data-page="dashboard"],[data-page="reports"]'):null;
    if(nav)setTimeout(function(){refreshDashboard();renderFinanceReport();},100);
  },true);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>
"""
    if "</body>" not in s:
        raise SystemExit("Tidak menemukan penutup body untuk peningkatan laporan dan saldo")
    s = s.replace("</body>", finance_ui_js + "\n</body>", 1)
    p.write_text(s)




# Append-on UI override for circular business statistics. Keeps the existing dashboard/navigation intact.
s = p.read_text()
if "KasUsaha donut business stats v2" not in s:
    donut_stats_js = r"""
<script>
/* KasUsaha donut business stats v2 */
(function(){
  if(window.__ruDonutBusinessStatsV2) return;
  window.__ruDonutBusinessStatsV2 = true;
  var colors=['#147d70','#5475d1','#e5a34c','#9b72cf','#e26f86'];
  function st(){return (typeof state!=='undefined'&&state)?state:(window.state||{});}
  function money(v){return 'Rp'+(Number(v)||0).toLocaleString('id-ID');}
  function esc(v){return String(v==null?'':v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
  function getMonthKey(t){
    var d=String(t&&t.date||'');
    if(/^\d{4}-\d{2}-\d{2}$/.test(d)) return d.slice(0,7);
    var m=String(t&&(t.reportMonth||t.monthKey||t.month)||'');
    return /^\d{4}-\d{2}/.test(m)?m.slice(0,7):'';
  }
  function getCurrentMonth(){
    var d=new Date();
    return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0');
  }
  function ensureMarkup(){
    var root=document.getElementById('ruFinanceDash');
    if(!root) return null;
    var h=root.querySelector('h2');
    if(h) h.textContent='Statistik usaha';
    var subtitle=root.querySelector('.ru-fd-head .ru-fd-sub');
    if(subtitle) subtitle.textContent='Perbandingan pemasukan dan pengeluaran tiap usaha pada bulan ini.';
    var kpis=document.getElementById('ruFdKpis');
    if(kpis) kpis.style.display='none';
    var oldChart=document.getElementById('ruFdChart');
    if(oldChart) oldChart.style.display='none';
    var oldLegend=root.querySelector('.ru-fd-legend');
    if(oldLegend) oldLegend.style.display='none';
    var host=document.getElementById('ruBusinessDonutStats');
    if(!host){
      host=document.createElement('div');
      host.id='ruBusinessDonutStats';
      host.className='ru-fd-business-charts';
      host.innerHTML='<div class="ru-fd-chart-card"><h3>Usaha dengan pemasukan terbesar</h3><div id="ruDonutIncome"></div></div><div class="ru-fd-chart-card"><h3>Usaha dengan pengeluaran terbesar</h3><div id="ruDonutExpense"></div></div>';
      var header=root.querySelector('.ru-fd-head');
      if(header) header.insertAdjacentElement('afterend',host);
      else root.appendChild(host);
    }
    return root;
  }
  function collect(){
    var data=st(),list=Array.isArray(data.transactions)?data.transactions:[],businessList=(Array.isArray(data.businesses)?data.businesses:[]).filter(function(b){return !b.archived;}),by={};
    businessList.forEach(function(b){by[b.id]={id:b.id,name:b.name||'Usaha',inc:0,out:0};});
    var month=getCurrentMonth();
    list.forEach(function(t){
      if(getMonthKey(t)!==month || (t.type!=='income'&&t.type!=='expense')) return;
      var id=t.businessId||'__general__';
      if(!by[id]) by[id]={id:id,name:id==='__general__'?'Operasional umum':'Usaha lainnya',inc:0,out:0};
      by[id][t.type==='income'?'inc':'out']+=Number(t.amount)||0;
    });
    return Object.keys(by).map(function(id){return by[id];});
  }
  function renderOne(id,kind){
    var host=document.getElementById(id);
    if(!host) return;
    var sorted=collect().filter(function(x){return x[kind]>0;}).sort(function(a,b){return b[kind]-a[kind];});
    var rows=sorted.slice(0,5),sum=rows.reduce(function(n,x){return n+x[kind];},0);
    if(!sum){
      host.innerHTML='<div class="ru-fd-sub" style="padding:6px 0 2px">Belum ada '+(kind==='inc'?'pemasukan':'pengeluaran')+' per usaha pada bulan ini.</div>';
      return;
    }
    var deg=0,stops=rows.map(function(x,i){
      var start=deg;deg+=x[kind]/sum*360;
      return colors[i%colors.length]+' '+start+'deg '+deg+'deg';
    }).join(',');
    host.innerHTML='<div class="ru-fd-winner">Terbesar: '+esc(rows[0].name)+'</div>'+
      '<div class="ru-fd-small-total">'+money(rows[0][kind])+'</div>'+
      '<div class="ru-fd-donut-wrap" style="margin-top:10px">'+
      '<div class="ru-fd-donut" style="background:conic-gradient('+stops+')"><div class="ru-fd-donut-center"><strong>'+rows.length+'</strong>usaha</div></div>'+
      '<div class="ru-fd-donut-legend">'+rows.map(function(x,i){
        return '<div><i class="ru-fd-dot" style="background:'+colors[i%colors.length]+'"></i>'+esc(x.name)+'<br><strong>'+money(x[kind])+'</strong></div>';
      }).join('')+'</div></div>';
  }
  function render(){
    if(!ensureMarkup()) return;
    renderOne('ruDonutIncome','inc');
    renderOne('ruDonutExpense','out');
  }
  var previousRender=window.render;
  if(typeof previousRender==='function'){
    window.render=function(){
      var out=previousRender.apply(this,arguments);
      setTimeout(render,50);
      return out;
    };
  }
  document.addEventListener('click',function(e){
    var nav=e.target&&e.target.closest?e.target.closest('[data-page="dashboard"]'):null;
    if(nav) setTimeout(render,100);
  },true);
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',function(){setTimeout(render,80);});
  else setTimeout(render,80);
  setTimeout(render,350);
})();
</script>
"""
    if "</body>" not in s:
        raise SystemExit("Tidak menemukan penutup body untuk statistik lingkaran")
    s = s.replace("</body>", donut_stats_js + "\n</body>", 1)
    p.write_text(s)



# KasUsaha editable transaction nominal and discount v1.
# Keep product unit prices editable and let transaction amount be the final customer price.
s = p.read_text()
if "KasUsaha editable transaction nominal and discount v1" not in s:
    old_calc = "function recalcSaleTotal(){const rows=[...document.querySelectorAll('#saleItems .sale-row')],sum=rows.reduce((n,r)=>n+(Number(r.dataset.subtotal)||0),0),amount=document.getElementById('fAmount');if(document.getElementById('fType').value==='income'&&rows.length){amount.value=Math.round(sum);amount.readOnly=true}else amount.readOnly=false}"
    new_calc = "function recalcSaleTotal(){const rows=[...document.querySelectorAll('#saleItems .sale-row')],sum=rows.reduce((n,r)=>n+(Number(r.dataset.subtotal)||0),0),amount=document.getElementById('fAmount');amount.readOnly=false;const info=document.getElementById('saleDiscountInfo');if(info){const finalAmount=Math.max(0,Number(amount.value)||0),discount=Math.max(0,Math.round(sum-finalAmount));info.innerHTML='Total harga produk: <strong>'+money(sum)+'</strong> · Harga transaksi: <strong>'+money(finalAmount)+'</strong> · Diskon: <strong style=\\\"color:var(--green)\\\">'+money(discount)+'</strong>';}}"
    if old_calc not in s:
        raise SystemExit("Tidak menemukan fungsi recalcSaleTotal untuk diubah")
    s=s.replace(old_calc,new_calc,1)
    old_override="if(type==='income'&&items.length)t.amount=Math.round(items.reduce((n,i)=>n+i.qty*i.price,0));"
    new_override="if(type==='income'&&items.length)t.discount=Math.max(0,Math.round(items.reduce((n,i)=>n+i.qty*i.price,0)-t.amount));"
    if old_override not in s:
        raise SystemExit("Tidak menemukan pengunci nominal transaksi untuk diubah")
    s=s.replace(old_override,new_override,1)
    old_wrap='<div id="saleItems"></div></div>'
    new_wrap='<div id="saleItems"></div><div id="saleDiscountInfo" class="desc" style="margin-top:8px;padding:10px;background:#f4f8f7;border-radius:10px">Total harga produk: Rp0 · Harga transaksi: Rp0 · Diskon: Rp0</div></div>'
    if old_wrap not in s:
        raise SystemExit("Tidak menemukan area produk terjual untuk menambah rincian diskon")
    s=s.replace(old_wrap,new_wrap,1)
    # Existing form values and item price inputs are left intact; update the discount hint while typing.
    discount_js = r"""
<script>
/* KasUsaha editable transaction nominal and discount v1 */
(function(){
  function refreshSaleDiscount(){
    var amount=document.getElementById('fAmount'),host=document.getElementById('saleDiscountInfo');
    if(!amount||!host)return;
    var rows=[].slice.call(document.querySelectorAll('#saleItems .sale-row'));
    var total=rows.reduce(function(n,r){return n+(Number(r.querySelector('.sale-q')&&r.querySelector('.sale-q').value)||0)*(Number(r.querySelector('.sale-v')&&r.querySelector('.sale-v').value)||0);},0);
    var finalAmount=Math.max(0,Number(amount.value)||0),discount=Math.max(0,Math.round(total-finalAmount));
    function rp(v){return 'Rp'+Math.round(Number(v)||0).toLocaleString('id-ID');}
    host.innerHTML='Total harga produk: <strong>'+rp(total)+'</strong> · Harga transaksi: <strong>'+rp(finalAmount)+'</strong> · Diskon: <strong style="color:var(--green)">'+rp(discount)+'</strong>';
  }
  document.addEventListener('input',function(e){
    if(e.target&&(['fAmount'].indexOf(e.target.id)>=0||e.target.closest&&e.target.closest('#saleItems')))refreshSaleDiscount();
  },true);
  document.addEventListener('change',function(e){if(e.target&&e.target.closest&&e.target.closest('#saleItems'))setTimeout(refreshSaleDiscount,0);},true);
  document.addEventListener('click',function(e){if(e.target&&e.target.closest&&e.target.closest('#saleItemsWrap'))setTimeout(refreshSaleDiscount,0);},true);
  var oldRender=window.render;
  if(typeof oldRender==='function')window.render=function(){var r=oldRender.apply(this,arguments);setTimeout(refreshSaleDiscount,0);return r;};
  setTimeout(refreshSaleDiscount,100);
})();
</script>
"""
    if "</body>" not in s:
        raise SystemExit("Tidak menemukan penutup body untuk tampilan diskon")
    s=s.replace("</body>",discount_js+"\n</body>",1)
    p.write_text(s)
