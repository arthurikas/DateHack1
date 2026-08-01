import re

file_path = r"C:\Users\Arthur\.gemini\antigravity\scratch\date-invite\dashboard.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. NAME Replacement:
content = content.replace("<title>DateInvite — Painel</title>", "<title>Date Hack — Painel</title>")
content = content.replace("💌 DateInvite", "💘 Date Hack")
content = content.replace("DateInvite", "Date Hack")

# Let's fix the history key back if it was replaced (we want to keep JS logic as-is, though the prompt said "all 'DateInvite' text", the history key shouldn't matter much. Let's fix JS just in case)
content = content.replace("'Date Hack_history", "'dateinvite_history")
content = content.replace("Date Hack_history_", "dateinvite_history_")

# 2. CSS variables
root_css = """  :root {
    --bg: #0d0d0f;
    --bg2: #1a1220;
    --bg3: #150e18;
    --surface: rgba(255,255,255,0.04);
    --surface2: rgba(255,255,255,0.07);
    --pink: #ff2d78;
    --pink2: #ff4d94;
    --pink-glow: rgba(255,45,120,0.25);
    --purple: #7a1f5c;
    --purple2: #4a0e3d;
    --text: #f5f5f5;
    --text-muted: #a0a0a8;
    --border: rgba(255,45,120,0.18);
    --border2: rgba(255,255,255,0.08);
    --radius: 16px;
    --transition: all 0.25s ease;
    --pink-50: #1a0d14;
    --pink-100: #2a0d1e;
    --pink-200: rgba(255,45,120,0.25);
    --pink-300: #ff4d94;
    --pink-400: #ff2d78;
    --pink-500: #e0205e;
    --pink-600: #c21855;
    --pink-700: #9e1048;
    --pink-800: #7a1f5c;
    --pink-900: #4a0e3d;
    --sidebar-w: 240px;
    --header-h: 64px;
    --shadow: 0 4px 24px rgba(229,33,74,0.1);
  }"""
content = re.sub(r'  :root\s*\{.*?(?=  \})  \}', root_css, content, flags=re.DOTALL)

# 3. BODY & LAYOUT
body_css = """  body {
    font-family: 'Quicksand', sans-serif;
    background: #0d0d0f;
    color: #f5f5f5;
    height: 100vh; overflow: hidden;
    display: flex;
  }"""
content = re.sub(r'  body\s*\{.*?(?=  /\* ===== LOADING)  ', body_css + '\n\n  ', content, flags=re.DOTALL)

# 4. SIDEBAR
sidebar_css = """  .sidebar {
    width: 260px; flex-shrink: 0;
    background: linear-gradient(180deg, #150e18 0%, #0d0d0f 100%);
    border-right: 1px solid rgba(255,45,120,0.15);
    display: flex; flex-direction: column;
    padding: 0; overflow-y: auto; z-index: 100;
    position: fixed; top: 0; left: 0; bottom: 0;
    transition: transform 0.3s ease;
  }
  .sidebar-brand {
    padding: 24px 20px 20px;
    font-family: 'Poppins', sans-serif;
    font-size: 1.35rem; font-weight: 800;
    color: #f5f5f5;
    border-bottom: 1px solid rgba(255,45,120,0.12);
    display: flex; align-items: center; gap: 8px;
    letter-spacing: -0.3px;
  }
  .sidebar-brand span { color: #ff2d78; }"""
content = re.sub(r'  \.sidebar\s*\{.*?(?=  \.sidebar-nav)', sidebar_css + '\n\n', content, flags=re.DOTALL)

# 5. NAV ITEMS
nav_item_css = """  .nav-item {
    display: flex; align-items: center; gap: 12px;
    padding: 13px 20px;
    cursor: pointer;
    color: #a0a0a8;
    font-weight: 600; font-size: 0.9rem;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
    text-decoration: none;
    background: none; border-top: none; border-right: none; border-bottom: none; width: 100%; text-align: left;
  }
  .nav-item:hover { background: rgba(255,45,120,0.08); color: #f5f5f5; }
  .nav-item.active {
    background: rgba(255,45,120,0.1);
    border-left-color: #ff2d78;
    color: #ff4d94;
  }"""
