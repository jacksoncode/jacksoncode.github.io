#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const DEFAULT_INPUT_DIR = __dirname;
const DEFAULT_OUTPUT_DIR = path.join(__dirname, 'build');

const CHAPTERS = [
  'index.html', 'index-full.html',
  'ch00.html', 'ch01.html', 'ch02.html', 'ch02b.html', 'ch03.html',
  'ch04.html', 'ch05.html', 'ch06.html', 'ch07.html', 'ch08.html',
  'ch09.html', 'ch10.html', 'ch11.html', 'ch12.html', 'ch13.html',
  'ch14.html', 'ch15.html', 'ch16.html', 'ch17.html', 'ch18.html',
  'ch19.html', 'ch20.html', 'ch21.html', 'ch22.html', 'ch23.html',
  'ch24.html', 'ch25.html', 'ch26.html',
  'appendix-a.html', 'appendix-b.html', 'appendix-c.html',
  'appendix-d.html', 'appendix-e.html', 'appendix-f.html'
];

function parseArgs() {
  const args = process.argv.slice(2);
  let inputDir = DEFAULT_INPUT_DIR;
  let outputDir = DEFAULT_OUTPUT_DIR;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--input-dir' && args[i+1]) inputDir = path.resolve(args[i+1]);
    if (args[i] === '--output-dir' && args[i+1]) outputDir = path.resolve(args[i+1]);
  }
  return { inputDir, outputDir };
}

