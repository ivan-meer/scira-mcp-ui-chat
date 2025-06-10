import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { type Chat } from '@/lib/db/schema';
import { toast } from 'sonner';

export function useChats(userId: string) {
  const queryClient = useQueryClient();
  
  // Main query to fetch chats
  const {
    data: chats = [],
    isLoading,
    error,
    refetch
  } = useQuery<Chat[]>({
    queryKey: ['chats', userId],
    queryFn: async () => {
      console.log('=== CHATS QUERY DEBUG ===');
      console.log('userId for chats query:', userId);
      
      if (!userId) {
        console.log('No userId, returning empty array');
        return [];
      }
      
      console.log('Fetching chats from /api/chats');
      const response = await fetch('/api/chats', {
        headers: {
          'x-user-id': userId
        }
      });
      
      console.log('Chats API response status:', response.status);
      
      if (!response.ok) {
        console.error('Failed to fetch chats, status:', response.status);
        throw new Error('Failed to fetch chats');
      }
      
      const chats = await response.json();
      console.log('Fetched chats:', chats);
      console.log('Chats count:', chats.length);
      
      return chats;
    },
    enabled: !!userId, // Only run query if userId exists
    staleTime: 1000 * 60 * 5, // Consider data fresh for 5 minutes
    refetchOnWindowFocus: true, // Refetch when window regains focus
  });

  // Mutation to delete a chat
  const deleteChat = useMutation({
    mutationFn: async (chatId: string) => {
      const response = await fetch(`/api/chats/${chatId}`, {
        method: 'DELETE',
        headers: {
          'x-user-id': userId
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to delete chat');
      }
      
      return chatId;
    },
    onSuccess: (deletedChatId) => {
      // Update cache by removing the deleted chat
      queryClient.setQueryData<Chat[]>(['chats', userId], (oldChats = []) => 
        oldChats.filter(chat => chat.id !== deletedChatId)
      );
      
      toast.success('Chat deleted');
    },
    onError: (error) => {
      console.error('Error deleting chat:', error);
      toast.error('Failed to delete chat');
    }
  });

  // Function to invalidate chats cache for refresh
  const refreshChats = () => {
    queryClient.invalidateQueries({ queryKey: ['chats', userId] });
  };

  return {
    chats,
    isLoading,
    error,
    deleteChat: deleteChat.mutate,
    isDeleting: deleteChat.isPending,
    refreshChats,
    refetch
  };
} 