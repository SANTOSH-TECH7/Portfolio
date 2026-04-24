// ── AOS ───────────────────────────────────────────────────────
AOS.init({ duration: 700, once: true, offset: 80 });

// ── SCROLL PROGRESS BAR ───────────────────────────────────────
window.addEventListener('scroll', () => {
  const bar = document.getElementById('scroll-progress');
  if (bar) {
    const pct = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
    bar.style.width = pct + '%';
  }
});

// ── CUSTOM CURSOR ─────────────────────────────────────────────
const cursor    = document.querySelector('.cursor');
const cursorDot = document.querySelector('.cursor-dot');
if (cursor && typeof gsap !== 'undefined') {
  document.addEventListener('mousemove', e => {
    gsap.to(cursor,    { x: e.clientX, y: e.clientY, duration: 0.15 });
    gsap.to(cursorDot, { x: e.clientX, y: e.clientY, duration: 0.08 });
  });
}

// ── PARTICLES ─────────────────────────────────────────────────
if (document.getElementById('particles-js')) {
  particlesJS('particles-js', {
    particles: {
      number: { value: 70, density: { enable: true, value_area: 800 } },
      color: { value: '#2563eb' },
      shape: { type: 'circle' },
      opacity: { value: 0.45, random: true },
      size: { value: 2.5, random: true },
      line_linked: { enable: true, distance: 140, color: '#2563eb', opacity: 0.3, width: 1 },
      move: { enable: true, speed: 1.8, direction: 'none', random: true, out_mode: 'out' }
    },
    interactivity: {
      detect_on: 'canvas',
      events: {
        onhover: { enable: true, mode: 'grab' },
        onclick: { enable: true, mode: 'push' }
      },
      modes: {
        grab: { distance: 160, line_linked: { opacity: 0.6 } },
        push: { particles_nb: 3 }
      }
    },
    retina_detect: true
  });
}

// ── THREE.JS HERO SPHERE ──────────────────────────────────────
(function initHero() {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas || typeof THREE === 'undefined') return;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 30;
  const sphere = new THREE.Mesh(
    new THREE.SphereGeometry(10, 32, 32),
    new THREE.MeshBasicMaterial({ color: 0x2563eb, wireframe: true, transparent: true, opacity: 0.25 })
  );
  scene.add(sphere);
  const smalls = [];
  for (let i = 0; i < 18; i++) {
    const sm = new THREE.Mesh(
      new THREE.SphereGeometry(Math.random() * 0.5 + 0.2, 12, 12),
      new THREE.MeshBasicMaterial({ color: 0x7e22ce, transparent: true, opacity: 0.6 })
    );
    const a1 = Math.random() * Math.PI * 2, a2 = Math.random() * Math.PI * 2;
    const d  = Math.random() * 10 + 10;
    sm.position.set(Math.cos(a1)*Math.sin(a2)*d, Math.sin(a1)*Math.sin(a2)*d, Math.cos(a2)*d);
    sm.userData.v = { x:(Math.random()-0.5)*0.05, y:(Math.random()-0.5)*0.05, z:(Math.random()-0.5)*0.05 };
    scene.add(sm); smalls.push(sm);
  }
  function animate() {
    requestAnimationFrame(animate);
    sphere.rotation.x += 0.004; sphere.rotation.y += 0.004;
    smalls.forEach(s => {
      s.position.x += s.userData.v.x;
      s.position.y += s.userData.v.y;
      s.position.z += s.userData.v.z;
      ['x','y','z'].forEach(ax => { if (Math.abs(s.position[ax]) > 15) s.userData.v[ax] *= -1; });
    });
    renderer.render(scene, camera);
  }
  animate();
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
})();

