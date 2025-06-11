from curl_cffi import requests
import json
from datetime import datetime

def format_image_url(relative_url):
    """Format image URL to use Booking.com's CDN domain"""
    if not relative_url:
        return None
    return f"https://cf.bstatic.com{relative_url}"

def get_user_dates():
    """Get check-in and check-out dates from user"""
    while True:
        try:
            checkin_str = input("Enter check-in date (MM/DD/YYYY): ").strip()
            checkout_str = input("Enter check-out date (MM/DD/YYYY): ").strip()
            
            # Parse dates
            checkin = datetime.strptime(checkin_str, "%m/%d/%Y")
            checkout = datetime.strptime(checkout_str, "%m/%d/%Y")
            
            # Validate dates
            if checkout <= checkin:
                print("Error: Check-out date must be after check-in date. Please try again.\n")
                continue
                
            if checkin < datetime.now():
                print("Error: Check-in date cannot be in the past. Please try again.\n")
                continue
            
            # Format for API (YYYY-MM-DD)
            checkin_formatted = checkin.strftime("%Y-%m-%d")
            checkout_formatted = checkout.strftime("%Y-%m-%d")
            
            return checkin_formatted, checkout_formatted
            
        except ValueError:
            print("Error: Invalid date format. Please use MM/DD/YYYY format.\n")

def get_max_price():
    """Get maximum price per night from user"""
    while True:
        try:
            price_input = input("Enter maximum price per night (USD, or press Enter for no limit): ").strip()
            if not price_input:
                return None
            
            max_price = float(price_input)
            if max_price <= 0:
                print("Error: Price must be greater than 0. Please try again.\n")
                continue
                
            return int(max_price)
            
        except ValueError:
            print("Error: Invalid price format. Please enter a number.\n")

def get_min_stars():
    """Get minimum star rating from user"""
    while True:
        try:
            stars_input = input("Enter minimum star rating (1-5, or press Enter for no filter): ").strip()
            if not stars_input:
                return None
                
            min_stars = int(stars_input)
            if min_stars < 1 or min_stars > 5:
                print("Error: Star rating must be between 1 and 5. Please try again.\n")
                continue
                
            return min_stars
            
        except ValueError:
            print("Error: Invalid star rating. Please enter a number between 1 and 5.\n")

def get_min_reviews():
    """Get minimum number of reviews from user"""
    while True:
        try:
            reviews_input = input("Enter minimum number of reviews (or press Enter for no filter): ").strip()
            if not reviews_input:
                return None
                
            min_reviews = int(reviews_input)
            if min_reviews < 0:
                print("Error: Number of reviews cannot be negative. Please try again.\n")
                continue
                
            return min_reviews
            
        except ValueError:
            print("Error: Invalid number of reviews. Please enter a number.\n")

# CLI Interface
print("=== Booking.com Hotel Search ===\n")

# Get user inputs
checkin_date, checkout_date = get_user_dates()
max_price = get_max_price()
min_stars = get_min_stars()
min_reviews = get_min_reviews()

print(f"\nSearching for hotels from {checkin_date} to {checkout_date}...")
if max_price:
    print(f"Max price per night: ${max_price}")
if min_stars:
    print(f"Minimum stars: {min_stars}")
if min_reviews:
    print(f"Minimum reviews: {min_reviews}")
print()

url = "https://www.booking.com/dml/graphql?ss=Seattle%2C+United+States&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaLQCiAEBmAExuAEHyAEM2AEB6AEB-AECiAIBqAIDuAK-iPnBBsACAdICJGZmMzBhOGRjLTQ1M2ItNGY0Ny04YmZjLWQyMDFjYTNiZWM1MdgCBeACAQ&sid=13b7b29af206a79542e44dfdce841b83&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=20144883&dest_type=city&checkin=2025-07-01&checkout=2025-07-19&group_adults=2&no_rooms=1&group_children=0"

