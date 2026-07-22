const fs = require('fs');

const message = `
[PoC] This file was created automatically by a 'postinstall' script.
Package: expresss
Timestamp: ${new Date().toISOString()}
This demonstrates how a malicious package could execute code silently during 'npm install'.
No harm done — this is a controlled security research demo.
`;

fs.writeFileSync('PROOF_OF_CONCEPT.txt', message);
console.log('[expresss] postinstall script executed — see PROOF_OF_CONCEPT.txt');