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

async function fetchStationPrediction() {
  const congProb = document.getElementById('cong-prob');
  const congQueue = document.getElementById('cong-queue');
  const congEta = document.getElementById('cong-eta');

  try {
    const response = await fetch('https://nexflow-ai.onrender.com/api/v1/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        cars: q + 20,
        speed: 60
      })
    });

    if (!response.ok) {
      throw new Error('API request failed');
    }

    const result = await response.json();

    // Confidence from AI API
    if (congProb) {
      congProb.textContent = result.confidence_score;
    }

    // Update queue based on simulation
    q = Math.min(48, q + 20);
    if (congQueue) {
      congQueue.textContent = q;
    }

    // Estimated wait time
    let eta = 2;

    if (result.traffic_status === 'Heavy Traffic') {
      eta = 5;
    } else if (result.traffic_status === 'Moderate Traffic') {
      eta = 4;
    }

    if (congEta) {
      congEta.textContent = `${eta} min`;
    }

    // Update station metrics
    util = Math.min(96, util + 15);
    renderMetrics();

    // Update recommendation text
    const actionText = document.querySelector('.tag.action')?.parentElement?.nextElementSibling;

    if (actionText) {
      actionText.textContent = result.suggested_plan;
    }

    // Show results
    if (simResult) {
      simResult.style.display = 'block';
    }

  } catch (error) {
    console.error('NexFlow API Error:', error);

    if (simResult) {
      simResult.style.display = 'block';
    }

    if (congProb) congProb.textContent = 'API Error';
    if (congQueue) congQueue.textContent = '--';
    if (congEta) congEta.textContent = '--';
  }

  if (runBtn) {
    runBtn.disabled = false;
    runBtn.textContent = '+20 vehicles ▸ Run again';
  }
}
