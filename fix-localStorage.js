// Script to fix localStorage issues
console.log('=== FIXING LOCALSTORAGE ===');

// Clear all storage
localStorage.clear();
console.log('Cleared localStorage');

// Set user ID
const userId = 'debug-user-' + Date.now();
localStorage.setItem('ai-chat-user-id', userId);
console.log('Set user ID:', userId);

// Set MCP servers
const servers = [{
  id: 'MCP-UI-Demo',
  name: 'MCP-UI Demo', 
  url: 'https://remote-mcp-server-authless.idosalomon.workers.dev/sse',
  type: 'sse',
  isFixed: true,
  status: 'connected'
}];

localStorage.setItem('mcp-servers', JSON.stringify(servers));
console.log('Set MCP servers:', servers);

// Set selected servers
localStorage.setItem('selected-mcp-servers', '["MCP-UI-Demo"]');
console.log('Set selected servers: ["MCP-UI-Demo"]');

// Verify
console.log('=== VERIFICATION ===');
console.log('User ID:', localStorage.getItem('ai-chat-user-id'));
console.log('MCP servers:', JSON.parse(localStorage.getItem('mcp-servers') || '[]'));
console.log('Selected servers:', JSON.parse(localStorage.getItem('selected-mcp-servers') || '[]'));

console.log('localStorage fixed! Reload the page.');