content = re.sub(r'  \.nav-item\s*\{.*?(?=  \.nav-icon)', nav_item_css + '\n\n', content, flags=re.DOTALL)

# 6. MAIN CONTENT
main_content_css = """  .main-content {
    flex: 1; display: flex; flex-direction: column;
    overflow: hidden; background: #0d0d0f;
    margin-left: 260px; height: 100vh;
  }"""
content = re.sub(r'  \.main-content\s*\{.*?(?=  /\* ===== HEADER)', main_content_css + '\n\n', content, flags=re.DOTALL)

# 7. HEADER
header_css = """  .main-header {
    height: 60px;
    background: rgba(13,13,15,0.95);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255,45,120,0.12);
    display: flex; align-items: center;
    padding: 0 24px; gap: 16px; flex-shrink: 0;
  }
  .header-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1rem; font-weight: 700;
    color: #f5f5f5; flex: 1;
  }"""
content = re.sub(r'  \.main-header\s*\{.*?(?=  \.header-badge)', header_css + '\n\n', content, flags=re.DOTALL)

# 8. WIZARD CARD / CARDS
wizard_css = """  .wizard-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,45,120,0.15);
    border-radius: 16px;
    backdrop-filter: blur(10px);
    position: relative; z-index: 10;
    width: 100%; max-width: 520px;
    padding: 40px 44px;
    min-height: 540px;
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
  }"""
content = re.sub(r'  \.wizard-card\s*\{.*?(?=  /\* Progress dots)', wizard_css + '\n\n', content, flags=re.DOTALL)

# 9. BUTTONS
content = re.sub(r'background:linear-gradient\(135deg,var\(--pink-400\),var\(--pink-600\)\);border:none;', 'background: linear-gradient(135deg, #ff2d78, #7a1f5c); border: none; color: white; box-shadow: 0 4px 16px rgba(255,45,120,0.35);', content)
content = re.sub(r'box-shadow:0 10px 30px rgba\(229,33,74,0\.4\);', 'box-shadow: 0 6px 24px rgba(255,45,120,0.55); transform: translateY(-1px);', content)
content = re.sub(r'transform:translateY\(-2px\);box-shadow:0 10px 30px rgba\(229,33,74,0\.4\);', 'box-shadow: 0 6px 24px rgba(255,45,120,0.55); transform: translateY(-1px);', content)

# 10. BUDGET CARDS & FOOD CARDS
cards_css = """  .budget-card, .food-card {
    background: rgba(255,255,255,0.04);
    border: 1.5px solid rgba(255,45,120,0.15);
    border-radius: 14px;
  }
  .budget-card:hover, .food-card:hover {
    border-color: #ff2d78;
    background: rgba(255,45,120,0.08);
  }
  .budget-card.selected, .food-card.selected {
    border-color: #ff2d78;
    background: rgba(255,45,120,0.12);
    box-shadow: 0 0 0 2px rgba(255,45,120,0.3);
  }"""
content = re.sub(r'  /\* Budget cards \*/.*?(?=  /\* Food grid \*/)', '  /* Budget cards */\n  .cards-grid-2 { display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:8px; }\n' + cards_css + '\n  .budget-card .card-emoji { font-size:1.7rem;display:block;margin-bottom:5px;position:relative;z-index:1;transition:transform 0.3s; }\n  .budget-card.selected .card-emoji { transform:scale(1.2); }\n  .budget-card .card-label { font-size:0.85rem;font-weight:700;color:var(--text);position:relative;z-index:1;transition:color 0.3s; }\n  .budget-card.selected .card-label { color:white; }\n  .budget-card .card-sub { font-size:0.7rem;color:var(--text-muted);position:relative;z-index:1;margin-top:2px;transition:color 0.3s; }\n  .budget-card.selected .card-sub { color:rgba(255,255,255,0.8); }\n\n', content, flags=re.DOTALL)

