
import { useState } from "react";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FilterState } from "@/types/hotel";

interface FilterPanelProps {
  filters: FilterState;
  onFiltersChange: (filters: FilterState) => void;
  onReset: () => void;
}

export const FilterPanel = ({ filters, onFiltersChange, onReset }: FilterPanelProps) => {
  const [priceRange, setPriceRange] = useState(filters.priceRange);
  const [guestRating, setGuestRating] = useState(filters.guestRating);

  const handlePriceRangeChange = (value: number[]) => {
    setPriceRange([value[0], value[1]]);
    onFiltersChange({
      ...filters,
      priceRange: [value[0], value[1]]
    });
  };

  const handleGuestRatingChange = (value: number[]) => {
    setGuestRating([value[0], value[1]]);
    onFiltersChange({
      ...filters,
      guestRating: [value[0], value[1]]
    });
  };

  const handleStarRatingChange = (star: number, checked: boolean) => {
    let newStarRating;
    if (checked) {
      newStarRating = [...filters.starRating, star].sort((a, b) => a - b);
    } else {
      newStarRating = filters.starRating.filter(s => s !== star);
    }
    onFiltersChange({
      ...filters,
      starRating: newStarRating
    });
  };

  const handleMinReviewsChange = (value: string) => {
    const numValue = parseInt(value) || 0;
    onFiltersChange({
      ...filters,
      minReviews: numValue
    });
  };

  return (
    <Card className="w-full">
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Filters</CardTitle>
          <Button variant="ghost" size="sm" onClick={onReset}>
            Reset
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Price Range */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Price per night</Label>
          <div className="px-2">
            <Slider
              value={priceRange}
              onValueChange={handlePriceRangeChange}
              max={1000}
              min={50}
              step={10}
              className="w-full"
            />
          </div>
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>${priceRange[0]}</span>
            <span>${priceRange[1]}</span>
          </div>
        </div>

        {/* Star Rating */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Star Rating</Label>
          <div className="space-y-2">
            {[1, 2, 3, 4, 5].map((star) => (
              <div key={star} className="flex items-center space-x-2">
                <Checkbox
                  id={`star-${star}`}
                  checked={filters.starRating.includes(star)}
                  onCheckedChange={(checked) => handleStarRatingChange(star, checked as boolean)}
                />
                <Label htmlFor={`star-${star}`} className="text-sm flex items-center">
                  {star} star{star > 1 ? 's' : ''}
                  <span className="ml-1 text-yellow-500">
                    {'★'.repeat(star)}{'☆'.repeat(5-star)}
                  </span>
                </Label>
              </div>
            ))}
          </div>
        </div>

        {/* Guest Rating */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Guest Rating</Label>
          <div className="px-2">
            <Slider
              value={guestRating}
              onValueChange={handleGuestRatingChange}
              max={10}
              min={1}
              step={0.1}
              className="w-full"
            />
          </div>
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>{guestRating[0].toFixed(1)}</span>
            <span>{guestRating[1].toFixed(1)}</span>
          </div>
        </div>

        {/* Minimum Reviews */}
        <div className="space-y-3">
          <Label htmlFor="min-reviews" className="text-sm font-medium">
            Minimum Reviews
          </Label>
          <Input
            id="min-reviews"
            type="number"
            value={filters.minReviews}
            onChange={(e) => handleMinReviewsChange(e.target.value)}
            placeholder="0"
            min="0"
          />
        </div>
      </CardContent>
    </Card>
  );
};
