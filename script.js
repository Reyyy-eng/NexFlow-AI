// ==========================================
// 1. Clock Logic
// ==========================================
function updateClock() {
  const clockEl = document.getElementById('clock');
  if (clockEl) {
    const d = new Date();
    clockEl.textContent = d.toLocaleTimeString('en-GB');
  }
}
updateClock();
setInterval(updateClock, 1000);

// ==========================================
// 2. Real-Time Telemetry Simulation
// ==========================================
let util = 64; // Fuel Station Utilization %
let thr = 1240; // Throughput (veh/hr)
let q = 18;    // Queue Length

function renderMetrics() {
  const valUtil = document.getElementById('val-util');
  const barUtil = document.getElementById('bar-util');
  const valThr = document.getElementById('val-thr');
  const barThr = document.getElementById('bar-thr');
  const valQ = document.getElementById('val-q');
  const barQ = document.getElementById('bar-q');

  if (valUtil && barUtil) {
    valUtil.innerHTML = `${util}<small>%</small>`;
    barUtil.style.width = `${util}%`;
  }
  if (valThr && barThr) {
    valThr.innerHTML = `${thr.toLocaleString('en-US')}<small> veh/hr</small>`;
    barThr.style.width = `${Math.min(100, (thr / 1800) * 100)}%`;
  }
  if (valQ && barQ) {
    valQ.innerHTML = `${q}<small> vehicles</small>`;
    barQ.style.width = `${Math.min(100, (q / 50) * 100)}%`;
  }
}
renderMetrics();

// Live updates every 4 seconds
setInterval(() => {
  util = Math.max(30, Math.min(96, Math.round(util + (Math.random() * 6 - 3))));
  thr = Math.max(600, Math.min(1700, Math.round(thr + (Math.random() * 80 - 40))));
  q = Math.max(4, Math.min(48, Math.round(q + (Math.random() * 4 - 2))));
  renderMetrics();
}, 4000);

// ==========================================
// 3. Pipeline Flow & Simulation Execution
// ==========================================
const stages = document.querySelectorAll('.stage');
const runBtn = document.getElementById('runSim');
const simEmpty = document.getElementById('simEmpty');
const simResult = document.getElementById('simResult');

function resetStages() {
  stages.forEach(s => s.classList.remove('active', 'done'));
}

if (runBtn) {
  runBtn.addEventListener('click', () => {
    runBtn.disabled = true;
    runBtn.textContent = 'Running NexFlow AI…';
    resetStages();

    if (simEmpty) simEmpty.style.display = 'none';
    if (simResult) simResult.style.display = 'none';

    let i = 0;
    const interval = setInterval(() => {
      if (i > 0) {
        stages[i - 1].classList.remove('active');
        stages[i - 1].classList.add('done');
      }
      if (i < stages.length) {
        stages[i].classList.add('active');
        i++;
      } else {
        clearInterval(interval);
        stages[stages.length - 1].classList.remove('active');
        stages[stages.length - 1].classList.add('done');

        // Reveal simulation results
        fetchStationPrediction();
      }
    }, 550);
  });
}

function fetchStationPrediction() {
  // Update prediction output
  const congProb = document.getElementById('cong-prob');
  const congQueue = document.getElementById('cong-queue');
  const congEta = document.getElementById('cong-eta');

  if (congProb) congProb.textContent = '84%';
  if (congQueue) congQueue.textContent = '37';
  if (congEta) congEta.textContent = '4 min';

  // Surge state metrics update
  q = 37;
  util = 89;
  renderMetrics();

  if (simResult) simResult.style.display = 'block';
  if (runBtn) {
    runBtn.disabled = false;
    runBtn.textContent = '+20 vehicles ▸ Run again';
  }
}