content = re.sub(r'  /\* Food grid \*/.*?(?=  /\* Dates \*/)', '  /* Food grid */\n  .food-grid { display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-bottom:8px;max-height:230px;overflow-y:auto;padding-right:4px; }\n  .food-grid::-webkit-scrollbar{width:4px;}.food-grid::-webkit-scrollbar-track{background:var(--pink-50);border-radius:4px;}.food-grid::-webkit-scrollbar-thumb{background:var(--pink-200);border-radius:4px;}\n  .food-card .check-badge { position:absolute;top:5px;right:5px;width:16px;height:16px;border-radius:50%;background:var(--pink-400);color:white;font-size:0.6rem;display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(0);transition:var(--transition); }\n  .food-card.selected .check-badge { opacity:1;transform:scale(1); }\n  .food-card .food-emoji { font-size:1.6rem;display:block;margin-bottom:4px; }\n  .food-card .food-name { font-size:0.68rem;font-weight:700;color:var(--text);line-height:1.2; }\n  .selection-hint { font-size:0.78rem;color:var(--text-muted);text-align:center;margin-bottom:4px; }\n\n', content, flags=re.DOTALL)


# 11. PROGRESS DOTS
dots_css = """  .dot { width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,0.15);transition:all 0.3s; }
  .dot.active { background:#ff2d78;box-shadow:0 0 10px rgba(255,45,120,0.6); width:28px;border-radius:6px; }
  .dot.done { background:#7a1f5c; }
  .dot-line { height:2px;flex:1;background:rgba(255,255,255,0.08); }
  .dot-line.done { background:#7a1f5c; }"""
content = re.sub(r'  \.dot \{.*?(?=  /\* Step \*/)', dots_css + '\n\n', content, flags=re.DOTALL)

# 12. INPUTS/TEXTAREAS
inputs_css = """  .text-input, .textarea-input {
    background: rgba(255,255,255,0.05);
    border: 1.5px solid rgba(255,45,120,0.2);
    border-radius: 12px;
    color: #f5f5f5;
    font-family: 'Quicksand', sans-serif;
    width: 100%; padding: 13px 16px; outline: none; transition: all 0.3s;
  }
  .text-input:focus, .textarea-input:focus {
    border-color: #ff2d78;
    box-shadow: 0 0 0 3px rgba(255,45,120,0.2);
    outline: none;
  }
  .text-input::placeholder, .textarea-input::placeholder { color: #404050; }"""
content = re.sub(r'  \.text-input, \.textarea-input\s*\{.*?(?=  \.textarea-input \{)', inputs_css + '\n', content, flags=re.DOTALL)

# 13. DATE SLOTS
dates_css = """  .date-slot input[type="date"], .date-slot input[type="time"] {
    background: rgba(255,255,255,0.05);
    border: 1.5px solid rgba(255,45,120,0.2);
    border-radius: 10px;
    color: #f5f5f5;
    padding: 8px 10px;
    font-family: 'Quicksand', sans-serif; font-size: 0.82rem; font-weight: 600; outline: none;
  }
  .date-slot input:focus {
    border-color: #ff2d78;
    outline: none;
    box-shadow: 0 0 0 2px rgba(255,45,120,0.2);
  }"""
content = re.sub(r'  \.date-slot input\[type="date"\].*?(?=  \.date-slot \.remove-btn)', dates_css + '\n', content, flags=re.DOTALL)

# 14. LINK BOX
linkbox_css = """  .link-box {
    background: rgba(255,45,120,0.06);
    border: 1.5px solid rgba(255,45,120,0.25);
    border-radius: 12px;
    padding: 10px 12px; display: flex; align-items: center; gap: 8px; margin-bottom: 10px;
  }
  .link-text { color: #ff4d94; flex:1;font-size:0.72rem;word-break:break-all;font-weight:600;font-family:monospace; }
  .copy-btn {
    background: linear-gradient(135deg, #ff2d78, #7a1f5c);
    color: white;
    border: none; border-radius: 8px;
    box-shadow: 0 2px 8px rgba(255,45,120,0.3);
    padding: 7px 12px; font-size: 0.78rem; font-weight: 700; cursor: pointer; transition: all 0.3s; white-space: nowrap; flex-shrink: 0;
  }"""
