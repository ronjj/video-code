
import { useState, useEffect, useMemo } from "react";
import { DateRange } from "react-day-picker";
import { format, addDays } from "date-fns";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { SlidersHorizontal, RefreshCcw, Calendar } from "lucide-react";
import { toast } from "@/hooks/use-toast";
import { FilterState, Hotel, SortOption, SearchParams } from "@/types/hotel";
import { SearchBar } from "@/components/SearchBar";
import { CitySelector } from "@/components/CitySelector";
import { FilterPanel } from "@/components/FilterPanel";
import { HotelCard } from "@/components/HotelCard";
import { DateRangePicker } from "@/components/DateRangePicker";
import { searchHotels, checkApiHealth } from "@/services/hotelService";
import { filterHotels, sortHotels } from "@/utils/hotelFilters";

// Extract cities from API response
const extractCities = (hotels: Hotel[]): string[] => {
  const citySet = new Set<string>();
  hotels.forEach(hotel => {
    if (hotel.location.city) {
      citySet.add(hotel.location.city);
    }
  });
  return Array.from(citySet).sort();
};

const sortOptions: SortOption[] = [
  { value: "price-asc", label: "Price: Low to High" },
  { value: "price-desc", label: "Price: High to Low" },
  { value: "rating-desc", label: "Guest Rating: High to Low" },
  { value: "rating-asc", label: "Guest Rating: Low to High" },
  { value: "stars-desc", label: "Star Rating: High to Low" },
  { value: "stars-asc", label: "Star Rating: Low to High" },
  { value: "reviews-desc", label: "Most Reviews" },
  { value: "name-asc", label: "Name: A to Z" },
  { value: "name-desc", label: "Name: Z to A" },
];

