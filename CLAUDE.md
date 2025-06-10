# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Core Commands
- `pnpm dev` - Start development server with turbopack
- `pnpm build` - Build production bundle with turbopack  
- `pnpm lint` - Run ESLint checks
- `pnpm start` - Start production server

### Database Commands
- `pnpm db:generate` - Generate Drizzle schema migrations
- `pnpm db:migrate` - Run database migrations
- `pnpm db:push` - Push schema changes to database
- `pnpm db:studio` - Open Drizzle Studio for database management

## Architecture Overview

This is a Next.js 15 application that creates an MCP-UI playground for experimenting with Model Context Protocol (MCP) servers. The application enables chat interfaces that can render UI components from MCP tool responses.

### Key Technologies
- **Next.js 15** with App Router and React 19
- **AI SDK by Vercel** for multi-provider AI chat streaming 
- **MCP-UI Client/Server** (`@mcp-ui/client`, `@mcp-ui/server`) for tool UI rendering
- **Drizzle ORM** with PostgreSQL for persistence
- **shadcn/ui** components with Tailwind CSS
- **Radix UI** primitives for complex components

### Core Architecture

**MCP Integration Flow:**
1. MCP servers are configured in `lib/context/mcp-context.tsx` with two transport types:
   - SSE (Server-Sent Events) for remote HTTP servers
   - stdio for local command-line servers (converted to SSE via sandbox)
2. stdio servers are wrapped in sandboxes (`lib/mcp-sandbox.ts`, `app/actions.ts`) that expose them as SSE endpoints
3. All MCP clients communicate via SSE in the API layer (`lib/mcp-client.ts`)
4. Chat API (`app/api/chat/route.ts`) initializes MCP clients and merges their tools for AI SDK

**Data Flow:**
- Chat state managed via React Context (`lib/chat-store.ts`) 
- Messages stored in PostgreSQL with JSON parts structure (`lib/db/schema.ts`)
- UI state persisted in localStorage for MCP server configs and selections
- AI responses stream through AI SDK with tool invocations rendered as UI components

**Key Components:**
- `components/chat.tsx` - Main chat interface with message streaming
- `components/mcp-server-manager.tsx` - Configure and manage MCP servers
- `components/tool-invocation.tsx` - Renders MCP tool results as UI
- `lib/context/mcp-context.tsx` - MCP server lifecycle and configuration management

### Database Schema
Messages use a flexible JSON parts structure to handle different content types (text, tool calls, attachments). Each message references a chat and user via foreign keys with cascade deletion.

### Environment Requirements
- `DATABASE_URL` - PostgreSQL connection string for Drizzle ORM
- AI provider API keys for chat functionality (configured in `ai/providers.ts`)
- `DAYTONA_API_KEY` - Required for stdio MCP servers (sandbox execution)

### Recent Fixes Applied
- **MCP Server Visibility**: Fixed reactivity in `mcpServersForApi` using `useMemo`
- **Chat Saving**: Added `onFinish` callback in chat API to save conversations
- **Database Driver**: Changed from Neon to PostgreSQL driver in `lib/db/index.ts`
- **Chat History**: Enabled loading of chat history with proper message conversion

### Troubleshooting
- See `/docs/troubleshooting/` for comprehensive debugging guides
- Common issues and solutions documented in `/docs/troubleshooting/common-issues.md`
- MCP-specific debugging in `/docs/troubleshooting/mcp-debugging.md`