
import { Hotel } from "@/types/hotel";

export const mockHotels: Hotel[] = [
  {
    id: "hotel_1",
    name: "Warwick Seattle",
    location: {
      address: "401 Lenora Street",
      city: "Seattle",
      full_address: "401 Lenora Street, Seattle, Washington"
    },
    star_rating: 4.0,
    guest_rating: {
      score: 8.1,
      review_count: 1023,
      text: "Very Good"
    },
    pricing: {
      total_price: "$3,106.50",
      currency: "USD",
      price_per_night: "$191.89",
      price_per_night_unformatted: 191.89
    },
    meal_plan: "Breakfast included",
    image_url: "https://images.unsplash.com/photo-1566073771259-6a8506099945"
  },
  {
    id: "hotel_2",
    name: "Hyatt House Seattle",
    location: {
      address: "201 5th Avenue",
      city: "Seattle",
      full_address: "201 5th Avenue, Seattle, Washington"
    },
    star_rating: 3.5,
    guest_rating: {
      score: 9.2,
      review_count: 856,
      text: "Exceptional"
    },
    pricing: {
      total_price: "$2,850.00",
      currency: "USD",
      price_per_night: "$178.13",
      price_per_night_unformatted: 178.13
    },
    meal_plan: "Breakfast & dinner included",
    image_url: "https://images.unsplash.com/photo-1564501049412-61c2a3083791"
  },
  {
    id: "hotel_3",
    name: "The Edgewater Hotel",
    location: {
      address: "2411 Alaskan Way",
      city: "Seattle",
      full_address: "2411 Alaskan Way, Seattle, Washington"
    },
    star_rating: 4.5,
    guest_rating: {
      score: 8.7,
      review_count: 1245,
      text: "Excellent"
    },
    pricing: {
      total_price: "$3,950.50",
      currency: "USD",
      price_per_night: "$246.91",
      price_per_night_unformatted: 246.91
    },
    meal_plan: "Room only",
    image_url: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4"
  },
  {
    id: "hotel_4",
    name: "Kimpton Hotel Monaco",
    location: {
      address: "1101 4th Avenue",
      city: "Seattle",
      full_address: "1101 4th Avenue, Seattle, Washington"
    },
    star_rating: 4.0,
    guest_rating: {
      score: 8.9,
      review_count: 934,
      text: "Excellent"
    },
    pricing: {
      total_price: "$3,280.00",
      currency: "USD",
      price_per_night: "$205.00",
      price_per_night_unformatted: 205.00
    },
    meal_plan: "Breakfast included",
    image_url: "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa"
  },
  {
    id: "hotel_5",
    name: "Fairmont Olympic Hotel",
    location: {
      address: "411 University Street",
      city: "Seattle",
      full_address: "411 University Street, Seattle, Washington"
    },
    star_rating: 5.0,
    guest_rating: {
      score: 9.5,
      review_count: 1652,
      text: "Exceptional"
    },
    pricing: {
      total_price: "$4,800.00",
      currency: "USD",
      price_per_night: "$300.00",
      price_per_night_unformatted: 300.00
    },
    meal_plan: "Breakfast & dinner included",
    image_url: "https://images.unsplash.com/photo-1606046604972-77cc76aee944"
  },
  {
    id: "hotel_6",
    name: "The Westin Seattle",
    location: {
      address: "1900 5th Avenue",
      city: "Seattle",
      full_address: "1900 5th Avenue, Seattle, Washington"
    },
    star_rating: 4.0,
    guest_rating: {
      score: 8.5,
      review_count: 1432,
      text: "Very Good"
    },
    pricing: {
      total_price: "$3,440.00",
      currency: "USD",
      price_per_night: "$215.00",
      price_per_night_unformatted: 215.00
    },
    meal_plan: "Breakfast included",
    image_url: "https://images.unsplash.com/photo-1566073771259-6a8506099945"
  }
];
