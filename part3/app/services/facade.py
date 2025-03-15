from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ----- User Methods -----
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user.to_dict()

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        return user.to_dict() if user else None

    def get_user_by_email(self, email):
        user = self.user_repo.get_by_attribute("email", email)
        return user.to_dict() if user else None

    def get_all_users(self):
        users = [user.to_dict() for user in self.user_repo.get_all()]
        for user in users:
            user.pop('password', None)  # Exclude the password from each user dictionary
        return users

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        user.update(user_data)
        user_dict = user.to_dict()
        self.user_repo.update(user_id, user_dict)
        return user_dict

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    # ----- Place Methods -----
    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id')
        amenities_ids = place_data.pop('amenities', [])

        owner = self.user_repo.get(owner_id)

        if not owner:
            raise ValueError("Owner not found")

        # Create a new dictionary excluding 'owner_id'
        place_data_without_owner_id = {
            k: v for k, v in place_data.items() if k != 'owner_id'}

        place = Place(owner=owner_id, **place_data_without_owner_id)
        self.place_repo.add(place)

        # Add amenities to the place
        for amenity_id in amenities_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                place.add_amenity(amenity)

        return place.to_dict_with_owner_id()

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        return place.to_dict() if place else None

    def get_all_places(self):
        return [place.to_dict() for place in self.place_repo.get_all()]

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner_id = place_data.pop('owner_id', None)
        amenities_ids = place_data.pop('amenities', [])

        if owner_id:
            owner = self.user_repo.get(owner_id)
            if owner:
                place.owner = owner_id

        place.update(place_data)

        # Update amenities
        place.amenities = []
        for amenity_id in amenities_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                place.add_amenity(amenity)

        place_dict = place.to_dict()
        self.place_repo.update(place_id, place_dict)
        return place_dict

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # ----- Amenity Methods -----
    def create_amenity(self, amenity_data):
        if "name" not in amenity_data:
            raise ValueError("Amenity name is required")
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity.to_dict()

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        return amenity.to_dict() if amenity else None

    def get_all_amenities(self):
        return [amenity.to_dict() for amenity in self.amenity_repo.get_all()]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        amenity.update(amenity_data)
        amenity_dict = amenity.to_dict()
        self.amenity_repo.update(amenity_id, amenity_dict)
        return amenity_dict

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

    # ----- Review Methods -----
    def create_review(self, review_data):
        if (
            "rating" not in review_data or
            "user_id" not in review_data or
            "place_id" not in review_data
        ):
            raise ValueError("Rating, user_id, and place_id are required")

        user_id = review_data.pop('user_id')
        place_id = review_data.pop('place_id')

        user = self.user_repo.get(user_id)
        place = self.place_repo.get(place_id)

        if not user:
            raise ValueError("User not found")

        if not place:
            raise ValueError("Place not found")

        review_data_without_place_id = {
            k: v for k, v in review_data.items() if (
                k != 'place_id' and
                k != 'user_id'
                )
            }
        review = Review(
            user=user_id,
            place=place_id,
            **review_data_without_place_id)
        self.review_repo.add(review)
        return review.to_dict_with_ids()

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        return review.to_dict_with_ids() if review else None

    def get_all_reviews(self):
        return [review.to_dict_with_ids()
                for review in self.review_repo.get_all()]

    # to fix
    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""
        # Get all reviews from the repository
        all_reviews = self.review_repo.get_all()

        # Filter reviews by place_id
        reviews_by_place_id = [
            review for review in all_reviews if review.place == place_id]

        # Convert each review to a dictionary with IDs
        reviews_by_place_id_dicts = [
            review.to_dict_with_ids() for review in reviews_by_place_id]

        return reviews_by_place_id_dicts

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        review.update(review_data)
        review_dict = review.to_dict()
        self.review_repo.update(review_id, review_dict)
        return review.to_dict_with_ids()

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
