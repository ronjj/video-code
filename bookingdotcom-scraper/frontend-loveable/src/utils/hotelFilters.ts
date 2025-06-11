
import { Hotel, FilterState } from "@/types/hotel";

export const filterHotels = (hotels: Hotel[], filters: FilterState): Hotel[] => {
  return hotels.filter(hotel => {
    // City filter
    if (filters.cities.length > 0 && !filters.cities.includes(hotel.location.city)) {
      return false;
    }

    // Price range filter
    if (hotel.pricing.price_per_night_unformatted < filters.priceRange[0] || 
        hotel.pricing.price_per_night_unformatted > filters.priceRange[1]) {
      return false;
    }

    // Star rating filter
    if (filters.starRating.length > 0 && !filters.starRating.includes(Math.floor(hotel.star_rating))) {
      return false;
    }

    // Guest rating filter
    if (hotel.guest_rating.score < filters.guestRating[0] || hotel.guest_rating.score > filters.guestRating[1]) {
      return false;
    }

    // Minimum reviews filter
    if (hotel.guest_rating.review_count < filters.minReviews) {
      return false;
    }

    // Search query filter
    if (filters.searchQuery) {
      const query = filters.searchQuery.toLowerCase();
      const searchableText = `${hotel.name} ${hotel.location.full_address}`.toLowerCase();
      if (!searchableText.includes(query)) {
        return false;
      }
    }

    return true;
  });
};

export const sortHotels = (hotels: Hotel[], sortBy: string): Hotel[] => {
  const sorted = [...hotels];
  
  switch (sortBy) {
    case 'price-asc':
      return sorted.sort((a, b) => a.pricing.price_per_night_unformatted - b.pricing.price_per_night_unformatted);
    case 'price-desc':
      return sorted.sort((a, b) => b.pricing.price_per_night_unformatted - a.pricing.price_per_night_unformatted);
    case 'rating-desc':
      return sorted.sort((a, b) => b.guest_rating.score - a.guest_rating.score);
    case 'rating-asc':
      return sorted.sort((a, b) => a.guest_rating.score - b.guest_rating.score);
    case 'stars-desc':
      return sorted.sort((a, b) => b.star_rating - a.star_rating);
    case 'stars-asc':
      return sorted.sort((a, b) => a.star_rating - b.star_rating);
    case 'reviews-desc':
      return sorted.sort((a, b) => b.guest_rating.review_count - a.guest_rating.review_count);
    case 'name-asc':
      return sorted.sort((a, b) => a.name.localeCompare(b.name));
    case 'name-desc':
      return sorted.sort((a, b) => b.name.localeCompare(a.name));
    default:
      return sorted;
  }
};
