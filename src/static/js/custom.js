// custom.js: Lógica para configurações dinâmicas
async function loadConfig() {
  const resp = await fetch('config.json');
  const config = await resp.json();
  // Carregar logo de localStorage se existir
  const logo = localStorage.getItem('dashboard_logo');
  if (logo) config.logo = logo;
  applyConfig(config);
  fillSettingsForm(config);
}

function applyConfig(config) {
  document.title = config.panel_name || 'Painel';
  document.querySelector('.sidebar h4').textContent = config.panel_name || 'Painel';
  document.documentElement.style.setProperty('--primary-color', config.primary_color || '#4f8cff');
  document.documentElement.style.setProperty('--secondary-color', config.secondary_color || '#232529');
  document.documentElement.style.setProperty('--font-family', config.font || 'Inter, Arial, sans-serif');
  document.documentElement.style.setProperty('--font-size', (config.font_size || 16) + 'px');
  document.body.setAttribute('data-theme', config.theme || 'dark');
  document.body.setAttribute('data-lang', config.lang || 'pt-BR');
  document.body.setAttribute('data-animations', config.animations || 'on');
  // Layout menu
  document.querySelector('.sidebar').classList.toggle('horizontal', config.menu_layout === 'horizontal');
  // Logo
  if (config.logo) {
    let logoEl = document.getElementById('dashboard-logo');
    if (!logoEl) {
      logoEl = document.createElement('img');
      logoEl.id = 'dashboard-logo';
      logoEl.style.maxWidth = '120px';
      logoEl.style.marginBottom = '16px';
      document.querySelector('.sidebar').insertBefore(logoEl, document.querySelector('.sidebar h4'));
    }
    logoEl.src = config.logo;
    logoEl.style.display = 'block';
  } else {
    const logoEl = document.getElementById('dashboard-logo');
    if (logoEl) logoEl.style.display = 'none';
  }
  // Animações
  if (config.animations === 'off') {
    document.body.classList.add('no-animations');
  } else {
    document.body.classList.remove('no-animations');
  }
}

function fillSettingsForm(config) {
  document.getElementById('panelNameInput').value = config.panel_name || '';
  document.getElementById('themeSelect').value = config.theme || 'dark';
  document.getElementById('primaryColorInput').value = config.primary_color || '#4f8cff';
  document.getElementById('secondaryColorInput').value = config.secondary_color || '#232529';
  document.getElementById('fontInput').value = config.font || 'Inter, Arial, sans-serif';
  document.getElementById('fontSizeInput').value = config.font_size || 16;
  document.getElementById('menuLayoutSelect').value = config.menu_layout || 'vertical';
  document.getElementById('langSelect').value = config.lang || 'pt-BR';
  document.getElementById('animationSelect').value = config.animations || 'on';
}

async function saveConfig() {
  const logoInput = document.getElementById('logoInput');
  let logoData = null;
  if (logoInput.files && logoInput.files[0]) {
    const reader = new FileReader();
    reader.onload = function(e) {
      localStorage.setItem('dashboard_logo', e.target.result);
      applyConfig({ ...getConfigFromForm(), logo: e.target.result });
    };
    reader.readAsDataURL(logoInput.files[0]);
    logoData = await new Promise(resolve => {
      reader.onloadend = () => resolve(reader.result);
    });
  } else if (localStorage.getItem('dashboard_logo')) {
    logoData = localStorage.getItem('dashboard_logo');
  }
  const config = getConfigFromForm();
  if (logoData) config.logo = logoData;
  await fetch('/config.json', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config)
  });
  applyConfig(config);
  bootstrap.Modal.getOrCreateInstance(document.getElementById('settingsModal')).hide();
}

function getConfigFromForm() {
  return {
    panel_name: document.getElementById('panelNameInput').value,
    theme: document.getElementById('themeSelect').value,
    primary_color: document.getElementById('primaryColorInput').value,
    secondary_color: document.getElementById('secondaryColorInput').value,
    font: document.getElementById('fontInput').value,
    font_size: parseInt(document.getElementById('fontSizeInput').value, 10),
    menu_layout: document.getElementById('menuLayoutSelect').value,
    lang: document.getElementById('langSelect').value,
    animations: document.getElementById('animationSelect').value
  };
}

function resetConfig() {
  localStorage.removeItem('dashboard_logo');
  fetch('/config.json')
    .then(r => r.json())
    .then(defaults => {
      // Reset para valores de fábrica
      applyConfig(defaults);
      fillSettingsForm(defaults);
    });
}

document.addEventListener('DOMContentLoaded', loadConfig);
window.saveConfig = saveConfig;
window.resetConfig = resetConfig;
