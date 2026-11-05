// 页面增强：学科配色、章节头部、二级标题编号徽章。
// 开启了 navigation.instant，切换页面时不会整页刷新，所以挂在 document$ 上，每次换页都重新执行。

// 一级目录名 → 学科标识，对应 components.css 中的 [data-subject] 配色。
const SUBJECTS = {
  "自然科学通识类": "science",
  "专业基础": "basic",
  "专业必修": "major",
  "金融学": "finance",
};

// 当前页面相对站点根目录的路径段，例如 ["金融学", "公司金融", "04-折现现金流估值"]。
function pathSegments() {
  const config = JSON.parse(document.getElementById("__config").textContent);
  const base = new URL(config.base, location.href).pathname;
  return decodeURIComponent(location.pathname.slice(base.length))
    .split("/")
    .filter(Boolean);
}

// 根据一级目录给 <body> 打上学科标记，CSS 据此切换强调色。
function applySubject(segments) {
  const subject = SUBJECTS[segments[0]];
  if (subject) document.body.dataset.subject = subject;
  else delete document.body.dataset.subject;
}

// 粗略估算阅读时间：中文约 400 字/分钟，英文约 200 词/分钟。
function readingMinutes(article) {
  const text = article.textContent;
  const cjk = (text.match(/[一-鿿]/g) || []).length;
  const words = (text.replace(/[一-鿿]/g, " ").match(/[A-Za-z]+/g) || []).length;
  return Math.max(1, Math.round(cjk / 400 + words / 200));
}

function chip(icon, label) {
  const el = document.createElement("span");
  el.className = "chapter-hero__chip";
  el.innerHTML = `<span class="chapter-hero__icon" data-icon="${icon}"></span>${label}`;
  return el;
}

// 把"第 N 章 标题"/"第 N 讲 标题"形式的 h1 升级为章节头部。
function buildChapterHero(article, segments) {
  const h1 = article.querySelector("h1");
  if (!h1 || h1.closest(".chapter-hero")) return;

  const textNode = [...h1.childNodes].find((n) => n.nodeType === Node.TEXT_NODE && n.textContent.trim());
  const match = textNode && textNode.textContent.trim().match(/^第\s*(\d+)\s*([章讲])\s*(.+)$/);
  if (!match) return;
  const [, num, unit, title] = match;

  const hero = document.createElement("header");
  hero.className = "chapter-hero";

  const number = document.createElement("div");
  number.className = "chapter-hero__num";
  number.textContent = num.padStart(2, "0");

  const body = document.createElement("div");
  body.className = "chapter-hero__body";

  const crumb = document.createElement("div");
  crumb.className = "chapter-hero__crumb";
  crumb.textContent = [segments[0], segments[1], `第 ${num} ${unit}`].filter(Boolean).join(" · ");

  const meta = document.createElement("div");
  meta.className = "chapter-hero__meta";
  meta.append(chip("clock", `约 ${readingMinutes(article)} 分钟`));
  const counts = [
    ["formula", article.querySelectorAll("div.arithmatex").length, "个公式"],
    ["warning", article.querySelectorAll(".admonition.warning, details.warning").length, "处易错"],
    ["example", article.querySelectorAll(".admonition.example, details.example").length, "道例题"],
  ];
  for (const [icon, n, label] of counts) {
    if (n > 0) meta.append(chip(icon, `${n} ${label}`));
  }

  // 替换前先把 h1 放进头部，再把标题文字去掉"第 N 章"前缀。
  h1.replaceWith(hero);
  textNode.textContent = title;
  body.append(crumb, h1);

  // 公司金融等笔记在 h1 后紧跟一行英文副标题，一并收进头部。
  const subtitle = hero.nextElementSibling;
  if (subtitle && subtitle.classList.contains("cf-subtitle")) body.append(subtitle);

  body.append(meta);
  hero.append(number, body);
}

// 把二级标题开头的"4.1"之类的编号包进徽章。
function badgeHeadingNumbers(article) {
  for (const h2 of article.querySelectorAll("h2")) {
    if (h2.querySelector(".h2-num")) continue;
    const first = h2.firstChild;
    if (!first || first.nodeType !== Node.TEXT_NODE) continue;
    const match = first.textContent.match(/^\s*(\d+(?:\.\d+)*)\s+/);
    if (!match) continue;
    const badge = document.createElement("span");
    badge.className = "h2-num";
    badge.textContent = match[1];
    first.textContent = first.textContent.slice(match[0].length);
    h2.insertBefore(badge, first);
  }
}

document$.subscribe(function () {
  const segments = pathSegments();
  applySubject(segments);

  const article = document.querySelector(".md-content__inner");
  if (!article) return;
  buildChapterHero(article, segments);
  badgeHeadingNumbers(article);
});