payload = json.dumps({
  "operationName": "FullSearch",
  "variables": {
    "includeBundle": False,
    "input": {
      "acidCarouselContext": None,
      "childrenAges": [],
      "dates": {
        "checkin": checkin_date,
        "checkout": checkout_date
      },
      "doAvailabilityCheck": False,
      "encodedAutocompleteMeta": None,
      "enableCampaigns": True,
      "filters": {},
      "flexibleDatesConfig": {
        "broadDatesCalendar": {
          "checkinMonths": [],
          "los": [],
          "startWeekdays": []
        },
        "dateFlexUseCase": "DATE_RANGE",
        "dateRangeCalendar": {
          "checkin": [
            checkin_date
          ],
          "checkout": [
            checkout_date
          ]
        }
      },
      "forcedBlocks": None,
      "location": {
        "searchString": "Seattle, United States",
        "destType": "CITY",
        "destId": 20144883
      },
      "metaContext": {
        "metaCampaignId": 0,
        "externalTotalPrice": None,
        "feedPrice": None,
        "hotelCenterAccountId": None,
        "rateRuleId": None,
        "dragongateTraceId": None,
        "pricingProductsTag": None
      },
      "nbRooms": 1,
      "nbAdults": 2,
      "nbChildren": 0,
      "showAparthotelAsHotel": True,
      "needsRoomsMatch": False,
      "optionalFeatures": {
        "forceArpExperiments": True,
        "testProperties": False
      },
      "pagination": {
        "rowsPerPage": 1000,
        "offset": 0
      },
      "rawQueryForSession": f"/searchresults.html?label=gen173nr-1FCAEoggI46AdIM1gEaLQCiAEBmAExuAEHyAEM2AEB6AEB-AECiAIBqAIDuAK-iPnBBsACAdICJGZmMzBhOGRjLTQ1M2ItNGY0Ny04YmZjLWQyMDFjYTNiZWM1MdgCBeACAQ&sid=13b7b29af206a79542e44dfdce841b83&aid=304142&ss=Seattle%2C+United+States&efdco=1&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=20144883&dest_type=city&checkin={checkin_date}&checkout={checkout_date}&group_adults=2&no_rooms=1&group_children=0",
      "referrerBlock": {
        "blockName": "searchbox"
      },
      "sbCalendarOpen": True,
      "sorters": {
        "selectedSorter": None,
        "referenceGeoId": None,
        "tripTypeIntentId": None
      },
      "travelPurpose": 2,
      "seoThemeIds": [],
      "useSearchParamsFromSession": True,
      "merchInput": {
        "testCampaignIds": []
      },
      "webSearchContext": {
        "reason": "CLIENT_SIDE_UPDATE",
        "source": "SEARCH_RESULTS",
        "outcome": "SEARCH_RESULTS"
      },
      "clientSideRequestId": "86ed05d965d10150"
    },
    "carouselLowCodeExp": False
  },
  "extensions": {},
  "query": "query FullSearch($input: SearchQueryInput!, $carouselLowCodeExp: Boolean!, $includeBundle: Boolean = false) {\n  searchQueries {\n    search(input: $input) {\n      ...FullSearchFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FullSearchFragment on SearchQueryOutput {\n  banners {\n    ...Banner\n    __typename\n  }\n  breadcrumbs {\n    ... on SearchResultsBreadcrumb {\n      ...SearchResultsBreadcrumb\n      __typename\n    }\n    ... on LandingPageBreadcrumb {\n      ...LandingPageBreadcrumb\n      __typename\n    }\n    __typename\n  }\n  carousels {\n    ...Carousel\n    __typename\n  }\n  destinationLocation {\n    ...DestinationLocation\n    __typename\n  }\n  entireHomesSearchEnabled\n  dateFlexibilityOptions {\n    enabled\n    __typename\n  }\n  flexibleDatesConfig {\n    broadDatesCalendar {\n      checkinMonths\n      los\n      startWeekdays\n      losType\n      __typename\n    }\n    dateFlexUseCase\n    dateRangeCalendar {\n      flexWindow\n      checkin\n      checkout\n      __typename\n    }\n    __typename\n  }\n  filters {\n    ...FilterData\n    __typename\n  }\n  filtersTrackOnView {\n    type\n    experimentHash\n    value\n    __typename\n  }\n  appliedFilterOptions {\n    ...FilterOption\n    __typename\n  }\n  recommendedFilterOptions {\n    ...FilterOption\n    __typename\n  }\n  pagination {\n    nbResultsPerPage\n    nbResultsTotal\n    __typename\n  }\n  tripTypes {\n    ...TripTypesData\n    __typename\n  }\n  results {\n    ...BasicPropertyData\n    ...PropertyUspBadges\n    ...MatchingUnitConfigurations\n    ...PropertyBlocks\n    ...BookerExperienceData\n    ...TopPhotos\n    generatedPropertyTitle\n    priceDisplayInfoIrene {\n      ...PriceDisplayInfoIrene\n      __typename\n    }\n    licenseDetails {\n      nextToHotelName\n      __typename\n    }\n    isTpiExclusiveProperty\n    propertyCribsAvailabilityLabel\n    mlBookingHomeTags\n    trackOnView {\n      experimentTag\n      __typename\n    }\n    __typename\n  }\n  searchMeta {\n    ...SearchMetadata\n    __typename\n  }\n  sorters {\n    option {\n      ...SorterFields\n      __typename\n    }\n    __typename\n  }\n  zeroResultsSection {\n    ...ZeroResultsSection\n    __typename\n  }\n  rocketmilesSearchUuid\n  previousSearches {\n    ...PreviousSearches\n    __typename\n  }\n  merchComponents {\n    ...MerchRegionIrene\n    __typename\n  }\n  wishlistData {\n    numProperties\n    __typename\n  }\n  seoThemes {\n    id\n    caption\n    __typename\n  }\n  gridViewPreference\n  advancedSearchWidget {\n    title\n    legalDisclaimer\n    description\n    placeholder\n    ctaText\n    helperText\n    __typename\n  }\n  visualFiltersGroups {\n    ...VisualFiltersGroup\n    __typename\n  }\n  __typename\n}\n\nfragment BasicPropertyData on SearchResultProperty {\n  acceptsWalletCredit\n  basicPropertyData {\n    accommodationTypeId\n    id\n    isTestProperty\n    location {\n      address\n      city\n      countryCode\n      __typename\n    }\n    pageName\n    ufi\n    photos {\n      main {\n        highResUrl {\n          relativeUrl\n          __typename\n        }\n        lowResUrl {\n          relativeUrl\n          __typename\n        }\n        highResJpegUrl {\n          relativeUrl\n          __typename\n        }\n        lowResJpegUrl {\n          relativeUrl\n          __typename\n        }\n        tags {\n          id\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    reviewScore: reviews {\n      score: totalScore\n      reviewCount: reviewsCount\n      totalScoreTextTag {\n        translation\n        __typename\n      }\n      showScore\n      secondaryScore\n      secondaryTextTag {\n        translation\n        __typename\n      }\n      showSecondaryScore\n      __typename\n    }\n    externalReviewScore: externalReviews {\n      score: totalScore\n      reviewCount: reviewsCount\n      showScore\n      totalScoreTextTag {\n        translation\n        __typename\n      }\n      __typename\n    }\n    starRating {\n      value\n      symbol\n      caption {\n        translation\n        __typename\n      }\n      tocLink {\n        translation\n        __typename\n      }\n      showAdditionalInfoIcon\n      __typename\n    }\n    isClosed\n    paymentConfig {\n      installments {\n        minPriceFormatted\n        maxAcceptCount\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  badges {\n    caption {\n      translation\n      __typename\n    }\n    closedFacilities {\n      startDate\n      endDate\n      __typename\n    }\n    __typename\n  }\n  customBadges {\n    showSkiToDoor\n    showBhTravelCreditBadge\n    showOnlineCheckinBadge\n    __typename\n  }\n  description {\n    text\n    __typename\n  }\n  displayName {\n    text\n    translationTag {\n      translation\n      __typename\n    }\n    __typename\n  }\n  geniusInfo {\n    benefitsCommunication {\n      header {\n        title\n        __typename\n      }\n      items {\n        title\n        __typename\n      }\n      __typename\n    }\n    geniusBenefits\n    geniusBenefitsData {\n      hotelCardHasFreeBreakfast\n      hotelCardHasFreeRoomUpgrade\n      sortedBenefits\n      __typename\n    }\n    showGeniusRateBadge\n    __typename\n  }\n  location {\n    displayLocation\n    mainDistance\n    mainDistanceDescription\n    publicTransportDistanceDescription\n    skiLiftDistance\n    beachDistance\n    nearbyBeachNames\n    beachWalkingTime\n    geoDistanceMeters\n    isCentrallyLocated\n    isWithinBestLocationScoreArea\n    popularFreeDistrictName\n    nearbyUsNaturalParkText\n    __typename\n  }\n  mealPlanIncluded {\n    mealPlanType\n    text\n    __typename\n  }\n  persuasion {\n    autoextended\n    geniusRateAvailable\n    highlighted\n    preferred\n    preferredPlus\n    showNativeAdLabel\n    nativeAdId\n    nativeAdsCpc\n    nativeAdsTracking\n    sponsoredAdsData {\n      isDsaCompliant\n      legalEntityName\n      sponsoredAdsDesign\n      __typename\n    }\n    __typename\n  }\n  policies {\n    showFreeCancellation\n    showNoPrepayment\n    showPetsAllowedForFree\n    enableJapaneseUsersSpecialCase\n    __typename\n  }\n  ribbon {\n    ribbonType\n    text\n    __typename\n  }\n  recommendedDate {\n    checkin\n    checkout\n    lengthOfStay\n    __typename\n  }\n  showGeniusLoginMessage\n  hostTraderLabel\n  soldOutInfo {\n    isSoldOut\n    messages {\n      text\n      __typename\n    }\n    alternativeDatesMessages {\n      text\n      __typename\n    }\n    __typename\n  }\n  nbWishlists\n  nonMatchingFlexibleFilterOptions {\n    label\n    __typename\n  }\n  visibilityBoosterEnabled\n  showAdLabel\n  isNewlyOpened\n  propertySustainability {\n    isSustainable\n    certifications {\n      name\n      __typename\n    }\n    __typename\n  }\n  seoThemes {\n    caption\n    __typename\n  }\n  relocationMode {\n    distanceToCityCenterKm\n    distanceToCityCenterMiles\n    distanceToOriginalHotelKm\n    distanceToOriginalHotelMiles\n    phoneNumber\n    __typename\n  }\n  bundleRatesAvailable\n  __typename\n}\n\nfragment Banner on Banner {\n  name\n  type\n  isDismissible\n  showAfterDismissedDuration\n  position\n  requestAlternativeDates\n  merchId\n  title {\n    text\n    __typename\n  }\n  imageUrl\n  paragraphs {\n    text\n    __typename\n  }\n  metadata {\n    key\n    value\n    __typename\n  }\n  pendingReviewInfo {\n    propertyPhoto {\n      lowResUrl {\n        relativeUrl\n        __typename\n      }\n      lowResJpegUrl {\n        relativeUrl\n        __typename\n      }\n      __typename\n    }\n    propertyName\n    urlAccessCode\n    __typename\n  }\n  nbDeals\n  primaryAction {\n    text {\n      text\n      __typename\n    }\n    action {\n      name\n      context {\n        key\n        value\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  secondaryAction {\n    text {\n      text\n      __typename\n    }\n    action {\n      name\n      context {\n        key\n        value\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  iconName\n  flexibleFilterOptions {\n    optionId\n    filterName\n    __typename\n  }\n  trackOnView {\n    type\n    experimentHash\n    value\n    __typename\n  }\n  dateFlexQueryOptions {\n    text {\n      text\n      __typename\n    }\n    action {\n      name\n      context {\n        key\n        value\n        __typename\n      }\n      __typename\n    }\n    isApplied\n    __typename\n  }\n  __typename\n}\n\nfragment Carousel on Carousel {\n  aggregatedCountsByFilterId\n  carouselId\n  position\n  contentType\n  hotelId\n  name\n  soldoutProperties\n  priority\n  themeId\n  title {\n    text\n    __typename\n  }\n  slides {\n    captionText {\n      text\n      __typename\n    }\n    name\n    photoUrl\n    subtitle {\n      text\n      __typename\n    }\n    type\n    title {\n      text\n      __typename\n    }\n    action {\n      context {\n        key\n        value\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment DestinationLocation on DestinationLocation {\n  name {\n    text\n    __typename\n  }\n  inName {\n    text\n    __typename\n  }\n  countryCode\n  ufi\n  __typename\n}\n\nfragment FilterData on Filter {\n  trackOnView {\n    type\n    experimentHash\n    value\n    __typename\n  }\n  trackOnClick {\n    type\n    experimentHash\n    value\n    __typename\n  }\n  name\n  field\n  category\n  filterStyle\n  title {\n    text\n    translationTag {\n      translation\n      __typename\n    }\n    __typename\n  }\n  subtitle\n  options {\n    parentId\n    genericId\n    trackOnView {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnClick {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnSelect {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnDeSelect {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnViewPopular {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnClickPopular {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnSelectPopular {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnDeSelectPopular {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    ...FilterOption\n    __typename\n  }\n  filterLayout {\n    isCollapsable\n    collapsedCount\n    __typename\n  }\n  stepperOptions {\n    min\n    max\n    default\n    selected\n    title {\n      text\n      translationTag {\n        translation\n        __typename\n      }\n      __typename\n    }\n    field\n    labels {\n      text\n      translationTag {\n        translation\n        __typename\n      }\n      __typename\n    }\n    trackOnView {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnClick {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnSelect {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnDeSelect {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnClickDecrease {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnClickIncrease {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnDecrease {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnIncrease {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    __typename\n  }\n  sliderOptions {\n    min\n    max\n    minSelected\n    maxSelected\n    minPriceStep\n    minSelectedFormatted\n    currency\n    histogram\n    selectedRange {\n      translation\n      __typename\n    }\n    __typename\n  }\n  sliderOptionsPerStay {\n    min\n    max\n    minSelected\n    maxSelected\n    minPriceStep\n    minSelectedFormatted\n    currency\n    histogram\n    selectedRange {\n      translation\n      __typename\n    }\n    __typename\n  }\n  distanceToPoiData {\n    options {\n      text\n      value\n      isDefault\n      __typename\n    }\n    poiNotFound\n    poiPlaceholder\n    poiHelper\n    isSelected\n    selectedOptionValue\n    selectedPlaceId {\n      numValue\n      stringValue\n      __typename\n    }\n    selectedPoiType {\n      destType\n      source\n      __typename\n    }\n    selectedPoiText\n    selectedPoiLatitude\n    selectedPoiLongitude\n    __typename\n  }\n  __typename\n}\n\nfragment FilterOption on Option {\n  optionId: id\n  count\n  selected\n  urlId\n  source\n  field\n  additionalLabel {\n    text\n    translationTag {\n      translation\n      __typename\n    }\n    __typename\n  }\n  value {\n    text\n    translationTag {\n      translation\n      __typename\n    }\n    __typename\n  }\n  starRating {\n    value\n    symbol\n    caption {\n      translation\n      __typename\n    }\n    showAdditionalInfoIcon\n    __typename\n  }\n  __typename\n}\n\nfragment LandingPageBreadcrumb on LandingPageBreadcrumb {\n  destType\n  name\n  urlParts\n  __typename\n}\n\nfragment MatchingUnitConfigurations on SearchResultProperty {\n  matchingUnitConfigurations {\n    commonConfiguration {\n      name\n      unitId\n      bedConfigurations {\n        beds {\n          count\n          type\n          __typename\n        }\n        nbAllBeds\n        __typename\n      }\n      nbAllBeds\n      nbBathrooms\n      nbBedrooms\n      nbKitchens\n      nbLivingrooms\n      nbUnits\n      unitTypeNames {\n        translation\n        __typename\n      }\n      localizedArea {\n        localizedArea\n        unit\n        __typename\n      }\n      __typename\n    }\n    unitConfigurations {\n      name\n      unitId\n      bedConfigurations {\n        beds {\n          count\n          type\n          __typename\n        }\n        nbAllBeds\n        __typename\n      }\n      apartmentRooms {\n        config {\n          roomId: id\n          roomType\n          bedTypeId\n          bedCount: count\n          __typename\n        }\n        roomName: tag {\n          tag\n          translation\n          __typename\n        }\n        __typename\n      }\n      nbAllBeds\n      nbBathrooms\n      nbBedrooms\n      nbKitchens\n      nbLivingrooms\n      nbUnits\n      unitTypeNames {\n        translation\n        __typename\n      }\n      localizedArea {\n        localizedArea\n        unit\n        __typename\n      }\n      unitTypeId\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyBlocks on SearchResultProperty {\n  blocks {\n    blockId {\n      roomId\n      occupancy\n      policyGroupId\n      packageId\n      mealPlanId\n      bundleId\n      __typename\n    }\n    finalPrice {\n      amount\n      currency\n      __typename\n    }\n    originalPrice {\n      amount\n      currency\n      __typename\n    }\n    onlyXLeftMessage {\n      tag\n      variables {\n        key\n        value\n        __typename\n      }\n      translation\n      __typename\n    }\n    freeCancellationUntil\n    hasCrib\n    blockMatchTags {\n      childStaysForFree\n      freeStayChildrenAges\n      __typename\n    }\n    thirdPartyInventoryContext {\n      isTpiBlock\n      __typename\n    }\n    bundle @include(if: $includeBundle) {\n      highlightedText\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PriceDisplayInfoIrene on PriceDisplayInfoIrene {\n  badges {\n    name {\n      translation\n      __typename\n    }\n    tooltip {\n      translation\n      __typename\n    }\n    style\n    identifier\n    __typename\n  }\n  chargesInfo {\n    translation\n    __typename\n  }\n  displayPrice {\n    copy {\n      translation\n      __typename\n    }\n    amountPerStay {\n      amount\n      amountRounded\n      amountUnformatted\n      currency\n      __typename\n    }\n    amountPerStayHotelCurr {\n      amount\n      amountRounded\n      amountUnformatted\n      currency\n      __typename\n    }\n    __typename\n  }\n  averagePricePerNight {\n    amount\n    amountRounded\n    amountUnformatted\n    currency\n    __typename\n  }\n  priceBeforeDiscount {\n    copy {\n      translation\n      __typename\n    }\n    amountPerStay {\n      amount\n      amountRounded\n      amountUnformatted\n      currency\n      __typename\n    }\n    __typename\n  }\n  rewards {\n    rewardsList {\n      termsAndConditions\n      amountPerStay {\n        amount\n        amountRounded\n        amountUnformatted\n        currency\n        __typename\n      }\n      breakdown {\n        productType\n        amountPerStay {\n          amount\n          amountRounded\n          amountUnformatted\n          currency\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    rewardsAggregated {\n      amountPerStay {\n        amount\n        amountRounded\n        amountUnformatted\n        currency\n        __typename\n      }\n      copy {\n        translation\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  useRoundedAmount\n  discounts {\n    amount {\n      amount\n      amountRounded\n      amountUnformatted\n      currency\n      __typename\n    }\n    name {\n      translation\n      __typename\n    }\n    description {\n      translation\n      __typename\n    }\n    itemType\n    productId\n    __typename\n  }\n  excludedCharges {\n    excludeChargesAggregated {\n      copy {\n        translation\n        __typename\n      }\n      amountPerStay {\n        amount\n        amountRounded\n        amountUnformatted\n        currency\n        __typename\n      }\n      __typename\n    }\n    excludeChargesList {\n      chargeMode\n      chargeInclusion\n      chargeType\n      amountPerStay {\n        amount\n        amountRounded\n        amountUnformatted\n        currency\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  taxExceptions {\n    shortDescription {\n      translation\n      __typename\n    }\n    longDescription {\n      translation\n      __typename\n    }\n    __typename\n  }\n  displayConfig {\n    key\n    value\n    __typename\n  }\n  serverTranslations {\n    key\n    value\n    __typename\n  }\n  __typename\n}\n\nfragment BookerExperienceData on SearchResultProperty {\n  bookerExperienceContentUIComponentProps {\n    ... on BookerExperienceContentLoyaltyBadgeListProps {\n      badges {\n        amount\n        variant\n        key\n        title\n        hidePopover\n        popover\n        tncMessage\n        tncUrl\n        logoSrc\n        logoAlt\n        __typename\n      }\n      __typename\n    }\n    ... on BookerExperienceContentFinancialBadgeProps {\n      paymentMethod\n      backgroundColor\n      hideAccepted\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment TopPhotos on SearchResultProperty {\n  topPhotos {\n    highResUrl {\n      relativeUrl\n      __typename\n    }\n    lowResUrl {\n      relativeUrl\n      __typename\n    }\n    highResJpegUrl {\n      relativeUrl\n      __typename\n    }\n    lowResJpegUrl {\n      relativeUrl\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SearchMetadata on SearchMeta {\n  availabilityInfo {\n    hasLowAvailability\n    unavailabilityPercent\n    totalAvailableNotAutoextended\n    totalAutoextendedAvailable\n    __typename\n  }\n  boundingBoxes {\n    swLat\n    swLon\n    neLat\n    neLon\n    type\n    __typename\n  }\n  childrenAges\n  dates {\n    checkin\n    checkout\n    lengthOfStayInDays\n    __typename\n  }\n  destId\n  destType\n  guessedLocation {\n    destId\n    destType\n    destName\n    __typename\n  }\n  maxLengthOfStayInDays\n  nbRooms\n  nbAdults\n  nbChildren\n  userHasSelectedFilters\n  customerValueStatus\n  isAffiliateBookingOwned\n  affiliatePartnerChannelId\n  affiliateVerticalType\n  geniusLevel\n  __typename\n}\n\nfragment SearchResultsBreadcrumb on SearchResultsBreadcrumb {\n  destId\n  destType\n  name\n  __typename\n}\n\nfragment SorterFields on SorterOption {\n  type: name\n  captionTranslationTag {\n    translation\n    __typename\n  }\n  tooltipTranslationTag {\n    translation\n    __typename\n  }\n  isSelected: selected\n  __typename\n}\n\nfragment TripTypesData on TripTypes {\n  beach {\n    isBeachUfi\n    isEnabledBeachUfi\n    __typename\n  }\n  ski {\n    isSkiExperience\n    isSkiScaleUfi\n    __typename\n  }\n  __typename\n}\n\nfragment ZeroResultsSection on ZeroResultsSection {\n  title {\n    text\n    __typename\n  }\n  primaryAction {\n    text {\n      text\n      __typename\n    }\n    action {\n      name\n      __typename\n    }\n    __typename\n  }\n  paragraphs {\n    text\n    __typename\n  }\n  type\n  __typename\n}\n\nfragment PreviousSearches on PreviousSearch {\n  childrenAges\n  __typename\n}\n\nfragment MerchRegionIrene on MerchComponentsResultIrene {\n  regions {\n    id\n    components {\n      ... on PromotionalBannerIrene {\n        promotionalBannerCampaignId\n        contentArea {\n          title {\n            ... on PromotionalBannerSimpleTitleIrene {\n              value\n              __typename\n            }\n            __typename\n          }\n          subTitle {\n            ... on PromotionalBannerSimpleSubTitleIrene {\n              value\n              __typename\n            }\n            __typename\n          }\n          caption {\n            ... on PromotionalBannerSimpleCaptionIrene {\n              value\n              __typename\n            }\n            ... on PromotionalBannerCountdownCaptionIrene {\n              campaignEnd\n              __typename\n            }\n            __typename\n          }\n          buttons {\n            variant\n            cta {\n              ariaLabel\n              text\n              targetLanding {\n                ... on OpenContextSheet {\n                  sheet {\n                    ... on WebContextSheet {\n                      title\n                      body {\n                        items {\n                          ... on ContextSheetTextItem {\n                            text\n                            __typename\n                          }\n                          ... on ContextSheetList {\n                            items {\n                              text\n                              __typename\n                            }\n                            __typename\n                          }\n                          __typename\n                        }\n                        __typename\n                      }\n                      buttons {\n                        variant\n                        cta {\n                          text\n                          ariaLabel\n                          targetLanding {\n                            ... on DirectLinkLanding {\n                              urlPath\n                              queryParams {\n                                name\n                                value\n                                __typename\n                              }\n                              __typename\n                            }\n                            ... on LoginLanding {\n                              stub\n                              __typename\n                            }\n                            ... on DeeplinkLanding {\n                              urlPath\n                              queryParams {\n                                name\n                                value\n                                __typename\n                              }\n                              __typename\n                            }\n                            ... on ResolvedLinkLanding {\n                              url\n                              __typename\n                            }\n                            __typename\n                          }\n                          __typename\n                        }\n                        __typename\n                      }\n                      __typename\n                    }\n                    __typename\n                  }\n                  __typename\n                }\n                ... on SearchResultsLandingIrene {\n                  destType\n                  destId\n                  checkin\n                  checkout\n                  nrAdults\n                  nrChildren\n                  childrenAges\n                  nrRooms\n                  filters {\n                    name\n                    value\n                    __typename\n                  }\n                  __typename\n                }\n                ... on DirectLinkLandingIrene {\n                  urlPath\n                  queryParams {\n                    name\n                    value\n                    __typename\n                  }\n                  __typename\n                }\n                ... on LoginLandingIrene {\n                  stub\n                  __typename\n                }\n                ... on DeeplinkLandingIrene {\n                  urlPath\n                  queryParams {\n                    name\n                    value\n                    __typename\n                  }\n                  __typename\n                }\n                ... on SorterLandingIrene {\n                  sorterName\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        designVariant {\n          ... on DesktopPromotionalFullBleedImageIrene {\n            image: image {\n              id\n              url(width: 814, height: 138)\n              alt\n              overlayGradient\n              primaryColorHex\n              __typename\n            }\n            colorScheme\n            signature\n            __typename\n          }\n          ... on DesktopPromotionalImageLeftIrene {\n            imageOpt: image {\n              id\n              url(width: 248, height: 248)\n              alt\n              overlayGradient\n              primaryColorHex\n              __typename\n            }\n            colorScheme\n            signature\n            __typename\n          }\n          ... on DesktopPromotionalImageRightIrene {\n            imageOpt: image {\n              id\n              url(width: 248, height: 248)\n              alt\n              overlayGradient\n              primaryColorHex\n              __typename\n            }\n            colorScheme\n            signature\n            __typename\n          }\n          ... on MdotPromotionalFullBleedImageIrene {\n            image: image {\n              id\n              url(width: 358, height: 136)\n              alt\n              overlayGradient\n              primaryColorHex\n              __typename\n            }\n            colorScheme\n            signature\n            __typename\n          }\n          ... on MdotPromotionalImageLeftIrene {\n            imageOpt: image {\n              id\n              url(width: 128, height: 128)\n              alt\n              overlayGradient\n              primaryColorHex\n              __typename\n            }\n            colorScheme\n            signature\n            __typename\n          }\n          ... on MdotPromotionalImageRightIrene {\n            imageOpt: image {\n              id\n              url(width: 128, height: 128)\n              alt\n              overlayGradient\n              primaryColorHex\n              __typename\n            }\n            colorScheme\n            signature\n            __typename\n          }\n          ... on MdotPromotionalImageTopIrene {\n            imageOpt: image {\n              id\n              url(width: 128, height: 128)\n              alt\n              overlayGradient\n              primaryColorHex\n              __typename\n            }\n            colorScheme\n            signature\n            __typename\n          }\n          ... on MdotPromotionalIllustrationLeftIrene {\n            imageOpt: image {\n              id\n              url(width: 200, height: 200)\n              alt\n              overlayGradient\n              primaryColorHex\n              __typename\n            }\n            colorScheme\n            signature\n            __typename\n          }\n          ... on MdotPromotionalIllustrationRightIrene {\n            imageOpt: image {\n              id\n              url(width: 200, height: 200)\n              alt\n              overlayGradient\n              primaryColorHex\n              __typename\n            }\n            colorScheme\n            signature\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on MerchCarouselIrene @include(if: $carouselLowCodeExp) {\n        carouselCampaignId\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment VisualFiltersGroup on VisualFiltersGroup {\n  groupId: id\n  position\n  title {\n    text\n    __typename\n  }\n  visualFilters {\n    title {\n      text\n      __typename\n    }\n    description {\n      text\n      __typename\n    }\n    photoUrl\n    action {\n      name\n      context {\n        key\n        value\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyUspBadges on SearchResultProperty {\n  propertyUspBadges {\n    name\n    translatedName\n    __typename\n  }\n  __typename\n}\n"
})
headers = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.8',
  'apollographql-client-name': 'b-search-web-searchresults_rust',
  'apollographql-client-version': 'ABJNVZXB',
  'content-type': 'application/json',
  'origin': 'https://www.booking.com',
  'priority': 'u=1, i',
  'referer': 'https://www.booking.com/searchresults.html?ss=Seattle%2C%20United%20States&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaLQCiAEBmAExuAEHyAEM2AEB6AEB-AECiAIBqAIDuAK-iPnBBsACAdICJGZmMzBhOGRjLTQ1M2ItNGY0Ny04YmZjLWQyMDFjYTNiZWM1MdgCBeACAQ&sid=13b7b29af206a79542e44dfdce841b83&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=20144883&dest_type=city&checkin=2025-07-01&checkout=2025-07-19&group_adults=2&no_rooms=1&group_children=0',
  'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
  'sec-ch-ua-mobile': '?1',
  'sec-ch-ua-platform': '"Android"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
  'x-booking-context-action-name': 'searchresults_irene',
  'x-booking-context-aid': '304142',
  'x-booking-dml-cluster': 'rust',
  'x-booking-pageview-id': '86ed05d965d10150',
  'x-booking-site-type-id': '2',
  'x-booking-topic': 'capla_browser_b-search-web-searchresults',
}

