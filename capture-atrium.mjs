#!/usr/bin/env node
// Capture Atrium landing page screenshots — hero viewport only
import puppeteer from 'puppeteer';
import { mkdirSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const outDir = resolve(__dirname, 'screenshots');
mkdirSync(outDir, { recursive: true });

const PORT = 9877;
const BASE = `http://localhost:${PORT}/2026-08-05-atrium-studio.html`;

async function capture() {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    // Desktop
    const desktopPage = await browser.newPage();
    await desktopPage.setViewport({ width: 1280, height: 800 });
    await desktopPage.goto(BASE, { waitUntil: 'networkidle0', timeout: 30000 });
    // Force light mode
    await desktopPage.evaluate(() => {
      localStorage.setItem('kairos-theme', 'light');
      document.documentElement.setAttribute('data-theme', 'light');
    });
    await desktopPage.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 2000));

    const desktopPath = resolve(outDir, 'atrium-desktop.png');
    await desktopPage.screenshot({ path: desktopPath, fullPage: false });
    const desktopStat = await desktopPage.evaluate(() => 1);
    console.log(`Desktop: ${desktopPath}`);

    // Mobile
    const mobilePage = await browser.newPage();
    await mobilePage.setViewport({ width: 390, height: 844 });
    await mobilePage.goto(BASE, { waitUntil: 'networkidle0', timeout: 30000 });
    await mobilePage.evaluate(() => {
      localStorage.setItem('kairos-theme', 'light');
      document.documentElement.setAttribute('data-theme', 'light');
    });
    await mobilePage.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 2000));

    const mobilePath = resolve(outDir, 'atrium-mobile.png');
    await mobilePage.screenshot({ path: mobilePath, fullPage: false });
    console.log(`Mobile: ${mobilePath}`);

    await browser.close();

    // Check file sizes
    const { statSync } = await import('fs');
    const dSize = statSync(desktopPath).size;
    const mSize = statSync(mobilePath).size;
    console.log(`Desktop size: ${(dSize / 1024).toFixed(1)}KB ${dSize > 50000 ? 'OK' : 'TOO SMALL'}`);
    console.log(`Mobile size: ${(mSize / 1024).toFixed(1)}KB ${mSize > 50000 ? 'OK' : 'TOO SMALL'}`);

  } catch (err) {
    console.error('Capture failed:', err.message);
    await browser.close();
    process.exit(1);
  }
}

capture();
