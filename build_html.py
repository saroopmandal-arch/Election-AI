html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ElectionIQ — AI Election Assistant for India</title>
<meta name="description" content="ElectionIQ helps Indian citizens understand the election process — voter registration, EVMs, polling day, and results.">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',sans-serif;background:#fff;color:#0A0A0A;min-height:100vh;display:flex;flex-direction:column}
:root{--navy:#1D3461;--bg:#fff;--text:#0A0A0A;--sub:#6B6B6B;--divider:#F0F0F0;--bubble-ai:#F5F5F7;--nav-h:68px}
a{text-decoration:none;color:inherit}
/* SCREENS */
.screen{display:none;flex:1;overflow-y:auto;padding-bottom:calc(var(--nav-h) + 16px);min-height:calc(100vh - var(--nav-h))}
.screen.active{display:block}
/* NAV */
nav{position:fixed;bottom:0;left:0;right:0;height:var(--nav-h);background:#fff;border-top:1px solid var(--divider);display:flex;align-items:stretch;z-index:100}
.nav-btn{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;border:none;background:none;cursor:pointer;color:var(--sub);font-size:10px;font-family:'Inter',sans-serif;font-weight:500;transition:color .2s;padding:8px 4px}
.nav-btn.active{color:var(--navy)}
.nav-btn svg{width:22px;height:22px;stroke-width:1.8}
.nav-btn span{font-size:10px;letter-spacing:.3px}
/* HOME */
#home{padding:0}
.home-hero{padding:60px 28px 32px}
.home-eyebrow{font-size:12px;font-weight:600;letter-spacing:2px;color:var(--sub);text-transform:uppercase;margin-bottom:16px}
.home-title{font-size:36px;font-weight:700;line-height:1.15;color:var(--text);margin-bottom:12px}
.home-title span{color:var(--navy)}
.home-sub{font-size:15px;color:var(--sub);line-height:1.6;max-width:340px}
.home-input-wrap{padding:0 20px 28px;position:sticky;bottom:calc(var(--nav-h) + 0px)}
.home-input-box{display:flex;align-items:center;gap:10px;background:#fff;border:1.5px solid var(--divider);border-radius:14px;padding:12px 16px;box-shadow:0 2px 16px rgba(0,0,0,.07)}
.home-input-box input{flex:1;border:none;outline:none;font-size:15px;font-family:'Inter',sans-serif;color:var(--text);background:transparent}
.home-input-box input::placeholder{color:#BCBCBC}
.send-btn{background:var(--navy);border:none;border-radius:9px;width:36px;height:36px;display:flex;align-items:center;justify-content:center;cursor:pointer;flex-shrink:0;transition:opacity .2s}
.send-btn:hover{opacity:.85}
.send-btn svg{width:17px;height:17px;stroke:#fff;stroke-width:2.2;fill:none}
.chips-wrap{padding:0 20px 32px;display:flex;flex-wrap:wrap;gap:10px}
.chip{background:#F5F5F7;border:none;border-radius:99px;padding:10px 18px;font-size:13px;font-weight:500;font-family:'Inter',sans-serif;color:var(--text);cursor:pointer;transition:background .18s,color .18s}
.chip:hover{background:var(--navy);color:#fff}
.chip.timeline-chip{border:1.5px solid var(--navy);background:#fff;color:var(--navy)}
.chip.timeline-chip:hover{background:var(--navy);color:#fff}
.section-label{font-size:11px;font-weight:600;letter-spacing:1.8px;text-transform:uppercase;color:var(--sub);padding:0 28px 14px}
/* CHAT */
#chat{display:none;flex-direction:column}
#chat.active{display:flex}
.chat-header{padding:20px 24px 16px;border-bottom:1px solid var(--divider);display:flex;align-items:center;gap:12px;background:#fff;position:sticky;top:0;z-index:10}
.chat-avatar{width:38px;height:38px;background:var(--navy);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.chat-avatar svg{width:20px;height:20px;stroke:#fff;fill:none;stroke-width:1.8}
.chat-head-info h2{font-size:15px;font-weight:600;margin-bottom:1px}
.chat-head-info p{font-size:12px;color:var(--sub)}
.status-dot{width:7px;height:7px;background:#34C759;border-radius:50%;display:inline-block;margin-right:5px}
.messages{flex:1;overflow-y:auto;padding:20px 20px 0}
.msg{display:flex;margin-bottom:16px}
.msg.user{justify-content:flex-end}
.msg.ai{justify-content:flex-start}
.bubble{max-width:78%;padding:12px 16px;border-radius:18px;font-size:14px;line-height:1.65;word-break:break-word}
.msg.user .bubble{background:var(--navy);color:#fff;border-bottom-right-radius:5px}
.msg.ai .bubble{background:var(--bubble-ai);color:var(--text);border-bottom-left-radius:5px}
.typing{display:flex;gap:5px;align-items:center;padding:14px 16px}
.dot{width:7px;height:7px;background:#BCBCBC;border-radius:50%;animation:bounce .9s infinite}
.dot:nth-child(2){animation-delay:.18s}
.dot:nth-child(3){animation-delay:.36s}
@keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}
.chat-input-area{padding:14px 16px;border-top:1px solid var(--divider);display:flex;gap:10px;align-items:center;background:#fff;position:sticky;bottom:var(--nav-h)}
.chat-input-area input{flex:1;border:1.5px solid var(--divider);border-radius:12px;padding:11px 14px;font-size:14px;font-family:'Inter',sans-serif;outline:none;box-shadow:0 1px 6px rgba(0,0,0,.06);transition:border-color .2s}
.chat-input-area input:focus{border-color:var(--navy)}
/* TIMELINE */
#timeline{padding:32px 24px}
.page-title{font-size:26px;font-weight:700;margin-bottom:6px}
.page-sub{font-size:14px;color:var(--sub);margin-bottom:36px;line-height:1.6}
.tl{position:relative;padding-left:32px}
.tl::before{content:'';position:absolute;left:10px;top:6px;bottom:6px;width:2px;background:var(--divider)}
.tl-item{position:relative;margin-bottom:32px}
.tl-item:last-child{margin-bottom:0}
.tl-dot{position:absolute;left:-32px;top:4px;width:20px;height:20px;border-radius:50%;background:var(--navy);border:3px solid #fff;box-shadow:0 0 0 2px var(--navy);display:flex;align-items:center;justify-content:center}
.tl-dot-inner{width:6px;height:6px;background:#fff;border-radius:50%}
.tl-phase{font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--navy);margin-bottom:4px}
.tl-name{font-size:16px;font-weight:600;margin-bottom:6px}
.tl-desc{font-size:14px;color:var(--sub);line-height:1.6}
/* HOW TO VOTE */
#guide{padding:32px 24px}
.steps{display:flex;flex-direction:column;gap:0}
.step{display:flex;gap:20px;padding:24px 0;border-bottom:1px solid var(--divider)}
.step:last-child{border-bottom:none}
.step-num{width:44px;height:44px;background:var(--navy);color:#fff;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700;flex-shrink:0}
.step-body h3{font-size:16px;font-weight:600;margin-bottom:6px}
.step-body p{font-size:14px;color:var(--sub);line-height:1.65}
/* FAQ */
#faq{padding:32px 24px}
.faq-list{display:flex;flex-direction:column;gap:0}
.faq-item{border-bottom:1px solid var(--divider)}
.faq-q{width:100%;background:none;border:none;text-align:left;padding:20px 0;display:flex;align-items:center;justify-content:space-between;gap:12px;cursor:pointer;font-family:'Inter',sans-serif;font-size:15px;font-weight:500;color:var(--text);line-height:1.5}
.faq-icon{width:22px;height:22px;stroke:var(--sub);stroke-width:2;fill:none;flex-shrink:0;transition:transform .25s}
.faq-item.open .faq-icon{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .3s ease,padding .3s}
.faq-item.open .faq-a{max-height:300px;padding-bottom:18px}
.faq-a p{font-size:14px;color:var(--sub);line-height:1.7}
</style>
</head>
<body>

<!-- ===== HOME ===== -->
<section id="home" class="screen active">
  <div class="home-hero">
    <div class="home-eyebrow">AI-Powered</div>
    <h1 class="home-title">Understand <span>India's<br>Elections</span>,<br>Simply.</h1>
    <p class="home-sub">Ask anything about voter registration, EVMs, polling day, or result declaration.</p>
  </div>
  <div class="home-input-wrap">
    <div class="home-input-box">
      <input id="home-input" type="text" placeholder="Ask about the election process…" autocomplete="off">
      <button class="send-btn" id="home-send-btn" aria-label="Send">
        <svg viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
      </button>
    </div>
  </div>
  <p class="section-label">Quick Questions</p>
  <div class="chips-wrap">
    <button class="chip" data-msg="How do I register to vote in India?">How do I register?</button>
    <button class="chip" data-msg="What is an EVM and how does it work?">What is EVM?</button>
    <button class="chip" data-msg="What should I do on voting day?">Voting Day</button>
    <button class="chip timeline-chip" data-nav="timeline">See Timeline →</button>
  </div>
</section>

<!-- ===== CHAT ===== -->
<section id="chat" class="screen">
  <div class="chat-header">
    <div class="chat-avatar">
      <svg viewBox="0 0 24 24"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>
    </div>
    <div class="chat-head-info">
      <h2>ElectionIQ</h2>
      <p><span class="status-dot"></span>Election Process Assistant</p>
    </div>
  </div>
  <div class="messages" id="messages">
    <div class="msg ai">
      <div class="bubble">Hello! I'm ElectionIQ, your guide to India's election process. Ask me about voter registration, EVMs, polling day, or how results are declared. 🗳️</div>
    </div>
  </div>
  <div class="chat-input-area">
    <input id="chat-input" type="text" placeholder="Type a question…" autocomplete="off">
    <button class="send-btn" id="chat-send-btn" aria-label="Send">
      <svg viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
    </button>
  </div>
</section>

<!-- ===== TIMELINE ===== -->
<section id="timeline" class="screen">
  <h1 class="page-title">Election Timeline</h1>
  <p class="page-sub">India's General Election process, as governed by the Election Commission of India (ECI).</p>
  <div class="tl">
    <div class="tl-item">
      <div class="tl-dot"><div class="tl-dot-inner"></div></div>
      <div class="tl-phase">Phase 01</div>
      <div class="tl-name">Election Announced</div>
      <div class="tl-desc">Election Commission issues the official schedule — dates for polling, model code of conduct activation, and result declaration.</div>
    </div>
    <div class="tl-item">
      <div class="tl-dot"><div class="tl-dot-inner"></div></div>
      <div class="tl-phase">Phase 02</div>
      <div class="tl-name">Voter Registration</div>
      <div class="tl-desc">Citizens verify and update their names on electoral rolls via NVSP (National Voters' Service Portal) or BLO visits.</div>
    </div>
    <div class="tl-item">
      <div class="tl-dot"><div class="tl-dot-inner"></div></div>
      <div class="tl-phase">Phase 03</div>
      <div class="tl-name">Nominations Filed</div>
      <div class="tl-desc">Candidates submit nomination papers to the Returning Officer. Papers are scrutinised; candidates may withdraw before the deadline.</div>
    </div>
    <div class="tl-item">
      <div class="tl-dot"><div class="tl-dot-inner"></div></div>
      <div class="tl-phase">Phase 04</div>
      <div class="tl-name">Campaign Period</div>
      <div class="tl-desc">Political campaigning takes place. The Model Code of Conduct is strictly active. Campaign ends 48 hours before polling (silence period).</div>
    </div>
    <div class="tl-item">
      <div class="tl-dot"><div class="tl-dot-inner"></div></div>
      <div class="tl-phase">Phase 05</div>
      <div class="tl-name">Polling Day</div>
      <div class="tl-desc">Voters cast ballots at designated booths using EVMs. VVPAT provides a paper trail. Polling officers ensure a free and fair process.</div>
    </div>
    <div class="tl-item">
      <div class="tl-dot"><div class="tl-dot-inner"></div></div>
      <div class="tl-phase">Phase 06</div>
      <div class="tl-name">Results Declared</div>
      <div class="tl-desc">Votes are counted on the declared date. ECI announces constituency-wise results on results.eci.gov.in as counting progresses.</div>
    </div>
  </div>
</section>

<!-- ===== HOW TO VOTE ===== -->
<section id="guide" class="screen">
  <h1 class="page-title">How to Vote</h1>
  <p class="page-sub">A simple 5-step guide to casting your ballot on election day.</p>
  <div class="steps">
    <div class="step">
      <div class="step-num">1</div>
      <div class="step-body">
        <h3>Check Voter List</h3>
        <p>Verify your name on the electoral roll at voters.eci.gov.in or via the Voter Helpline app before polling day.</p>
      </div>
    </div>
    <div class="step">
      <div class="step-num">2</div>
      <div class="step-body">
        <h3>Carry Valid ID</h3>
        <p>Bring your Voter ID (EPIC). Alternatives accepted: Aadhaar, PAN card, passport, driving licence, or MNREGA job card.</p>
      </div>
    </div>
    <div class="step">
      <div class="step-num">3</div>
      <div class="step-body">
        <h3>Go to Your Polling Booth</h3>
        <p>Locate your designated booth using the Voter Helpline (1950) or the ECI website. Arrive during polling hours — typically 7 AM to 6 PM.</p>
      </div>
    </div>
    <div class="step">
      <div class="step-num">4</div>
      <div class="step-body">
        <h3>Get Marked &amp; Collect Slip</h3>
        <p>The polling officer verifies your identity, marks your left forefinger with indelible ink, and issues a voter slip.</p>
      </div>
    </div>
    <div class="step">
      <div class="step-num">5</div>
      <div class="step-body">
        <h3>Cast Your Vote</h3>
        <p>Enter the voting compartment and press the button next to your chosen candidate on the Ballot Unit. A beep confirms your vote is recorded.</p>
      </div>
    </div>
  </div>
</section>

<!-- ===== FAQ ===== -->
<section id="faq" class="screen">
  <h1 class="page-title">FAQs</h1>
  <p class="page-sub">Common questions about voting in India, answered simply.</p>
  <div class="faq-list" id="faq-list">
    <div class="faq-item">
      <button class="faq-q">Who is eligible to vote in India?<svg class="faq-icon" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
      <div class="faq-a"><p>Any Indian citizen aged 18 or above whose name appears on the electoral roll of their constituency is eligible to vote.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">What ID is accepted at polling booths?<svg class="faq-icon" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
      <div class="faq-a"><p>Voter ID card (EPIC) is the primary document. Accepted alternatives: Aadhaar card, PAN card, passport, driving licence, and MNREGA job card.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">How does the EVM work?<svg class="faq-icon" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
      <div class="faq-a"><p>The EVM has two units — a Control Unit with the polling officer and a Ballot Unit with the voter. Press the button next to your candidate's name; a beep confirms your vote is recorded.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">What if my name isn't on the voter list?<svg class="faq-icon" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
      <div class="faq-a"><p>Visit your nearest Booth Level Officer (BLO) or apply online at voters.eci.gov.in to register or correct your details in the electoral roll.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q">How and when are results announced?<svg class="faq-icon" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
      <div class="faq-a"><p>Counting begins on the declared counting date. The ECI announces constituency-wise results progressively on results.eci.gov.in as counting continues throughout the day.</p></div>
    </div>
  </div>
</section>

<!-- ===== BOTTOM NAV ===== -->
<nav id="bottom-nav" role="navigation" aria-label="Main navigation">
  <button class="nav-btn active" data-screen="home" id="nav-home">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
    <span>Home</span>
  </button>
  <button class="nav-btn" data-screen="chat" id="nav-chat">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
    <span>Chat</span>
  </button>
  <button class="nav-btn" data-screen="timeline" id="nav-timeline">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
    <span>Timeline</span>
  </button>
  <button class="nav-btn" data-screen="guide" id="nav-guide">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/><path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/></svg>
    <span>Guide</span>
  </button>
  <button class="nav-btn" data-screen="faq" id="nav-faq">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
    <span>FAQ</span>
  </button>
</nav>

<script>
const API = '';
let history = [];

function navigate(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  const btn = document.querySelector('.nav-btn[data-screen="' + id + '"]');
  if (btn) btn.classList.add('active');
  window.scrollTo(0, 0);
}

document.querySelectorAll('.nav-btn').forEach(btn => {
  btn.addEventListener('click', () => navigate(btn.dataset.screen));
});

document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => {
    if (chip.dataset.nav) { navigate(chip.dataset.nav); return; }
    const msg = chip.dataset.msg;
    navigate('chat');
    setTimeout(() => sendMessage(msg), 100);
  });
});

document.getElementById('home-send-btn').addEventListener('click', () => {
  const v = document.getElementById('home-input').value.trim();
  if (!v) return;
  document.getElementById('home-input').value = '';
  navigate('chat');
  setTimeout(() => sendMessage(v), 100);
});
document.getElementById('home-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') document.getElementById('home-send-btn').click();
});

document.getElementById('chat-send-btn').addEventListener('click', () => {
  const inp = document.getElementById('chat-input');
  const v = inp.value.trim();
  if (!v) return;
  inp.value = '';
  sendMessage(v);
});
document.getElementById('chat-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') document.getElementById('chat-send-btn').click();
});

function addMsg(role, text) {
  const msgs = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'msg ' + (role === 'user' ? 'user' : 'ai');
  const b = document.createElement('div');
  b.className = 'bubble';
  b.textContent = text;
  div.appendChild(b);
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
  return div;
}

function showTyping() {
  const msgs = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'msg ai';
  div.id = 'typing';
  div.innerHTML = '<div class="bubble"><div class="typing"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div></div>';
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function hideTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}

async function sendMessage(text) {
  addMsg('user', text);
  showTyping();
  try {
    const res = await fetch(API + '/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({messages: history, user_message: text})
    });
    const data = await res.json();
    hideTyping();
    const reply = data.response || data.detail || 'Sorry, something went wrong.';
    addMsg('ai', reply);
    history.push({role: 'user', content: text});
    history.push({role: 'model', content: reply});
  } catch(e) {
    hideTyping();
    addMsg('ai', 'Could not reach the server. Make sure the backend is running at localhost:8080.');
  }
}

document.getElementById('faq-list').addEventListener('click', e => {
  const btn = e.target.closest('.faq-q');
  if (!btn) return;
  const item = btn.closest('.faq-item');
  const wasOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
  if (!wasOpen) item.classList.add('open');
});
</script>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html written successfully —", len(html), "chars")
