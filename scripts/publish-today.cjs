#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SCHEDULE_PATH = 'src/data/schedule.json';
const PUBLISHED_PATH = 'src/data/published.json';
const DRAFTS_DIR = 'drafts';
const BLOG_DIR = 'src/pages/blog';

function main() {
  if (!fs.existsSync(SCHEDULE_PATH)) {
    console.error(`ERROR: No se encuentra ${SCHEDULE_PATH}`);
    process.exit(1);
  }

  const schedule = JSON.parse(fs.readFileSync(SCHEDULE_PATH, 'utf8'));
  const next = schedule.find(item => !item.published);

  if (!next) {
    console.log('No hay más artículos programados.');
    process.exit(0);
  }

  const dayPadded = String(next.day).padStart(2, '0');
  const draftFile = path.join(DRAFTS_DIR, `${dayPadded}-${next.slug}.astro`);
  const destFile = path.join(BLOG_DIR, `${next.slug}.astro`);

  if (!fs.existsSync(draftFile)) {
    console.error(`ERROR: Draft no encontrado: ${draftFile}`);
    process.exit(1);
  }

  if (fs.existsSync(destFile)) {
    console.log(`El artículo ya existe en blog/: ${destFile}`);
    console.log('Se sobrescribirá con la versión del draft.');
  }

  fs.copyFileSync(draftFile, destFile);
  console.log(`Copiado: ${draftFile} → ${destFile}`);

  const published = JSON.parse(fs.readFileSync(PUBLISHED_PATH, 'utf8'));
  const exists = published.some(e => e.slug === next.slug);
  if (exists) {
    console.log(`El slug ya existe en published.json, se actualizará la entrada.`);
  }

  const entry = {
    slug: next.slug,
    title: next.title,
    excerpt: next.excerpt || '',
    date: new Date().toLocaleDateString('es-ES', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    }).replace('.', ''),
    readTime: next.readTime,
    category: next.category,
    views: 0
  };

  if (exists) {
    const idx = published.findIndex(e => e.slug === next.slug);
    published[idx] = { ...published[idx], ...entry };
  } else {
    published.push(entry);
  }

  fs.writeFileSync(PUBLISHED_PATH, JSON.stringify(published, null, 2));
  console.log(`Registrado en published.json: ${entry.slug}`);

  next.published = true;
  fs.writeFileSync(SCHEDULE_PATH, JSON.stringify(schedule, null, 2));
  console.log(`Marcado como publicado en schedule.json.`);

  try {
    execSync(`git add "${destFile}" "${PUBLISHED_PATH}" "${SCHEDULE_PATH}"`, { stdio: 'inherit' });

    const hasChanges = execSync('git diff --cached --stat', { encoding: 'utf8' }).trim();
    if (!hasChanges) {
      console.log('No hay cambios nuevos. El artículo ya fue publicado.');
      process.exit(0);
    }
    console.log('Cambios a commitear:\n' + hasChanges);

    execSync(`git commit -m "Publicar: ${entry.title}"`, { stdio: 'inherit' });

    execSync('git pull --rebase origin main 2>/dev/null; true', { stdio: 'ignore' });
    execSync('git push', { stdio: 'inherit' });

    console.log(`\n✓ "${entry.title}" publicado y subido a GitHub.`);
  } catch (err) {
    console.error('\n✗ Error en git push:', err.message);
    console.log('Los archivos fueron modificados localmente pero no se pudieron subir.');
    process.exit(1);
  }
}

main();
