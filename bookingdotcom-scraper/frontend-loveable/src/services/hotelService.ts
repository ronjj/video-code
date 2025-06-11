
import { SearchParams, ApiResponse } from "@/types/hotel";

const API_BASE_URL = "http://localhost:5000";

export const searchHotels = async (params: SearchParams): Promise<ApiResponse> => {
  console.log("Sending search request with params:", params);
  
  try {
    const response = await fetch(`${API_BASE_URL}/search`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
      mode: "cors",
      body: JSON.stringify(params),
    });

    console.log("Response status:", response.status);
    console.log("Response ok:", response.ok);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Error response:", errorText);
      throw new Error(`HTTP ${response.status}: ${errorText}`);
    }

    const data = await response.json();
    console.log("Received data:", data);
    return data;
  } catch (error) {
    console.error("Error fetching hotel data:", error);
    throw error;
  }
};

export const checkApiHealth = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
      mode: "cors",
      headers: {
        "Accept": "application/json",
      },
    });
    
    console.log("Health check response:", response.status, response.ok);
    return response.ok;
  } catch (error) {
    console.error("API health check failed:", error);
    return false;
  }
};
