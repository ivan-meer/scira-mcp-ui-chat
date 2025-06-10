import { nanoid } from 'nanoid';

const USER_ID_KEY = 'ai-chat-user-id';

export function getUserId(): string {
  // Only run this on the client side
  if (typeof window === 'undefined') return 'server-user';
  
  let userId = localStorage.getItem(USER_ID_KEY);
  
  if (!userId) {
    // Generate a new user ID and store it
    userId = nanoid();
    localStorage.setItem(USER_ID_KEY, userId);
    console.log('Generated new user ID:', userId);
  }
  
  console.log('Using user ID:', userId);
  return userId;
}

export function updateUserId(newUserId: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(USER_ID_KEY, newUserId);
} 