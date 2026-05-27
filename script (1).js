/* =========================================================
   Glass Calculator — script.js
   Handles all calculator logic + keyboard support + theme
   ========================================================= */

// ── DOM references ──────────────────────────────────────────
const expressionEl = document.getElementById('expression');
const resultEl     = document.getElementById('result');
const calcEl       = document.querySelector('.calculator');
const themeToggle  = document.getElementById('themeToggle');
const htmlEl       = document.documentElement;

// ── State ───────────────────────────────────────────────────
let currentInput  = '';   // what user is currently typing
let previousInput = '';   // left-hand operand
let operator      = '';   // pending operator (+, −, ×, ÷)
let justEvaluated = false; // did we just press "="?

// ── Display helpers ─────────────────────────────────────────

/**
 * Update the result display.
 * Shrinks font when the number is long.
 */
function updateDisplay(value, expr = '') {
  resultEl.textContent = value === '' ? '0' : value;
  expressionEl.textContent = expr;

  // Shrink font for long numbers
  resultEl.classList.toggle('small', String(value).length > 10);
}

/**
 * Format a number nicely (strip floating-point artifacts).
 */
function formatNumber(num) {
  if (isNaN(num) || !isFinite(num)) return 'Error';
  // Round to avoid 0.1+0.2 = 0.30000000004 style issues
  const rounded = parseFloat(parseFloat(num).toPrecision(12));
  return String(rounded);
}

// ── Core logic ───────────────────────────────────────────────

/**
 * Append a digit or '.' to currentInput.
 */
function inputDigit(digit) {
  if (justEvaluated) {
    // After "=", start a fresh number
    currentInput  = digit;
    previousInput = '';
    operator      = '';
    justEvaluated = false;
  } else {
    // Prevent leading zeros (e.g. "007")
    if (currentInput === '0' && digit !== '.') {
      currentInput = digit;
    } else {
      currentInput += digit;
    }
  }
  updateDisplay(currentInput, buildExpr());
}

/**
 * Append decimal point (only once per number).
 */
function inputDecimal() {
  if (justEvaluated) { currentInput = '0.'; justEvaluated = false; }
  if (currentInput === '')         currentInput = '0';
  if (!currentInput.includes('.')) currentInput += '.';
  updateDisplay(currentInput, buildExpr());
}

/**
 * Set the pending operator. If we already have one, evaluate first.
 */
function inputOperator(op) {
  justEvaluated = false;

  if (currentInput === '' && previousInput !== '') {
    // Just change the operator
    operator = op;
    updateDisplay(previousInput, previousInput + ' ' + op);
    return;
  }

  if (previousInput !== '' && currentInput !== '') {
    // Chain calculation
    const result = evaluate();
    previousInput = formatNumber(result);
    currentInput  = '';
    operator      = op;
    updateDisplay(previousInput, previousInput + ' ' + op);
    return;
  }

  previousInput = currentInput || previousInput || '0';
  currentInput  = '';
  operator      = op;

  // Highlight the active operator button
  highlightOp(op);
  updateDisplay(previousInput, previousInput + ' ' + op);
}

/**
 * Evaluate the pending operation and show result.
 */
function handleEquals() {
  if (operator === '' || (previousInput === '' && currentInput === '')) return;

  const result = evaluate();
  const expr   = `${previousInput} ${operator} ${currentInput || previousInput} =`;

  updateDisplay(formatNumber(result), expr);

  // Reset state but keep result visible
  previousInput = formatNumber(result);
  currentInput  = '';
  operator      = '';
  justEvaluated = true;

  clearOpHighlight();
}

/**
 * Perform the arithmetic. Returns a number.
 */
function evaluate() {
  const a = parseFloat(previousInput);
  const b = parseFloat(currentInput !== '' ? currentInput : previousInput);

  switch (operator) {
    case '+': return a + b;
    case '−': return a - b;
    case '×': return a * b;
    case '÷':
      if (b === 0) { triggerError(); return 0; }
      return a / b;
    default:  return b;
  }
}

/**
 * Build the live expression string shown above the result.
 */
function buildExpr() {
  if (operator) return `${previousInput} ${operator} ${currentInput}`;
  return '';
}

