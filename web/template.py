
from .config import VERSION

_RAW = r'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>存档编辑器 V__VER__</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#1a1a2e;--card:#16213e;--accent:#e94560;--text:#e0e0e0;
  --text2:#a0a0b0;--border:#2a2a4a;--hover:#1f2f4f;--green:#00e676;
  --blue:#448aff;--orange:#ff9100;--tag-bg:#0f3460;--dream:#9c27b0;
  --normal:#ff9100;--gold:#ffd700;
}
body{font:14px/1.5 'Noto Sans CJK SC','Segoe UI',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
header{
  position:sticky;top:0;z-index:100;background:var(--card);border-bottom:1px solid var(--border);
  padding:8px 12px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;
}
header h1{font-size:16px;white-space:nowrap;color:var(--accent);cursor:pointer}
header h1:hover{filter:brightness(1.2)}
.tabs{
  display:flex;gap:0;background:var(--bg);border-radius:8px;overflow:hidden;
  border:1px solid var(--border);margin:6px 12px 0;
}
.tab{
  flex:1;padding:10px;text-align:center;font-size:13px;font-weight:600;cursor:pointer;
  transition:all .2s;color:var(--text2);border-bottom:2px solid transparent;
  display:flex;align-items:center;justify-content:center;gap:5px;
}
.tab.active{color:var(--accent);border-bottom-color:var(--accent)}
.tab:hover{color:var(--text)}
.panel-wrap{padding:8px 12px 80px}
.weapon-top{
  display:flex;align-items:center;gap:8px;margin-bottom:10px;flex-wrap:wrap;
}
.weapon-top .btn-apply{
  padding:8px 20px;background:var(--accent);color:#fff;border:none;border-radius:8px;
  font-size:14px;font-weight:700;cursor:pointer;transition:all .2s;
  display:flex;align-items:center;gap:4px;
}
.weapon-top .btn-apply:hover{filter:brightness(1.2)}
.weapon-top .btn-apply:disabled{opacity:.4;cursor:default}
.weapon-top .info{font-size:12px;color:var(--text2)}
.weapon-info{
  display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;
}
.weapon-info .info-card{
  background:var(--card);border-radius:10px;padding:12px;border:1px solid var(--border);
}
.weapon-info .info-card .label{
  font-size:11px;color:var(--text2);margin-bottom:6px;text-transform:uppercase;
}
.weapon-info .info-card select{
  width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);
  background:var(--bg);color:var(--text);font-size:13px;outline:none;
}
.weapon-info .info-card select:focus{border-color:var(--accent)}
.level-opts{display:flex;gap:6px;flex-wrap:wrap}
.level-opt{
  flex:1;min-width:60px;padding:8px 6px;border-radius:8px;border:2px solid var(--border);
  text-align:center;cursor:pointer;transition:all .2s;font-size:12px;
  background:var(--bg);color:var(--text2);
}
.level-opt .lv-short{font-size:16px;font-weight:700;display:block}
.level-opt .lv-full{font-size:10px;display:block}
.level-opt:hover{border-color:var(--blue)}
.level-opt.selected{background:var(--tag-bg);color:var(--text)}
.level-opt.selected[data-idx="0"]{border-color:#448aff;background:rgba(68,138,255,.15)}
.level-opt.selected[data-idx="1"]{border-color:#9c27b0;background:rgba(156,39,176,.15)}
.level-opt.selected[data-idx="2"]{border-color:#ffd700;background:rgba(255,215,0,.15)}
.level-opt.selected[data-idx="3"]{border-color:#e94560;background:rgba(233,69,96,.15)}
.slot-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}
.slot-card{
  background:var(--card);border-radius:10px;padding:12px;border:1px solid var(--border);
  transition:border-color .2s;
}
.slot-card:hover{border-color:var(--blue)}
.slot-card .slot-header{
  display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;
}
.slot-card .slot-num{
  font-size:12px;font-weight:700;color:var(--text2);background:var(--bg);
  padding:2px 8px;border-radius:4px;
}
.slot-card .slot-tag{
  font-size:10px;padding:2px 8px;border-radius:4px;font-weight:600;
}
.slot-card .slot-tag.normal{background:var(--normal);color:#000}
.slot-card .slot-tag.dream{background:var(--dream);color:#fff}
.slot-card select{
  width:100%;padding:8px;border-radius:6px;border:1px solid var(--border);
  background:var(--bg);color:var(--text);font-size:12px;outline:none;margin-bottom:6px;
}
.slot-card select:focus{border-color:var(--accent)}
.slot-card .row{display:flex;gap:8px;align-items:center}
.slot-card .row label{font-size:11px;color:var(--text2);white-space:nowrap;min-width:28px}
.slot-card .row input{
  flex:1;padding:6px 8px;border-radius:6px;border:1px solid var(--border);
  background:var(--bg);color:var(--text);font-size:13px;outline:none;width:60px;
}
.slot-card .row input:focus{border-color:var(--accent)}
.slot-card .row input:disabled{opacity:.5;background:var(--border)}
.slot-card .row input.locked{color:var(--dream);font-weight:600}
.nightmare-row{padding:4px 0;margin-bottom:2px}
.nightmare-row label{display:flex;align-items:center;gap:6px;font-size:11px;color:var(--text2);cursor:pointer;user-select:none}
.nightmare-row input[type=checkbox]{appearance:none;width:16px;height:16px;border:2px solid var(--border);border-radius:4px;background:var(--bg);cursor:pointer;position:relative;flex-shrink:0}
.nightmare-row input[type=checkbox]:checked{border-color:var(--dream);background:var(--dream)}
.nightmare-row input[type=checkbox]:checked::after{content:'\2713';position:absolute;top:-1px;left:2px;font-size:13px;color:#fff;font-weight:700}
.rune-card{
  background:var(--card);border-radius:10px;padding:12px;border:1px solid var(--border);
  margin-bottom:10px;transition:border-color .2s;
}
.rune-card:hover{border-color:var(--blue)}
.rune-header{
  display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;flex-wrap:wrap;gap:6px;
}
.rune-header .rune-name{
  font-size:14px;font-weight:700;color:var(--text);flex:1;min-width:120px;
}
.rune-id-select{
  flex:1;min-width:120px;padding:4px 6px;border-radius:6px;border:1px solid var(--border);
  background:var(--bg);color:var(--text);font-size:12px;outline:none;
}
.rune-id-select:focus{border-color:var(--accent)}
.rune-header .rune-idx{
  font-size:11px;color:var(--text2);background:var(--bg);padding:2px 8px;border-radius:4px;
}
.rune-header .lock-btn{
  padding:4px 12px;border-radius:6px;border:1px solid var(--border);cursor:pointer;
  font-size:11px;font-weight:600;background:var(--bg);color:var(--text2);transition:all .2s;
}
.rune-header .lock-btn.locked{background:var(--accent);color:#fff;border-color:var(--accent)}
.rune-mod-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.rune-mod-grid .mod-row{
  display:flex;align-items:center;gap:4px;background:var(--bg);border-radius:6px;padding:4px 8px;
}
.rune-mod-grid .mod-row label{font-size:10px;color:var(--text2);white-space:nowrap;min-width:14px}
.rune-mod-grid .mod-row select{
  flex:1;padding:4px;border-radius:4px;border:1px solid var(--border);
  background:var(--card);color:var(--text);font-size:11px;outline:none;min-width:0;
}
.rune-mod-grid .mod-row input{
  width:55px;padding:4px 6px;border-radius:4px;border:1px solid var(--border);
  background:var(--card);color:var(--text);font-size:11px;outline:none;
}
.rune-mod-grid .mod-row select:focus,.rune-mod-grid .mod-row input:focus{border-color:var(--accent)}
.rune-mod-grid .mod-row input:disabled{opacity:0.7;cursor:not-allowed;background:var(--border)}
.general-grid{display:grid;grid-template-columns:1fr;gap:10px;max-width:500px;margin:0 auto}
.general-item{background:var(--card);border-radius:10px;padding:12px 16px;border:1px solid var(--border);display:flex;align-items:center;gap:12px}
.general-item .gi-label{font-size:14px;font-weight:600;color:var(--text);min-width:100px}
.general-item .gi-name{font-size:11px;color:var(--text2)}
.general-item input{flex:1;padding:10px 12px;border-radius:8px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-size:16px;font-weight:600;outline:none;text-align:right}
.general-item input:focus{border-color:var(--accent)}
.search-wrap{flex:1;min-width:150px;position:relative}
.search-wrap input{
  width:100%;padding:7px 30px 7px 10px;border-radius:6px;border:1px solid var(--border);
  background:var(--bg);color:var(--text);font-size:13px;outline:none;
}
.search-wrap input:focus{border-color:var(--accent)}
.search-wrap .clear{
  position:absolute;right:8px;top:50%;transform:translateY(-50%);cursor:pointer;
  color:var(--text2);font-size:16px;line-height:1;display:none;
}
.search-wrap .clear.show{display:block}
.btn{
  padding:6px 12px;border-radius:6px;border:none;cursor:pointer;font-size:12px;
  font-weight:600;white-space:nowrap;transition:all .2s;
  display:flex;align-items:center;gap:4px;
}
.btn-save{background:var(--accent);color:#fff}
.btn-save:hover{filter:brightness(1.2)}
.btn-reload{background:var(--border);color:var(--text)}
.btn-reload:hover{background:var(--hover)}
.icon{width:16px;height:16px;flex-shrink:0}.icon-stroke{fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.stats{font-size:11px;color:var(--text2);padding:4px 12px;display:flex;gap:12px;flex-wrap:wrap}
.stats span{background:var(--tag-bg);padding:2px 8px;border-radius:4px}
main{padding:8px 12px 80px}
.leaf-row{
  display:flex;align-items:center;padding:6px 8px;border-bottom:1px solid var(--border);
  gap:6px;transition:background .15s;cursor:pointer;
}
.leaf-row:hover{background:var(--hover)}
.leaf-row .path{flex:1;font-size:12px;color:var(--text2);word-break:break-all;min-width:0}
.leaf-row .path .seg{color:var(--blue)}
.leaf-row .path .sep{color:var(--border);margin:0 3px}
.leaf-row .val{
  font-size:13px;font-weight:600;white-space:nowrap;padding:2px 8px;
  border-radius:4px;background:var(--tag-bg);cursor:pointer;min-width:40px;text-align:center;
}
.leaf-row .val:hover{background:var(--accent);color:#fff}
.leaf-row .val.int{color:var(--orange)}
.leaf-row .val.float{color:var(--green)}
.leaf-row .val.bool{color:var(--blue)}
.leaf-row .val.str{color:#ce93d8}
.leaf-row .edit-btn{
  font-size:11px;padding:2px 8px;border-radius:4px;background:var(--border);
  color:var(--text2);cursor:pointer;border:none;white-space:nowrap;
}
.leaf-row .edit-btn:hover{background:var(--accent);color:#fff}
.modal-overlay{
  position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.6);
  z-index:200;display:flex;align-items:center;justify-content:center;padding:20px;
}
.modal{
  background:var(--card);border-radius:12px;padding:20px;width:100%;max-width:400px;
  border:1px solid var(--border);
}
.modal h3{font-size:14px;margin-bottom:8px;color:var(--text2);word-break:break-all}
.modal .current{font-size:12px;color:var(--text2);margin-bottom:12px}
.modal input{
  width:100%;padding:10px;border-radius:8px;border:1px solid var(--border);
  background:var(--bg);color:var(--text);font-size:16px;outline:none;margin-bottom:12px;
}
.modal input:focus{border-color:var(--accent)}
.modal .hint{font-size:11px;color:var(--text2);margin-bottom:12px}
.modal .btns{display:flex;gap:8px;justify-content:flex-end}
.modal .btns button{padding:8px 16px;border-radius:6px;border:none;font-size:13px;cursor:pointer}
.modal .btns .ok{background:var(--accent);color:#fff}
.modal .btns .cancel{background:var(--border);color:var(--text)}
.pager{
  display:flex;align-items:center;justify-content:center;gap:6px;
  padding:12px;position:sticky;bottom:0;background:var(--card);border-top:1px solid var(--border);
}
.pager button{
  padding:6px 12px;border-radius:6px;border:1px solid var(--border);
  background:var(--bg);color:var(--text);cursor:pointer;font-size:12px;
  display:flex;align-items:center;gap:4px;
}
.pager button:disabled{opacity:.4;cursor:default}
.pager button:hover:not(:disabled){background:var(--hover)}
.pager .info{font-size:12px;color:var(--text2);padding:0 8px}
.toast{
  position:fixed;bottom:80px;left:50%;transform:translateX(-50%);z-index:300;
  padding:10px 20px;border-radius:8px;font-size:13px;font-weight:600;
  animation:toastIn .3s ease;pointer-events:none;
}
.toast.ok{background:var(--green);color:#000}
.toast.err{background:var(--accent);color:#fff}
@keyframes toastIn{from{opacity:0;transform:translateX(-50%) translateY(10px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
@media(max-width:480px){
  .rune-mod-grid{grid-template-columns:1fr;gap:4px}
  .rune-mod-grid .mod-row{padding:6px 8px}
  .rune-mod-grid .mod-row label{font-size:10px;min-width:12px}
  .rune-mod-grid .mod-row select{font-size:10px;padding:4px 2px}
  .rune-mod-grid .mod-row input{width:48px;font-size:10px;padding:4px}
  .rune-header .rune-name{font-size:12px}
  .rune-header .lock-btn{font-size:10px;padding:3px 8px}
  .rune-card{padding:10px;margin-bottom:8px}
  .weapon-info{grid-template-columns:1fr}
  .weapon-top{gap:4px}
  .weapon-top .btn-apply{font-size:12px;padding:6px 14px}
  .general-grid{max-width:100%}
  .general-item{padding:10px 12px;gap:8px}
  .general-item .gi-label{min-width:80px;font-size:13px}
  .general-item input{font-size:14px;padding:8px 10px}
  header{padding:6px 8px}
  header h1{font-size:14px}
  .tab{font-size:11px;padding:8px 4px}
}
@media(max-width:360px){
  .tab{font-size:10px;padding:6px 2px}
  .rune-mod-grid .mod-row input{width:40px}
}
.loading{
  position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);
  z-index:250;display:flex;align-items:center;justify-content:center;
}
.spinner{
  width:40px;height:40px;border:3px solid var(--border);
  border-top-color:var(--accent);border-radius:50%;animation:spin .8s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg)}}
.hidden{display:none !important}
</style>
</head>
<body>

<header>
  <h1 onclick="switchTab('weapon')">存档编辑V1.89</h1>
  <span class="file" id="filePath"></span>
  <div class="search-wrap" id="searchWrap">
    <input type="text" id="search" placeholder="搜索路径或数值..." autocomplete="off">
    <span class="clear" id="clearSearch">&times;</span>
  </div>
  <button class="btn btn-save" onclick="saveAll()" title="保存所有修改"><svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <path d="M17.2928932,3.29289322 L21,7 L21,20 C21,20.5522847 20.5522847,21 20,21 L4,21 C3.44771525,21 3,20.5522847 3,20 L3,4 C3,3.44771525 3.44771525,3 4,3 L16.5857864,3 C16.8510029,3 17.1053568,3.10535684 17.2928932,3.29289322 Z"/> <rect width="10" height="8" x="7" y="13"/> <rect width="8" height="5" x="8" y="3"/> </svg>保存</button>
  <button class="btn btn-reload" onclick="reloadData()"><svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <path d="M2 13.0399V11C2 7.68629 4.68629 5 8 5H21V5"/> <path d="M19 2L22 5L19 8"/> <path d="M22 9.98004V12.02C22 15.3337 19.3137 18.02 16 18.02H3V18.02"/> <path d="M5 21L2 18L5 15"/> </svg>重载</button>
</header>

<div class="tabs">
  <div class="tab active" id="tabWeapon" onclick="switchTab('weapon')"><svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <polyline points="21 14 18 14 15 7 10 17 7 11 5 14 3 14"/> </svg>武器修改</div>
  <div class="tab" id="tabPotion" onclick="switchTab('potion')"><svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <path d="M9 8h5"/> <path d="M18 3v18H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h12z"/> <path d="M5 19v-1a1 1 0 0 1 1-1h12"/> </svg>圣物修改</div>
  <div class="tab" id="tabRune" onclick="switchTab('rune')"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"> <path d="M9 4C9 2.89543 9.89543 2 11 2C12.1046 2 13 2.89543 13 4V6H18V11H20C21.1046 11 22 11.8954 22 13C22 14.1046 21.1046 15 20 15H18V20H13V18C13 16.8954 12.1046 16 11 16C9.89543 16 9 16.8954 9 18V20H4V15H6C7.10457 15 8 14.1046 8 13C8 11.8954 7.10457 11 6 11H4V6H9V4Z"/> </svg>残响修改</div>
  <div class="tab" id="tabGeneral" onclick="switchTab('general')"><svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <polygon points="12 17.844 6.183 20.902 7.294 14.425 2.588 9.838 9.092 8.893 12 3 14.908 8.893 21.412 9.838 16.706 14.425 17.817 20.902"/> </svg>常规修改</div>
  <div class="tab" id="tabAll" onclick="switchTab('all')"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"> <path d="M7 8L3 12L7 16"/> <path d="M17 16L21 12L17 8"/> <path d="M9 19.5L14.5 5"/> </svg>全部字段</div>
</div>

<div class="panel-wrap" id="weaponPanel">
  <div class="weapon-top">
    <button class="btn-apply" id="btnApply" onclick="applyAllWeapon()"><svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <path d="M8 18l-6-6 6-6h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H8z"/> </svg>一键应用全部修改</button>
    <span class="info" id="weaponInfo"></span>
  </div>

  <div class="weapon-info">
    <div class="info-card">
      <div class="label">武器名称</div>
      <select id="weaponName" onchange="onWeaponNameChange()"><option value="0">0 - 一把普通的剑</option><option value="1">1 - 无名[七剑修罗专属]</option><option value="2">2 - 幻灭[七剑修罗专属]</option><option value="3">3 - 骤雨[无量尊者专属]</option><option value="4">4 - 堕日[无量尊者专属]</option><option value="5">5 - 炽焰[神饮明王专属]</option><option value="6">6 - 酒神[神饮明王专属]</option><option value="7">7 - 牙刃</option><option value="8">8 - 空明</option><option value="9">9 - 青蛇</option><option value="10">10 - 养战</option><option value="11">11 - 蛮武</option><option value="12">12 - 咒杀</option><option value="13">13 - 血仇</option><option value="14">14 - 霜降</option><option value="15">15 - 凋零</option><option value="16">16 - 烈风</option><option value="17">17 - 须臾</option><option value="18">18 - 墨炎</option><option value="19">19 - 流火</option><option value="20">20 - 碎冰</option><option value="21">21 - 珠光</option><option value="22">22 - 星辰</option><option value="23">23 - 雷息[圣威怒雷金刚专属]</option><option value="24">24 - 万钧[圣威怒雷金刚专属]</option><option value="25">25 - 百足[三尸慈姑娘娘专属]</option><option value="26">26 - 血虱[三尸慈姑娘娘专属]</option><option value="27">27 - 霸者</option><option value="28">28 - 狂屠</option><option value="29">29 - 狂乱</option><option value="30">30 - 醉仙</option><option value="31">31 - 雪莲</option><option value="32">32 - 冥将</option><option value="33">33 - 狼王</option><option value="34">34 - 华佗</option><option value="35">35 - 鹰眼</option><option value="36">36 - 屠灭</option><option value="37">37 - 太祖</option><option value="38">38 - 普通</option><option value="39">39 - 暴怒</option><option value="40">40 - 山崩</option><option value="41">41 - 风火</option><option value="42">42 - 黄泉[三川苦寒菩萨专属]</option><option value="43">43 - 寒川[三川苦寒菩萨专属]</option><option value="44">44 - 冥妆</option><option value="45">45 - 三元</option><option value="46">46 - 八荒</option><option value="47">47 - 深冬</option><option value="48">48 - 惊蛰</option><option value="49">49 - 斩龙</option><option value="50">50 - 时裂[神行迷踪天尊专属]</option><option value="51">51 - 双生[神行迷踪天尊专属]</option><option value="52">52 - 两仪[日月轮转双天专属]</option><option value="53">53 - 吞星[日月轮转双天专属]</option><option value="54">54 - 赤玺[阎罗地藏明王专属]</option><option value="55">55 - 鬼毫[阎罗地藏明王专属]</option><option value="56">56 - 无限[灵剑修罗专属]</option><option value="57">57 - 圆满[灵剑修罗专属]</option><option value="58">58 - 毒渊</option><option value="59">59 - 断肢</option><option value="60">60 - 铁剑</option><option value="61">61 - 躺平</option><option value="62">62 - 碧水</option><option value="63">63 - 飞瀑</option><option value="64">64 - 芳华</option><option value="65">65 - 云眠</option><option value="66">66 - 始末</option><option value="67">67 - 药仙</option><option value="68">68 - 斩铁</option><option value="69">69 - 永焰</option><option value="70">70 - 回魂</option><option value="71">71 - 风起</option><option value="72">72 - 同心</option><option value="73">73 - 孟章</option><option value="74">74 - 陵光</option><option value="75">75 - 监兵</option><option value="76">76 - 执明</option></select>
    </div>
    <div class="info-card">
      <div class="label">武器等级</div>
      <div class="level-opts" id="levelOpts"></div>
    </div>
  </div>

  <div class="slot-grid" id="slotGrid"></div>
</div>

<div class="hidden panel-wrap" id="potionPanel">
  <div class="weapon-top">
    <button class="btn-apply" id="btnApplyPotion" onclick="applyAllPotion()"><svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <path d="M8 18l-6-6 6-6h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H8z"/> </svg>一键应用全部修改</button>
    <span class="info" id="potionInfo"></span>
  </div>
  <div class="slot-grid" id="potionGrid"></div>
</div>

<div class="hidden panel-wrap" id="runePanel">
  <div class="weapon-top">
    <button class="btn-apply" id="btnApplyRune" onclick="applyAllRune()"><svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <path d="M8 18l-6-6 6-6h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H8z"/> </svg>一键应用全部修改</button>
    <span class="info" id="runeInfo"></span>
  </div>
  <div id="runeGrid"></div>
  <div class="pager" id="runePager"></div>
</div>

<div class="hidden panel-wrap" id="generalPanel">
  <div class="weapon-top">
    <button class="btn-apply" id="btnApplyGeneral" onclick="applyAllGeneral()"><svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <path d="M8 18l-6-6 6-6h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H8z"/> </svg>一键应用全部修改</button>
    <span class="info" id="generalInfo"></span>
  </div>
  <div class="general-grid" id="generalGrid"></div>
</div>

<div class="hidden" id="allPanel">
  <div class="stats" id="stats"></div>
  <main id="main"></main>
  <div class="pager" id="pager"></div>
</div>

<script>
const ENTRY_LIST = [{"id": 0, "name": "\u8fd1\u6218\u653b\u51fb", "type": "\u666e\u901a"}, {"id": 1, "name": "\u8fdc\u7aef\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 2, "name": "\u6240\u6709\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 3, "name": "\u65e0\u89c6\u9632\u5fa1", "type": "\u666e\u901a"}, {"id": 4, "name": "\u8fd1\u6218\u653b\u51fb\u901f\u5ea6", "type": "\u666e\u901a"}, {"id": 5, "name": "\u6536\u5251\u51b7\u5374\u65f6\u95f4", "type": "\u666e\u901a"}, {"id": 6, "name": "\u5bf9[\u4e2d\u6bd2]\u654c\u4eba\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 7, "name": "\u5bf9[\u9152\u9189]\u654c\u4eba\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 8, "name": "\u5bf9[\u71c3\u70e7]\u654c\u4eba\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 9, "name": "\u5bf9[\u6d41\u8840]\u654c\u4eba\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 10, "name": "\u5bf9[\u51bb\u7ed3]\u654c\u4eba\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 11, "name": "\u5bf9[\u660f\u8ff7]\u654c\u4eba\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 12, "name": "\u79fb\u52a8\u901f\u5ea6", "type": "\u666e\u901a"}, {"id": 13, "name": "\u4f20\u8bf4\u5723\u7269\u51fa\u73b0\u673a\u7387", "type": "\u666e\u901a"}, {"id": 14, "name": "\u5e7d\u51a5\u4e4b\u9b42\u83b7\u5f97\u6570\u91cf", "type": "\u666e\u901a"}, {"id": 15, "name": "\u6012\u6c14\u83b7\u53d6", "type": "\u666e\u901a"}, {"id": 16, "name": "\u706b\u7130\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 17, "name": "\u51b0\u971c\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 18, "name": "\u6bd2\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 19, "name": "\u95ea\u7535\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 20, "name": "\u9020\u6210\u4f24\u5bb3\u65f6\uff0cn\u673a\u7387\u4f7f\u654c\u4eba\u53d7\u5230\u7684\u4f24\u5bb3\u63d0\u9ad830%\uff0c\u6301\u7eed3\u79d2", "type": "\u666e\u901a"}, {"id": 21, "name": "\u9020\u6210\u4f24\u5bb3\u65f6\uff0cn\u673a\u7387\u9020\u62102\u500d\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 22, "name": "\u9020\u6210\u4f24\u5bb3\u65f6\uff0cn\u673a\u7387\u9020\u62104\u500d\u4f24\u5bb3", "type": "\u666e\u901a"}, {"id": 23, "name": "\u9020\u6210\u4f24\u5bb3\u65f6\uff0cn\u673a\u7387\u4f7f\u654c\u4eba\u53d7\u5230\u7684\u4f24\u5bb3\u63d0\u9ad860%\uff0c\u6301\u7eed3\u79d2", "type": "\u666e\u901a"}, {"id": 24, "name": "\u6240\u6709\u4f24\u5bb3+35%", "type": "\u68a6\u5883"}, {"id": 25, "name": "\u8fd1\u6218\u4f24\u5bb3+60%", "type": "\u68a6\u5883"}, {"id": 26, "name": "\u8fdc\u7aef\u4f24\u5bb3+60%", "type": "\u68a6\u5883"}, {"id": 27, "name": "\u706b\u7130\u4f24\u5bb3+80%", "type": "\u68a6\u5883"}, {"id": 28, "name": "\u51b0\u971c\u4f24\u5bb3+80%", "type": "\u68a6\u5883"}, {"id": 29, "name": "\u95ea\u7535\u4f24\u5bb3+80%", "type": "\u68a6\u5883"}, {"id": 30, "name": "\u6bd2\u4f24\u5bb3+80%", "type": "\u68a6\u5883"}, {"id": 31, "name": "\u6536\u5251\u51b7\u5374-40%", "type": "\u68a6\u5883"}, {"id": 32, "name": "\u65e0\u89c6\u9632\u5fa1+60%", "type": "\u68a6\u5883"}, {"id": 33, "name": "\u9632\u5fa1+20%", "type": "\u68a6\u5883"}, {"id": 34, "name": "\u6700\u5927\u751f\u547d+15%", "type": "\u68a6\u5883"}, {"id": 35, "name": "\u4f60\u7684\u8fd1\u6218\u653b\u51fb\u670915%\u673a\u7387\u4f7f\u654c\u4eba[\u6d41\u8840]3\u79d2", "type": "\u68a6\u5883"}, {"id": 36, "name": "\u4f60\u7684\u8fd1\u6218\u653b\u51fb\u670915%\u673a\u7387\u4f7f\u654c\u4eba[\u4e2d\u6bd2]3\u79d2", "type": "\u68a6\u5883"}, {"id": 37, "name": "\u4f60\u7684\u8fd1\u6218\u653b\u51fb\u670915%\u673a\u7387\u4f7f\u654c\u4eba[\u71c3\u70e7]3\u79d2", "type": "\u68a6\u5883"}, {"id": 38, "name": "\u4f60\u7684\u8fd1\u6218\u653b\u51fb\u670915%\u673a\u7387\u4f7f\u654c\u4eba[\u51bb\u7ed3]1\u79d2", "type": "\u68a6\u5883"}, {"id": 39, "name": "\u9020\u6210\u4f24\u5bb3\u65f6\uff0c10%\u673a\u7387\u9020\u62104\u500d\u4f24\u5bb3", "type": "\u68a6\u5883"}, {"id": 40, "name": "\u8fd1\u6218\u6216\u98de\u5251\u9020\u6210\u4f24\u5bb3\u65f6\uff0c15%\u673a\u7387\u4f7f\u4f60\u6240\u6709\u4f24\u5bb3\u63d0\u9ad880%\uff0c\u6301\u7eed5\u79d2", "type": "\u68a6\u5883"}, {"id": 41, "name": "\u8fd1\u6218\u4f24\u5bb3\u63d0\u9ad880%\uff0c\u9020\u6210\u8fd1\u6218\u4f24\u5bb3\u65f6\uff0c35%\u673a\u7387\u4f7f\u654c\u4eba[\u6d41\u8840]6\u79d2", "type": "\u68a6\u5883"}, {"id": 42, "name": "\u98de\u5251\u4f24\u5bb3\u63d0\u9ad880%\uff0c\u9020\u6210\u98de\u5251\u4f24\u5bb3\u65f6\uff0c15%\u673a\u7387\u9020\u62102.5\u500d\u4f24\u5bb3", "type": "\u68a6\u5883"}, {"id": 43, "name": "\u706b\u7130\u4f24\u5bb3\u63d0\u9ad8110%\uff0c\u5f53\u4f60\u9020\u6210\u706b\u7130\u4f24\u5bb3\u65f6\u4f1a\u9644\u52a03\u79d2\u7684[\u71c3\u70e7]\u6548\u679c", "type": "\u68a6\u5883"}, {"id": 44, "name": "\u51b0\u971c\u4f24\u5bb3\u63d0\u9ad8110%\uff0c\u5bf9[\u51bb\u7ed3]\u7684\u5355\u4f4d\u9020\u6210\u4f24\u5bb3\u65f6\uff0c10%\u673a\u7387\u9020\u62105\u500d\u4f24\u5bb3", "type": "\u68a6\u5883"}, {"id": 45, "name": "\u95ea\u7535\u4f24\u5bb3\u63d0\u9ad8110%\uff0c\u4f60\u7684\u77ac\u8eab\u4f1a\u5bf9\u8def\u5f84\u4e0a\u7684\u654c\u4eba\u9020\u621060%\u7684\u95ea\u7535\u4f24\u5bb3", "type": "\u68a6\u5883"}, {"id": 46, "name": "\u6bd2\u4f24\u5bb3\u63d0\u9ad8110%\uff0c\u5f53\u4f60\u5bf9[\u4e2d\u6bd2]\u654c\u4eba\u9020\u6210\u4f24\u5bb3\u65f6\uff0c15%\u673a\u7387\u9020\u62103.5\u500d\u4f24\u5bb3", "type": "\u68a6\u5883"}, {"id": 47, "name": "\u6536\u5251\u51b7\u5374-50%\uff0c\u6536\u5251\u65f625%\u673a\u7387\u91cd\u7f6e\u6536\u5251\u51b7\u5374\u65f6\u95f4", "type": "\u68a6\u5883"}, {"id": 48, "name": "\u9020\u6210\u4f24\u5bb3\u65f6\uff0c15%\u673a\u7387\u9020\u62107\u500d\u4f24\u5bb3", "type": "\u68a6\u5883"}, {"id": 49, "name": "\u8fd1\u6218\u653b\u51fb\u65f6\u670910%\u673a\u7387\u53d1\u52a8\u68a6\u9b47\u6ce2\u52a8\uff0c\u5bf9\u524d\u65b9\u9020\u62102000%\u7684\u771f\u5b9e\u4f24\u5bb3", "type": "\u68a6\u5883"}, {"id": 50, "name": "\u98de\u5251\u653b\u51fb\u65f6\u670915%\u673a\u7387\u53ec\u55241\u679a\u68a6\u9b47\u661f\u8fb0", "type": "\u68a6\u5883"}, {"id": 51, "name": "\u4f7f\u4f60\u7684\u6012\u6c14\u7206\u53d1\u53d8\u4e3a\u68a6\u9b47\u7206\u53d1\uff0c\u989d\u5916\u589e\u52a0100%\u7684\u6240\u6709\u4f24\u5bb3", "type": "\u68a6\u5883"}, {"id": 52, "name": "\u5f53\u4f60\u65bd\u653e\u6838\u5fc3\u69fd\u5723\u7269\u65f6\uff0c\u53d1\u5c045\u679a\u8150\u8680\u5b9d\u73e0\u653b\u51fb\u9644\u8fd1\u7684\u654c\u4eba", "type": "\u68a6\u5883"}, {"id": 53, "name": "\u9020\u6210\u4f24\u5bb3\u65f6\uff0c15%\u673a\u7387\u9020\u621012\u500d\u4f24\u5bb3\uff0c\u4f46\u4f60\u4f1a\u635f\u59317%\u7684\u76ee\u524d\u751f\u547d\u503c", "type": "\u68a6\u5883"}, {"id": 54, "name": "\u5f53\u4f60\u65bd\u653e\u6536\u5251\u6280\u80fd\u65f6\uff0c\u7acb\u523b\u53ec\u5524\u5927\u91cf\u68a6\u9b47\u5012\u523a\u653b\u51fb\u9644\u8fd1\u7684\u654c\u4eba", "type": "\u68a6\u5883"}, {"id": 55, "name": "\u9020\u6210\u4f24\u5bb3\u65f6\u67095%\u673a\u7387\u53ec\u5524\u68a6\u9b47\u5de8\u9cb2\uff0c\u7838\u51fb\u5730\u9762\u9020\u62105000%\u7684\u771f\u5b9e\u4f24\u5bb3", "type": "\u68a6\u5883"}, {"id": 56, "name": "\u4f60\u7684\u751f\u547d\u63d0\u9ad8200%\uff0c\u9632\u5fa1\u63d0\u9ad820%\uff0c\u83b7\u5f97[\u514d\u63a7\u72b6\u6001]", "type": "\u68a6\u5883"}, {"id": 57, "name": "\u6240\u6709\u4f24\u5bb3\u63d0\u9ad880%\uff0c\u4f60\u7684\u6240\u6709\u653b\u51fb\u53d8\u4e3a\u771f\u5b9e\u4f24\u5bb3", "type": "\u68a6\u5883"}];
const WEAPON_NAMES = [{"id": 0, "name": "\u4e00\u628a\u666e\u901a\u7684\u5251"}, {"id": 1, "name": "\u65e0\u540d[\u4e03\u5251\u4fee\u7f57\u4e13\u5c5e]"}, {"id": 2, "name": "\u5e7b\u706d[\u4e03\u5251\u4fee\u7f57\u4e13\u5c5e]"}, {"id": 3, "name": "\u9aa4\u96e8[\u65e0\u91cf\u5c0a\u8005\u4e13\u5c5e]"}, {"id": 4, "name": "\u5815\u65e5[\u65e0\u91cf\u5c0a\u8005\u4e13\u5c5e]"}, {"id": 5, "name": "\u70bd\u7130[\u795e\u996e\u660e\u738b\u4e13\u5c5e]"}, {"id": 6, "name": "\u9152\u795e[\u795e\u996e\u660e\u738b\u4e13\u5c5e]"}, {"id": 7, "name": "\u7259\u5203"}, {"id": 8, "name": "\u7a7a\u660e"}, {"id": 9, "name": "\u9752\u86c7"}, {"id": 10, "name": "\u517b\u6218"}, {"id": 11, "name": "\u86ee\u6b66"}, {"id": 12, "name": "\u5492\u6740"}, {"id": 13, "name": "\u8840\u4ec7"}, {"id": 14, "name": "\u971c\u964d"}, {"id": 15, "name": "\u51cb\u96f6"}, {"id": 16, "name": "\u70c8\u98ce"}, {"id": 17, "name": "\u987b\u81fe"}, {"id": 18, "name": "\u58a8\u708e"}, {"id": 19, "name": "\u6d41\u706b"}, {"id": 20, "name": "\u788e\u51b0"}, {"id": 21, "name": "\u73e0\u5149"}, {"id": 22, "name": "\u661f\u8fb0"}, {"id": 23, "name": "\u96f7\u606f[\u5723\u5a01\u6012\u96f7\u91d1\u521a\u4e13\u5c5e]"}, {"id": 24, "name": "\u4e07\u94a7[\u5723\u5a01\u6012\u96f7\u91d1\u521a\u4e13\u5c5e]"}, {"id": 25, "name": "\u767e\u8db3[\u4e09\u5c38\u6148\u59d1\u5a18\u5a18\u4e13\u5c5e]"}, {"id": 26, "name": "\u8840\u8671[\u4e09\u5c38\u6148\u59d1\u5a18\u5a18\u4e13\u5c5e]"}, {"id": 27, "name": "\u9738\u8005"}, {"id": 28, "name": "\u72c2\u5c60"}, {"id": 29, "name": "\u72c2\u4e71"}, {"id": 30, "name": "\u9189\u4ed9"}, {"id": 31, "name": "\u96ea\u83b2"}, {"id": 32, "name": "\u51a5\u5c06"}, {"id": 33, "name": "\u72fc\u738b"}, {"id": 34, "name": "\u534e\u4f57"}, {"id": 35, "name": "\u9e70\u773c"}, {"id": 36, "name": "\u5c60\u706d"}, {"id": 37, "name": "\u592a\u7956"}, {"id": 38, "name": "\u666e\u901a"}, {"id": 39, "name": "\u66b4\u6012"}, {"id": 40, "name": "\u5c71\u5d29"}, {"id": 41, "name": "\u98ce\u706b"}, {"id": 42, "name": "\u9ec4\u6cc9[\u4e09\u5ddd\u82e6\u5bd2\u83e9\u8428\u4e13\u5c5e]"}, {"id": 43, "name": "\u5bd2\u5ddd[\u4e09\u5ddd\u82e6\u5bd2\u83e9\u8428\u4e13\u5c5e]"}, {"id": 44, "name": "\u51a5\u5986"}, {"id": 45, "name": "\u4e09\u5143"}, {"id": 46, "name": "\u516b\u8352"}, {"id": 47, "name": "\u6df1\u51ac"}, {"id": 48, "name": "\u60ca\u86f0"}, {"id": 49, "name": "\u65a9\u9f99"}, {"id": 50, "name": "\u65f6\u88c2[\u795e\u884c\u8ff7\u8e2a\u5929\u5c0a\u4e13\u5c5e]"}, {"id": 51, "name": "\u53cc\u751f[\u795e\u884c\u8ff7\u8e2a\u5929\u5c0a\u4e13\u5c5e]"}, {"id": 52, "name": "\u4e24\u4eea[\u65e5\u6708\u8f6e\u8f6c\u53cc\u5929\u4e13\u5c5e]"}, {"id": 53, "name": "\u541e\u661f[\u65e5\u6708\u8f6e\u8f6c\u53cc\u5929\u4e13\u5c5e]"}, {"id": 54, "name": "\u8d64\u73ba[\u960e\u7f57\u5730\u85cf\u660e\u738b\u4e13\u5c5e]"}, {"id": 55, "name": "\u9b3c\u6beb[\u960e\u7f57\u5730\u85cf\u660e\u738b\u4e13\u5c5e]"}, {"id": 56, "name": "\u65e0\u9650[\u7075\u5251\u4fee\u7f57\u4e13\u5c5e]"}, {"id": 57, "name": "\u5706\u6ee1[\u7075\u5251\u4fee\u7f57\u4e13\u5c5e]"}, {"id": 58, "name": "\u6bd2\u6e0a"}, {"id": 59, "name": "\u65ad\u80a2"}, {"id": 60, "name": "\u94c1\u5251"}, {"id": 61, "name": "\u8eba\u5e73"}, {"id": 62, "name": "\u78a7\u6c34"}, {"id": 63, "name": "\u98de\u7011"}, {"id": 64, "name": "\u82b3\u534e"}, {"id": 65, "name": "\u4e91\u7720"}, {"id": 66, "name": "\u59cb\u672b"}, {"id": 67, "name": "\u836f\u4ed9"}, {"id": 68, "name": "\u65a9\u94c1"}, {"id": 69, "name": "\u6c38\u7130"}, {"id": 70, "name": "\u56de\u9b42"}, {"id": 71, "name": "\u98ce\u8d77"}, {"id": 72, "name": "\u540c\u5fc3"}, {"id": 73, "name": "\u5b5f\u7ae0"}, {"id": 74, "name": "\u9675\u5149"}, {"id": 75, "name": "\u76d1\u5175"}, {"id": 76, "name": "\u6267\u660e"}];
const WEAPON_LEVELS = [{"id": 0, "short": "\u84dd", "full": "\u7cbe\u826f", "color": "#448aff"}, {"id": 1, "short": "\u7d2b", "full": "\u53f2\u8bd7", "color": "#9c27b0"}, {"id": 2, "short": "\u9ec4", "full": "\u4f20\u8bf4", "color": "#ffd700"}, {"id": 3, "short": "\u7ea2", "full": "\u7edd\u4e16", "color": "#e94560"}];
const POTION_NAMES = [{"id": 0, "name": "\u65e0"}, {"id": 1, "name": "\u7384\u6b66\u4e4b\u9b42"}, {"id": 2, "name": "\u767d\u864e\u4e4b\u9b42"}, {"id": 3, "name": "\u9752\u9f99\u4e4b\u9b42"}, {"id": 4, "name": "\u6731\u96c0\u4e4b\u9b42"}, {"id": 5, "name": "\u5c38\u53d8\u65ad\u80a2"}, {"id": 6, "name": "\u950b\u9510\u4e4b\u7259"}, {"id": 7, "name": "\u8dcc\u6253\u8349"}, {"id": 8, "name": "\u5927\u9aa8"}, {"id": 9, "name": "\u73cd\u73e0"}, {"id": 10, "name": "\u96c4\u9ec4"}, {"id": 11, "name": "\u618e\u6068\u4e4b\u5fc3"}, {"id": 12, "name": "\u51dd\u6c14\u8349"}, {"id": 13, "name": "\u8840\u7389\u9ad3"}, {"id": 14, "name": "\u706b\u785d\u77f3"}, {"id": 15, "name": "\u9189\u4ed9\u917f"}, {"id": 16, "name": "\u8840\u7075\u829d"}, {"id": 17, "name": "\u5343\u5e74\u5bd2\u51b0"}, {"id": 18, "name": "\u72fc\u738b\u767d\u9b03"}, {"id": 19, "name": "\u6b7b\u4e4b\u83b2"}, {"id": 20, "name": "\u72c2\u66b4\u4e4b\u8840"}, {"id": 21, "name": "\u8e0f\u98ce\u8349"}, {"id": 22, "name": "\u7834\u51b0\u77f3"}, {"id": 23, "name": "\u987b\u81fe\u4e4b\u6c99"}, {"id": 24, "name": "\u58a8\u706b\u7ed3\u6676"}, {"id": 25, "name": "\u661f\u8fb0\u4e4b\u7389"}, {"id": 26, "name": "\u52a8\u529b\u6838\u5fc3"}, {"id": 27, "name": "\u673a\u5173\u70ae\u8f6e"}, {"id": 28, "name": "\u673a\u5173\u55b7\u53e3"}, {"id": 29, "name": "\u673a\u5173\u5916\u58f3"}, {"id": 30, "name": "\u9ec4\u7eb8"}, {"id": 31, "name": "\u5317\u98ce\u82b1"}, {"id": 32, "name": "\u6bd2\u56ca"}, {"id": 33, "name": "\u9b3c\u5983\u65ad\u53d1"}, {"id": 34, "name": "\u4e09\u8272\u7ed3\u6676"}, {"id": 35, "name": "\u5f15\u96f7\u9501"}, {"id": 36, "name": "\u53d8\u5f02\u6b8b\u80a2"}, {"id": 37, "name": "\u731b\u864e\u4e4b\u5370"}, {"id": 38, "name": "\u5815\u9f99"}, {"id": 39, "name": "\u54cd\u96f7\u77f3"}, {"id": 40, "name": "\u9ed1\u706b\u836f"}, {"id": 41, "name": "\u6c34\u94f6"}, {"id": 42, "name": "\u9752\u94a2"}, {"id": 43, "name": "\u7075\u7389"}, {"id": 44, "name": "\u9547\u5c71\u77f3"}, {"id": 45, "name": "\u751f\u547d\u4e4b\u79cd"}, {"id": 46, "name": "\u98de\u785d\u7bad"}, {"id": 47, "name": "\u6050\u60e7\u4e4b\u5fc3"}, {"id": 48, "name": "\u9f99\u5f62\u89e5"}, {"id": 49, "name": "\u4d19\u9e48\u9e1f"}, {"id": 50, "name": "\u5f02\u661f\u4e4b\u77f3"}, {"id": 51, "name": "\u7591\u65e0\u7269"}, {"id": 52, "name": "\u51e4\u51f0\u5599"}, {"id": 53, "name": "\u6e0a\u9f99\u7259"}, {"id": 54, "name": "\u5317\u51a5\u77f3"}, {"id": 55, "name": "\u7384\u8be1\u5203"}, {"id": 56, "name": "\u91cd\u5c71\u94e0"}, {"id": 57, "name": "\u631a\u7231\u4e4b\u5fc3"}, {"id": 58, "name": "\u8150\u80a2\u9b3c\u7532"}, {"id": 59, "name": "\u62a4\u5fc3\u955c"}, {"id": 60, "name": "\u72c2\u5c06\u9501"}, {"id": 61, "name": "\u5c38\u9b3c\u866b"}, {"id": 62, "name": "\u795e\u7687\u5a01\u88c5"}, {"id": 63, "name": "\u6c38\u6052\u5951\u6587"}, {"id": 64, "name": "\u6bcd\u795e\u65e7\u5370"}, {"id": 65, "name": "\u957f\u68a6\u96fe\u9748"}, {"id": 66, "name": "\u65e0\u6839\u795e\u9ab8"}, {"id": 67, "name": "\u9707\u9f99\u9aa8"}, {"id": 68, "name": "\u5317\u6d77\u9ccd"}];
const POTION_LEVELS = [{"id": 0, "short": "\u767d", "full": "\u666e\u901a", "color": "#b0b0b0"}, {"id": 1, "short": "\u7d2b", "full": "\u53f2\u8bd7", "color": "#9c27b0"}, {"id": 2, "short": "\u6a59", "full": "\u4f20\u8bf4", "color": "#ff9100"}];
const RUNE_NAMES = [{id:0,name:"绝命鸳鸯"},{id:1,name:"贪婪之视"},{id:2,name:"死亡之钳"},{id:3,name:"深渊之须"},{id:4,name:"蛇之血裔"},{id:5,name:"受肉残骸"},{id:6,name:"沉眠之拳"},{id:7,name:"蛇母之缠"},{id:8,name:"何罗神祇"},{id:9,name:"绝对王权"},{id:10,name:"苦舟"},{id:11,name:"轩辕"},{id:12,name:"终解之术"},{id:13,name:"魂玉"},{id:14,name:"仙酒会"},{id:15,name:"破天刃"},{id:16,name:"鬼面佛"},{id:17,name:"血菩提"},{id:18,name:"雷玉"},{id:19,name:"冰玉"},{id:20,name:"黑玉"},{id:21,name:"落日刃"},{id:22,name:"三彩玉"},{id:23,name:"镇魂衣"},{id:24,name:"满月"},{id:25,name:"修罗刃"},{id:26,name:"无量法"},{id:27,name:"醉仙剑"},{id:28,name:"怒雷楔"},{id:29,name:"苦寒锥"},{id:30,name:"三尸帖"},{id:31,name:"刹时光"},{id:32,name:"日月环"},{id:33,name:"生死簿"},{id:34,name:"逆生灵"},{id:35,name:"圣王之法"},{id:36,name:"天火弹"},{id:37,name:"无相刃"},{id:38,name:"混沌之法"},{id:39,name:"金刚盾"},{id:40,name:"不坏身"},{id:41,name:"寒火"},{id:42,name:"电刺"},{id:43,name:"冰锋"},{id:44,name:"炎牙"},{id:45,name:"脏雷"},{id:46,name:"污冰"},{id:47,name:"邪火"},{id:48,name:"白刃之法"},{id:49,name:"飞刃之法"},{id:50,name:"体魄之法"},{id:51,name:"弦月"},{id:52,name:"夺魄之刃"},{id:53,name:"五行之法"},{id:54,name:"真男人"},{id:55,name:"突袭之法"},{id:56,name:"镇魂刃"},{id:57,name:"锋刃"},{id:58,name:"利剑"},{id:59,name:"攻守玉"},{id:60,name:"决战"},{id:61,name:"余香"},{id:62,name:"千叠之足"},{id:63,name:"千叠之爪"},{id:64,name:"千叠飞刃"},{id:65,name:"千叠之伤"},{id:66,name:"千叠之甲"},{id:67,name:"千叠之命"},{id:68,name:"千斤石"},{id:69,name:"不融冰"},{id:70,name:"可怖面"},{id:71,name:"新月"},{id:72,name:"回魂夜"},{id:73,name:"真实之刃"},{id:74,name:"灵魂余辉"},{id:75,name:"聚魂玉"},{id:76,name:"恐惧真气"},{id:77,name:"强袭真气"},{id:78,name:"霜冻真气"},{id:79,name:"治愈真气"},{id:80,name:"灵魂护盾"},{id:81,name:"毒破符"},{id:82,name:"燃破符"},{id:83,name:"血破符"},{id:84,name:"冰破符"},{id:85,name:"岩破符"},{id:86,name:"胆破符"},{id:87,name:"上好药剂"},{id:88,name:"树体"},{id:89,name:"石盾"},{id:90,name:"盗怒"},{id:91,name:"盗命"},{id:92,name:"盗力"},{id:93,name:"盗速"},{id:94,name:"盗咒"},{id:95,name:"盗御"},{id:96,name:"刺盾"},{id:97,name:"轻盾"},{id:98,name:"白刃药剂"},{id:99,name:"飞刃药剂"},{id:100,name:"飞身药剂"}];
const RUNE_ATTRS = [{id:0,name:"近战攻击",type:"normal"},{id:1,name:"飞剑攻击",type:"normal"},{id:2,name:"所有伤害",type:"normal"},{id:3,name:"无视防御",type:"normal"},{id:4,name:"武器攻击攻速",type:"normal"},{id:5,name:"收剑冷却时间",type:"normal"},{id:6,name:"移动速度",type:"normal"},{id:7,name:"怒气获取",type:"normal"},{id:8,name:"火焰伤害",type:"normal"},{id:9,name:"冰霜伤害",type:"normal"},{id:10,name:"毒伤害",type:"normal"},{id:11,name:"闪电伤害",type:"normal"},{id:12,name:"防御",type:"normal"},{id:13,name:"最大生命值",type:"normal"},{id:14,name:"幽冥之魂获得数量",type:"normal"},{id:15,name:"传说圣物出现几率",type:"normal"},{id:16,name:"近战第一击伤害",type:"normal"},{id:17,name:"近战最后一击伤害",type:"normal"},{id:18,name:"护盾吸收量",type:"normal"},{id:19,name:"挚爱之心(绝命鸳鸯·秘宝级)",type:"locked"},{id:20,name:"相互依偎(绝命鸳鸯·秘宝级)",type:"locked"},{id:21,name:"千魂之喉(贪婪之视·秘宝级)",type:"locked"},{id:22,name:"欲壑难填(贪婪之视·秘宝级)",type:"locked"},{id:23,name:"沙海狂风(死亡之钳·秘宝级)",type:"locked"},{id:24,name:"风沙领主(死亡之钳·秘宝级)",type:"locked"},{id:25,name:"腐化之卵(深渊之触·秘宝级)",type:"locked"},{id:26,name:"深渊毒喉(深渊之触·秘宝级)",type:"locked"},{id:27,name:"切肤之痛(蛇之血裔·秘宝级)",type:"locked"},{id:28,name:"分离之恨(蛇之血裔·秘宝级)",type:"locked"},{id:29,name:"天地精华(受肉残骸·秘宝级)",type:"locked"},{id:30,name:"受肉时刻(受肉残骸·秘宝级)",type:"locked"},{id:31,name:"赤练之拳(沉眠之拳·秘宝级)",type:"locked"},{id:32,name:"毁灭之拳(沉眠之拳·秘宝级)",type:"locked"},{id:33,name:"恐怖疆域(蛇母之缠·秘宝级)",type:"locked"},{id:34,name:"古蛇血月(蛇母之缠·秘宝级)",type:"locked"},{id:35,name:"狭间当铺(何罗神祉·秘宝级)",type:"locked"},{id:36,name:"远古宝库(何罗神祉·秘宝级)",type:"locked"},{id:37,name:"斩立决(秘宝级)",type:"locked"},{id:38,name:"无涯学海(秘宝级)",type:"locked"},{id:39,name:"百兵之王(秘宝级)",type:"locked"},{id:40,name:"森罗能量(秘宝级)",type:"locked"},{id:41,name:"噬魂(传说级)",type:"locked"},{id:42,name:"醉八仙(传说级)",type:"locked"},{id:43,name:"破天式(传说级)",type:"locked"},{id:44,name:"猛毒咒(传说级)",type:"locked"},{id:45,name:"鲜血咒(传说级)",type:"locked"},{id:46,name:"天极雷(传说级)",type:"locked"},{id:47,name:"天极冰(传说级)",type:"locked"},{id:48,name:"堕天(传说级)",type:"locked"},{id:49,name:"最终式(传说级)",type:"locked"},{id:50,name:"三彩(秘宝级)",type:"locked"},{id:51,name:"镇魂(传说级)",type:"locked"},{id:52,name:"月能满溢(传说级)",type:"locked"},{id:53,name:"[七剑修罗]专属-[冷血]升级(传说级)",type:"locked"},{id:54,name:"[无量尊者]专属-[无量]升级(传说级)",type:"locked"},{id:55,name:"[神饮明王]专属-[燃刃]升级(传说级)",type:"locked"},{id:56,name:"[圣威怒雷金刚]专属-[怒雷]升级(传说级)",type:"locked"},{id:57,name:"[三川苦寒菩萨]专属-[极寒]升级(传说级)",type:"locked"},{id:58,name:"[三尸慈姑娘娘]专属-[血毒]升级(传说级)",type:"locked"},{id:59,name:"[神行迷踪金刚]专属-[一刹]升级(传说级)",type:"locked"},{id:60,name:"[日月轮转双天]专属-[晨昏]升级(传说级)",type:"locked"},{id:61,name:"[阎罗地藏明王]专属-[四苦]升级(传说级)",type:"locked"},{id:62,name:"[灵剑修罗]专属-[逆生剑灵]升级(传说级)",type:"locked"},{id:63,name:"圣王灵能(传说级)",type:"locked"},{id:64,name:"大爆炸(传说级)",type:"locked"},{id:65,name:"无相一击(史诗级)",type:"locked"},{id:66,name:"真实混沌(史诗级)",type:"locked"},{id:67,name:"不坏之盾(史诗级)",type:"locked"},{id:68,name:"自愈(史诗级)",type:"locked"},{id:69,name:"熵能反转(史诗级)",type:"locked"},{id:70,name:"血雷(史诗级)",type:"locked"},{id:71,name:"血冰(史诗级)",type:"locked"},{id:72,name:"血炎(史诗级)",type:"locked"},{id:73,name:"毒雷(史诗级)",type:"locked"},{id:74,name:"毒霜(史诗级)",type:"locked"},{id:75,name:"毒火(史诗级)",type:"locked"},{id:76,name:"白刃强能(史诗级)",type:"locked"},{id:77,name:"飞刃强能(史诗级)",type:"locked"},{id:78,name:"体能强能(史诗级)",type:"locked"},{id:79,name:"月能近满(传说级)",type:"locked"},{id:80,name:"夺魂(传说级)",type:"locked"},{id:81,name:"五行紊乱(传说级)",type:"locked"},{id:82,name:"从不回头(传说级)",type:"locked"},{id:83,name:"奇击(传说级)",type:"locked"},{id:84,name:"魂归刃里(史诗级)",type:"locked"},{id:85,name:"致命挥砍(史诗级)",type:"locked"},{id:86,name:"致命飞刃(史诗级)",type:"locked"},{id:87,name:"体魄之力(史诗级)",type:"locked"},{id:88,name:"不屈护盾(史诗级)",type:"locked"},{id:89,name:"残念护体(史诗级)",type:"locked"},{id:90,name:"移速增幅(稀有级)",type:"locked"},{id:91,name:"攻速增幅(稀有级)",type:"locked"},{id:92,name:"冷却增幅(稀有级)",type:"locked"},{id:93,name:"伤害增幅(稀有级)",type:"locked"},{id:94,name:"防御增幅(稀有级)",type:"locked"},{id:95,name:"生命增幅(稀有级)",type:"locked"},{id:96,name:"深度昏迷(稀有级)",type:"locked"},{id:97,name:"深度冻结(稀有级)",type:"locked"},{id:98,name:"深度畏惧(稀有级)",type:"locked"},{id:99,name:"月能初涨(传说级)",type:"locked"},{id:100,name:"灵魂反流(传说级)",type:"locked"},{id:101,name:"真实强化(传说级)",type:"locked"},{id:102,name:"魂力治愈(史诗级)",type:"locked"},{id:103,name:"魂力强化(史诗级)",type:"locked"},{id:104,name:"恐惧威压(史诗级)",type:"locked"},{id:105,name:"昏迷威压(史诗级)",type:"locked"},{id:106,name:"冻结威压(史诗级)",type:"locked"},{id:107,name:"修身养性(史诗级)",type:"locked"},{id:108,name:"魂力护体(史诗级)",type:"locked"},{id:109,name:"毒性增伤(稀有级)",type:"locked"},{id:110,name:"燃烧增伤(稀有级)",type:"locked"},{id:111,name:"流血增伤(稀有级)",type:"locked"},{id:112,name:"冻结增伤(稀有级)",type:"locked"},{id:113,name:"昏迷增伤(稀有级)",type:"locked"},{id:114,name:"恐惧增伤(稀有级)",type:"locked"},{id:115,name:"药效提纯(稀有级)",type:"locked"},{id:116,name:"治疗强化(稀有级)",type:"locked"},{id:117,name:"护盾强化(稀有级)",type:"locked"},{id:118,name:"愤怒汲取(稀有级)",type:"locked"},{id:119,name:"生命汲取(稀有级)",type:"locked"},{id:120,name:"力量夺取(稀有级)",type:"locked"},{id:121,name:"速度夺取(稀有级)",type:"locked"},{id:122,name:"咒力夺取(稀有级)",type:"locked"},{id:123,name:"防御夺取(稀有级)",type:"locked"},{id:124,name:"强袭护盾(稀有级)",type:"locked"},{id:125,name:"极速护盾(稀有级)",type:"locked"},{id:126,name:"白刃增强(稀有级)",type:"locked"},{id:127,name:"飞刃增强(稀有级)",type:"locked"},{id:128,name:"飞身增强(稀有级)",type:"locked"}];

let currentTab = 'weapon';
let allLeaves = [];
let currentPage = 1;
let perPage = 100;
let searchQuery = '';
let slotData = [];
let weaponNameId = 0;
let weaponLevel = 0;
let potionSlots = [];
let runeData = [];
let runePage = 1;
let runeTotal = 0;
let runePages = 1;
let generalData = {};

function switchTab(tab) {
  currentTab = tab;
  document.getElementById('tabWeapon').classList.toggle('active', tab === 'weapon');
  document.getElementById('tabPotion').classList.toggle('active', tab === 'potion');
  document.getElementById('tabRune').classList.toggle('active', tab === 'rune');
  document.getElementById('tabGeneral').classList.toggle('active', tab === 'general');
  document.getElementById('tabAll').classList.toggle('active', tab === 'all');
  document.getElementById('weaponPanel').classList.toggle('hidden', tab !== 'weapon');
  document.getElementById('potionPanel').classList.toggle('hidden', tab !== 'potion');
  document.getElementById('runePanel').classList.toggle('hidden', tab !== 'rune');
  document.getElementById('generalPanel').classList.toggle('hidden', tab !== 'general');
  document.getElementById('allPanel').classList.toggle('hidden', tab !== 'all');
  document.getElementById('searchWrap').classList.toggle('hidden', tab !== 'all');
  if (tab === 'weapon') {
    loadWeaponState();
  } else if (tab === 'potion') {
    loadPotionState();
  } else if (tab === 'rune') {
    loadRuneState();
  } else if (tab === 'general') {
    loadGeneralState();
  } else {
    loadLeaves();
  }
}

async function loadWeaponState() {
  showLoading(true);
  try {
    const res = await fetch('/api/magic_sword_state');
    const data = await res.json();
    slotData = data.slots || [];
    weaponNameId = data.weaponNameId || 0;
    weaponLevel = data.weaponLevel || 0;
    if (slotData.length === 0) {
      for (let i = 0; i < 5; i++) slotData.push({index: i, entryId: 0, level: 0, values: 0, isNightmare: false});
    }
    renderWeaponUI();
  } catch(e) {
    toast('加载失败', 'err');
  }
  showLoading(false);
}

function renderWeaponUI() {
  document.getElementById('weaponName').value = weaponNameId;

  const lvDiv = document.getElementById('levelOpts');
  let lvHtml = '';
  for (const lv of WEAPON_LEVELS) {
    const sel = weaponLevel === lv.id ? ' selected' : '';
    lvHtml += '<div class="level-opt' + sel + '" data-idx="' + lv.id + '" onclick="selectLevel(' + lv.id + ')">' +
      '<span class="lv-short" style="color:' + lv.color + '">' + esc(lv.short) + '</span>' +
      '<span class="lv-full">' + esc(lv.full) + '</span>' +
      '</div>';
  }
  lvDiv.innerHTML = lvHtml;

  renderSlots();
}

function selectLevel(lv) {
  weaponLevel = lv;
  const opts = document.querySelectorAll('#levelOpts .level-opt');
  opts.forEach(o => {
    o.classList.toggle('selected', parseInt(o.dataset.idx) === lv);
  });
}

function renderSlots() {
  const grid = document.getElementById('slotGrid');
  let html = '';
  for (const slot of slotData) {
    const entry = ENTRY_LIST.find(e => e.id === slot.entryId) || ENTRY_LIST[0];
    const isDream = entry.type === '梦境';
    const tagClass = isDream ? 'dream' : 'normal';
    const tagText = isDream ? '梦境' : '普通';
    const valLocked = isDream;
    const valDisplay = isDream ? 0 : slot.values;

    let opts = '<optgroup label="—— 普通词条 ——">';
    for (const e of ENTRY_LIST) {
      if (e.type !== '普通') continue;
      const sel = slot.entryId === e.id ? ' selected' : '';
      opts += '<option value="' + e.id + '"' + sel + '>' + e.id + ' - ' + esc(e.name) + '</option>';
    }
    opts += '</optgroup><optgroup label="—— 梦境词条 ——">';
    for (const e of ENTRY_LIST) {
      if (e.type !== '梦境') continue;
      const sel = slot.entryId === e.id ? ' selected' : '';
      opts += '<option value="' + e.id + '"' + sel + '>' + e.id + ' - ' + esc(e.name) + '</option>';
    }
    opts += '</optgroup>';

    html += '<div class="slot-card" id="slotCard' + slot.index + '">' +
      '<div class="slot-header">' +
        '<span class="slot-num">插槽 ' + slot.index + '</span>' +
        '<span class="slot-tag ' + tagClass + '" id="slotTag' + slot.index + '">' + tagText + '</span>' +
      '</div>' +
      '<select onchange="onEntryChange(' + slot.index + ')" id="slotEntry' + slot.index + '">' +
        opts +
      '</select>' +
      '<div class="row nightmare-row">' +
        '<label>' +
        '<input type="checkbox" id="slotNightmare' + slot.index + '" ' + (slot.isNightmare ? 'checked' : '') + '>' +
        '梦境词条' +
        '</label>' +
      '</div>' +
      '<div class="row">' +
        '<label>等级</label>' +
        '<input type="number" id="slotLevel' + slot.index + '" value="' + slot.level + '" min="0" max="99">' +
        '<label>数值</label>' +
        '<input type="number" id="slotValues' + slot.index + '" value="' + valDisplay + '" step="0.0001" ' +
          (valLocked ? 'disabled class="locked"' : '') + '>' +
      '</div>' +
    '</div>';
  }
  grid.innerHTML = html;
}

function onEntryChange(idx) {
  const sel = document.getElementById('slotEntry' + idx);
  const entryId = parseInt(sel.value);
  const entry = ENTRY_LIST.find(e => e.id === entryId);
  if (!entry) return;
  const isDream = entry.type === '梦境';
  const tag = document.getElementById('slotTag' + idx);
  tag.textContent = isDream ? '梦境' : '普通';
  tag.className = 'slot-tag ' + (isDream ? 'dream' : 'normal');
  const valInput = document.getElementById('slotValues' + idx);
  if (isDream) {
    valInput.value = 0;
    valInput.disabled = true;
    valInput.classList.add('locked');
  } else {
    valInput.disabled = false;
    valInput.classList.remove('locked');
  }
}

function onWeaponNameChange() {
  weaponNameId = parseInt(document.getElementById('weaponName').value);
}

async function applyAllWeapon() {
  const btn = document.getElementById('btnApply');
  btn.disabled = true;
  btn.innerHTML = '应用中...';

  const items = [];
  items.push({ path: 'magicSword > magicSwordName', value: weaponNameId });
  items.push({ path: 'magicSword > Level', value: weaponLevel });

  for (let i = 0; i < 5; i++) {
    const entryId = parseInt(document.getElementById('slotEntry' + i).value);
    const level = parseInt(document.getElementById('slotLevel' + i).value) || 0;
    const entry = ENTRY_LIST.find(e => e.id === entryId);
    const isDream = entry && entry.type === '梦境';
    const values = isDream ? 0 : (parseFloat(document.getElementById('slotValues' + i).value) || 0);
    const base = 'magicSword > magicSwordEntrys > ' + i + ' > ';
    items.push({ path: base + 'magicSwordEntryName', value: entryId });
    const isNightmare = document.getElementById('slotNightmare' + i).checked;
    items.push({ path: base + 'level', value: level });
    items.push({ path: base + 'values', value: values });
    items.push({ path: base + 'isNightmare', value: isNightmare });
  }

  showLoading(true);
  try {
    const res = await fetch('/api/set_batch', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ items: items })
    });
    const data = await res.json();
    const okCount = data.results.filter(r => r.ok).length;
    toast('应用完成: ' + okCount + '/' + data.results.length + ' 个字段已修改', 'ok');
    await loadWeaponState();
  } catch(e) {
    toast('应用失败: ' + e.message, 'err');
  }
  showLoading(false);
  btn.disabled = false;
  btn.innerHTML = '<svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <path d="M8 18l-6-6 6-6h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H8z"/> </svg>一键应用全部修改';
}

async function init() {
  document.getElementById('search').addEventListener('input', debounce(onSearch, 300));
  document.getElementById('clearSearch').addEventListener('click', clearSearch);
  await loadWeaponState();
}

async function loadPotionState() {
  showLoading(true);
  try {
    const res = await fetch('/api/potion_state');
    const data = await res.json();
    potionSlots = data.slots || [];
    if (potionSlots.length === 0) {
      for (let i = 0; i < 4; i++) potionSlots.push({index: i, potionId: 0, level: 0, elementType: 0});
    }
    renderPotionUI();
  } catch(e) {
    toast('加载失败', 'err');
  }
  showLoading(false);
}

function renderPotionUI() {
  const grid = document.getElementById('potionGrid');
  let html = '';
  for (const slot of potionSlots) {
    const potion = POTION_NAMES.find(p => p.id === slot.potionId) || POTION_NAMES[0];
    let nameOpts = '';
    for (const p of POTION_NAMES) {
      const sel = slot.potionId === p.id ? ' selected' : '';
      nameOpts += '<option value="' + p.id + '"' + sel + '>' + p.id + ' - ' + esc(p.name) + '</option>';
    }
    let lvOpts = '';
    for (const lv of POTION_LEVELS) {
      const sel = slot.level === lv.id ? ' selected' : '';
      lvOpts += '<div class="level-opt' + sel + '" data-idx="' + lv.id + '" onclick="selectPotionLevel(' + slot.index + ',' + lv.id + ')">' +
        '<span class="lv-short" style="color:' + lv.color + '">' + esc(lv.short) + '</span>' +
        '<span class="lv-full">' + esc(lv.full) + '</span>' +
        '</div>';
    }
    html += '<div class="slot-card" id="potionSlotCard' + slot.index + '">' +
      '<div class="slot-header">' +
        '<span class="slot-num">圣物槽 ' + slot.index + '</span>' +
        '<span class="slot-tag normal" style="background:' + (POTION_LEVELS[slot.level] || POTION_LEVELS[0]).color + ';color:#fff">' +
          esc((POTION_LEVELS[slot.level] || POTION_LEVELS[0]).full) + '</span>' +
      '</div>' +
      '<select onchange="onPotionNameChange(' + slot.index + ')" id="potionName' + slot.index + '">' +
        nameOpts +
      '</select>' +
      '<div class="row"><label>品质</label><div class="level-opts" id="potionLevelOpts' + slot.index + '">' + lvOpts + '</div></div>' +
      '<div class="row"><label>元素</label><input type="number" id="potionElem' + slot.index + '" value="' + (slot.elementType || 0) + '" min="0" onchange="onPotionElemChange(' + slot.index + ')" style="width:60px"></div>' +
    '</div>';
  }
  grid.innerHTML = html;
}

function onPotionNameChange(idx) {
  const sel = document.getElementById('potionName' + idx);
  potionSlots[idx].potionId = parseInt(sel.value);
}

function onPotionElemChange(idx) {
  const inp = document.getElementById('potionElem' + idx);
  potionSlots[idx].elementType = parseInt(inp.value) || 0;
}

function selectPotionLevel(slotIdx, lv) {
  potionSlots[slotIdx].level = lv;
  const opts = document.querySelectorAll('#potionLevelOpts' + slotIdx + ' .level-opt');
  opts.forEach(o => {
    o.classList.toggle('selected', parseInt(o.dataset.idx) === lv);
  });
  const tag = document.querySelector('#potionSlotCard' + slotIdx + ' .slot-tag');
  const lvData = POTION_LEVELS[lv];
  tag.textContent = lvData.full;
  tag.style.background = lvData.color;
}

async function applyAllPotion() {
  const btn = document.getElementById('btnApplyPotion');
  btn.disabled = true;
  btn.innerHTML = '应用中...';

  const items = [];
  for (let i = 0; i < 4; i++) {
    const potionId = potionSlots[i].potionId;
    const level = potionSlots[i].level;
    const elementType = potionSlots[i].elementType;
    const base = 'potions > ' + i + ' > ';
    items.push({ path: base + 'PotionName', value: potionId });
    items.push({ path: base + 'Level', value: level });
    items.push({ path: base + 'elementType', value: elementType });
  }

  showLoading(true);
  try {
    const res = await fetch('/api/set_batch', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ items: items })
    });
    const data = await res.json();
    const okCount = data.results.filter(r => r.ok).length;
    toast('应用完成: ' + okCount + '/' + data.results.length + ' 个字段已修改', 'ok');
    await loadPotionState();
  } catch(e) {
    toast('应用失败: ' + e.message, 'err');
  }
  showLoading(false);
  btn.disabled = false;
  btn.innerHTML = '<svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <path d="M8 18l-6-6 6-6h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H8z"/> </svg>一键应用全部修改';
}

async function loadRuneState() {
  showLoading(true);
  try {
    const res = await fetch('/api/rune_state?page=' + runePage + '&per_page=10');
    const data = await res.json();
    runeData = data.runes || [];
    runeTotal = data.total;
    runePages = data.pages;
    renderRuneUI(data);
  } catch(e) {
    toast('加载失败', 'err');
  }
  showLoading(false);
}

function renderRuneUI(data) {
  document.getElementById('runeInfo').textContent = '共 ' + data.total + ' 个残响，第 ' + data.page + '/' + data.pages + ' 页';
  const grid = document.getElementById('runeGrid');
  let html = '';
  for (const rune of runeData) {
    const isLocked = rune.locked;
    let runeNameOpts = '';
    for (const r of RUNE_NAMES) {
      const sel = rune.id === r.id ? ' selected' : '';
      runeNameOpts += '<option value="' + r.id + '"' + sel + '>' + r.id + ' - ' + esc(r.name) + '</option>';
    }
    let attrOpts = '<option value="0">-- 无 --</option>';
    for (const a of RUNE_ATTRS) {
      attrOpts += '<option value="' + a.id + '">' + a.id + ' - ' + esc(a.name) + '</option>';
    }
    let modHtml = '';
    for (const mod of rune.modifiers) {
      const attr = RUNE_ATTRS.find(a => a.id === mod.key);
      const isLockedAttr = attr && attr.type === 'locked';
      const lockedStyle = isLockedAttr ? ' style="color:var(--accent);font-weight:600"' : '';
      modHtml += '<div class="mod-row">' +
        '<label>#' + mod.idx + '</label>' +
        '<select onchange="onRuneModChange(' + rune.index + ',' + mod.idx + ')" id="runeModKey' + rune.index + '_' + mod.idx + '">' +
          attrOpts.replace('value="' + mod.key + '"', 'value="' + mod.key + '" selected') +
        '</select>' +
        '<input type="number" id="runeModVal' + rune.index + '_' + mod.idx + '" value="' + (isLockedAttr ? 0 : mod.value) + '" step="0.0001"' +
          (isLockedAttr ? ' disabled' : '') + ' onchange="onRuneModValChange(' + rune.index + ',' + mod.idx + ')"' + lockedStyle + '>' +
        '</div>';
    }
    html += '<div class="rune-card" id="runeCard' + rune.index + '">' +
      '<div class="rune-header">' +
        '<select class="rune-id-select" onchange="onRuneIdChange(' + rune.index + ')" id="runeId' + rune.index + '">' + runeNameOpts + '</select>' +
        '<span class="rune-idx">#' + rune.index + '</span>' +
        '<button class="lock-btn' + (isLocked ? ' locked' : '') + '" id="runeLockBtn' + rune.index + '" onclick="toggleRuneLock(' + rune.index + ')">' + (isLocked ? '已锁定' : '未锁定') + '</button>' +
      '</div>' +
      '<div class="rune-mod-grid">' + modHtml + '</div>' +
    '</div>';
  }
  grid.innerHTML = html;

  const pager = document.getElementById('runePager');
  let ph = '';
  ph += '<button ' + (data.page <= 1 ? 'disabled' : '') + ' onclick="runeGoPage(' + (data.page - 1) + ')">上一页</button>';
  ph += '<span class="info">' + data.page + ' / ' + data.pages + '</span>';
  ph += '<button ' + (data.page >= data.pages ? 'disabled' : '') + ' onclick="runeGoPage(' + (data.page + 1) + ')">下一页</button>';
  pager.innerHTML = ph;
}

function onRuneIdChange(runeIdx) {
  const sel = document.getElementById('runeId' + runeIdx);
  const rune = runeData.find(r => r.index === runeIdx);
  if (rune) rune.id = parseInt(sel.value);
}

function runeGoPage(p) {
  runePage = p;
  loadRuneState();
  window.scrollTo(0, 0);
}

function onRuneModChange(runeIdx, modIdx) {
  const sel = document.getElementById('runeModKey' + runeIdx + '_' + modIdx);
  const rune = runeData.find(r => r.index === runeIdx);
  if (rune) {
    const mod = rune.modifiers.find(m => m.idx === modIdx);
    if (mod) {
      mod.key = parseInt(sel.value);
      const attr = RUNE_ATTRS.find(a => a.id === mod.key);
      const isLocked = attr && attr.type === 'locked';
      const inp = document.getElementById('runeModVal' + runeIdx + '_' + modIdx);
      if (isLocked) {
        mod.value = 0;
        inp.value = 0;
        inp.disabled = true;
        inp.style.color = 'var(--accent)';
        inp.style.fontWeight = '600';
      } else {
        inp.disabled = false;
        inp.style.color = '';
        inp.style.fontWeight = '';
      }
    }
  }
}

function onRuneModValChange(runeIdx, modIdx) {
  const inp = document.getElementById('runeModVal' + runeIdx + '_' + modIdx);
  const rune = runeData.find(r => r.index === runeIdx);
  if (rune) {
    const mod = rune.modifiers.find(m => m.idx === modIdx);
    if (mod) mod.value = parseFloat(inp.value) || 0;
  }
}

function toggleRuneLock(idx) {
  const rune = runeData.find(r => r.index === idx);
  if (rune) {
    rune.locked = !rune.locked;
    const btn = document.getElementById('runeLockBtn' + idx);
    btn.textContent = rune.locked ? '已锁定' : '未锁定';
    btn.classList.toggle('locked', rune.locked);
  }
}

async function applyAllRune() {
  const btn = document.getElementById('btnApplyRune');
  btn.disabled = true;
  btn.innerHTML = '应用中...';

  const items = [];
  for (const rune of runeData) {
    const base = 'runeInventory > ' + rune.index + ' > ';
    items.push({ path: base + 'id', value: rune.id });
    items.push({ path: base + 'locked', value: rune.locked });
    for (const mod of rune.modifiers) {
      const attr = RUNE_ATTRS.find(a => a.id === mod.key);
      const val = (attr && attr.type === 'locked') ? 0 : mod.value;
      items.push({ path: base + 'modifiers > ' + mod.idx + ' > key', value: mod.key });
      items.push({ path: base + 'modifiers > ' + mod.idx + ' > value', value: val });
    }
  }

  showLoading(true);
  try {
    const res = await fetch('/api/set_batch', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ items: items })
    });
    const data = await res.json();
    const okCount = data.results.filter(r => r.ok).length;
    toast('应用完成: ' + okCount + '/' + data.results.length + ' 个字段已修改', 'ok');
    await loadRuneState();
  } catch(e) {
    toast('应用失败: ' + e.message, 'err');
  }
  showLoading(false);
  btn.disabled = false;
  btn.innerHTML = '<svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <path d="M8 18l-6-6 6-6h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H8z"/> </svg>一键应用全部修改';
}

async function loadGeneralState() {
  showLoading(true);
  try {
    const res = await fetch('/api/general_state');
    generalData = await res.json();
    renderGeneralUI();
  } catch(e) {
    toast('加载失败', 'err');
  }
  showLoading(false);
}

function renderGeneralUI() {
  const fields = [
    {key: 'souls', label: '灵魂', name: 'souls'},
    {key: 'redsouls', label: '红魂', name: 'redsouls'},
    {key: 'dreamAsh', label: '梦境余辉', name: 'dreamAsh'},
    {key: 'timeGlow', label: '时间碎片', name: 'timeGlow'},
    {key: 'TotalPlayCount', label: '游玩次数', name: 'TotalPlayCount'},
  ];
  let html = '';
  for (const f of fields) {
    html += '<div class="general-item">' +
      '<div><div class="gi-label">' + esc(f.label) + '</div><div class="gi-name">' + esc(f.name) + '</div></div>' +
      '<input type="number" id="gi_' + f.key + '" value="' + (generalData[f.key] || 0) +
      '" onchange="onGeneralChange(\'' + f.key + '\')">' +
    '</div>';
  }
  document.getElementById('generalGrid').innerHTML = html;
}

function onGeneralChange(key) {
  const inp = document.getElementById('gi_' + key);
  generalData[key] = parseInt(inp.value) || 0;
}

async function applyAllGeneral() {
  const btn = document.getElementById('btnApplyGeneral');
  btn.disabled = true;
  btn.innerHTML = '应用中...';
  const items = [
    {path: 'souls', value: generalData.souls},
    {path: 'redsouls', value: generalData.redsouls},
    {path: 'dreamAsh', value: generalData.dreamAsh},
    {path: 'timeGlow', value: generalData.timeGlow},
    {path: 'TotalPlayCount', value: generalData.TotalPlayCount},
  ];
  showLoading(true);
  try {
    const res = await fetch('/api/set_batch', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({items: items})
    });
    const data = await res.json();
    const okCount = data.results.filter(r => r.ok).length;
    toast('应用完成: ' + okCount + '/' + data.results.length + ' 个字段已修改', 'ok');
    await loadGeneralState();
  } catch(e) {
    toast('应用失败: ' + e.message, 'err');
  }
  showLoading(false);
  btn.disabled = false;
  btn.innerHTML = '<svg class="icon" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" fill="none"> <path d="M8 18l-6-6 6-6h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H8z"/> </svg>一键应用全部修改';
}

async function loadLeaves() {
  showLoading(true);
  const q = searchQuery ? '&q=' + encodeURIComponent(searchQuery) : '';
  const res = await fetch('/api/leaves?page=' + currentPage + '&per_page=' + perPage + q);
  const data = await res.json();
  allLeaves = data.leaves;
  totalCount = data.total;
  document.getElementById('stats').innerHTML =
    '<span>总计: ' + data.total + ' 个字段</span>' +
    (searchQuery ? '<span>匹配: ' + data.total + '</span>' : '') +
    '<span>第 ' + data.page + '/' + data.pages + ' 页</span>';
  renderLeaves();
  renderPager(data);
  showLoading(false);
}

function renderLeaves() {
  const main = document.getElementById('main');
  if (allLeaves.length === 0) {
    main.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text2)">无匹配结果</div>';
    return;
  }
  let html = '';
  for (const leaf of allLeaves) {
    const pathHtml = leaf.parts.map((p, i) => {
      const isNum = /^\d+$/.test(p);
      return '<span class="seg" style="color:' + (isNum ? 'var(--orange)' : 'var(--blue)') + '">' +
        esc(p) + '</span>';
    }).join('<span class="sep">&#9656;</span>');
    const v = leaf.value;
    let valClass = 'str';
    let displayVal = String(v);
    if (typeof v === 'number') {
      valClass = Number.isInteger(v) ? 'int' : 'float';
      if (!Number.isInteger(v)) displayVal = v.toFixed(6);
    } else if (typeof v === 'boolean') {
      valClass = 'bool';
      displayVal = v ? 'True' : 'False';
    } else if (v === null) {
      displayVal = 'null';
    }
    html += '<div class="leaf-row" onclick="editLeaf(\'' + escAttr(leaf.path) + '\', ' +
      JSON.stringify(v).replace(/'/g, "&#39;") + ')">' +
      '<div class="path">' + pathHtml + '</div>' +
      '<div class="val ' + valClass + '">' + esc(displayVal) + '</div>' +
      '<button class="edit-btn" onclick="event.stopPropagation();editLeaf(\'' +
      escAttr(leaf.path) + '\', ' + JSON.stringify(v).replace(/'/g, "&#39;") + ')">编辑</button>' +
      '</div>';
  }
  main.innerHTML = html;
}

function renderPager(data) {
  const pager = document.getElementById('pager');
  let html = '';
  html += '<button ' + (data.page <= 1 ? 'disabled' : '') + ' onclick="goPage(' + (data.page - 1) + ')">上一页</button>';
  html += '<span class="info">' + data.page + ' / ' + data.pages + '</span>';
  html += '<button ' + (data.page >= data.pages ? 'disabled' : '') + ' onclick="goPage(' + (data.page + 1) + ')">下一页</button>';
  pager.innerHTML = html;
}

function goPage(p) { currentPage = p; loadLeaves(); window.scrollTo(0, 0); }

function onSearch() {
  const q = document.getElementById('search').value.trim();
  const clear = document.getElementById('clearSearch');
  if (q) clear.classList.add('show'); else clear.classList.remove('show');
  searchQuery = q; currentPage = 1; loadLeaves();
}

function clearSearch() {
  document.getElementById('search').value = '';
  searchQuery = ''; currentPage = 1;
  document.getElementById('clearSearch').classList.remove('show');
  loadLeaves();
}

function editLeaf(path, currentVal) {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  let valType = 'number';
  if (typeof currentVal === 'boolean') valType = 'bool';
  else if (typeof currentVal === 'string') valType = 'string';
  const hint = valType === 'bool' ? '输入 true 或 false' :
    valType === 'number' ? '输入数字' : '输入字符串';
  overlay.innerHTML = '<div class="modal">' +
    '<h3>' + esc(path) + '</h3>' +
    '<div class="current">当前值: <strong>' + esc(String(currentVal)) + '</strong></div>' +
    '<input type="text" id="editInput" value="' + escAttr(String(currentVal)) + '" autofocus>' +
    '<div class="hint">' + hint + '</div>' +
    '<div class="btns">' +
    '<button class="cancel" onclick="closeModal()">取消</button>' +
    '<button class="ok" onclick="doEdit(\'' + escAttr(path) + '\', ' +
    JSON.stringify(currentVal).replace(/'/g, "&#39;") + ')">确认修改</button>' +
    '</div></div>';
  overlay.addEventListener('click', function(e) { if (e.target === overlay) closeModal(); });
  document.body.appendChild(overlay);
  setTimeout(() => {
    const inp = document.getElementById('editInput');
    if (inp) { inp.focus(); inp.select(); }
  }, 100);
}

function closeModal() {
  const overlay = document.querySelector('.modal-overlay');
  if (overlay) overlay.remove();
}

function getValType(v) {
  if (typeof v === 'boolean') return 'bool';
  if (typeof v === 'number') return Number.isInteger(v) ? 'int' : 'float';
  return 'string';
}

async function doEdit(path, currentVal) {
  const inp = document.getElementById('editInput');
  if (!inp) return;
  let rawVal = inp.value.trim();
  let newVal;
  const vtype = getValType(currentVal);
  if (vtype === 'bool') {
    if (rawVal.toLowerCase() === 'true' || rawVal === '1') newVal = true;
    else if (rawVal.toLowerCase() === 'false' || rawVal === '0') newVal = false;
    else { toast('请输入 true 或 false', 'err'); return; }
  } else if (vtype === 'int') {
    newVal = parseInt(rawVal);
    if (isNaN(newVal)) { toast('请输入整数', 'err'); return; }
  } else if (vtype === 'float') {
    newVal = parseFloat(rawVal);
    if (isNaN(newVal)) { toast('请输入数字', 'err'); return; }
  } else {
    newVal = rawVal;
  }
  closeModal();
  showLoading(true);
  try {
    const res = await fetch('/api/set', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({path: path, value: newVal})
    });
    const data = await res.json();
    if (data.ok) {
      toast('已修改: ' + path + ' = ' + newVal, 'ok');
      await loadLeaves();
    } else {
      toast(data.error || '修改失败', 'err');
    }
  } catch(e) {
    toast('网络错误: ' + e.message, 'err');
  }
  showLoading(false);
}

async function saveAll() { toast('已自动保存', 'ok'); }

async function reloadData() {
  showLoading(true);
  try {
    await fetch('/api/reload', {method: 'POST'});
    currentPage = 1; searchQuery = '';
    document.getElementById('search').value = '';
    document.getElementById('clearSearch').classList.remove('show');
    if (currentTab === 'weapon') await loadWeaponState();
    else if (currentTab === 'potion') await loadPotionState();
    else if (currentTab === 'rune') await loadRuneState();
    else if (currentTab === 'general') await loadGeneralState();
    else await loadLeaves();
    toast('存档已重新加载', 'ok');
  } catch(e) { toast('重载失败', 'err'); }
  showLoading(false);
}

function toast(msg, type) {
  const t = document.createElement('div');
  t.className = 'toast ' + type;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2000);
}

function showLoading(show) {
  let el = document.getElementById('loading');
  if (show) {
    if (!el) {
      el = document.createElement('div');
      el.id = 'loading';
      el.className = 'loading';
      el.innerHTML = '<div class="spinner"></div>';
      document.body.appendChild(el);
    }
  } else {
    if (el) el.remove();
  }
}

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function escAttr(s) {
  return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function debounce(fn, ms) {
  let timer;
  return function() { clearTimeout(timer); timer = setTimeout(fn, ms); };
}

init();
</script>
</body>
</html>'''

HTML_PAGE = _RAW.replace('__VER__', VERSION)
