import { readFileSync } from 'fs';

try {
  const pkg = JSON.parse(readFileSync('./package.json', 'utf8'));
  console.log('Dependencies:', Object.keys(pkg.dependencies || {}));
  console.log('DevDependencies:', Object.keys(pkg.devDependencies || {}));
  console.log('\nChecking main files...');
  
  const files = ['src/main.tsx', 'src/App.tsx', 'src/index.css', 'index.html'];
  files.forEach(f => {
    try {
      readFileSync(f, 'utf8');
      console.log(`✓ ${f}`);
    } catch(e) {
      console.log(`✗ ${f} - ${e.message}`);
    }
  });
} catch(e) {
  console.error('Error:', e.message);
}
