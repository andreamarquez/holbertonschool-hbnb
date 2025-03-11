# HolbertonSchool-hbnb

Uses: https://www.mermaidchart.com/play to generate the pngs for the mermaid diagrams
under ./mermaid/*.mmd

### How to contribute

Use the live mermaid.js editor to write the needed code, copy that code under
the mermaid repository on a file that matches the naming of the diagram (ex: package-diagram.mmd)
using the .mmd extension.

Then, export the image on the playground as a png file and add it on the root level of this repo.

Add this on top of the mmd file to keep style coherence:
```
---
config:
  theme: default
  themeVariables:
    primaryColor: '#ffcc00'
    edgeLabelBackground: '#ffffff'
    tertiaryColor: '#ffffff'
  look: handDrawn
---
```

### Explanation:

#### Presentation Layer:
- **Services** and **APIs**: These components handle user interactions and expose endpoints for various operations.
  - **UserService**: Manages user-related operations.
  - **PlaceService**: Handles property listing operations.
  - **ReviewService**: Manages review-related operations.
  - **AmenityService**: Manages amenities.
  - **UserAPI**:
    - `registerUser()`: Endpoint to register a new user.
    - `loginUser()`: Endpoint for user login.
    - `updateUserProfile()`: Endpoint to update user profile.
    - `getUserProfile()`: Endpoint to get user profile details.
  - **PlaceAPI**:
    - `addPlace()`: Endpoint to add a new place.
    - `updatePlace()`: Endpoint to update place details.
    - `getPlaceDetails()`: Endpoint to get details of a specific place.
    - `listPlaces()`: Endpoint to list all places.
  - **ReviewAPI**:
    - `addReview()`: Endpoint to add a new review.
    - `getReviews()`: Endpoint to get reviews for a place.
    - `updateReview()`: Endpoint to update a review.
    - `deleteReview()`: Endpoint to delete a review.
  - **AmenityAPI**:
    - `addAmenity()`: Endpoint to add a new amenity.
    - `getAmenities()`: Endpoint to get a list of amenities.
    - `updateAmenity()`: Endpoint to update an amenity.
    - `deleteAmenity()`: Endpoint to delete an amenity.

#### Business Logic Layer:
- **Managers**: These components handle the core business logic and operations for different entities.
  - **UserManager**: Handles user-related operations.
    - `createUser()`: Creates a new user.
    - `updateUser()`: Updates user details.
    - `getUser()`: Retrieves user information.
    - `deleteUser()`: Deletes a user.
  - **PlaceManager**: Handles place-related operations.
    - `createPlace()`: Creates a new place.
    - `updatePlace()`: Updates place details.
    - `getPlace()`: Retrieves place information.
    - `deletePlace()`: Deletes a place.
  - **ReviewManager**: Handles review-related operations.
    - `createReview()`: Creates a new review.
    - `updateReview()`: Updates review details.
    - `getReview()`: Retrieves review information.
    - `deleteReview()`: Deletes a review.
  - **AmenityManager**: Handles amenity-related operations.
    - `createAmenity()`: Creates a new amenity.
    - `updateAmenity()`: Updates amenity details.
    - `getAmenity()`: Retrieves amenity information.
    - `deleteAmenity()`: Deletes an amenity.
- **Core Models**: These represent the entities in the system.
  - **User**: Represents a user entity.
  - **Place**: Represents a place entity.
  - **Review**: Represents a review entity.
  - **Amenity**: Represents an amenity entity.
- **Additional Services**:
  - **AuthenticationService**: Manages user authentication (e.g., login, logout).
    - `authenticate()`: Authenticates a user.
    - `logout()`: Logs out a user.
  - **AuthorizationService**: Manages user authorization.
    - `authorize()`: Authorizes a user.

#### Persistence Layer:
- **DatabaseAccessObject**: Handles direct interactions with the database.

#### Facade Pattern:
- The communication between layers is simplified using the facade pattern, represented by the arrows between the layers. This pattern provides a unified interface to a set of interfaces in the subsystem, making it easier to interact with the system.