// ── Action handlers ──────────────────────────────────────────

function handleClear() {
  currentInput  = '';
  previousInput = '';
  operator      = '';
  justEvaluated = false;
  clearOpHighlight();
  updateDisplay('0', '');
}

function handleBackspace() {
  if (justEvaluated) { handleClear(); return; }
  currentInput = currentInput.slice(0, -1);
  updateDisplay(currentInput || '0', buildExpr());
}

function handlePercent() {
  if (currentInput === '') return;
  currentInput = formatNumber(parseFloat(currentInput) / 100);
  updateDisplay(currentInput, buildExpr());
}

function handleSign() {
  if (currentInput === '' || currentInput === '0') return;
  currentInput = currentInput.startsWith('-')
    ? currentInput.slice(1)
    : '-' + currentInput;
  updateDisplay(currentInput, buildExpr());
}

// ── Error feedback ───────────────────────────────────────────

function triggerError() {
  updateDisplay('Error', '');
  calcEl.classList.add('shake');
  calcEl.addEventListener('animationend', () => {
    calcEl.classList.remove('shake');
    handleClear();
  }, { once: true });
}

// ── Operator button highlight ─────────────────────────────────

function highlightOp(op) {
  clearOpHighlight();
  document.querySelectorAll('.btn-op').forEach(btn => {
    if (btn.dataset.op === op) btn.classList.add('active');
  });
}

function clearOpHighlight() {
  document.querySelectorAll('.btn-op').forEach(b => b.classList.remove('active'));
}

// ── Button click handler ─────────────────────────────────────

function handleButton(btn) {
  // Flash animation
  btn.classList.add('key-press');
  btn.addEventListener('animationend', () => btn.classList.remove('key-press'), { once: true });

  const num    = btn.dataset.num;
  const op     = btn.dataset.op;
  const action = btn.dataset.action;

  if (num    !== undefined) { inputDigit(num); return; }
  if (op     !== undefined) { inputOperator(op); return; }

  switch (action) {
    case 'clear':     handleClear();     break;
    case 'backspace': handleBackspace(); break;
    case 'percent':   handlePercent();   break;
    case 'sign':      handleSign();      break;
    case 'dot':       inputDecimal();    break;
    case 'equals':    handleEquals();    break;
  }
}

// Attach click listeners to all calculator buttons
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', () => handleButton(btn));
});

// ── Keyboard support ─────────────────────────────────────────

const KEY_MAP = {
  '0':'0','1':'1','2':'2','3':'3','4':'4',
  '5':'5','6':'6','7':'7','8':'8','9':'9',
  '.': 'dot', ',': 'dot',
  '+': '+', '-': '−', '*': '×', '/': '÷',
  'Enter': 'equals', '=': 'equals',
  'Backspace': 'backspace', 'Delete': 'clear',
  'Escape': 'clear', '%': 'percent',
};

document.addEventListener('keydown', e => {
  const mapped = KEY_MAP[e.key];
  if (!mapped) return;
  e.preventDefault();

  // Find matching button and trigger it visually + logically
  let btn = null;
  if ('0123456789'.includes(mapped)) {
    btn = document.querySelector(`.btn-num[data-num="${mapped}"]`);
    if (btn) handleButton(btn); else inputDigit(mapped);
  } else if (['+','−','×','÷'].includes(mapped)) {
    btn = document.querySelector(`.btn-op[data-op="${mapped}"]`);
    if (btn) handleButton(btn); else inputOperator(mapped);
  } else {
    btn = document.querySelector(`.btn[data-action="${mapped}"]`);
    if (btn) handleButton(btn);
  }

  // Flash the button visually even if we handled it without a button ref
  if (btn) {
    btn.classList.add('key-press');
    btn.addEventListener('animationend', () => btn.classList.remove('key-press'), { once: true });
  }
});

// ── Theme toggle ─────────────────────────────────────────────

themeToggle.addEventListener('click', () => {
  const isDark = htmlEl.getAttribute('data-theme') === 'dark';
  htmlEl.setAttribute('data-theme', isDark ? 'light' : 'dark');
});

// ── Init ──────────────────────────────────────────────────────
updateDisplay('0', '');
