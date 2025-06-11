
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Hotel } from "@/types/hotel";

interface HotelCardProps {
  hotel: Hotel;
}

export const HotelCard = ({ hotel }: HotelCardProps) => {
  const getRatingColor = (rating: number) => {
    if (rating >= 9) return "bg-green-500";
    if (rating >= 8) return "bg-blue-500";
    if (rating >= 7) return "bg-yellow-500";
    return "bg-gray-500";
  };

  const getRatingBadgeVariant = (ratingText: string) => {
    switch (ratingText.toLowerCase()) {
      case "exceptional":
        return "default";
      case "excellent":
        return "secondary";
      case "very good":
        return "outline";
      default:
        return "outline";
    }
  };

  return (
    <Card className="hover:shadow-lg transition-shadow duration-200 overflow-hidden">
      <div className="aspect-video relative overflow-hidden">
        <img
          src={hotel.image_url || "https://images.unsplash.com/photo-1566073771259-6a8506099945"}
          alt={hotel.name}
          className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
        />
        <div className="absolute top-3 right-3">
          <Badge variant="secondary" className="bg-white/90 text-black">
            {'★'.repeat(Math.floor(hotel.star_rating))}
            {hotel.star_rating % 1 !== 0 && '½'}
          </Badge>
        </div>
        {hotel.meal_plan && (
          <div className="absolute bottom-3 left-3">
            <Badge variant="outline" className="bg-white/90 text-black">
              {hotel.meal_plan}
            </Badge>
          </div>
        )}
      </div>
      
      <CardContent className="p-4 space-y-3">
        <div>
          <h3 className="font-semibold text-lg text-foreground leading-tight mb-1">
            {hotel.name}
          </h3>
          <p className="text-sm text-muted-foreground">
            {hotel.location.full_address}
          </p>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          <div className={`px-2 py-1 rounded text-white text-xs font-medium ${getRatingColor(hotel.guest_rating.score)}`}>
            {hotel.guest_rating.score.toFixed(1)}
          </div>
          <Badge variant={getRatingBadgeVariant(hotel.guest_rating.text)}>
            {hotel.guest_rating.text}
          </Badge>
          <span className="text-xs text-muted-foreground">
            {hotel.guest_rating.review_count.toLocaleString()} reviews
          </span>
        </div>

        <div className="flex items-end justify-between pt-2 border-t">
          <div>
            <p className="text-2xl font-bold text-foreground">
              {hotel.pricing.price_per_night}
            </p>
            <p className="text-xs text-muted-foreground">per night</p>
          </div>
          <div className="text-right">
            <p className="text-sm font-medium text-foreground">
              {hotel.pricing.total_price}
            </p>
            <p className="text-xs text-muted-foreground">total</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
