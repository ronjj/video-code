
export interface Hotel {
  id: string;
  name: string;
  location: {
    address: string;
    city: string;
    full_address: string;
  };
  star_rating: number;
  guest_rating: {
    score: number;
    review_count: number;
    text: string;
  };
  pricing: {
    total_price: string;
    currency: string;
    price_per_night: string;
    price_per_night_unformatted: number;
  };
  meal_plan?: string;
  image_url?: string;
}

export interface FilterState {
  cities: string[];
  priceRange: [number, number];
  starRating: number[];
  guestRating: [number, number];
  minReviews: number;
  searchQuery: string;
  checkinDate: string;
  checkoutDate: string;
}

export interface SortOption {
  value: string;
  label: string;
}

export interface SearchParams {
  checkin_date: string;
  checkout_date: string;
  location?: string;
  max_price?: number;
  min_stars?: number;
  min_reviews?: number;
  adults?: number;
  rooms?: number;
  children?: number;
}

export interface ApiResponse {
  success: boolean;
  search_params: {
    checkin_date: string;
    checkout_date: string;
    location: string;
    adults: number;
    rooms: number;
    children: number;
    filters: {
      max_price?: number;
      min_stars?: number;
      min_reviews?: number;
    }
  };
  results_count: number;
  hotels: Hotel[];
}