const Index = () => {
  // Default to 2 weeks from now for the initial date range
  const today = new Date();
  const defaultFrom = addDays(today, 14);
  const defaultTo = addDays(defaultFrom, 4);
  
  const [dateRange, setDateRange] = useState<DateRange | undefined>({
    from: defaultFrom,
    to: defaultTo,
  });

  const [filters, setFilters] = useState<FilterState>({
    cities: [],
    priceRange: [50, 1000],
    starRating: [],
    guestRating: [1, 10],
    minReviews: 0,
    searchQuery: "",
    checkinDate: format(defaultFrom, "yyyy-MM-dd"),
    checkoutDate: format(defaultTo, "yyyy-MM-dd"),
  });

  const [sortBy, setSortBy] = useState("price-asc");
  const [mobileFiltersOpen, setMobileFiltersOpen] = useState(false);
  const [hotels, setHotels] = useState<Hotel[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cities, setCities] = useState<string[]>([]);

  // Fetch hotels when date range changes
  useEffect(() => {
    if (dateRange?.from && dateRange.to) {
      const checkinDate = format(dateRange.from, "yyyy-MM-dd");
      const checkoutDate = format(dateRange.to, "yyyy-MM-dd");
      
      setFilters(prev => ({
        ...prev,
        checkinDate,
        checkoutDate
      }));

      fetchHotels(checkinDate, checkoutDate);
    }
  }, [dateRange]);

  // Check API health on component mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const healthy = await checkApiHealth();
        if (!healthy) {
          toast({
            title: "API Unavailable",
            description: "The hotel search API is currently unavailable. Please try again later.",
            variant: "destructive",
          });
        } else {
          // If API is healthy and we have dates, fetch hotels
          if (dateRange?.from && dateRange.to) {
            fetchHotels(filters.checkinDate, filters.checkoutDate);
          }
        }
      } catch (error) {
        toast({
          title: "Connection Error",
          description: "Failed to connect to the hotel search API. Is the local server running?",
          variant: "destructive",
        });
      }
    };

    checkHealth();
  }, []);

  const fetchHotels = async (checkinDate: string, checkoutDate: string) => {
    setLoading(true);
    setError(null);

    try {
      const searchParams: SearchParams = {
        checkin_date: checkinDate,
        checkout_date: checkoutDate,
        max_price: filters.priceRange[1],
        min_stars: Math.min(...filters.starRating) || undefined,
        min_reviews: filters.minReviews || undefined,
        adults: 2,
        rooms: 1
      };

      // If cities are selected, search for each city
      if (filters.cities.length === 1) {
        searchParams.location = `${filters.cities[0]}, United States`;
      }

      const response = await searchHotels(searchParams);
      if (response.success) {
        setHotels(response.hotels);
        const extractedCities = extractCities(response.hotels);
        setCities(extractedCities);
        
        toast({
          title: "Search Complete",
          description: `Found ${response.results_count} hotels for your dates.`,
        });
      } else {
        setError("Search failed. Please try different search criteria.");
      }
    } catch (error) {
      console.error("Hotel search error:", error);
      setError("Failed to fetch hotels. Please check if the API server is running.");
      toast({
        title: "Search Error",
        description: "Failed to fetch hotel data. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDateRangeChange = (range: DateRange | undefined) => {
    setDateRange(range);
  };

  const handleRefreshSearch = () => {
    if (dateRange?.from && dateRange.to) {
      fetchHotels(format(dateRange.from, "yyyy-MM-dd"), format(dateRange.to, "yyyy-MM-dd"));
    } else {
      toast({
        title: "Please select dates",
        description: "Both check-in and check-out dates are required.",
        variant: "destructive",
      });
    }
  };

  const filteredAndSortedHotels = useMemo(() => {
    const filtered = filterHotels(hotels, filters);
    return sortHotels(filtered, sortBy);
  }, [hotels, filters, sortBy]);

  const handleFiltersChange = (newFilters: FilterState) => {
    setFilters(newFilters);
  };

  const handleSearchChange = (query: string) => {
    setFilters(prev => ({ ...prev, searchQuery: query }));
  };

  const handleCitiesChange = (selectedCities: string[]) => {
    setFilters(prev => ({ ...prev, cities: selectedCities }));
  };

  const resetFilters = () => {
    setFilters({
      cities: [],
      priceRange: [50, 1000],
      starRating: [],
      guestRating: [1, 10],
      minReviews: 0,
      searchQuery: "",
      checkinDate: filters.checkinDate,
      checkoutDate: filters.checkoutDate,
    });
  };

  const activeFiltersCount = 
    filters.cities.length +
    (filters.starRating.length > 0 ? 1 : 0) +
    (filters.minReviews > 0 ? 1 : 0) +
    (filters.priceRange[0] !== 50 || filters.priceRange[1] !== 1000 ? 1 : 0) +
    (filters.guestRating[0] !== 1 || filters.guestRating[1] !== 10 ? 1 : 0);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center">
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-foreground mb-2">Hotel Booking Aggregator</h1>
              <p className="text-muted-foreground">Find and compare the best hotel deals</p>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-3 w-full lg:w-auto">
              <div className="w-full sm:w-64">
                <SearchBar
                  value={filters.searchQuery}
                  onChange={handleSearchChange}
                  placeholder="Search hotels..."
                />
              </div>
              
              <div className="w-full sm:w-48">
                <CitySelector
                  cities={cities}
                  selectedCities={filters.cities}
                  onCitiesChange={handleCitiesChange}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-6">
        <div className="flex gap-6">
          {/* Desktop Sidebar */}
          <div className="hidden lg:block w-80 flex-shrink-0">
            <div className="sticky top-32">
              <div className="mb-6">
                <DateRangePicker 
                  dateRange={dateRange} 
                  onDateRangeChange={handleDateRangeChange} 
                />
                <Button 
                  className="w-full mt-2"
                  onClick={handleRefreshSearch}>
                  <RefreshCcw className="h-4 w-4 mr-2" />
                  Search Hotels
                </Button>
              </div>
              <FilterPanel
                filters={filters}
                onFiltersChange={handleFiltersChange}
                onReset={resetFilters}
              />
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1">
            {/* Controls Bar */}
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
              <div className="flex flex-wrap items-center gap-4">
                <div className="lg:hidden">
                  <DateRangePicker 
                    dateRange={dateRange} 
                    onDateRangeChange={handleDateRangeChange} 
                  />
                </div>
                <Button 
                  className="lg:hidden"
                  onClick={handleRefreshSearch}>
                  <RefreshCcw className="h-4 w-4 mr-2" />
                  Search
                </Button>
                <p className="text-muted-foreground">
                  {loading ? 'Loading...' : `${filteredAndSortedHotels.length} hotels found`}
                </p>
                
                {/* Mobile Filter Button */}
                <Sheet open={mobileFiltersOpen} onOpenChange={setMobileFiltersOpen}>
                  <SheetTrigger asChild>
                    <Button variant="outline" size="sm" className="lg:hidden">
                      <SlidersHorizontal className="h-4 w-4 mr-2" />
                      Filters
                      {activeFiltersCount > 0 && (
                        <Badge variant="secondary" className="ml-2 h-5 w-5 p-0 flex items-center justify-center text-xs">
                          {activeFiltersCount}
                        </Badge>
                      )}
                    </Button>
                  </SheetTrigger>
                  <SheetContent side="left" className="w-80 p-0">
                    <div className="p-6">
                      <FilterPanel
                        filters={filters}
                        onFiltersChange={handleFiltersChange}
                        onReset={resetFilters}
                      />
                    </div>
                  </SheetContent>
                </Sheet>
              </div>

              <div className="w-full sm:w-64">
                <Select value={sortBy} onValueChange={setSortBy}>
                  <SelectTrigger>
                    <SelectValue placeholder="Sort by..." />
                  </SelectTrigger>
                  <SelectContent>
                    {sortOptions.map((option) => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Active Filters */}
            {activeFiltersCount > 0 && (
              <div className="flex flex-wrap gap-2 mb-6">
                {filters.cities.map((city) => (
                  <Badge key={city} variant="secondary">
                    {city}
                  </Badge>
                ))}
                {filters.starRating.length > 0 && (
                  <Badge variant="secondary">
                    Star rating: {filters.starRating.join(", ")}
                  </Badge>
                )}
                {filters.minReviews > 0 && (
                  <Badge variant="secondary">
                    Min reviews: {filters.minReviews}
                  </Badge>
                )}
                {(filters.priceRange[0] !== 50 || filters.priceRange[1] !== 1000) && (
                  <Badge variant="secondary">
                    ${filters.priceRange[0]} - ${filters.priceRange[1]}
                  </Badge>
                )}
                {(filters.guestRating[0] !== 1 || filters.guestRating[1] !== 10) && (
                  <Badge variant="secondary">
                    Rating: {filters.guestRating[0]} - {filters.guestRating[1]}
                  </Badge>
                )}
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="bg-destructive/10 text-destructive rounded-md p-4 mb-6">
                <p>{error}</p>
              </div>
            )}

            {/* Loading State */}
            {loading && (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-t-primary border-r-primary border-b-primary/20 border-l-primary/20"></div>
                <p className="mt-4 text-muted-foreground">Loading hotels...</p>
              </div>
            )}

            {/* Empty State */}
            {!loading && filteredAndSortedHotels.length === 0 && (
              <div className="text-center py-12">
                <Calendar className="mx-auto h-12 w-12 text-muted-foreground" />
                <p className="text-xl text-muted-foreground mb-2 mt-4">No hotels found</p>
                <p className="text-muted-foreground mb-6">Try adjusting your filters or search criteria</p>
                <div className="flex flex-col sm:flex-row gap-3 justify-center">
                  <Button variant="outline" onClick={resetFilters}>
                    Reset Filters
                  </Button>
                  <Button onClick={handleRefreshSearch}>
                    <RefreshCcw className="h-4 w-4 mr-2" />
                    Search Again
                  </Button>
                </div>
              </div>
            )}

            {/* Hotels Grid */}
            {!loading && filteredAndSortedHotels.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredAndSortedHotels.map((hotel) => (
                  <HotelCard key={hotel.id} hotel={hotel} />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
