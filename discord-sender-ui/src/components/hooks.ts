import { useState } from "react";

interface FetchMessagesCheckParams {
  user_id: string;
  body: string; // Assuming body is a string; adjust if it's a different type
}

interface FetchMessagesCheckResponse {
  data: any; // Replace `any` with the actual response type if known
  error: string | null;
  isLoading: boolean;
}

export const useFetchMessagesCheck = (
  apiUrl: string
): [(params: FetchMessagesCheckParams) => Promise<void>, FetchMessagesCheckResponse] => {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const fetchMessagesCheck = async ({ user_id, body }: FetchMessagesCheckParams): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${apiUrl}/api/messages/check`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_id, body }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();
      setData(result);
    } catch (err: any) {
      setError(err.message || "An unknown error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return [fetchMessagesCheck, { data, error, isLoading }];
};