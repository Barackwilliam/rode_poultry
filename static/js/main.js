// ── RODE POULTRY — Main JS ──

document.addEventListener('DOMContentLoaded', () => {

  // ── MOBILE SIDEBAR ──
  const hamburger      = document.getElementById('hamburger');
  const mobileSidebar  = document.getElementById('mobileSidebar');
  const sidebarOverlay = document.getElementById('sidebarOverlay');
  const sidebarClose   = document.getElementById('sidebarClose');

  function openSidebar() {
    mobileSidebar.classList.add('open');
    sidebarOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  function closeSidebar() {
    mobileSidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (hamburger) hamburger.addEventListener('click', openSidebar);
  if (sidebarClose) sidebarClose.addEventListener('click', closeSidebar);
  if (sidebarOverlay) sidebarOverlay.addEventListener('click', closeSidebar);

  // Close sidebar on link click (navigation)
  document.querySelectorAll('.sidebar-link').forEach(link => {
    link.addEventListener('click', closeSidebar);
  });

  // Close sidebar on Escape key
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeSidebar();
  });

  // ── Language switcher ──
  document.querySelectorAll('[data-lang]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const lang = btn.dataset.lang;

      // Skip if already active
      if (btn.classList.contains('active')) return;

      // 1. Update active state immediately on all lang buttons
      document.querySelectorAll('[data-lang]').forEach(b => b.classList.remove('active'));
      document.querySelectorAll(`[data-lang="${lang}"]`).forEach(b => b.classList.add('active'));

      // 2. Show full-screen loading overlay with spinner + label
      showLangLoader(lang);

      // 3. Prepare CSRF + path
      const form   = document.getElementById('django-lang-form');
      const csrf   = form.querySelector('[name=csrfmiddlewaretoken]').value;
      let nextPath = window.location.pathname + window.location.search;
      nextPath     = nextPath.replace(/^\/(en|sw)(\/|$)/, '/');

      try {
        await fetch('/i18n/setlang/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrf,
          },
          body: `language=${lang}&next=${encodeURIComponent(nextPath)}`,
        });
        // Redirect — loader stays visible until new page paints
        window.location.href = (lang === 'sw' ? '' : '/' + lang) + nextPath;
      } catch (e) {
        // Fallback: traditional form submit (loader still shows)
        let langInput = form.querySelector('input[name="language"]');
        if (!langInput) {
          langInput = document.createElement('input');
          langInput.type = 'hidden';
          langInput.name = 'language';
          form.appendChild(langInput);
        }
        langInput.value = lang;
        let nextInput = form.querySelector('input[name="next"]');
        if (!nextInput) {
          nextInput = document.createElement('input');
          nextInput.type = 'hidden';
          nextInput.name = 'next';
          form.appendChild(nextInput);
        }
        nextInput.value = nextPath;
        form.submit();
      }
    });
  });

  // ── Add to cart (AJAX) ──
  document.querySelectorAll('.ajax-add-cart').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const productId = btn.dataset.productId;
      const cartUrl   = btn.dataset.cartUrl;
      const qty       = document.querySelector(`#qty-${productId}`)?.value || 1;
      try {
        const res = await fetch(cartUrl, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: `quantity=${qty}`,
        });
        if (!res.ok) throw new Error('Network error');
        const data = await res.json();
        // Update navbar badge
        let badge = document.querySelector('.cart-badge');
        if (data.cart_count > 0) {
          if (!badge) {
            const cartIcon = document.querySelector('.cart-icon');
            if (cartIcon) {
              badge = document.createElement('span');
              badge.className = 'cart-badge';
              cartIcon.appendChild(badge);
            }
          }
          if (badge) {
            badge.textContent = data.cart_count;
            badge.style.transform = 'scale(1.4)';
            setTimeout(() => badge.style.transform = '', 300);
          }
        }
        // Update floating cart
        const fc      = document.getElementById('floatingCart');
        const fcCount = document.getElementById('fcCount');
        if (fc && data.cart_count > 0) {
          fc.classList.remove('empty');
          if (fcCount) { fcCount.textContent = data.cart_count; fcCount.style.display = 'flex'; }
        }
        showToast(data.message || 'Imeongezwa kwenye Cart! 🛒', 'success');
        const origText = btn.innerHTML;
        btn.innerHTML = '✓ Imeongezwa';
        btn.style.background = 'var(--success)';
        setTimeout(() => {
          btn.innerHTML = origText;
          btn.style.background = '';
        }, 2000);
      } catch (err) {
        showToast('Kuna tatizo. Jaribu tena.', 'error');
      }
    });
  });

  // ── Direct Order (Buy Now) — add to cart then go to checkout ──
  document.querySelectorAll('.btn-direct-order').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const cartUrl     = btn.dataset.cartUrl;
      const checkoutUrl = btn.dataset.checkoutUrl;
      const productId   = btn.dataset.productId;
      const qty         = document.querySelector(`#qty-${productId}`)?.value || 1;
      btn.disabled = true;
      btn.innerHTML = '⏳ Inasubiri...';
      try {
        const res = await fetch(cartUrl, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: `quantity=${qty}`,
        });
        if (!res.ok) throw new Error('Network error');
        window.location.href = checkoutUrl;
      } catch (err) {
        btn.disabled = false;
        btn.innerHTML = '⚡ Oda Moja Kwa Moja';
        showToast('Kuna tatizo. Jaribu tena.', 'error');
      }
    });
  });

  // ── Quantity input controls ──
  document.querySelectorAll('.qty-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.parentElement.querySelector('.qty-input');
      const min   = parseInt(input.min) || 1;
      const max   = parseInt(input.max) || 9999;
      let val     = parseInt(input.value) || 1;
      val += btn.dataset.action === 'inc' ? 1 : -1;
      input.value = Math.min(max, Math.max(min, val));
      // Auto-submit cart update forms
      const form = input.closest('form');
      if (form && form.dataset.autosubmit) form.submit();
      // Trigger change event for price preview
      input.dispatchEvent(new Event('input'));
    });
  });

  // ── Auto-dismiss alerts ──
  document.querySelectorAll('.alert-auto').forEach(el => {
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transition = 'opacity 0.5s';
      setTimeout(() => el.remove(), 500);
    }, 4000);
  });

  // ── Gallery lightbox ──
  document.querySelectorAll('.gallery-item[data-type="image"]').forEach(item => {
    item.addEventListener('click', () => {
      openLightbox(item.dataset.src, item.dataset.title || '');
    });
  });

  // ── YouTube modal ──
  document.querySelectorAll('.gallery-item[data-type="youtube"]').forEach(item => {
    item.addEventListener('click', () => {
      openVideoModal(item.dataset.embed);
    });
  });
});

