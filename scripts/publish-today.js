#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const SCHEDULE_PATH = 'src/data/schedule.json';
const PUBLISHED_PATH = 'src/data/published.json';
const DRAFTS_DIR = 'drafts';
const BLOG_DIR = 'src/pages/blog';

function main() {
  const schedule = JSON.parse(fs.readFileSync(SCHEDULE_PATH, 'utf8'));
  const next = schedule.find(item => !item.published);
  if (!next) {
    console.log('No hay más artículos programados.');
    return;
  }

  const draftFile = path.join(DRAFTS_DIR, `${String(next.day).padStart(2, '0')}-${next.slug}.astro`);
  if (!fs.existsSync(draftFile)) {
    console.error(`Draft no encontrado: ${draftFile}`);
    process.exit(1);
  }

  const destFile = path.join(BLOG_DIR, `${next.slug}.astro`);
  fs.copyFileSync(draftFile, destFile);
  console.log(`Copiado: ${draftFile} → ${destFile}`);

  const entry = {
    slug: next.slug,
    title: next.title,
    excerpt: next.excerpt || '',
    date: new Date().toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' }).replace('.', ''),
    readTime: next.readTime,
    category: next.category,
    views: 0
  };

  const published = JSON.parse(fs.readFileSync(PUBLISHED_PATH, 'utf8'));
  published.push(entry);
  fs.writeFileSync(PUBLISHED_PATH, JSON.stringify(published, null, 2));
  console.log(`Registrado en published.json: ${entry.slug}`);

  next.published = true;
  fs.writeFileSync(SCHEDULE_PATH, JSON.stringify(schedule, null, 2));
  console.log(`Marcado como publicado en schedule.json.`);

  const { execSync } = require('child_process');
  execSync(`git add ${destFile} ${PUBLISHED_PATH} ${SCHEDULE_PATH}`, { stdio: 'inherit' });
  execSync(`git commit -m "Publicar: ${entry.title}"`, { stdio: 'inherit' });
  execSync('git push', { stdio: 'inherit' });

  console.log(`\n✓ "${entry.title}" publicado y subido a GitHub. Cloudflare lo desplegará en breve.`);
}

main();