content = re.sub(r'  \.link-box \{.*?(?=  \.copy-btn:hover)', linkbox_css + '\n', content, flags=re.DOTALL)

# 15. HEARTS BG
content = re.sub(r'\.heart-p \{ position: absolute; .*? \}', '.heart-p { position: absolute; bottom: -60px; opacity: 0; animation: floatUp linear infinite; font-size: 1.2rem; filter: drop-shadow(0 0 6px #ff2d78); }', content)

# 16. SIDEBAR USER
user_css = """  .sidebar-footer {
    padding: 16px 12px;
    border-top: 1px solid rgba(255,45,120,0.12);
    background: rgba(255,255,255,0.02);
  }
  .user-chip {
    display: flex; align-items: center; gap: 10px; padding: 10px 12px;
    background: rgba(255,255,255,0.04); border-radius: 12px; margin-bottom: 8px;
  }
  .user-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    background: linear-gradient(135deg, #ff2d78, #7a1f5c);
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 0.85rem; font-weight: 700; flex-shrink: 0;
  }"""
content = re.sub(r'  \.sidebar-footer \{.*?(?=  \.user-name)', user_css + '\n', content, flags=re.DOTALL)

# 17. LOADING OVERLAY
loading_css = """  #loading-overlay {
    position: fixed; inset: 0; background: #0d0d0f;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    z-index: 9999; transition: opacity 0.4s ease;
  }"""
content = re.sub(r'  #loading-overlay \{.*?(?=  #loading-overlay\.hidden)', loading_css + '\n', content, flags=re.DOTALL)
content = re.sub(r'\.loading-spinner \{.*?\}', '.loading-spinner { width:36px;height:36px;border:3px solid var(--pink-200);border-top-color:var(--pink-400);border-radius:50%;animation:spin 0.7s linear infinite; }', content)

# 18. HISTORY CARD
history_css = """  .history-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,45,120,0.15);
    border-radius: 16px;
    padding: 20px; transition: var(--transition);
  }
  .history-card:hover {
    border-color: rgba(255,45,120,0.4);
    box-shadow: 0 8px 32px rgba(255,45,120,0.15);
    transform: translateY(-3px);
  }"""
content = re.sub(r'  \.history-card \{.*?(?=  \.hc-header)', history_css + '\n', content, flags=re.DOTALL)

# 19. THEME CARDS
theme_css = """  .theme-card {
    background: rgba(255,255,255,0.04);
    border: 1.5px solid rgba(255,45,120,0.15);
    border-radius: 12px; padding: 12px 8px; text-align: center; cursor: pointer; transition: var(--transition); position: relative; overflow: hidden;
  }
  .theme-card.selected {
    border-color: #ff2d78;
    background: rgba(255,45,120,0.1);
    box-shadow: 0 0 0 2px rgba(255,45,120,0.3);
    transform: translateY(-3px);
  }"""
content = re.sub(r'  \.theme-card \{.*?(?=  \.theme-card\[data-theme)', theme_css + '\n', content, flags=re.DOTALL)
content = re.sub(r'\.theme-card\[data-theme="romantic"\] \{.*?\}', '', content)
content = re.sub(r'\.theme-card\[data-theme="romantic"\]\.selected \{.*?\}', '', content)
content = re.sub(r'\.theme-card\[data-theme="casual"\] \{.*?\}', '', content)
content = re.sub(r'\.theme-card\[data-theme="casual"\]\.selected \{.*?\}', '', content)
content = re.sub(r'\.theme-card\[data-theme="elegant"\] \{.*?\}', '', content)
content = re.sub(r'\.theme-card\[data-theme="elegant"\]\.selected \{.*?\}', '', content)
content = re.sub(r'\.theme-card\[data-theme="romantic"\] \.theme-name \{.*?\}', '', content)
content = re.sub(r'\.theme-card\[data-theme="casual"\] \.theme-name \{.*?\}', '', content)
content = re.sub(r'\.theme-card\[data-theme="elegant"\] \.theme-name \{.*?\}', '', content)
content = re.sub(r'\.hc-theme-badge \{.*?\}', '.hc-theme-badge { width: 30px; height: 30px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1rem; background: rgba(255,45,120,0.1); }', content)
content = re.sub(r'\.theme-romantic-bg \{.*?\}', '', content)
content = re.sub(r'\.theme-casual-bg \{.*?\}', '', content)
content = re.sub(r'\.theme-elegant-bg \{.*?\}', '', content)