response = requests.request("POST", url, headers=headers, data=payload, impersonate="chrome")

print(f"Response Status Code: {response.status_code}")

if response.status_code == 200:
    try:
        data = response.json()
        
        # Navigate to the results
        search_results = data.get("data", {}).get("searchQueries", {}).get("search", {}).get("results", [])
        
        print(f"\nFound {len(search_results)} hotels:")
        
        # Filter results based on user criteria
        filtered_results = []
        for hotel in search_results:
            # Check price filter
            if max_price:
                price_info = hotel.get("priceDisplayInfoIrene") or {}
                avg_price_per_night = price_info.get("averagePricePerNight") or {}
                price_unformatted = avg_price_per_night.get("amountUnformatted", 0)
                if price_unformatted > max_price:
                    continue
            
            # Check star rating filter
            if min_stars:
                basic_data = hotel.get("basicPropertyData") or {}
                star_rating_data = basic_data.get("starRating") or {}
                star_rating = star_rating_data.get("value", 0)
                if star_rating < min_stars:
                    continue
            
            # Check review count filter
            if min_reviews:
                basic_data = hotel.get("basicPropertyData") or {}
                review_score = basic_data.get("reviewScore") or {}
                review_count = review_score.get("reviewCount", 0)
                if review_count < min_reviews:
                    continue
            
            filtered_results.append(hotel)
        
        print(f"Showing {len(filtered_results)} hotels matching your criteria:\n")
        print("=" * 80)
        
        for i, hotel in enumerate(filtered_results, 1):
            # Extract hotel name
            display_name_data = hotel.get("displayName") or {}
            display_name = display_name_data.get("text", "No name available")
            
            # Extract pricing information
            price_info = hotel.get("priceDisplayInfoIrene") or {}
            display_price = price_info.get("displayPrice") or {}
            amount_per_stay = display_price.get("amountPerStay") or {}
            total_price = amount_per_stay.get("amount", "Price not available")
            currency = amount_per_stay.get("currency", "")
            
            # Extract average price per night
            avg_price_per_night = price_info.get("averagePricePerNight") or {}
            avg_price = avg_price_per_night.get("amount", "N/A")
            
            # Extract location
            basic_data = hotel.get("basicPropertyData") or {}
            location_data = basic_data.get("location") or {}
            address = location_data.get("address", "")
            city = location_data.get("city", "")
            full_location = f"{address}, {city}" if address and city else city or address or "Location not available"
            
            # Extract rating information
            review_score = basic_data.get("reviewScore") or {}
            rating = review_score.get("score", 0)
            review_count = review_score.get("reviewCount", 0)
            rating_text_data = review_score.get("totalScoreTextTag") or {}
            rating_text = rating_text_data.get("translation", "")
            
            # Extract star rating
            star_rating_data = basic_data.get("starRating") or {}
            star_rating = star_rating_data.get("value", 0)
            
            # Extract meal plan if available
            meal_plan = hotel.get("mealPlanIncluded") or {}
            meal_info = meal_plan.get("text", "").strip() if meal_plan else ""
            
            # Extract and format image URLs
            photos = basic_data.get("photos") or {}
            main_photo = photos.get("main") or {}
            
            # Try different image formats in order of preference
            image_url = None
            for url_type in ["highResJpegUrl", "highResUrl", "lowResJpegUrl", "lowResUrl"]:
                url_data = main_photo.get(url_type) or {}
                relative_url = url_data.get("relativeUrl")
                if relative_url:
                    image_url = format_image_url(relative_url)
                    break
            
            # Print hotel information
            print(f"Hotel #{i}: {display_name}")
            print(f"Location: {full_location}")
            print(f"Star Rating: {star_rating} stars" if star_rating > 0 else "Star Rating: Not rated")
            print(f"Guest Rating: {rating}/10 ({rating_text}) - {review_count} reviews" if rating > 0 else "Guest Rating: No reviews")
            if meal_info:
                print(f"Meals: {meal_info}")
            print(f"Price per night: {avg_price}")
            print(f"Total price: {total_price} {currency}")
            if image_url:
                print(f"Image URL: {image_url}")
            print("-" * 80)
            
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
    except Exception as e:
        print(f"Error processing response: {e}")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(f"Response: {response.text[:500]}...")  # Print first 500 chars of error