// ══════════════════════════════════════════════
// ── Language change loader overlay ──
// ══════════════════════════════════════════════
function showLangLoader(lang) {
  // Remove any existing loader
  document.getElementById('rp-lang-loader')?.remove();

  const labels = {
    sw: { loading: 'Inabadilisha lugha...', flag: '🇹🇿', name: 'Kiswahili' },
    en: { loading: 'Switching language...', flag: '🇬🇧', name: 'English'   },
  };
  const { loading, flag, name } = labels[lang] || labels.en;

  const overlay = document.createElement('div');
  overlay.id    = 'rp-lang-loader';
  overlay.innerHTML = `
    <div class="rp-lang-loader-box">
      <div class="rp-lang-spinner"></div>
      <div class="rp-lang-flag">${flag}</div>
      <p class="rp-lang-name">${name}</p>
      <p class="rp-lang-label">${loading}</p>
      <div class="rp-lang-bar"><div class="rp-lang-bar-fill"></div></div>
    </div>
  `;

  // Inline styles — no dependency on external CSS
  overlay.style.cssText = `
    position: fixed;
    inset: 0;
    z-index: 99999;
    background: rgba(10, 26, 58, 0.82);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    display: flex;
    align-items: center;
    justify-content: center;
    animation: rpLangFadeIn 0.18s ease;
  `;

  const box = overlay.querySelector('.rp-lang-loader-box');
  box.style.cssText = `
    background: #ffffff;
    border-radius: 20px;
    padding: 2.2rem 2.8rem;
    text-align: center;
    box-shadow: 0 24px 64px rgba(0,0,0,0.35);
    min-width: 220px;
    animation: rpLangSlideUp 0.22s cubic-bezier(.22,.68,0,1.2);
  `;

  const spinner = overlay.querySelector('.rp-lang-spinner');
  spinner.style.cssText = `
    width: 44px;
    height: 44px;
    border: 4px solid #e8eef6;
    border-top-color: #0a1a3a;
    border-radius: 50%;
    margin: 0 auto 0.6rem;
    animation: rpLangSpin 0.7s linear infinite;
  `;

  const flagEl = overlay.querySelector('.rp-lang-flag');
  flagEl.style.cssText = `
    font-size: 2rem;
    line-height: 1;
    margin-bottom: 0.35rem;
    animation: rpLangPop 0.3s cubic-bezier(.22,.68,0,1.4) 0.1s both;
  `;

  const nameEl = overlay.querySelector('.rp-lang-name');
  nameEl.style.cssText = `
    font-size: 1.1rem;
    font-weight: 800;
    color: #0a1a3a;
    margin: 0 0 0.15rem;
    letter-spacing: 0.01em;
  `;

  const labelEl = overlay.querySelector('.rp-lang-label');
  labelEl.style.cssText = `
    font-size: 0.82rem;
    color: #6b7b96;
    margin: 0 0 1rem;
  `;

  const bar = overlay.querySelector('.rp-lang-bar');
  bar.style.cssText = `
    height: 4px;
    background: #e8eef6;
    border-radius: 4px;
    overflow: hidden;
  `;

  const fill = overlay.querySelector('.rp-lang-bar-fill');
  fill.style.cssText = `
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #0a1a3a, #c9a227);
    border-radius: 4px;
    animation: rpLangProgress 1.2s cubic-bezier(.4,0,.2,1) forwards;
  `;

  document.body.appendChild(overlay);
}

