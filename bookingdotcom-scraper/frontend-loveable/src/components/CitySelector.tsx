
import { useState } from "react";
import { Check, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Badge } from "@/components/ui/badge";

interface CitySelectorProps {
  cities: string[];
  selectedCities: string[];
  onCitiesChange: (cities: string[]) => void;
}

export const CitySelector = ({ cities, selectedCities, onCitiesChange }: CitySelectorProps) => {
  const [open, setOpen] = useState(false);

  const toggleCity = (city: string) => {
    if (selectedCities.includes(city)) {
      onCitiesChange(selectedCities.filter(c => c !== city));
    } else {
      onCitiesChange([...selectedCities, city]);
    }
  };

  const clearAll = () => {
    onCitiesChange([]);
  };

  return (
    <div className="space-y-2">
      <DropdownMenu open={open} onOpenChange={setOpen}>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" className="w-full justify-between h-12">
            <span>
              {selectedCities.length === 0 
                ? "Select cities..." 
                : `${selectedCities.length} cities selected`}
            </span>
            <ChevronDown className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-56 bg-background border">
          <DropdownMenuLabel>Select Cities</DropdownMenuLabel>
          <DropdownMenuSeparator />
          {cities.map((city) => (
            <DropdownMenuItem
              key={city}
              onClick={() => toggleCity(city)}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <div className="flex items-center space-x-2 flex-1">
                <div className={`h-4 w-4 border rounded flex items-center justify-center ${
                  selectedCities.includes(city) ? 'bg-primary border-primary' : 'border-muted-foreground'
                }`}>
                  {selectedCities.includes(city) && (
                    <Check className="h-3 w-3 text-primary-foreground" />
                  )}
                </div>
                <span>{city}</span>
              </div>
            </DropdownMenuItem>
          ))}
          {selectedCities.length > 0 && (
            <>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={clearAll} className="cursor-pointer">
                Clear All
              </DropdownMenuItem>
            </>
          )}
        </DropdownMenuContent>
      </DropdownMenu>
      
      {selectedCities.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {selectedCities.map((city) => (
            <Badge key={city} variant="secondary" className="text-xs">
              {city}
            </Badge>
          ))}
        </div>
      )}
    </div>
  );
};
