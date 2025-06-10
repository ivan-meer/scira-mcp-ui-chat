"use client";

import { useEffect } from 'react';

interface MCPServer {
  id: string;
  name: string;
  url: string;
  type: string;
  isFixed: boolean;
  status: string;
}

export function LocalStorageFix() {
  useEffect(() => {
    if (typeof window === 'undefined') return;
    
    console.log('=== LOCALSTORAGE FIX COMPONENT RUNNING ===');
    
    // Check if localStorage needs fixing
    const userId = localStorage.getItem('ai-chat-user-id');
    const selectedServers = localStorage.getItem('selected-mcp-servers');
    const mcpServers = localStorage.getItem('mcp-servers');
    
    console.log('Current localStorage state:');
    console.log('userId:', userId);
    console.log('selectedServers:', selectedServers);
    console.log('mcpServers:', mcpServers);
    
    let needsReload = false;
    
    // Set user ID if missing
    if (!userId) {
      const newUserId = 'user-' + Date.now();
      localStorage.setItem('ai-chat-user-id', newUserId);
      console.log('Set user ID:', newUserId);
      needsReload = true;
    }
    
    // Ensure demo MCP server exists in servers list
    let currentServers: MCPServer[] = [];
    try {
      if (mcpServers) {
        currentServers = JSON.parse(mcpServers);
      }
    } catch (e) {
      console.log('Error parsing existing servers, will reset');
    }
    
    const demoServer: MCPServer = {
      id: 'MCP-UI-Demo',
      name: 'MCP-UI Demo', 
      url: 'https://remote-mcp-server-authless.idosalomon.workers.dev/sse',
      type: 'sse',
      isFixed: true,
      status: 'connected'
    };
    
    // Add demo server if not present
    const hasDemoServer = currentServers.some((server: MCPServer) => server.id === 'MCP-UI-Demo');
    if (!hasDemoServer) {
      currentServers.push(demoServer);
      localStorage.setItem('mcp-servers', JSON.stringify(currentServers));
      console.log('Added demo MCP server to servers list');
      needsReload = true;
    }
    
    // Add local demo server
    const localDemoServer: MCPServer = {
      id: 'Local-Demo-UI-Generator',
      name: 'Demo UI Generator Server',
      url: 'http://localhost:8813/sse',
      type: 'sse',
      isFixed: false,
      status: 'disconnected'
    };
    
    const hasLocalServer = currentServers.some((server: MCPServer) => server.id === 'Local-Demo-UI-Generator');
    if (!hasLocalServer) {
      currentServers.push(localDemoServer);
      localStorage.setItem('mcp-servers', JSON.stringify(currentServers));
      console.log('Added local demo server to servers list');
      needsReload = true;
    }
    
    // Set selected servers if missing or empty
    let currentSelected: string[] = [];
    try {
      if (selectedServers) {
        currentSelected = JSON.parse(selectedServers);
      }
    } catch (e) {
      console.log('Error parsing selected servers, will reset');
    }
    
    if (!selectedServers || selectedServers === '[]' || currentSelected.length === 0) {
      const newSelected = ['MCP-UI-Demo'];
      localStorage.setItem('selected-mcp-servers', JSON.stringify(newSelected));
      console.log('Set selected MCP servers:', newSelected);
      needsReload = true;
    }
    
    // Only reload if we made changes
    if (needsReload) {
      console.log('=== RELOADING PAGE TO APPLY CHANGES ===');
      setTimeout(() => {
        window.location.reload();
      }, 100);
    } else {
      console.log('localStorage is already properly configured');
    }
  }, []);
  
  return null;
}