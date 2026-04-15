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
    btn.addEventListener('click', () => {
      const lang = btn.dataset.lang;

      // Update active state immediately for visual feedback
      document.querySelectorAll('[data-lang]').forEach(b => b.classList.remove('active'));
      document.querySelectorAll(`[data-lang="${lang}"]`).forEach(b => b.classList.add('active'));

      // Use the existing Django-rendered form (has real CSRF token)
      const form = document.getElementById('django-lang-form');

      // Inject or update language input
      let langInput = form.querySelector('input[name="language"]');
      if (!langInput) {
        langInput = document.createElement('input');
        langInput.type = 'hidden';
        langInput.name = 'language';
        form.appendChild(langInput);
      }
      langInput.value = lang;

      // Inject or update next input
      let nextInput = form.querySelector('input[name="next"]');
      if (!nextInput) {
        nextInput = document.createElement('input');
        nextInput.type = 'hidden';
        nextInput.name = 'next';
        form.appendChild(nextInput);
      }
      nextInput.value = window.location.pathname + window.location.search;

      form.submit();
    });
  });

  // ── Add to cart (AJAX) ──
  document.querySelectorAll('.ajax-add-cart').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const productId = btn.dataset.productId;
      const qty = document.querySelector(`#qty-${productId}`)?.value || 1;
      try {
        const res = await fetch(`/orders/cart/add/${productId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: `quantity=${qty}`,
        });
        const data = await res.json();
        const badge = document.querySelector('.cart-badge');
        if (badge) {
          badge.textContent = data.cart_count;
          badge.style.transform = 'scale(1.4)';
          setTimeout(() => badge.style.transform = '', 300);
        }
        showToast('Added to cart! 🛒', 'success');
        btn.textContent = 'Added ✓';
        btn.style.background = 'var(--success)';
        setTimeout(() => {
          btn.textContent = 'Add to Cart';
          btn.style.background = '';
        }, 2000);
      } catch (err) {
        showToast('Something went wrong. Try again.', 'error');
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

// ── CSS animations ──
const style = document.createElement('style');
style.textContent = `
  @keyframes slideUp { from { transform: translateY(20px); opacity:0; } to { transform: translateY(0); opacity:1; } }
`;
document.head.appendChild(style);