// ── THREE.JS SECTION DIVIDERS (color-shifting) ────────────────
document.querySelectorAll('.divider-canvas').forEach(canvas => {
  if (typeof THREE === 'undefined') return;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
  camera.position.z = 5;
  const geo = new THREE.PlaneGeometry(10, 2, 50, 10);
  const mat = new THREE.MeshBasicMaterial({ color: 0x00d4ff, wireframe: true, transparent: true, opacity: 0.4 });
  const plane = new THREE.Mesh(geo, mat);
  scene.add(plane);
  (function animDiv() {
    requestAnimationFrame(animDiv);
    const pos  = geo.attributes.position.array;
    const time = Date.now() * 0.001;
    for (let i = 0; i < pos.length; i += 3) pos[i+2] = Math.sin(pos[i]*2 + time) * 0.3;
    geo.attributes.position.needsUpdate = true;
    // shift hue: blue → purple over time
    const hue = (Math.sin(time * 0.3) * 0.5 + 0.5); // 0..1
    const r = Math.round(hue * 191);
    const b = Math.round((1 - hue) * 255 + hue * 255);
    const g = 0;
    mat.color.setRGB(r / 255, g / 255, b / 255);
    renderer.render(scene, camera);
  })();
});

// ── TYPED.JS ROLE ANIMATION ───────────────────────────────────
if (document.getElementById('typed-role') && typeof Typed !== 'undefined') {
  new Typed('#typed-role', {
    strings: ['AI & Data Science Engineer', 'Machine Learning Developer', 'Full Stack Developer', 'Automation Engineer'],
    typeSpeed: 55, backSpeed: 30, loop: true, backDelay: 1800
  });
}

// ── SKILL BAR ANIMATION (star schema nodes) ───────────────────
const skillsSection = document.getElementById('skills');
if (skillsSection) {
  new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      // legacy bars (if any)
      document.querySelectorAll('.skill-progress').forEach(bar => {
        bar.style.width = bar.getAttribute('data-width') + '%';
      });
      // star schema: staggered spoke reveal + node fill
      document.querySelectorAll('.star-schema-wrap').forEach(wrap => {
        const spokes = wrap.querySelectorAll('.star-spoke-item');
        spokes.forEach((spoke, i) => {
          setTimeout(() => spoke.classList.add('spoke-visible'), i * 120);
        });
        setTimeout(() => {
          wrap.querySelectorAll('.star-node-fill').forEach(fill => {
            fill.style.width = fill.getAttribute('data-width') + '%';
          });
        }, spokes.length * 120 + 200);
      });
    });
  }, { threshold: 0.15 }).observe(skillsSection);
}

// ── EDUCATION: connector draw-in + node power-on ──────────────
const eduSection = document.getElementById('education');
if (eduSection) {
  new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      // draw connector lines
      eduSection.querySelectorAll('.edu-connector-line').forEach((line, i) => {
        setTimeout(() => line.classList.add('drawn'), i * 400 + 300);
      });
      // power-on flicker for each node
      eduSection.querySelectorAll('.edu-node').forEach((node, i) => {
        setTimeout(() => node.classList.add('powered-on'), i * 350);
      });
    });
  }, { threshold: 0.2 }).observe(eduSection);
}

// ── ACTIVE NAV HIGHLIGHT ──────────────────────────────────────
const sections = document.querySelectorAll('section[id]');
const navLinks  = document.querySelectorAll('.nav-link-item');
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(sec => { if (window.scrollY >= sec.offsetTop - 130) current = sec.id; });
  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('data-section') === current) link.classList.add('active');
  });
  const nav = document.getElementById('mainNav');
  if (nav) nav.style.boxShadow = window.scrollY > 50 ? '0 4px 24px rgba(0,0,0,0.5)' : 'none';
});

// ── PROJECT FILTER TABS ───────────────────────────────────────
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.getAttribute('data-filter');
    document.querySelectorAll('.project-item').forEach(card => {
      const cat = card.getAttribute('data-category') || '';
      card.style.display = (filter === 'all' || cat.toLowerCase().includes(filter.toLowerCase())) ? '' : 'none';
    });
  });
});

// ── DARK / LIGHT MODE ─────────────────────────────────────────
const themeBtn = document.getElementById('theme-toggle');
if (themeBtn) {
  const saved = localStorage.getItem('theme');
  if (saved === 'light') document.body.classList.add('light-mode');
  themeBtn.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    localStorage.setItem('theme', document.body.classList.contains('light-mode') ? 'light' : 'dark');
    themeBtn.innerHTML = document.body.classList.contains('light-mode')
      ? '<i class="fas fa-moon"></i>' : '<i class="fas fa-sun"></i>';
  });
}