// ── Toast notification ──
function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  toast.style.cssText = `
    position:fixed; bottom:2rem; right:1rem; z-index:9999;
    background:${type === 'success' ? 'var(--navy)' : 'var(--danger)'};
    color:white; padding:0.85rem 1.4rem; border-radius:8px;
    font-size:0.9rem; font-weight:700; max-width:calc(100vw - 2rem);
    box-shadow:0 8px 32px rgba(0,0,0,0.25);
    animation:slideUp 0.3s ease;
    border-left:4px solid var(--gold);
  `;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = '0.4s';
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}

// ── Lightbox ──
function openLightbox(src, title) {
  const lb = document.createElement('div');
  lb.style.cssText = `position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:10000;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:1rem;cursor:zoom-out;padding:1rem;`;
  lb.innerHTML = `<img src="${src}" style="max-width:90vw;max-height:85vh;object-fit:contain;border-radius:8px;">
    <p style="color:rgba(255,255,255,0.8);font-size:0.88rem;text-align:center;">${title}</p>`;
  lb.addEventListener('click', () => lb.remove());
  document.body.appendChild(lb);
}

// ── Video Modal ──
function openVideoModal(embedUrl) {
  const modal = document.createElement('div');
  modal.style.cssText = `position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:10000;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:1rem;`;
  modal.innerHTML = `
    <div style="width:min(90vw,900px);aspect-ratio:16/9;cursor:default;" onclick="event.stopPropagation()">
      <iframe src="${embedUrl}?autoplay=1" style="width:100%;height:100%;border-radius:12px;border:none;"
        allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe>
    </div>
    <button style="position:absolute;top:1rem;right:1rem;background:rgba(255,255,255,0.15);border:none;color:white;font-size:1.6rem;width:40px;height:40px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;">&times;</button>
  `;
  modal.addEventListener('click', () => modal.remove());
  modal.querySelector('button').addEventListener('click', () => modal.remove());
  document.body.appendChild(modal);
}

// ── Get CSRF cookie ──
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    for (let cookie of document.cookie.split(';')) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// ── CSS animations (injected once) ──
const style = document.createElement('style');
style.textContent = `
  @keyframes slideUp       { from { transform:translateY(20px); opacity:0; } to { transform:translateY(0); opacity:1; } }
  @keyframes rpLangFadeIn  { from { opacity:0; } to { opacity:1; } }
  @keyframes rpLangSlideUp { from { transform:translateY(30px) scale(0.95); opacity:0; } to { transform:translateY(0) scale(1); opacity:1; } }
  @keyframes rpLangSpin    { to   { transform:rotate(360deg); } }
  @keyframes rpLangPop     { from { transform:scale(0.4); opacity:0; } to { transform:scale(1); opacity:1; } }
  @keyframes rpLangProgress{ 0%{width:0%} 40%{width:55%} 80%{width:85%} 100%{width:98%} }
`;
document.head.appendChild(style);