function copyDirRecursive(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function extractMeta(html) {
  const titleMatch = html.match(/<title>(.*?)<\/title>/s);
  const descMatch = html.match(/<meta\s+name="description"\s+content="(.*?)"/s) || 
                    html.match(/<meta\s+content="(.*?)"\s+name="description"/s);
  const keywordsMatch = html.match(/<meta\s+name="keywords"\s+content="(.*?)"/s) ||
                        html.match(/<meta\s+content="(.*?)"\s+name="keywords"/s);
  return {
    title: titleMatch ? titleMatch[1].trim() : 'AI学习笔记',
    description: descMatch ? descMatch[1].trim() : '',
    keywords: keywordsMatch ? keywordsMatch[1].trim() : ''
  };
}

function extractChapterId(html, filename) {
  const idMatch = html.match(/var chapterId\s*=\s*['"]([\w-]+)['"]/);
  if (idMatch) return idMatch[1];
  const name = filename.replace('.html', '');
  return name === 'index' ? 'index' : name;
}

function extractTOC(html) {
  const tocMatch = html.match(/<div class="toc"[^>]*>([\s\S]*?)<\/div>/) ||
                   html.match(/<div class="chapter-toc"[^>]*>([\s\S]*?)<\/div>/);
  if (tocMatch) return tocMatch[1];
  const sidebarMatch = html.match(/<aside[^>]*class="[^"]*sidebar[^"]*"[^>]*>([\s\S]*?)<\/aside>/);
  if (sidebarMatch) {
    const tocContent = sidebarMatch[1].match(/<ul>([\s\S]*?)<\/ul>/);
    if (tocContent) return tocContent[0];
  }
  return '';
}

function extractMainContent(html) {
  const mainMatch = html.match(/<main[^>]*>([\s\S]*?)<\/main>/);
  if (!mainMatch) return '';
  let content = mainMatch[1];
  content = content.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');
  return content.trim();
}

function extractChapterNav(html) {
  const navMatch = html.match(/<div class="chapter-nav"[\s\S]*?<\/div>/) ||
                   html.match(/<nav class="[^"]*chapter[^"]*nav[^"]*"[\s\S]*?<\/nav>/);
  return navMatch ? navMatch[0] : '';
}

function extractFooter(html) {
  const footerMatch = html.match(/<footer[\s\S]*?<\/footer>/);
  return footerMatch ? footerMatch[0] : '';
}

function generateNewHead(meta, filename) {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="${meta.description}">
    <meta name="keywords" content="${meta.keywords}">
    <title>${meta.title}</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="assets/vendor/font-awesome/css/all.min.css">
    <link rel="stylesheet" href="assets/ai-notes.css">
    <link rel="stylesheet" href="css/${filename.replace('.html', '.css')}" onerror="this.remove()">
    
    <link rel="stylesheet" href="assets/vendor/katex/katex.min.css">
    <script defer src="assets/vendor/katex/katex.min.js"></script>
    <script defer src="assets/vendor/katex/auto-render.min.js"></script>
    
    <link rel="stylesheet" href="assets/vendor/prismjs/prism-tomorrow.min.css">
    <script src="assets/vendor/prismjs/prism.min.js"></script>
    <script src="assets/vendor/prismjs/prism-python.min.js"></script>
    <script src="assets/vendor/prismjs/prism-bash.min.js"></script>
    <script src="assets/vendor/prismjs/prism-json.min.js"></script>
    <script src="assets/vendor/prismjs/prism-yaml.min.js"></script>
    
    <link rel="manifest" href="assets/manifest.json">
    <meta name="theme-color" content="#4299e1">
    
    <script src="assets/ai-notes.js" defer></script>
    <script>
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('assets/sw.js').catch(() => {});
      }
    </script>
</head>
<body>`;
}

function generateNav() {
  return `
<nav class="navbar">
  <a href="index.html" class="navbar-brand"><i class="fas fa-robot"></i> AI学习笔记</a>
  <ul class="navbar-links">
    <li><a href="index.html"><i class="fas fa-home"></i> 首页</a></li>
    <li><a href="https://github.com/jacksoncode" target="_blank"><i class="fab fa-github"></i> GitHub</a></li>
  </ul>
  <button class="navbar-toggle"><i class="fas fa-bars"></i></button>
</nav>`;
}

function extractHero(html) {
  const heroMatch = html.match(/<section class="hero"[\s\S]*?<\/section>/) ||
                    html.match(/<section class="[^"]*hero[^"]*"[\s\S]*?<\/section>/);
  return heroMatch ? heroMatch[0] : '';
}

function generateCompleteButton(chapterId) {
  return `
<div class="complete-btn" data-chapter-id="${chapterId}">
  <i class="far fa-circle"></i> 标记为已完成
</div>`;
}

function generateMobileTOC(tocHtml) {
  if (!tocHtml) return '';
  return `
<div class="mobile-toc-overlay"></div>
<div class="mobile-toc">
  <button class="mobile-toc-close"><i class="fas fa-times"></i></button>
  <h3><i class="fas fa-list-ul"></i> 目录</h3>
  ${tocHtml}
</div>
<button class="mobile-toc-toggle" aria-label="打开目录"><i class="fas fa-list-ul"></i></button>`;
}

function transformContentClasses(content) {
  content = content.replace(/class="learning-objectives"/g, 'class="ai-box ai-box--objectives"');
  content = content.replace(/class="prerequisite-box"/g, 'class="ai-box ai-box--prereq"');
  content = content.replace(/class="exercise-box"/g, 'class="ai-box ai-box--exercise"');
  content = content.replace(/class="summary-box"/g, 'class="ai-box ai-box--summary"');
  content = content.replace(/class="tip-box"/g, 'class="ai-tip"');
  content = content.replace(/class="warning-box"/g, 'class="ai-warning"');
  content = content.replace(/class="success-box"/g, 'class="ai-success"');
  content = content.replace(/class="info-box"/g, 'class="ai-info"');
  content = content.replace(/class="code-block"/g, 'class="ai-code"');
  content = content.replace(/class="code-block-header"/g, 'class="ai-code-header"');
  content = content.replace(/class="section-title"/g, 'class="ai-section-title"');
  content = content.replace(/class="section-subtitle"/g, 'class="ai-section-subtitle"');
  content = content.replace(/class="chapter-nav"/g, 'class="ai-chapter-nav"');
  content = content.replace(/class="footer"/g, 'class="ai-footer"');
  content = content.replace(/class="navbar"/g, 'class="ai-nav"');
  content = content.replace(/class="navbar-brand"/g, 'class="ai-nav-brand"');
  content = content.replace(/class="navbar-links"/g, 'class="ai-nav-links"');
  content = content.replace(/class="navbar-toggle"/g, 'class="ai-nav-toggle"');
  content = content.replace(/class="exercise-item"/g, 'class="ai-exercise-item"');
  content = content.replace(/class="exercise-number"/g, 'class="num"');
  content = content.replace(/class="copy-btn" onclick="copyCode\(this\)"/g, 'class="copy-btn"');
  return content;
}

function buildChapter(inputDir, outputDir, filename) {
  const inputPath = path.join(inputDir, filename);
  if (!fs.existsSync(inputPath)) {
    console.log(`  ⚠️  跳过不存在: ${filename}`);
    return false;
  }

  const html = fs.readFileSync(inputPath, 'utf8');
  const meta = extractMeta(html);
  const chapterId = extractChapterId(html, filename);
  const tocHtml = extractTOC(html);
  let mainContent = extractMainContent(html);
  const chapterNav = extractChapterNav(html);
  const footer = extractFooter(html);
  const heroHtml = extractHero(html);

  mainContent = transformContentClasses(mainContent);

  let newHtml = generateNewHead(meta, filename);
  newHtml += generateNav();

  if (heroHtml) {
    newHtml += '\n' + heroHtml;
  }

  newHtml += `\n<div class="ai-content-wrapper">`;
  newHtml += `\n<main class="ai-main">`;
  newHtml += mainContent;

  if (filename !== 'index.html' && filename !== 'index-full.html') {
    newHtml += generateCompleteButton(chapterId);
  }

  newHtml += `\n</main>`;

  if (filename !== 'index.html' && filename !== 'index-full.html' && tocHtml) {
    newHtml += `\n<aside class="ai-toc">`;
    newHtml += `<h3><i class="fas fa-list-ul"></i> 目录</h3>`;
    newHtml += `<ul class="toc-list">${tocHtml}</ul>`;
    newHtml += `\n</aside>`;
  }

  newHtml += `\n</div>`;

  if (filename !== 'index.html' && filename !== 'index-full.html') {
    newHtml += generateMobileTOC(tocHtml);
  }

  if (chapterNav) {
    newHtml += '\n' + transformContentClasses(chapterNav);
  }

  if (footer) {
    newHtml += '\n' + transformContentClasses(footer);
  }

  newHtml += `\n</body>\n</html>`;

  const outputPath = path.join(outputDir, filename);
  fs.writeFileSync(outputPath, newHtml, 'utf8');
  return true;
}

function main() {
  const { inputDir, outputDir } = parseArgs();
  
  console.log('🔨 AI学习笔记构建脚本\n');
  console.log(`  输入: ${inputDir}`);
  console.log(`  输出: ${outputDir}\n`);

  fs.mkdirSync(outputDir, { recursive: true });
  fs.mkdirSync(path.join(outputDir, 'assets'), { recursive: true });

  const assetsDir = path.join(inputDir, 'assets');
  if (fs.existsSync(path.join(assetsDir, 'ai-notes.css'))) {
    fs.copyFileSync(path.join(assetsDir, 'ai-notes.css'), path.join(outputDir, 'assets', 'ai-notes.css'));
  }
  if (fs.existsSync(path.join(assetsDir, 'ai-notes.js'))) {
    fs.copyFileSync(path.join(assetsDir, 'ai-notes.js'), path.join(outputDir, 'assets', 'ai-notes.js'));
  }
  if (fs.existsSync(path.join(assetsDir, 'manifest.json'))) {
    fs.copyFileSync(path.join(assetsDir, 'manifest.json'), path.join(outputDir, 'assets', 'manifest.json'));
  }
  if (fs.existsSync(path.join(assetsDir, 'sw.js'))) {
    fs.copyFileSync(path.join(assetsDir, 'sw.js'), path.join(outputDir, 'assets', 'sw.js'));
  }
  
  const vendorDir = path.join(assetsDir, 'vendor');
  if (fs.existsSync(vendorDir)) {
    copyDirRecursive(vendorDir, path.join(outputDir, 'assets', 'vendor'));
  }
  
  console.log('📦 构建章节...\n');
  let successCount = 0;

  for (const chapter of CHAPTERS) {
    const result = buildChapter(inputDir, outputDir, chapter);
    if (result) {
      successCount++;
      console.log(`  ✅ ${chapter}`);
    }
  }

  console.log(`\n✨ 完成! ${successCount} 个文件 → ${outputDir}\n`);
}

main();