# 20. PREVIEW BOX
preview_css = """  .preview-box {
    background: rgba(255,45,120,0.05);
    border: 1.5px solid rgba(255,45,120,0.2);
    border-radius: 14px;
    padding: 16px; margin-bottom: 14px; text-align: center; position: relative; overflow: hidden;
  }
  .preview-box::before { content:'💌';position:absolute;top:-10px;right:-10px;font-size:3rem;opacity:0.12;transform:rotate(20deg); }
  .preview-name { color: #ff4d94; font-family:'Poppins',sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:4px; }"""
content = re.sub(r'  \.preview-box \{.*?(?=  \.preview-phrase)', preview_css + '\n', content, flags=re.DOTALL)

# 21. CHIPS
chip_css = """  .chip {
    background: rgba(255,45,120,0.12);
    border: 1px solid rgba(255,45,120,0.3);
    color: #ff4d94;
    border-radius: 20px;
    padding: 3px 10px; font-size: 0.7rem; font-weight: 600;
  }"""
content = re.sub(r'  \.chip \{.*?(?=  /\* Link \+ result \*/)', chip_css + '\n\n', content, flags=re.DOTALL)

# 22. STEP TITLES/SUBTITLES
content = re.sub(r'\.step-title \{.*?\}', '.step-title { color: #f5f5f5; font-family:\'Poppins\',sans-serif;font-size:1.45rem;font-weight:700;text-align:center;margin-bottom:6px;line-height:1.3; }', content)
content = re.sub(r'\.step-subtitle \{.*?\}', '.step-subtitle { color: #a0a0a8; font-size:0.88rem;text-align:center;margin-bottom:24px;font-weight:500; }', content)
content = re.sub(r'\.field-label \{.*?\}', '.field-label { color: #ff4d94; font-size:0.8rem;font-weight:700;margin-bottom:7px;display:block;letter-spacing:0.5px;text-transform:uppercase; }', content)

# 23. SECTION TITLE
content = re.sub(r'\.section-title \{.*?(?=    margin-bottom: 20px;)', '.section-title {\n    color: #f5f5f5;\n    font-family: \'Poppins\', sans-serif;\n    font-size: 1.2rem;\n    font-weight: 700;\n', content, flags=re.DOTALL)

# 24. PROFILE CARD
profile_css = """  .profile-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,45,120,0.15);
    border-radius: 20px;
    padding: 32px; width: 100%; max-width: 500px; box-shadow: var(--shadow); z-index: 10; position: relative;
  }
  .profile-avatar-big {
    background: linear-gradient(135deg, #ff2d78, #7a1f5c);
    width: 72px; height: 72px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.8rem; font-weight: 700; margin: 0 auto 20px; box-shadow: 0 8px 24px rgba(229,33,74,0.3);
  }
  .profile-name-big { color: #f5f5f5; font-family:'Poppins',sans-serif;font-size:1.3rem;font-weight:700;text-align:center;margin-bottom:4px; }
  .profile-email-big { color: #a0a0a8; font-size:0.85rem;text-align:center;margin-bottom:24px;font-weight:500; }"""
content = re.sub(r'  \.profile-card \{.*?(?=  \.profile-info-list)', profile_css + '\n\n', content, flags=re.DOTALL)

# Fix background panel color
content = re.sub(r'background: linear-gradient\(135deg, #faf5f7 0%, #fff0f3 100%\);', 'background: transparent;', content)

# Write output
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
